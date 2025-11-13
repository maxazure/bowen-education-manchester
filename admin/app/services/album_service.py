"""
相册服务层

提供相册管理的核心业务逻辑：
1. 相册 CRUD 操作
2. 照片管理
3. 相册分类管理
4. Slug 生成
"""

import re
from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session, joinedload

from app.models.album import Album, AlbumCategory, AlbumPhoto
from app.models.media import MediaFile


class AlbumService:
    """相册服务类"""

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # 相册分类管理
    # ============================================================

    def get_categories(self, enabled_only: bool = False) -> List[AlbumCategory]:
        """获取所有分类"""
        query = self.db.query(AlbumCategory).order_by(AlbumCategory.sort_order)

        if enabled_only:
            query = query.filter(AlbumCategory.is_enabled == True)

        return query.all()

    def get_category(self, category_id: int) -> Optional[AlbumCategory]:
        """获取单个分类"""
        return (
            self.db.query(AlbumCategory)
            .filter(AlbumCategory.id == category_id)
            .first()
        )

    def create_category(
        self, name: str, slug: Optional[str] = None, **kwargs
    ) -> Tuple[Optional[AlbumCategory], Optional[str]]:
        """创建分类"""
        # 生成 slug
        if not slug:
            slug = self.generate_slug(name)

        # 检查 slug 是否已存在
        if self.db.query(AlbumCategory).filter(AlbumCategory.slug == slug).first():
            return None, f"Slug '{slug}' 已存在"

        category = AlbumCategory(name=name, slug=slug, **kwargs)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category, None

    def update_category(
        self, category_id: int, **kwargs
    ) -> Tuple[bool, Optional[str]]:
        """更新分类"""
        category = self.get_category(category_id)
        if not category:
            return False, "分类不存在"

        # 如果更新 slug，检查是否重复
        if "slug" in kwargs and kwargs["slug"] != category.slug:
            if (
                self.db.query(AlbumCategory)
                .filter(AlbumCategory.slug == kwargs["slug"])
                .first()
            ):
                return False, f"Slug '{kwargs['slug']}' 已存在"

        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)

        self.db.commit()
        return True, None

    def delete_category(self, category_id: int) -> Tuple[bool, Optional[str]]:
        """删除分类"""
        category = self.get_category(category_id)
        if not category:
            return False, "分类不存在"

        # 检查是否有相册使用该分类
        if category.albums:
            return False, f"该分类下有 {len(category.albums)} 个相册，无法删除"

        self.db.delete(category)
        self.db.commit()
        return True, None

    # ============================================================
    # 相册管理
    # ============================================================

    def get_albums(
        self,
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Album], int]:
        """获取相册列表"""
        query = self.db.query(Album).options(
            joinedload(Album.category), joinedload(Album.cover_media)
        )

        # 状态筛选
        if status:
            query = query.filter(Album.status == status)

        # 分类筛选
        if category_id:
            query = query.filter(Album.category_id == category_id)

        # 统计总数
        total = query.count()

        # 排序和分页
        query = query.order_by(Album.sort_order, Album.created_at.desc())
        albums = query.offset((page - 1) * page_size).limit(page_size).all()

        return albums, total

    def get_album(self, album_id: int) -> Optional[Album]:
        """获取单个相册（包含照片）"""
        return (
            self.db.query(Album)
            .options(
                joinedload(Album.category),
                joinedload(Album.cover_media),
                joinedload(Album.photos).joinedload(AlbumPhoto.media),
            )
            .filter(Album.id == album_id)
            .first()
        )

    def get_album_by_slug(self, slug: str) -> Optional[Album]:
        """通过 slug 获取相册"""
        return (
            self.db.query(Album)
            .options(
                joinedload(Album.category),
                joinedload(Album.cover_media),
                joinedload(Album.photos).joinedload(AlbumPhoto.media),
            )
            .filter(Album.slug == slug)
            .first()
        )

    def create_album(
        self,
        title: str,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
        **kwargs,
    ) -> Tuple[Optional[Album], Optional[str]]:
        """创建相册"""
        # 生成 slug
        if not slug:
            slug = self.generate_slug(title)

        # 检查 slug 是否已存在
        if self.db.query(Album).filter(Album.slug == slug).first():
            return None, f"Slug '{slug}' 已存在"

        album = Album(
            title=title, slug=slug, description=description, category_id=category_id, **kwargs
        )
        self.db.add(album)
        self.db.commit()
        self.db.refresh(album)

        return album, None

    def update_album(self, album_id: int, **kwargs) -> Tuple[bool, Optional[str]]:
        """更新相册"""
        album = self.get_album(album_id)
        if not album:
            return False, "相册不存在"

        # 如果更新 slug，检查是否重复
        if "slug" in kwargs and kwargs["slug"] != album.slug:
            if self.db.query(Album).filter(Album.slug == kwargs["slug"]).first():
                return False, f"Slug '{kwargs['slug']}' 已存在"

        for key, value in kwargs.items():
            if hasattr(album, key):
                setattr(album, key, value)

        self.db.commit()
        return True, None

    def delete_album(self, album_id: int) -> Tuple[bool, Optional[str]]:
        """删除相册（级联删除照片关联）"""
        album = self.get_album(album_id)
        if not album:
            return False, "相册不存在"

        self.db.delete(album)
        self.db.commit()
        return True, None

    def publish_album(self, album_id: int) -> Tuple[bool, Optional[str]]:
        """发布相册"""
        album = self.get_album(album_id)
        if not album:
            return False, "相册不存在"

        album.publish()
        self.db.commit()
        return True, None

    def unpublish_album(self, album_id: int) -> Tuple[bool, Optional[str]]:
        """取消发布相册"""
        album = self.get_album(album_id)
        if not album:
            return False, "相册不存在"

        album.unpublish()
        self.db.commit()
        return True, None

    # ============================================================
    # 照片管理
    # ============================================================

    def add_photo(
        self,
        album_id: int,
        media_id: int,
        caption: Optional[str] = None,
        sort_order: int = 0,
    ) -> Tuple[Optional[AlbumPhoto], Optional[str]]:
        """添加照片到相册"""
        # 检查相册是否存在
        album = self.get_album(album_id)
        if not album:
            return None, "相册不存在"

        # 检查媒体文件是否存在
        media = self.db.query(MediaFile).filter(MediaFile.id == media_id).first()
        if not media:
            return None, "媒体文件不存在"

        # 检查是否已添加
        existing = (
            self.db.query(AlbumPhoto)
            .filter(AlbumPhoto.album_id == album_id, AlbumPhoto.media_id == media_id)
            .first()
        )
        if existing:
            return None, "该照片已在相册中"

        # 如果未指定排序，放在最后
        if sort_order == 0:
            max_order = (
                self.db.query(AlbumPhoto)
                .filter(AlbumPhoto.album_id == album_id)
                .count()
            )
            sort_order = max_order

        photo = AlbumPhoto(
            album_id=album_id,
            media_id=media_id,
            caption=caption,
            sort_order=sort_order,
        )
        self.db.add(photo)
        self.db.commit()
        self.db.refresh(photo)

        return photo, None

    def add_photos_batch(
        self, album_id: int, media_ids: List[int]
    ) -> Tuple[int, List[str]]:
        """批量添加照片"""
        added_count = 0
        errors = []

        for media_id in media_ids:
            photo, error = self.add_photo(album_id, media_id)
            if photo:
                added_count += 1
            else:
                errors.append(f"媒体文件 {media_id}: {error}")

        return added_count, errors

    def remove_photo(
        self, album_id: int, photo_id: int
    ) -> Tuple[bool, Optional[str]]:
        """从相册移除照片"""
        photo = (
            self.db.query(AlbumPhoto)
            .filter(AlbumPhoto.id == photo_id, AlbumPhoto.album_id == album_id)
            .first()
        )

        if not photo:
            return False, "照片不存在"

        self.db.delete(photo)
        self.db.commit()
        return True, None

    def update_photo_caption(
        self, photo_id: int, caption: str
    ) -> Tuple[bool, Optional[str]]:
        """更新照片说明"""
        photo = self.db.query(AlbumPhoto).filter(AlbumPhoto.id == photo_id).first()

        if not photo:
            return False, "照片不存在"

        photo.caption = caption
        self.db.commit()
        return True, None

    def sort_photos(
        self, album_id: int, photo_orders: List[Tuple[int, int]]
    ) -> Tuple[bool, Optional[str]]:
        """
        排序相册照片

        Args:
            album_id: 相册 ID
            photo_orders: [(photo_id, sort_order), ...] 照片ID和排序值的列表
        """
        album = self.get_album(album_id)
        if not album:
            return False, "相册不存在"

        for photo_id, sort_order in photo_orders:
            photo = (
                self.db.query(AlbumPhoto)
                .filter(AlbumPhoto.id == photo_id, AlbumPhoto.album_id == album_id)
                .first()
            )
            if photo:
                photo.sort_order = sort_order

        self.db.commit()
        return True, None

    def set_cover(self, album_id: int, media_id: int) -> Tuple[bool, Optional[str]]:
        """设置相册封面"""
        album = self.get_album(album_id)
        if not album:
            return False, "相册不存在"

        # 检查媒体文件是否存在
        media = self.db.query(MediaFile).filter(MediaFile.id == media_id).first()
        if not media:
            return False, "媒体文件不存在"

        album.cover_media_id = media_id
        self.db.commit()
        return True, None

    # ============================================================
    # 工具方法
    # ============================================================

    def generate_slug(self, text: str) -> str:
        """
        生成 URL slug

        将中文转换为拼音，移除特殊字符
        """
        # 转小写
        slug = text.lower()

        # 替换空格为连字符
        slug = re.sub(r"\s+", "-", slug)

        # 移除特殊字符（保留字母、数字、连字符、下划线）
        slug = re.sub(r"[^a-z0-9\u4e00-\u9fa5-_]", "", slug)

        # 移除多余的连字符
        slug = re.sub(r"-+", "-", slug)

        # 移除首尾连字符
        slug = slug.strip("-")

        # 如果 slug 为空，使用时间戳
        if not slug:
            slug = f"album-{int(datetime.now().timestamp())}"

        return slug

    def increment_view_count(self, album_id: int):
        """增加浏览次数"""
        album = self.get_album(album_id)
        if album:
            album.view_count += 1
            self.db.commit()

    def get_statistics(self) -> dict:
        """获取相册统计信息"""
        total_albums = self.db.query(Album).count()
        published_albums = (
            self.db.query(Album).filter(Album.status == "published").count()
        )
        draft_albums = self.db.query(Album).filter(Album.status == "draft").count()
        total_photos = self.db.query(AlbumPhoto).count()

        return {
            "total_albums": total_albums,
            "published_albums": published_albums,
            "draft_albums": draft_albums,
            "total_photos": total_photos,
        }
