#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态页面生成器服务

将动态网站页面渲染为静态 HTML 文件
"""

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.database import get_db
from app.models import ColumnType, SiteColumn
from app.models.static_generation import StaticGenerationLog, StaticGenerationDetail
from app.routes.frontend_i18n import get_template_engine
from app.services import post_service, product_service, site_service
from app.services import layout_service as layout_render_service

logger = logging.getLogger("docms")


class MockRequest:
    """模拟 FastAPI Request 对象用于模板渲染"""

    def __init__(self, url: str, base_url: str = "http://localhost:8000"):
        self.url = type('obj', (object,), {'path': url})()
        self.base_url = type('obj', (object,), {'scheme': 'http', 'netloc': 'localhost:8000'})()
        self.query_params = {}
        self.path_params = {}
        self.headers = {}


class StaticPageGenerator:
    """静态页面生成器"""

    def __init__(
        self,
        db: Session,
        output_dir: str = "public",
        base_url: str = "http://localhost:8000",
    ):
        """
        初始化生成器

        Args:
            db: 数据库会话
            output_dir: 输出目录路径
            base_url: 网站基础 URL
        """
        self.db = db
        self.output_dir = Path(output_dir)
        self.base_url = base_url.rstrip("/")
        self.log: Optional[StaticGenerationLog] = None

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 统计信息
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
        }

    def generate_all(self) -> StaticGenerationLog:
        """
        生成所有页面

        Returns:
            StaticGenerationLog: 生成日志记录
        """
        logger.info("开始生成静态页面...")

        # 创建生成日志
        self.log = StaticGenerationLog(
            generation_type="full",
            start_time=datetime.now(),
            status="running",
        )
        self.db.add(self.log)
        self.db.commit()
        self.db.refresh(self.log)

        try:
            # 1. 生成首页 (中英文)
            self._generate_homepage("zh")
            self._generate_homepage("en")

            # 2. 获取所有已启用的栏目
            columns = (
                self.db.query(SiteColumn)
                .filter(SiteColumn.is_enabled == True)
                .order_by(SiteColumn.sort_order)
                .all()
            )

            # 3. 按栏目类型生成页面
            for column in columns:
                # 跳过首页栏目（已单独处理）
                if column.slug == "home":
                    continue

                # 中英文双语生成
                for lang in ["zh", "en"]:
                    try:
                        if column.column_type == ColumnType.SINGLE_PAGE:
                            self._generate_single_page(column, lang)
                        elif column.column_type == ColumnType.PRODUCT:
                            self._generate_product_pages(column, lang)
                        elif column.column_type == ColumnType.POST:
                            self._generate_post_pages(column, lang)
                        elif column.column_type == ColumnType.GALLERY:
                            self._generate_gallery_page(column, lang)
                        elif column.column_type == ColumnType.CUSTOM:
                            self._generate_custom_page(column, lang)
                    except Exception as e:
                        logger.error(f"生成栏目 {column.slug} ({lang}) 失败: {str(e)}")
                        self._record_detail(
                            page_type="column",
                            page_id=column.id,
                            language=lang,
                            url_path=f"/{lang}/{column.slug}" if lang == "en" else f"/{column.slug}",
                            file_path="",
                            status="failed",
                            error_message=str(e),
                        )

            # 更新生成日志状态
            self.log.end_time = datetime.now()
            self.log.total_pages = self.stats["total"]
            self.log.successful_pages = self.stats["success"]
            self.log.failed_pages = self.stats["failed"]
            self.log.status = "completed" if self.stats["failed"] == 0 else "partial"
            self.db.commit()

            logger.info(
                f"静态页面生成完成: 总计 {self.stats['total']} 页, "
                f"成功 {self.stats['success']} 页, "
                f"失败 {self.stats['failed']} 页"
            )

            return self.log

        except Exception as e:
            logger.error(f"生成过程出错: {str(e)}")
            if self.log:
                self.log.end_time = datetime.now()
                self.log.status = "failed"
                self.log.error_message = str(e)
                self.log.total_pages = self.stats["total"]
                self.log.successful_pages = self.stats["success"]
                self.log.failed_pages = self.stats["failed"]
                self.db.commit()
            raise

    def _generate_homepage(self, lang: str = "zh"):
        """
        生成首页

        Args:
            lang: 语言代码 ('zh' 或 'en')
        """
        start_time = time.time()
        url_path = f"/{lang}/" if lang == "en" else "/"
        file_path = self.output_dir / lang / "index.html"

        try:
            # 创建模拟 Request 对象
            request = MockRequest(url_path, self.base_url)

            # 获取模板引擎
            templates = get_template_engine(lang)

            # 准备上下文
            context = self._get_base_context(request, lang)

            # 检查是否有已发布的布局
            from app.models.layout import LayoutScope
            published_layout = layout_render_service.get_published_layout(
                self.db, LayoutScope.HOME
            )

            if published_layout:
                # 使用布局系统渲染
                html = layout_render_service.render_layout_html(self.db, published_layout)
                rendered_html = templates.TemplateResponse(
                    "layout_page.html",
                    {"request": request, **context, "layout_html": html},
                ).body.decode("utf-8")
            else:
                # 获取首页数据
                home_column = site_service.get_column_by_slug(self.db, "home")
                if home_column and home_column.column_type == ColumnType.SINGLE_PAGE:
                    page = site_service.get_single_page(self.db, home_column.id)
                    context["page"] = page

                # 获取推荐活动
                featured_event = post_service.get_posts(self.db, is_recommended=True, limit=1)
                context["featured_event"] = featured_event[0] if featured_event else None

                # 获取最新文章
                latest_posts = post_service.get_posts(self.db, limit=6, status="published")
                context["latest_posts"] = latest_posts

                # 获取推荐产品
                context["featured_products"] = product_service.get_products(
                    self.db, is_recommended=True, limit=6
                )

                # 渲染首页模板
                rendered_html = templates.TemplateResponse(
                    "home.html", context
                ).body.decode("utf-8")

            # 保存 HTML 文件
            self._save_html(file_path, rendered_html)

            # 记录详情
            generation_time = time.time() - start_time
            self._record_detail(
                page_type="home",
                page_id=None,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.info(f"首页 ({lang}) 生成成功: {file_path}")

        except Exception as e:
            logger.error(f"首页 ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="home",
                page_id=None,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )
            raise

    def _generate_single_page(self, column: SiteColumn, lang: str = "zh"):
        """
        生成单页

        Args:
            column: 栏目对象
            lang: 语言代码
        """
        start_time = time.time()
        url_path = f"/{lang}/{column.slug}" if lang == "en" else f"/{column.slug}"
        file_path = self.output_dir / lang / column.slug / "index.html"

        try:
            # 获取单页内容
            page = site_service.get_single_page(self.db, column.id)
            if not page:
                logger.warning(f"栏目 {column.slug} 没有关联的单页内容")
                return

            # 创建模拟 Request 对象
            request = MockRequest(url_path, self.base_url)

            # 准备上下文
            context = self._get_base_context(request, lang)
            context["column"] = column
            context["page"] = page

            # 检查是否有已发布的布局
            from app.models.layout import LayoutScope
            published_layout = layout_render_service.get_published_layout(
                self.db, LayoutScope.COLUMN, scope_id=column.id
            )

            templates = get_template_engine(lang)

            if published_layout:
                # 使用布局系统渲染
                html = layout_render_service.render_layout_html(self.db, published_layout)
                rendered_html = templates.TemplateResponse(
                    "layout_page.html",
                    {"request": request, **context, "layout_html": html},
                ).body.decode("utf-8")
            else:
                # 尝试使用自定义模板，否则使用默认模板
                try:
                    rendered_html = templates.TemplateResponse(
                        f"{column.slug}.html", context
                    ).body.decode("utf-8")
                except TemplateNotFound:
                    rendered_html = templates.TemplateResponse(
                        "single_page.html", context
                    ).body.decode("utf-8")

            # 保存 HTML 文件
            self._save_html(file_path, rendered_html)

            # 记录详情
            generation_time = time.time() - start_time
            self._record_detail(
                page_type="single_page",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"单页 {column.slug} ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"单页 {column.slug} ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="single_page",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _generate_product_pages(self, column: SiteColumn, lang: str = "zh"):
        """
        生成产品列表和详情页

        Args:
            column: 栏目对象
            lang: 语言代码
        """
        # 1. 生成产品列表页
        self._generate_product_list(column, lang)

        # 2. 生成所有产品详情页
        products = product_service.get_products(self.db, column_id=column.id)
        for product in products:
            self._generate_product_detail(column, product, lang)

    def _generate_product_list(self, column: SiteColumn, lang: str = "zh"):
        """生成产品列表页"""
        start_time = time.time()
        url_path = f"/{lang}/{column.slug}" if lang == "en" else f"/{column.slug}"
        file_path = self.output_dir / lang / column.slug / "index.html"

        try:
            request = MockRequest(url_path, self.base_url)
            context = self._get_base_context(request, lang)
            context["column"] = column

            # 获取产品分类和产品列表
            categories = product_service.get_product_categories(self.db, column.id)
            products = product_service.get_products(self.db, column_id=column.id)

            context["categories"] = categories
            context["products"] = products
            context["current_category_id"] = None
            context["total"] = product_service.get_product_count(self.db, column_id=column.id)

            templates = get_template_engine(lang)

            # 尝试使用自定义模板
            try:
                rendered_html = templates.TemplateResponse(
                    f"{column.slug}.html", context
                ).body.decode("utf-8")
            except TemplateNotFound:
                rendered_html = templates.TemplateResponse(
                    "product_list.html", context
                ).body.decode("utf-8")

            self._save_html(file_path, rendered_html)

            generation_time = time.time() - start_time
            self._record_detail(
                page_type="product_list",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"产品列表 {column.slug} ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"产品列表 {column.slug} ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="product_list",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _generate_product_detail(self, column: SiteColumn, product, lang: str = "zh"):
        """生成产品详情页"""
        start_time = time.time()
        url_path = (
            f"/{lang}/{column.slug}/{product.slug}"
            if lang == "en"
            else f"/{column.slug}/{product.slug}"
        )
        file_path = self.output_dir / lang / column.slug / product.slug / "index.html"

        try:
            request = MockRequest(url_path, self.base_url)
            context = self._get_base_context(request, lang)
            context["column"] = column
            context["product"] = product

            # 获取相关产品
            if product.categories:
                context["related_products"] = product_service.get_products(
                    self.db, category_id=product.categories[0].id, limit=4
                )

            templates = get_template_engine(lang)
            rendered_html = templates.TemplateResponse(
                "product_detail.html", context
            ).body.decode("utf-8")

            self._save_html(file_path, rendered_html)

            generation_time = time.time() - start_time
            self._record_detail(
                page_type="product",
                page_id=product.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"产品详情 {product.slug} ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"产品详情 {product.slug} ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="product",
                page_id=product.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _generate_post_pages(self, column: SiteColumn, lang: str = "zh"):
        """
        生成文章列表和详情页

        Args:
            column: 栏目对象
            lang: 语言代码
        """
        # 1. 生成文章列表页
        self._generate_post_list(column, lang)

        # 2. 生成所有文章详情页
        is_approved_filter = True if column.slug == "guestbook" else None
        posts = post_service.get_posts(
            self.db, column_id=column.id, is_approved=is_approved_filter
        )
        for post in posts:
            self._generate_post_detail(column, post, lang)

    def _generate_post_list(self, column: SiteColumn, lang: str = "zh"):
        """生成文章列表页"""
        start_time = time.time()
        url_path = f"/{lang}/{column.slug}" if lang == "en" else f"/{column.slug}"
        file_path = self.output_dir / lang / column.slug / "index.html"

        try:
            request = MockRequest(url_path, self.base_url)
            context = self._get_base_context(request, lang)
            context["column"] = column

            # 获取文章分类和文章列表
            categories = post_service.get_post_categories(self.db, column.id)
            is_approved_filter = True if column.slug == "guestbook" else None
            posts = post_service.get_posts(
                self.db, column_id=column.id, is_approved=is_approved_filter
            )

            # 获取侧边栏数据
            popular_posts = post_service.get_popular_posts(self.db, column.id, limit=5)
            category_stats = post_service.get_category_stats(self.db, column.id)
            popular_tags = post_service.get_popular_tags(self.db, column.id, limit=20)

            context["categories"] = categories
            context["posts"] = posts
            context["current_category_id"] = None
            context["total"] = post_service.get_post_count(
                self.db, column_id=column.id, is_approved=is_approved_filter
            )
            context["popular_posts"] = popular_posts
            context["category_stats"] = category_stats
            context["popular_tags"] = popular_tags

            # 添加父栏目和兄弟栏目（用于侧边栏导航）
            if column.parent_id:
                parent_column = (
                    self.db.query(SiteColumn)
                    .filter(SiteColumn.id == column.parent_id)
                    .first()
                )
                context["parent_column"] = parent_column
                sibling_columns = site_service.get_child_columns(self.db, column.parent_id)
                context["sibling_columns"] = sibling_columns

            templates = get_template_engine(lang)

            # 根据栏目选择合适的模板
            template_name = "post_list.html"
            if column.slug == "school-curriculum":
                template_name = "post_list_with_sidebar.html"
            elif column.slug in ["chess-events", "chess-news", "news", "badminton-events"]:
                template_name = "post_list_universal.html"

            # 尝试使用自定义模板
            try:
                rendered_html = templates.TemplateResponse(
                    f"{column.slug}.html", context
                ).body.decode("utf-8")
            except TemplateNotFound:
                rendered_html = templates.TemplateResponse(
                    template_name, context
                ).body.decode("utf-8")

            self._save_html(file_path, rendered_html)

            generation_time = time.time() - start_time
            self._record_detail(
                page_type="post_list",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"文章列表 {column.slug} ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"文章列表 {column.slug} ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="post_list",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _generate_post_detail(self, column: SiteColumn, post, lang: str = "zh"):
        """生成文章详情页"""
        start_time = time.time()
        url_path = (
            f"/{lang}/{column.slug}/{post.slug}"
            if lang == "en"
            else f"/{column.slug}/{post.slug}"
        )
        file_path = self.output_dir / lang / column.slug / post.slug / "index.html"

        try:
            request = MockRequest(url_path, self.base_url)
            context = self._get_base_context(request, lang)
            context["column"] = column
            context["post"] = post

            # 获取相关文章
            if post.categories:
                context["related_posts"] = post_service.get_posts(
                    self.db, category_id=post.categories[0].id, limit=3
                )

            # 添加父栏目和兄弟栏目（用于侧边栏导航）
            if column.parent_id:
                parent_column = (
                    self.db.query(SiteColumn)
                    .filter(SiteColumn.id == column.parent_id)
                    .first()
                )
                context["parent_column"] = parent_column
                sibling_columns = site_service.get_child_columns(self.db, column.parent_id)
                context["sibling_columns"] = sibling_columns

            templates = get_template_engine(lang)
            rendered_html = templates.TemplateResponse(
                "post_detail.html", context
            ).body.decode("utf-8")

            self._save_html(file_path, rendered_html)

            generation_time = time.time() - start_time
            self._record_detail(
                page_type="post",
                page_id=post.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"文章详情 {post.slug} ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"文章详情 {post.slug} ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="post",
                page_id=post.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _generate_gallery_page(self, column: SiteColumn, lang: str = "zh"):
        """生成相册页面"""
        start_time = time.time()
        url_path = f"/{lang}/{column.slug}" if lang == "en" else f"/{column.slug}"
        file_path = self.output_dir / lang / column.slug / "index.html"

        try:
            from app.services.gallery_service import GalleryService

            gallery_service = GalleryService(self.db)
            gallery = gallery_service.get_gallery_by_slug(column.slug)

            if not gallery:
                logger.warning(f"未找到相册: {column.slug}")
                return

            request = MockRequest(url_path, self.base_url)
            context = self._get_base_context(request, lang)
            context["column"] = column
            context["gallery"] = gallery

            # 获取相册图片
            images = gallery_service.get_gallery_images(gallery.id)
            media_files = [img.media for img in images if img.media and img.is_visible]

            context["images"] = images
            context["media_files"] = media_files

            templates = get_template_engine(lang)
            rendered_html = templates.TemplateResponse(
                "gallery.html", context
            ).body.decode("utf-8")

            self._save_html(file_path, rendered_html)

            generation_time = time.time() - start_time
            self._record_detail(
                page_type="gallery",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"相册页面 {column.slug} ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"相册页面 {column.slug} ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="gallery",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _generate_custom_page(self, column: SiteColumn, lang: str = "zh"):
        """生成自定义页面"""
        # 特殊处理：gallery 总览页
        if column.slug == "gallery":
            self._generate_gallery_list_page(column, lang)
            return

        # 其他自定义页面尝试使用自定义模板
        start_time = time.time()
        url_path = f"/{lang}/{column.slug}" if lang == "en" else f"/{column.slug}"
        file_path = self.output_dir / lang / column.slug / "index.html"

        try:
            request = MockRequest(url_path, self.base_url)
            context = self._get_base_context(request, lang)
            context["column"] = column

            # 检查是否有子栏目（概览页）
            child_columns = site_service.get_child_columns(self.db, column.id)
            if child_columns:
                sections = site_service.get_overview_sections(self.db, column.id)
                context["sections"] = sections
                template_name = "overview.html"
            else:
                template_name = f"{column.slug}.html"

            templates = get_template_engine(lang)

            try:
                rendered_html = templates.TemplateResponse(
                    template_name, context
                ).body.decode("utf-8")
            except TemplateNotFound:
                logger.warning(f"未找到自定义模板: {template_name}")
                return

            self._save_html(file_path, rendered_html)

            generation_time = time.time() - start_time
            self._record_detail(
                page_type="custom",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"自定义页面 {column.slug} ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"自定义页面 {column.slug} ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="custom",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _generate_gallery_list_page(self, column: SiteColumn, lang: str = "zh"):
        """生成相册总览页"""
        start_time = time.time()
        url_path = f"/{lang}/gallery" if lang == "en" else "/gallery"
        file_path = self.output_dir / lang / "gallery" / "index.html"

        try:
            from app.models.gallery import Gallery

            request = MockRequest(url_path, self.base_url)
            context = self._get_base_context(request, lang)
            context["column"] = column

            # 获取所有公开相册
            all_galleries = (
                self.db.query(Gallery)
                .filter(Gallery.is_public == True)
                .order_by(Gallery.sort_order)
                .all()
            )
            context["galleries"] = all_galleries
            context["page"] = column

            templates = get_template_engine(lang)

            try:
                rendered_html = templates.TemplateResponse(
                    "gallery_list.html", context
                ).body.decode("utf-8")
            except TemplateNotFound:
                rendered_html = templates.TemplateResponse(
                    "single_page.html", context
                ).body.decode("utf-8")

            self._save_html(file_path, rendered_html)

            generation_time = time.time() - start_time
            self._record_detail(
                page_type="gallery_list",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)),
                status="success",
                generation_time=generation_time,
            )

            logger.debug(f"相册总览页 ({lang}) 生成成功")

        except Exception as e:
            logger.error(f"相册总览页 ({lang}) 生成失败: {str(e)}")
            self._record_detail(
                page_type="gallery_list",
                page_id=column.id,
                language=lang,
                url_path=url_path,
                file_path=str(file_path.relative_to(self.output_dir)) if file_path else "",
                status="failed",
                error_message=str(e),
            )

    def _get_base_context(self, request: MockRequest, lang: str = "zh") -> Dict[str, Any]:
        """
        获取基础模板上下文

        Args:
            request: 模拟 Request 对象
            lang: 语言代码

        Returns:
            基础上下文字典
        """
        site_settings = site_service.get_all_site_settings(self.db)
        return {
            "request": request,
            "db": self.db,
            "site_settings": site_settings,
            "site": site_settings,
            "navigation": site_service.get_navigation(self.db, "header"),
            "footer_navigation": site_service.get_navigation(self.db, "footer"),
            "lang": lang,
            "current_lang": lang,
        }

    def _save_html(self, file_path: Path, html_content: str):
        """
        保存 HTML 文件

        Args:
            file_path: 文件路径
            html_content: HTML 内容
        """
        # 创建目录
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 保存文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.stats["total"] += 1
        self.stats["success"] += 1

    def _record_detail(
        self,
        page_type: str,
        language: str,
        url_path: str,
        file_path: str,
        status: str = "success",
        page_id: Optional[int] = None,
        error_message: Optional[str] = None,
        generation_time: Optional[float] = None,
    ):
        """
        记录生成详情

        Args:
            page_type: 页面类型
            language: 语言
            url_path: URL 路径
            file_path: 文件路径
            status: 状态
            page_id: 页面 ID
            error_message: 错误信息
            generation_time: 生成耗时
        """
        if not self.log:
            return

        detail = StaticGenerationDetail(
            log_id=self.log.id,
            page_type=page_type,
            page_id=page_id,
            language=language,
            url_path=url_path,
            file_path=file_path,
            status=status,
            error_message=error_message,
            generation_time=generation_time,
        )

        self.db.add(detail)
        self.db.commit()

        if status == "failed":
            self.stats["failed"] += 1
