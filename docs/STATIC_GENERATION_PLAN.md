# 静态 HTML 生成功能实施计划

**文档版本**: v1.0
**创建日期**: 2025-11-17
**项目**: 博文教育曼彻斯特 CMS
**功能目标**: 添加类似 DedeCMS 的静态页面生成功能

---

## 📋 一、需求概述

### 1.1 功能描述

在现有博文教育 CMS 系统基础上，添加**静态 HTML 页面生成功能**，类似 DedeCMS 的静态化功能：

- 管理员可在后台手动触发静态页面生成
- 支持全站生成或选择性生成
- 内容更新时自动重新生成对应页面
- 生成的静态 HTML 文件可被 Web 服务器直接服务
- 表单提交改为 AJAX 方式，提交到动态 API

### 1.2 用户需求确认

基于与用户的沟通，确认以下关键需求：

| 配置项 | 用户选择 | 说明 |
|--------|---------|------|
| **输出目录** | `public/` (新建目录) | 独立目录，与源代码分离 |
| **后台位置** | 独立的「静态页面管理」菜单 | 专门的管理页面，便于操作 |
| **生成范围** | ✅ 支持全站生成<br>✅ 支持单页生成 | 灵活的生成粒度控制 |
| **触发方式** | ✅ 手动触发<br>✅ 内容更新自动生成 | 手动控制 + 自动化 |

### 1.3 技术目标

- ✅ **零破坏性**：不影响现有动态网站功能
- ✅ **高性能**：静态页面加载速度 < 200ms
- ✅ **易维护**：基于现有代码结构，逻辑清晰
- ✅ **可扩展**：支持未来添加更多页面类型

---

## 📊 二、当前系统分析

### 2.1 前台路由结构

**主要动态路由** (`app/routes/frontend.py`):

```python
# 首页
GET /                    # 中文首页
GET /zh/                 # 中文首页（显式）
GET /en/                 # 英文首页

# 栏目页（列表页）
GET /{column_slug}       # 中文栏目页
GET /en/{column_slug}    # 英文栏目页

# 详情页
GET /{column_slug}/{item_slug}          # 详情页
GET /{column_slug}/detail/{item_slug}   # 详情页（旧版URL）

# 表单提交（需要保持动态）
POST /contact/submit     # 联系表单提交
POST /api/contact        # API 联系表单（JSON）
POST /guestbook/submit   # 留言板提交
```

### 2.2 模板文件统计

**中文模板** (`templates/zh/`): 26 个模板文件
**英文模板** (`templates/en/`): 26 个模板文件（结构相同）

**关键模板**：
- `index.html` - 首页
- `single_page.html` - 单页模板
- `product_list.html`, `product_detail.html` - 产品
- `post_list.html`, `post_list_universal.html`, `post_detail.html` - 文章
- `events.html` - 活动列表
- `contact.html` - 联系页面（包含表单）

### 2.3 数据库内容统计

| 内容类型 | 表名 | 已发布数量 | 双语支持 |
|---------|------|----------|---------|
| 产品（课程） | `product` | 7 | ✅ |
| 文章 | `post` | 21 | ✅ |
| 单页 | `single_page` | 24 | ✅ |
| 活动 | `event` | 8 | ✅ |
| 栏目 | `site_column` | 33 | ✅ |

**双语字段命名规则**：
- 中文字段：`name`, `title`, `content_html` 等
- 英文字段：`name_en`, `title_en`, `content_html_en` 等

### 2.4 栏目类型分析

```python
class ColumnType(str, enum.Enum):
    SINGLE_PAGE = "SINGLE_PAGE"  # 单页（如：关于我们、联系我们）
    POST = "POST"                # 文章栏目（如：新闻、博客）
    PRODUCT = "PRODUCT"          # 产品栏目（如：课程）
    GALLERY = "GALLERY"          # 相册模块
    CUSTOM = "CUSTOM"            # 自定义模块
```

**重要栏目列表**（15 个顶级栏目）：
1. 首页 (home) - CUSTOM
2. 关于博文 (about) - SINGLE_PAGE
3. 中文学校 (school) - CUSTOM
4. 补习中心 (tuition) - PRODUCT
5. 国际象棋俱乐部 (chess) - CUSTOM
6. 羽毛球俱乐部 (badminton) - CUSTOM
7. 政府项目 (programmes) - CUSTOM
8. 博文活动 (events) - CUSTOM
9. 博文新闻 (news) - POST
10. 图库 (gallery) - GALLERY
11. 常见问题 (faq) - SINGLE_PAGE
12. 联系我们 (contact) - SINGLE_PAGE
13. 隐私政策 (privacy) - SINGLE_PAGE
14. 使用条款 (terms) - SINGLE_PAGE
15. Cookie政策 (cookie-policy) - SINGLE_PAGE

### 2.5 需要 AJAX 转换的表单

| 表单位置 | 当前实现 | 目标实现 | API 端点 |
|---------|---------|---------|---------|
| 联系表单 | `<form method="POST" action="/contact/submit">` | AJAX 提交 | `/api/contact` |
| 留言板 | `<form method="POST" action="/guestbook/submit">` | AJAX 提交 | `/guestbook/submit` |
| 活动报名 | 未实现 | （如需要）AJAX 提交 | `/api/event/register` |

---

## 🏗️ 三、技术方案设计

### 3.1 静态生成架构

```
静态生成系统架构
┌─────────────────────────────────────────────────────┐
│            管理后台触发                              │
│  /admin/static-pages (管理界面)                      │
│  ├─ 全站生成按钮                                     │
│  ├─ 选择性生成                                       │
│  └─ 生成历史                                         │
└─────────────────┬───────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────┐
│         StaticPageGenerator (核心生成器)             │
│  app/services/static_generator.py                   │
│  ├─ generate_all() - 全站生成                        │
│  ├─ _generate_homepage() - 首页                      │
│  ├─ _generate_all_products() - 产品                  │
│  ├─ _generate_all_posts() - 文章                     │
│  ├─ _generate_all_single_pages() - 单页              │
│  └─ _generate_all_events() - 活动                    │
└─────────────────┬───────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────┐
│          模板渲染 (Jinja2)                           │
│  ├─ 复用现有模板 (templates/zh/, templates/en/)      │
│  ├─ 模拟 Request 对象                                │
│  ├─ 注入上下文数据                                   │
│  └─ 渲染为 HTML 字符串                               │
└─────────────────┬───────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────┐
│         文件系统输出 (public/)                        │
│  public/                                            │
│  ├─ zh/                                             │
│  │   ├─ index.html (首页)                           │
│  │   ├─ school/index.html                           │
│  │   ├─ tuition/                                    │
│  │   │   ├─ index.html (列表)                       │
│  │   │   └─ chess-course/index.html (详情)          │
│  │   └─ news/                                       │
│  │       ├─ index.html (列表第1页)                   │
│  │       ├─ page-2/index.html (列表第2页)            │
│  │       └─ article-slug/index.html (详情)           │
│  └─ en/ (结构同zh/)                                  │
└─────────────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────┐
│        Web 服务器服务 (Nginx 或 FastAPI)              │
│  Nginx 配置:                                         │
│  location / {                                       │
│      try_files $uri $uri/ @dynamic;                 │
│  }                                                  │
│  location @dynamic {                                │
│      proxy_pass http://localhost:10034;            │
│  }                                                  │
└─────────────────────────────────────────────────────┘
```

### 3.2 URL 映射策略

**动态 URL → 静态文件路径**：

| 动态 URL | 静态文件路径 | 说明 |
|---------|-------------|------|
| `/` 或 `/zh/` | `public/zh/index.html` | 中文首页 |
| `/en/` | `public/en/index.html` | 英文首页 |
| `/school` | `public/zh/school/index.html` | 栏目页 |
| `/en/school` | `public/en/school/index.html` | 英文栏目页 |
| `/tuition` | `public/zh/tuition/index.html` | 产品列表 |
| `/tuition/chess-course` | `public/zh/tuition/chess-course/index.html` | 产品详情 |
| `/news` | `public/zh/news/index.html` | 文章列表（第1页） |
| `/news?page=2` | `public/zh/news/page-2/index.html` | 文章列表（第2页） |
| `/news/article-slug` | `public/zh/news/article-slug/index.html` | 文章详情 |
| `/events` | `public/zh/events/index.html` | 活动列表 |

**URL 规范化规则**：
1. 所有页面使用 `/index.html` 结尾（利于 Web 服务器默认索引）
2. 中文页面放在 `public/zh/` 目录
3. 英文页面放在 `public/en/` 目录
4. 分页使用 `page-N/index.html` 格式
5. 栏目和详情页使用 slug 作为目录名

### 3.3 数据库扩展 - 生成日志

创建两张新表记录生成历史：

#### 表1: `static_generation_log` (生成任务日志)

```sql
CREATE TABLE static_generation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generation_type VARCHAR(20) NOT NULL,     -- 'full' 或 'partial'
    total_pages INTEGER DEFAULT 0,            -- 总页面数
    successful_pages INTEGER DEFAULT 0,       -- 成功生成数
    failed_pages INTEGER DEFAULT 0,           -- 失败数
    start_time DATETIME NOT NULL,             -- 开始时间
    end_time DATETIME,                        -- 结束时间
    status VARCHAR(20) DEFAULT 'running',     -- 'running', 'completed', 'failed'
    error_message TEXT,                       -- 错误信息
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 表2: `static_generation_detail` (页面生成详情)

```sql
CREATE TABLE static_generation_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER NOT NULL,                  -- 关联 log 表
    page_type VARCHAR(20) NOT NULL,           -- 'home', 'product', 'post', 'single_page', 'event'
    page_id INTEGER,                          -- 页面ID（如产品ID、文章ID）
    language VARCHAR(5) NOT NULL,             -- 'zh' 或 'en'
    url_path VARCHAR(500) NOT NULL,           -- URL路径（如 /zh/tuition/chess）
    file_path VARCHAR(500) NOT NULL,          -- 文件路径（如 public/zh/tuition/chess/index.html）
    status VARCHAR(20) DEFAULT 'success',     -- 'success', 'failed'
    error_message TEXT,                       -- 错误信息
    generation_time FLOAT,                    -- 生成耗时（秒）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(log_id) REFERENCES static_generation_log(id) ON DELETE CASCADE
);

CREATE INDEX idx_generation_detail_log_id ON static_generation_detail(log_id);
CREATE INDEX idx_generation_detail_page_type ON static_generation_detail(page_type);
```

### 3.4 核心生成器设计

#### 类结构：`StaticPageGenerator`

```python
from pathlib import Path
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
import logging

class StaticPageGenerator:
    """静态页面生成器"""

    def __init__(self, db: Session, output_dir: Path, log_id: Optional[int] = None):
        """
        初始化生成器

        Args:
            db: 数据库会话
            output_dir: 输出目录（如 Path('public')）
            log_id: 生成日志ID（用于记录详情）
        """
        self.db = db
        self.output_dir = output_dir
        self.log_id = log_id
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'errors': []
        }
        self.logger = logging.getLogger("docms.static_generator")

    # ========== 主生成函数 ==========

    def generate_all(self, languages: List[str] = ['zh', 'en']) -> Dict:
        """
        生成全站静态页面

        Args:
            languages: 要生成的语言列表

        Returns:
            统计信息 {'total': 132, 'success': 130, 'failed': 2}
        """
        for lang in languages:
            self._generate_homepage(lang)
            self._generate_all_columns(lang)
            self._generate_all_products(lang)
            self._generate_all_posts(lang)
            self._generate_all_single_pages(lang)
            self._generate_all_events(lang)

        return self.stats

    # ========== 各类型页面生成 ==========

    def _generate_homepage(self, lang: str):
        """生成首页"""
        # 实现逻辑...

    def _generate_all_columns(self, lang: str):
        """生成所有栏目列表页"""
        # 实现逻辑...

    def _generate_all_products(self, lang: str):
        """生成所有产品页面（列表+详情）"""
        # 实现逻辑...

    def _generate_all_posts(self, lang: str):
        """生成所有文章页面（列表+详情+分页）"""
        # 实现逻辑...

    def _generate_all_single_pages(self, lang: str):
        """生成所有单页"""
        # 实现逻辑...

    def _generate_all_events(self, lang: str):
        """生成活动列表页"""
        # 实现逻辑...

    # ========== 辅助函数 ==========

    def _render_template(
        self,
        template_name: str,
        context: Dict,
        lang: str
    ) -> str:
        """渲染模板并返回 HTML 字符串"""
        # 实现逻辑...

    def _save_html(self, html: str, path: Path):
        """保存 HTML 到文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding='utf-8')
        self.logger.info(f"Generated: {path}")

    def _record_detail(
        self,
        page_type: str,
        page_id: Optional[int],
        language: str,
        url_path: str,
        file_path: str,
        status: str,
        generation_time: float,
        error_message: Optional[str] = None
    ):
        """记录页面生成详情到数据库"""
        if self.log_id:
            detail = StaticGenerationDetail(
                log_id=self.log_id,
                page_type=page_type,
                page_id=page_id,
                language=language,
                url_path=url_path,
                file_path=file_path,
                status=status,
                generation_time=generation_time,
                error_message=error_message
            )
            self.db.add(detail)
            self.db.commit()
```

### 3.5 模板渲染技术

使用 **Jinja2 模板引擎**（项目已使用）：

```python
from jinja2 import Environment, FileSystemLoader
from starlette.requests import Request

def create_mock_request(url_path: str) -> Request:
    """创建模拟的 Request 对象"""
    scope = {
        "type": "http",
        "method": "GET",
        "path": url_path,
        "query_string": b"",
        "headers": [],
        "server": ("localhost", 8000),
    }
    return Request(scope)

def render_template_to_html(
    template_name: str,
    context: Dict,
    lang: str
) -> str:
    """渲染模板为 HTML 字符串"""
    # 使用项目现有的模板引擎
    from app.routes.frontend import get_template_engine

    templates = get_template_engine(lang)
    template = templates.env.get_template(template_name)

    return template.render(**context)
```

**关键点**：
1. **Request 对象模拟**：创建最小化的 Request 对象供模板使用
2. **上下文复用**：重用 `get_base_context()` 函数获取导航、设置等数据
3. **模板函数**：确保注册与动态模板相同的 Jinja2 全局函数（`product_list`, `post_list` 等）

---

## 🎯 四、详细实施计划

### 阶段一：核心生成器开发（3-4天）

#### 任务 1.1：创建数据模型（0.5天）

**文件**: `app/models/static_generation.py`

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class StaticGenerationLog(BaseModel):
    """静态生成日志"""
    __tablename__ = "static_generation_log"

    id = Column(Integer, primary_key=True)
    generation_type = Column(String(20), nullable=False)  # 'full' or 'partial'
    total_pages = Column(Integer, default=0)
    successful_pages = Column(Integer, default=0)
    failed_pages = Column(Integer, default=0)
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime)
    status = Column(String(20), default='running')  # 'running', 'completed', 'failed'
    error_message = Column(Text)

    # 关系
    details = relationship("StaticGenerationDetail", back_populates="log", cascade="all, delete-orphan")


class StaticGenerationDetail(BaseModel):
    """页面生成详情"""
    __tablename__ = "static_generation_detail"

    id = Column(Integer, primary_key=True)
    log_id = Column(Integer, ForeignKey('static_generation_log.id'), nullable=False)
    page_type = Column(String(20), nullable=False)
    page_id = Column(Integer)
    language = Column(String(5), nullable=False)
    url_path = Column(String(500), nullable=False)
    file_path = Column(String(500), nullable=False)
    status = Column(String(20), default='success')
    error_message = Column(Text)
    generation_time = Column(Float)  # 秒

    # 关系
    log = relationship("StaticGenerationLog", back_populates="details")
```

**数据库迁移**：
```bash
alembic revision --autogenerate -m "Add static generation log tables"
alembic upgrade head
```

#### 任务 1.2：创建生成器核心（2天）

**文件**: `app/services/static_generator.py`

**实现内容**：
1. `StaticPageGenerator` 类
2. 各类型页面生成函数
3. 模板渲染辅助函数
4. 文件保存与日志记录

**示例实现**（产品详情页生成）：

```python
def _generate_product_detail(
    self,
    column: SiteColumn,
    product: Product,
    lang: str
):
    """生成单个产品详情页"""
    import time
    start_time = time.time()

    # 1. 构建 URL 和文件路径
    if lang == 'zh':
        url_path = f"/{column.slug}/{product.slug}"
        file_path = self.output_dir / 'zh' / column.slug / product.slug / 'index.html'
    else:
        url_path = f"/en/{column.slug}/{product.slug}"
        file_path = self.output_dir / 'en' / column.slug / product.slug / 'index.html'

    # 2. 创建模拟请求
    mock_request = create_mock_request(url_path)

    # 3. 构建上下文（复用动态路由的逻辑）
    from app.routes.frontend import get_base_context
    context = get_base_context(mock_request, self.db, lang=lang)
    context['column'] = column
    context['product'] = product

    # 获取相关产品
    if product.categories:
        from app.services import product_service
        context['related_products'] = product_service.get_products(
            self.db,
            category_id=product.categories[0].id,
            limit=4
        )

    # 4. 渲染模板
    try:
        html = self._render_template('product_detail.html', context, lang)

        # 5. 保存文件
        self._save_html(html, file_path)

        # 6. 记录详情
        generation_time = time.time() - start_time
        self._record_detail(
            page_type='product',
            page_id=product.id,
            language=lang,
            url_path=url_path,
            file_path=str(file_path),
            status='success',
            generation_time=generation_time
        )

        self.stats['success'] += 1
        self.stats['total'] += 1

        self.logger.info(f"✓ Generated product: {url_path} ({generation_time:.2f}s)")

    except Exception as e:
        self.logger.error(f"✗ Failed to generate {url_path}: {e}")

        generation_time = time.time() - start_time
        self._record_detail(
            page_type='product',
            page_id=product.id,
            language=lang,
            url_path=url_path,
            file_path=str(file_path),
            status='failed',
            generation_time=generation_time,
            error_message=str(e)
        )

        self.stats['failed'] += 1
        self.stats['total'] += 1
        self.stats['errors'].append({
            'page': url_path,
            'error': str(e)
        })
```

#### 任务 1.3：单元测试（0.5天）

**文件**: `tests/test_static_generator.py`

```python
import pytest
from pathlib import Path
from app.services.static_generator import StaticPageGenerator
from app.database import SessionLocal

def test_generate_homepage():
    """测试首页生成"""
    db = SessionLocal()
    output_dir = Path('test_output')

    generator = StaticPageGenerator(db, output_dir)
    generator._generate_homepage('zh')

    # 验证文件存在
    assert (output_dir / 'zh' / 'index.html').exists()

    # 清理
    import shutil
    shutil.rmtree(output_dir)

def test_generate_product_detail():
    """测试产品详情页生成"""
    # 实现测试逻辑...
```

#### 任务 1.4：命令行工具（0.5天）

**文件**: `scripts/generate_static.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态页面生成命令行工具

用法:
    python scripts/generate_static.py --all                    # 全站生成
    python scripts/generate_static.py --lang zh                # 仅生成中文
    python scripts/generate_static.py --type product           # 仅生成产品
    python scripts/generate_static.py --page-id 123 --page-type product  # 生成单个产品
"""

import sys
sys.path.insert(0, '.')

import argparse
from pathlib import Path
from app.database import SessionLocal
from app.services.static_generator import StaticPageGenerator

def main():
    parser = argparse.ArgumentParser(description='静态页面生成工具')
    parser.add_argument('--all', action='store_true', help='生成全站')
    parser.add_argument('--lang', choices=['zh', 'en', 'both'], default='both', help='生成语言')
    parser.add_argument('--type', choices=['home', 'product', 'post', 'single_page', 'event'], help='页面类型')
    parser.add_argument('--page-id', type=int, help='页面ID（配合 --page-type 使用）')
    parser.add_argument('--page-type', help='页面类型（配合 --page-id 使用）')
    parser.add_argument('--output', default='public', help='输出目录')

    args = parser.parse_args()

    db = SessionLocal()
    output_dir = Path(args.output)
    generator = StaticPageGenerator(db, output_dir)

    if args.all:
        print("🚀 开始全站生成...")
        languages = ['zh', 'en'] if args.lang == 'both' else [args.lang]
        stats = generator.generate_all(languages)
        print(f"\n✅ 生成完成！")
        print(f"   总计: {stats['total']} 页")
        print(f"   成功: {stats['success']} 页")
        print(f"   失败: {stats['failed']} 页")
    elif args.type:
        print(f"🚀 生成 {args.type} 类型页面...")
        # 实现部分生成逻辑
    elif args.page_id and args.page_type:
        print(f"🚀 生成单页: {args.page_type} #{args.page_id}")
        # 实现单页生成逻辑
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

**使用权限**：
```bash
chmod +x scripts/generate_static.py
```

---

### 阶段二：管理后台开发（2天）

#### 任务 2.1：创建路由（0.5天）

**文件**: `admin/app/routers/static_pages.py`

```python
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from admin.app.dependencies import require_admin
from admin.app.templates import admin_templates
from app.models.static_generation import StaticGenerationLog, StaticGenerationDetail
from datetime import datetime
from pathlib import Path

router = APIRouter()

@router.get("/static-pages", response_class=HTMLResponse)
async def static_pages_management(
    request: Request,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """静态页面管理界面"""

    # 获取最近的生成历史
    recent_logs = db.query(StaticGenerationLog).order_by(
        StaticGenerationLog.created_at.desc()
    ).limit(20).all()

    return admin_templates.TemplateResponse(
        "static_pages/index.html",
        {
            "request": request,
            "recent_logs": recent_logs,
        }
    )

@router.post("/static-pages/generate-all")
async def generate_all_static_pages(
    background_tasks: BackgroundTasks,
    languages: str = 'both',  # 'both', 'zh', 'en'
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """触发全站静态页面生成"""
    from app.services.static_generator import StaticPageGenerator

    # 创建生成日志
    log = StaticGenerationLog(
        generation_type='full',
        status='running',
        start_time=datetime.now()
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # 在后台任务中执行生成
    def generate_task():
        try:
            generator = StaticPageGenerator(
                db=db,
                output_dir=Path('public'),
                log_id=log.id
            )

            langs = ['zh', 'en'] if languages == 'both' else [languages]
            stats = generator.generate_all(langs)

            # 更新日志
            log.total_pages = stats['total']
            log.successful_pages = stats['success']
            log.failed_pages = stats['failed']
            log.status = 'completed' if stats['failed'] == 0 else 'partial'
            log.end_time = datetime.now()

            if stats['errors']:
                log.error_message = '\n'.join([
                    f"{err['page']}: {err['error']}" for err in stats['errors'][:10]
                ])

            db.commit()

        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.end_time = datetime.now()
            db.commit()

    background_tasks.add_task(generate_task)

    return JSONResponse({
        "success": True,
        "message": "静态页面生成任务已启动",
        "log_id": log.id
    })

@router.post("/static-pages/generate-single")
async def generate_single_page(
    page_type: str,
    page_id: int,
    language: str = 'both',
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """生成单个页面"""
    from app.services.static_generator import StaticPageGenerator

    # 创建日志
    log = StaticGenerationLog(
        generation_type='partial',
        status='running',
        start_time=datetime.now()
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    try:
        generator = StaticPageGenerator(db, Path('public'), log.id)
        langs = ['zh', 'en'] if language == 'both' else [language]

        # 根据类型生成
        if page_type == 'product':
            from app.models.product import Product
            product = db.query(Product).filter(Product.id == page_id).first()
            if product:
                for lang in langs:
                    generator._generate_product_detail(product.column, product, lang)

        # ... 其他类型类似

        log.total_pages = generator.stats['total']
        log.successful_pages = generator.stats['success']
        log.failed_pages = generator.stats['failed']
        log.status = 'completed'
        log.end_time = datetime.now()
        db.commit()

        return JSONResponse({
            "success": True,
            "message": f"生成完成: {generator.stats['success']} 页"
        })

    except Exception as e:
        log.status = 'failed'
        log.error_message = str(e)
        log.end_time = datetime.now()
        db.commit()

        return JSONResponse({
            "success": False,
            "message": str(e)
        }, status_code=500)

@router.get("/static-pages/progress/{log_id}")
async def get_generation_progress(
    log_id: int,
    db: Session = Depends(get_db)
):
    """获取生成进度（用于前端轮询）"""
    log = db.query(StaticGenerationLog).filter(
        StaticGenerationLog.id == log_id
    ).first()

    if not log:
        return JSONResponse({"error": "Log not found"}, status_code=404)

    progress = 0
    if log.total_pages > 0:
        progress = (log.successful_pages + log.failed_pages) / log.total_pages * 100

    return JSONResponse({
        "status": log.status,
        "total": log.total_pages,
        "success": log.successful_pages,
        "failed": log.failed_pages,
        "progress": round(progress, 1),
        "error_message": log.error_message
    })

@router.delete("/static-pages/clear-output")
async def clear_static_output(
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin)
):
    """清空静态输出目录"""
    import shutil

    output_dir = Path('public')
    if output_dir.exists():
        shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)

    return JSONResponse({
        "success": True,
        "message": "静态输出目录已清空"
    })
```

**注册路由**（在 `admin/app/main.py`）：

```python
from admin.app.routers import static_pages

app.include_router(
    static_pages.router,
    prefix="/admin",
    tags=["static-pages"]
)
```

#### 任务 2.2：创建管理界面（1天）

**文件**: `admin/templates/static_pages/index.html`

```html
{% extends "base.html" %}

{% block title %}静态页面管理 - 博文教育 CMS{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <!-- 页面标题 -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3 mb-0">
            <i class="fas fa-file-code"></i> 静态页面生成
        </h1>
        <div>
            <button class="btn btn-outline-secondary btn-sm" onclick="location.reload()">
                <i class="fas fa-sync-alt"></i> 刷新
            </button>
        </div>
    </div>

    <!-- 说明卡片 -->
    <div class="alert alert-info mb-4" role="alert">
        <i class="fas fa-info-circle"></i>
        <strong>功能说明:</strong> 将动态网站页面生成为静态 HTML 文件，提升访问速度，降低服务器负载。
        生成的文件保存在 <code>public/</code> 目录，可通过 Web 服务器（如 Nginx）直接服务。
    </div>

    <!-- 生成控制面板 -->
    <div class="row mb-4">
        <!-- 全站生成 -->
        <div class="col-md-6 mb-3">
            <div class="card h-100 shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0"><i class="fas fa-globe"></i> 全站生成</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">生成所有中英文页面，包括：</p>
                    <ul class="mb-3">
                        <li>首页 (2页)</li>
                        <li>产品列表 + 详情页 (~14页)</li>
                        <li>文章列表 + 详情页 (~42页)</li>
                        <li>单页 (~48页)</li>
                        <li>活动列表 (~2页)</li>
                    </ul>
                    <div class="alert alert-warning alert-sm mb-3">
                        <small>
                            <i class="fas fa-clock"></i>
                            预计生成 <strong>~130+</strong> 页面，耗时 <strong>1-2 分钟</strong>
                        </small>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">生成语言</label>
                        <select class="form-select" id="fullSiteLanguage">
                            <option value="both" selected>中英文</option>
                            <option value="zh">仅中文</option>
                            <option value="en">仅英文</option>
                        </select>
                    </div>

                    <button class="btn btn-primary btn-lg w-100" id="generateAllBtn">
                        <i class="fas fa-rocket"></i> 开始全站生成
                    </button>
                </div>
            </div>
        </div>

        <!-- 选择性生成 -->
        <div class="col-md-6 mb-3">
            <div class="card h-100 shadow-sm">
                <div class="card-header bg-secondary text-white">
                    <h5 class="mb-0"><i class="fas fa-cog"></i> 选择性生成</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label class="form-label">页面类型</label>
                        <select class="form-select" id="partialPageType">
                            <option value="home">首页</option>
                            <option value="product">所有产品页</option>
                            <option value="post">所有文章页</option>
                            <option value="single_page">所有单页</option>
                            <option value="event">所有活动页</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">语言</label>
                        <select class="form-select" id="partialLanguage">
                            <option value="both">中英文</option>
                            <option value="zh">仅中文</option>
                            <option value="en">仅英文</option>
                        </select>
                    </div>

                    <button class="btn btn-secondary btn-lg w-100" id="generatePartialBtn">
                        <i class="fas fa-tasks"></i> 开始选择性生成
                    </button>

                    <hr>

                    <h6 class="mt-3">或生成单个页面:</h6>
                    <div class="input-group mb-3">
                        <select class="form-select" id="singlePageType">
                            <option value="product">产品</option>
                            <option value="post">文章</option>
                            <option value="single_page">单页</option>
                        </select>
                        <input type="number" class="form-control" id="singlePageId" placeholder="页面 ID">
                        <button class="btn btn-outline-secondary" id="generateSingleBtn">
                            <i class="fas fa-file"></i> 生成
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 进度显示卡片 -->
    <div class="card mb-4 shadow-sm" id="progressCard" style="display: none;">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0"><i class="fas fa-spinner fa-spin"></i> 生成进度</h5>
        </div>
        <div class="card-body">
            <div class="progress mb-3" style="height: 35px;">
                <div class="progress-bar progress-bar-striped progress-bar-animated bg-success"
                     role="progressbar"
                     id="progressBar"
                     style="width: 0%">
                    <span id="progressText" class="fw-bold">0%</span>
                </div>
            </div>
            <div class="row text-center">
                <div class="col">
                    <div class="text-muted small">总计</div>
                    <div class="h4 mb-0" id="totalPages">0</div>
                </div>
                <div class="col">
                    <div class="text-muted small">成功</div>
                    <div class="h4 mb-0 text-success" id="successPages">0</div>
                </div>
                <div class="col">
                    <div class="text-muted small">失败</div>
                    <div class="h4 mb-0 text-danger" id="failedPages">0</div>
                </div>
            </div>
            <div class="mt-3">
                <p class="mb-0" id="progressStatus">准备中...</p>
            </div>
        </div>
    </div>

    <!-- 生成历史 -->
    <div class="card shadow-sm">
        <div class="card-header">
            <h5 class="mb-0"><i class="fas fa-history"></i> 生成历史</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover table-striped">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>开始时间</th>
                            <th>类型</th>
                            <th>总页面</th>
                            <th>成功</th>
                            <th>失败</th>
                            <th>耗时</th>
                            <th>状态</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if recent_logs %}
                            {% for log in recent_logs %}
                            <tr>
                                <td>#{{ log.id }}</td>
                                <td>{{ log.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                                <td>
                                    {% if log.generation_type == 'full' %}
                                        <span class="badge bg-primary">全站</span>
                                    {% else %}
                                        <span class="badge bg-secondary">部分</span>
                                    {% endif %}
                                </td>
                                <td>{{ log.total_pages }}</td>
                                <td class="text-success fw-bold">{{ log.successful_pages }}</td>
                                <td class="text-danger fw-bold">{{ log.failed_pages }}</td>
                                <td>
                                    {% if log.end_time and log.start_time %}
                                        {{ "%.1f"|format((log.end_time - log.start_time).total_seconds()) }}秒
                                    {% else %}
                                        <span class="text-muted">-</span>
                                    {% endif %}
                                </td>
                                <td>
                                    {% if log.status == 'completed' %}
                                        <span class="badge bg-success">完成</span>
                                    {% elif log.status == 'running' %}
                                        <span class="badge bg-info">进行中</span>
                                    {% elif log.status == 'failed' %}
                                        <span class="badge bg-danger">失败</span>
                                    {% elif log.status == 'partial' %}
                                        <span class="badge bg-warning">部分成功</span>
                                    {% endif %}
                                </td>
                                <td>
                                    {% if log.error_message %}
                                        <button class="btn btn-sm btn-outline-danger"
                                                onclick="showError({{ log.id }}, '{{ log.error_message|escape }}')">
                                            <i class="fas fa-exclamation-circle"></i> 查看错误
                                        </button>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="9" class="text-center text-muted">
                                    暂无生成历史
                                </td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- 清空输出目录（危险操作） -->
    <div class="card border-danger mt-4">
        <div class="card-header bg-danger text-white">
            <h6 class="mb-0"><i class="fas fa-exclamation-triangle"></i> 危险操作</h6>
        </div>
        <div class="card-body">
            <p class="mb-2">清空 <code>public/</code> 目录下的所有静态文件</p>
            <button class="btn btn-danger btn-sm" onclick="confirmClearOutput()">
                <i class="fas fa-trash"></i> 清空静态输出目录
            </button>
        </div>
    </div>
</div>

<!-- 错误详情模态框 -->
<div class="modal fade" id="errorModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title">生成错误详情</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <pre id="errorContent" class="bg-light p-3 rounded"></pre>
            </div>
        </div>
    </div>
</div>

<script>
// 全站生成
document.getElementById('generateAllBtn').addEventListener('click', async () => {
    const language = document.getElementById('fullSiteLanguage').value;

    if (!confirm('确定要生成全站静态页面吗？这将需要 1-2 分钟。')) return;

    const progressCard = document.getElementById('progressCard');
    progressCard.style.display = 'block';
    progressCard.scrollIntoView({ behavior: 'smooth' });

    try {
        const response = await fetch('/admin/static-pages/generate-all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `languages=${language}`
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('progressStatus').textContent = '生成任务已启动，正在生成页面...';
            pollProgress(data.log_id);
        } else {
            alert('生成失败: ' + data.message);
            progressCard.style.display = 'none';
        }
    } catch (error) {
        alert('生成失败: ' + error.message);
        progressCard.style.display = 'none';
    }
});

// 单页生成
document.getElementById('generateSingleBtn').addEventListener('click', async () => {
    const pageType = document.getElementById('singlePageType').value;
    const pageId = document.getElementById('singlePageId').value;

    if (!pageId) {
        alert('请输入页面 ID');
        return;
    }

    try {
        const response = await fetch('/admin/static-pages/generate-single', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `page_type=${pageType}&page_id=${pageId}&language=both`
        });

        const data = await response.json();

        if (data.success) {
            alert('✓ ' + data.message);
            location.reload();
        } else {
            alert('✗ ' + data.message);
        }
    } catch (error) {
        alert('生成失败: ' + error.message);
    }
});

// 轮询进度
function pollProgress(logId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`/admin/static-pages/progress/${logId}`);
            const data = await response.json();

            const progressBar = document.getElementById('progressBar');
            const progressText = document.getElementById('progressText');
            const progressStatus = document.getElementById('progressStatus');
            const totalPages = document.getElementById('totalPages');
            const successPages = document.getElementById('successPages');
            const failedPages = document.getElementById('failedPages');

            progressBar.style.width = data.progress + '%';
            progressText.textContent = Math.round(data.progress) + '%';
            progressStatus.textContent = `已生成 ${data.success + data.failed}/${data.total} 页面`;
            totalPages.textContent = data.total;
            successPages.textContent = data.success;
            failedPages.textContent = data.failed;

            if (data.status === 'completed' || data.status === 'partial' || data.status === 'failed') {
                clearInterval(interval);
                progressBar.classList.remove('progress-bar-animated');

                if (data.status === 'completed') {
                    progressBar.classList.remove('bg-success');
                    progressBar.classList.add('bg-success');
                    alert('✅ 生成完成！所有页面均已成功生成。');
                } else if (data.status === 'partial') {
                    progressBar.classList.remove('bg-success');
                    progressBar.classList.add('bg-warning');
                    alert(`⚠️ 生成完成，但有 ${data.failed} 个页面失败。`);
                } else {
                    progressBar.classList.remove('bg-success');
                    progressBar.classList.add('bg-danger');
                    alert('❌ 生成失败: ' + (data.error_message || '未知错误'));
                }

                setTimeout(() => location.reload(), 1000);
            }
        } catch (error) {
            clearInterval(interval);
            alert('获取进度失败: ' + error.message);
        }
    }, 1000);  // 每秒轮询一次
}

// 显示错误详情
function showError(logId, errorMessage) {
    document.getElementById('errorContent').textContent = errorMessage;
    new bootstrap.Modal(document.getElementById('errorModal')).show();
}

// 清空输出目录
function confirmClearOutput() {
    if (confirm('⚠️ 确定要清空静态输出目录吗？这将删除所有已生成的静态文件！')) {
        if (confirm('此操作无法撤销，请再次确认！')) {
            fetch('/admin/static-pages/clear-output', {
                method: 'DELETE'
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✓ 静态输出目录已清空');
                    location.reload();
                } else {
                    alert('✗ 操作失败');
                }
            });
        }
    }
}
</script>

<style>
.alert-sm {
    padding: 0.5rem;
    font-size: 0.875rem;
}

.table-responsive {
    max-height: 500px;
    overflow-y: auto;
}

#errorContent {
    white-space: pre-wrap;
    word-wrap: break-word;
    max-height: 400px;
    overflow-y: auto;
}
</style>
{% endblock %}
```

#### 任务 2.3：添加侧边栏菜单（0.5天）

**文件**: `admin/templates/partials/sidebar.html`

在现有侧边栏中添加菜单项：

```html
<!-- 在 "系统设置" 区块添加 -->
<li class="nav-item">
    <a class="nav-link" href="/admin/static-pages">
        <i class="fas fa-file-code"></i>
        <span>静态页面生成</span>
    </a>
</li>
```

---

### 阶段三：自动生成 Hook（1天）

#### 任务 3.1：产品保存 Hook（0.3天）

**文件**: `admin/app/routers/products.py`

修改产品创建和更新函数：

```python
@router.post("/products")
async def create_product(
    # ... 现有参数
    background_tasks: BackgroundTasks,  # 新增
    db: Session = Depends(get_db),
):
    # ... 现有创建逻辑

    # 保存成功后，检查是否启用自动生成
    if is_auto_regenerate_enabled(db):
        background_tasks.add_task(
            regenerate_product_pages,
            db,
            product.id
        )

    # ... 返回响应

@router.post("/products/{product_id}")
async def update_product(
    product_id: int,
    background_tasks: BackgroundTasks,  # 新增
    # ... 现有参数
):
    # ... 现有更新逻辑

    # 更新成功后，自动重新生成
    if is_auto_regenerate_enabled(db):
        background_tasks.add_task(
            regenerate_product_pages,
            db,
            product_id
        )

    # ... 返回响应

def is_auto_regenerate_enabled(db: Session) -> bool:
    """检查是否启用自动重新生成"""
    from app.models.site import SiteSetting
    setting = db.query(SiteSetting).filter(
        SiteSetting.key == 'auto_regenerate_static'
    ).first()
    return setting and setting.value == 'true'

def regenerate_product_pages(db: Session, product_id: int):
    """重新生成产品相关页面"""
    from app.services.static_generator import StaticPageGenerator
    from app.models.product import Product
    from pathlib import Path
    import logging

    logger = logging.getLogger("docms.static_generator")

    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f"Product {product_id} not found for regeneration")
            return

        generator = StaticPageGenerator(db, Path('public'))

        # 生成中文版本
        generator._generate_product_detail(product.column, product, 'zh')
        # 生成英文版本
        generator._generate_product_detail(product.column, product, 'en')

        # 重新生成产品列表页
        generator._generate_product_list(product.column, 'zh')
        generator._generate_product_list(product.column, 'en')

        logger.info(f"✓ Auto-regenerated product pages for #{product_id}")

    except Exception as e:
        logger.error(f"✗ Failed to auto-regenerate product #{product_id}: {e}")
```

#### 任务 3.2：文章保存 Hook（0.3天）

**文件**: `admin/app/routers/posts.py`

类似产品的实现，添加文章的自动生成逻辑。

#### 任务 3.3：单页保存 Hook（0.3天）

**文件**: `admin/app/routers/single_pages.py`

类似产品的实现，添加单页的自动生成逻辑。

#### 任务 3.4：添加系统设置（0.1天）

**文件**: `admin/app/routers/settings.py`

在系统设置中添加开关：

```python
# 添加设置项
auto_regenerate_setting = SiteSetting(
    key='auto_regenerate_static',
    value='true',  # 默认启用
    description='内容更新时自动重新生成静态页面'
)
```

在设置界面添加开关：

```html
<div class="form-check form-switch">
    <input class="form-check-input" type="checkbox" id="autoRegenerateStatic"
           {% if settings.auto_regenerate_static == 'true' %}checked{% endif %}>
    <label class="form-check-label" for="autoRegenerateStatic">
        内容更新时自动重新生成静态页面
    </label>
</div>
```

---

### 阶段四：表单 AJAX 化（1天）

#### 任务 4.1：改造联系表单（0.5天）

**文件**: `templates/zh/contact.html` 和 `templates/en/contact.html`

将现有表单改为 AJAX 提交：

```html
<!-- 原表单 -->
<form method="POST" action="/contact/submit">
    <!-- 字段... -->
</form>

<!-- 改为 -->
<form id="contactForm" class="contact-form">
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="name" class="form-label">Name *</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="col-md-6 mb-3">
            <label for="email" class="form-label">Email *</label>
            <input type="email" class="form-control" id="email" name="email" required>
        </div>
    </div>

    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="phone" class="form-label">Phone</label>
            <input type="tel" class="form-control" id="phone" name="phone">
        </div>
        <div class="col-md-6 mb-3">
            <label for="subject" class="form-label">Subject *</label>
            <input type="text" class="form-control" id="subject" name="subject" required>
        </div>
    </div>

    <div class="mb-3">
        <label for="message" class="form-label">Message *</label>
        <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
    </div>

    <button type="submit" class="btn btn-primary btn-lg">
        <i class="fas fa-paper-plane"></i> Send Message
    </button>
</form>

<!-- 成功/失败提示 -->
<div id="formFeedback" class="mt-3" style="display: none;"></div>

<script>
document.getElementById('contactForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const submitBtn = form.querySelector('button[type="submit"]');
    const feedback = document.getElementById('formFeedback');

    // 禁用提交按钮
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // 成功提示
            feedback.className = 'alert alert-success';
            feedback.innerHTML = '<i class="fas fa-check-circle"></i> <strong>Success!</strong> Your message has been sent. We will get back to you soon.';
            feedback.style.display = 'block';

            // 清空表单
            form.reset();

            // 3秒后隐藏提示
            setTimeout(() => {
                feedback.style.display = 'none';
            }, 5000);
        } else {
            // 错误提示
            feedback.className = 'alert alert-danger';
            feedback.innerHTML = '<i class="fas fa-exclamation-circle"></i> <strong>Error:</strong> ' + (result.message || 'Failed to send message. Please try again.');
            feedback.style.display = 'block';
        }
    } catch (error) {
        // 网络错误
        feedback.className = 'alert alert-danger';
        feedback.innerHTML = '<i class="fas fa-exclamation-triangle"></i> <strong>Network Error:</strong> Failed to send message. Please check your connection.';
        feedback.style.display = 'block';
    } finally {
        // 恢复提交按钮
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    }
});
</script>
```

#### 任务 4.2：添加 CORS 支持（0.2天）

**文件**: `app/main.py`

添加 CORS 中间件：

```python
from fastapi.middleware.cors import CORSMiddleware

def register_middlewares(app: FastAPI):
    # 添加 CORS 中间件（在其他中间件之前）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应改为具体域名
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # ... 现有中间件
```

**生产环境配置**（推荐）：

```python
# 从环境变量读取允许的域名
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

`.env` 文件添加：

```bash
# 允许的CORS源（逗号分隔）
ALLOWED_ORIGINS=https://boweneducation.org,https://www.boweneducation.org
```

#### 任务 4.3：测试表单提交（0.3天）

创建测试用例：

```python
# tests/test_contact_form.py
def test_contact_form_api():
    """测试联系表单 API"""
    from fastapi.testclient import TestClient
    from app.main import create_app

    client = TestClient(create_app())

    response = client.post("/api/contact", json={
        "name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "subject": "Test Subject",
        "message": "Test message content"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
```

---

### 阶段五：部署与优化（1天）

#### 任务 5.1：Nginx 配置（0.3天）

**文件**: `nginx/bowen-static.conf`

```nginx
# Nginx 配置 - 静态文件优先服务
server {
    listen 80;
    server_name boweneducation.org www.boweneducation.org;

    # 根目录指向静态文件
    root /home/maxazure/projects/bowen-education-manchester/public;
    index index.html;

    # 日志
    access_log /var/log/nginx/bowen-access.log;
    error_log /var/log/nginx/bowen-error.log;

    # 静态资源（CSS、JS、图片）
    location /static/ {
        alias /home/maxazure/projects/bowen-education-manchester/templates/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        add_header X-Served-By "Nginx-Static";
    }

    # 上传文件
    location /upload/ {
        alias /home/maxazure/projects/bowen-education-manchester/upload/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # API 路由（表单提交等）
    location /api/ {
        proxy_pass http://127.0.0.1:10034;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 表单提交路由
    location /contact/submit {
        proxy_pass http://127.0.0.1:10034;
        proxy_set_header Host $host;
    }

    location /guestbook/submit {
        proxy_pass http://127.0.0.1:10034;
        proxy_set_header Host $host;
    }

    # 管理后台始终走动态路由
    location /admin {
        proxy_pass http://127.0.0.1:10034;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 主要路由：优先使用静态文件
    location / {
        # 尝试静态文件，如果不存在则转发到动态后端
        try_files $uri $uri/ $uri/index.html @dynamic;

        # 静态 HTML 缓存策略
        add_header Cache-Control "public, max-age=3600";  # 1小时
        add_header X-Served-By "Nginx-Static";
    }

    # 动态后端（回退）
    location @dynamic {
        proxy_pass http://127.0.0.1:10034;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        add_header X-Served-By "FastAPI-Dynamic";
    }

    # 404 页面
    error_page 404 /404.html;
    location = /404.html {
        root /home/maxazure/projects/bowen-education-manchester/public;
        internal;
    }

    # 50x 错误页面
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
        internal;
    }
}
```

**启用配置**：

```bash
# 创建软链接
sudo ln -s /home/maxazure/projects/bowen-education-manchester/nginx/bowen-static.conf /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

#### 任务 5.2：部署脚本（0.2天）

**文件**: `scripts/deploy_static.sh`

```bash
#!/bin/bash
# 静态站点部署脚本

set -e  # 遇到错误立即退出

PROJECT_DIR="/home/maxazure/projects/bowen-education-manchester"
VENV_DIR="$PROJECT_DIR/venv"
PUBLIC_DIR="$PROJECT_DIR/public"

echo "========================================="
echo "博文教育 CMS - 静态站点部署"
echo "========================================="
echo ""

# 1. 激活虚拟环境
echo "1. 激活 Python 虚拟环境..."
source "$VENV_DIR/bin/activate"

# 2. 生成静态文件
echo "2. 生成静态文件..."
python "$PROJECT_DIR/scripts/generate_static.py" --all

# 3. 检查生成结果
if [ -d "$PUBLIC_DIR/zh" ] && [ -d "$PUBLIC_DIR/en" ]; then
    echo "✓ 静态文件生成成功"
    echo "  - 中文目录: $PUBLIC_DIR/zh"
    echo "  - 英文目录: $PUBLIC_DIR/en"
else
    echo "✗ 静态文件生成失败"
    exit 1
fi

# 4. 设置文件权限
echo "3. 设置文件权限..."
chmod -R 755 "$PUBLIC_DIR"

# 5. 重启 Nginx（如果使用 Nginx）
if command -v nginx &> /dev/null; then
    echo "4. 重启 Nginx..."
    sudo systemctl restart nginx
    echo "✓ Nginx 已重启"
fi

# 6. 显示统计信息
echo ""
echo "========================================="
echo "部署完成！"
echo "========================================="
echo "统计信息:"
echo "  - 中文页面: $(find $PUBLIC_DIR/zh -name 'index.html' | wc -l) 页"
echo "  - 英文页面: $(find $PUBLIC_DIR/en -name 'index.html' | wc -l) 页"
echo "  - 总大小: $(du -sh $PUBLIC_DIR | cut -f1)"
echo ""
```

**使用权限**：

```bash
chmod +x scripts/deploy_static.sh
```

#### 任务 5.3：性能测试（0.3天）

创建性能测试脚本：

```bash
# scripts/test_performance.sh
#!/bin/bash

echo "静态页面性能测试"
echo "=================="

# 测试首页加载速度
echo "测试首页..."
curl -o /dev/null -s -w "Time: %{time_total}s\n" http://localhost/zh/index.html

# 测试产品详情页
echo "测试产品详情页..."
curl -o /dev/null -s -w "Time: %{time_total}s\n" http://localhost/zh/tuition/chess-course/index.html

# 测试文章详情页
echo "测试文章详情页..."
curl -o /dev/null -s -w "Time: %{time_total}s\n" http://localhost/zh/news/article-slug/index.html
```

#### 任务 5.4：使用文档（0.2天）

**文件**: `docs/STATIC_GENERATION_USAGE.md`

```markdown
# 静态页面生成功能使用手册

## 一、管理后台使用

### 1.1 访问管理界面

登录管理后台后，点击左侧菜单的 **"静态页面生成"**。

### 1.2 全站生成

1. 选择生成语言（中英文/仅中文/仅英文）
2. 点击 **"开始全站生成"** 按钮
3. 系统将在后台生成所有页面（约 1-2 分钟）
4. 生成过程中可查看实时进度
5. 完成后会显示成功/失败页面数

### 1.3 选择性生成

- 选择页面类型（首页/产品/文章/单页/活动）
- 选择语言
- 点击 **"开始选择性生成"**

### 1.4 单页生成

- 选择页面类型
- 输入页面 ID
- 点击 **"生成"** 按钮

## 二、命令行使用

### 2.1 全站生成

```bash
cd /home/maxazure/projects/bowen-education-manchester
source venv/bin/activate
python scripts/generate_static.py --all
```

### 2.2 仅生成中文

```bash
python scripts/generate_static.py --all --lang zh
```

### 2.3 仅生成产品页

```bash
python scripts/generate_static.py --type product
```

### 2.4 生成单个页面

```bash
python scripts/generate_static.py --page-id 123 --page-type product
```

## 三、自动生成

内容更新时自动重新生成相关页面（需在系统设置中启用）：

- 保存产品 → 自动生成产品详情页 + 产品列表页
- 保存文章 → 自动生成文章详情页 + 文章列表页
- 保存单页 → 自动生成单页

**启用/禁用自动生成**：
系统设置 → 勾选/取消勾选 "内容更新时自动重新生成静态页面"

## 四、部署到生产

### 4.1 使用部署脚本

```bash
cd /home/maxazure/projects/bowen-education-manchester
./scripts/deploy_static.sh
```

### 4.2 手动部署

1. 生成静态文件（见上文）
2. 确保 Nginx 配置正确
3. 重启 Nginx: `sudo systemctl restart nginx`

## 五、故障排查

### 5.1 生成失败

**查看错误日志**：
- 管理后台：生成历史 → 点击 "查看错误"
- 命令行：检查输出的错误信息

### 5.2 页面不更新

**可能原因**：
1. 浏览器缓存：强制刷新（Ctrl+Shift+R）
2. Nginx 缓存：重启 Nginx
3. 未重新生成：手动触发生成

### 5.3 表单提交失败

**检查项**：
1. API 端点是否正常：访问 http://localhost:10034/health
2. CORS 配置是否正确
3. 检查浏览器控制台错误信息

## 六、最佳实践

1. **内容大量更新后**：使用全站生成确保一致性
2. **单个页面修改**：使用自动生成或单页生成
3. **定期全站生成**：建议每周执行一次全站生成
4. **监控生成历史**：定期检查是否有失败记录
```

---

## 📈 五、预估页面数量与性能

### 5.1 页面统计

| 内容类型 | 中文 | 英文 | 小计 | 备注 |
|---------|------|------|------|------|
| 首页 | 1 | 1 | 2 | |
| 单页 | 24 | 24 | 48 | 关于、联系、政策等 |
| 产品列表 | 1 | 1 | 2 | tuition 栏目 |
| 产品详情 | 7 | 7 | 14 | 7 个课程 |
| 文章列表 | 5 | 5 | 10 | 多个文章栏目（假设5个） |
| 文章列表（分页） | 5 | 5 | 10 | 假设每个栏目2页 |
| 文章详情 | 21 | 21 | 42 | 21 篇文章 |
| 活动列表 | 1 | 1 | 2 | events 页面 |
| 图库 | 1 | 1 | 2 | gallery 页面 |
| **总计** | **66** | **66** | **~132** | |

### 5.2 性能估算

**单页生成时间**：
- 简单页面（首页、单页）：~0.1 秒/页
- 列表页（带数据库查询）：~0.15 秒/页
- 详情页（关联查询）：~0.2 秒/页

**全站生成时间**：
- 最快：132 × 0.1 = **13.2 秒**
- 最慢：132 × 0.2 = **26.4 秒**
- **预估：15-25 秒**

**静态页面访问速度**（Nginx 服务）：
- 首次访问：< 50ms
- 带缓存：< 20ms
- **目标：< 200ms**（含网络延迟）

### 5.3 磁盘空间

**单页大小估算**：
- HTML 文件：5-50 KB/页
- 平均：~20 KB/页

**总空间占用**：
- 132 页 × 20 KB = **~2.6 MB**
- 加上 CSS/JS/图片（共享）：**< 50 MB**

---

## ⚠️ 六、潜在挑战与解决方案

### 挑战 1: Request 对象模拟

**问题**：Jinja2 模板中使用了 `request.url`、`request.query_params` 等属性

**解决方案**：

```python
from starlette.requests import Request
from starlette.datastructures import URL, QueryParams

class MockRequest:
    """模拟 Request 对象"""
    def __init__(self, url_path: str):
        self.url = URL(f"http://localhost{url_path}")
        self.query_params = QueryParams({})
        self.path_params = {}
        self.headers = {}
        self.method = "GET"

    def url_for(self, name: str, **path_params):
        # 简单实现（如需要）
        return f"/{name}"
```

### 挑战 2: 数据库会话管理

**问题**：生成过程中大量数据库查询可能导致内存问题

**解决方案**：

```python
def generate_all(self, languages: List[str] = ['zh', 'en']) -> Dict:
    """生成全站（分批处理）"""
    batch_size = 50  # 每批生成50页

    for lang in languages:
        self._generate_homepage(lang)

        # 分批生成产品
        products = self.db.query(Product).all()
        for i in range(0, len(products), batch_size):
            batch = products[i:i+batch_size]
            for product in batch:
                self._generate_product_detail(product.column, product, lang)

            # 清理会话缓存
            self.db.expire_all()
            gc.collect()

    return self.stats
```

### 挑战 3: 分页链接处理

**问题**：文章列表分页链接在静态页面中如何处理

**解决方案**：

生成分页页面时，确保链接指向静态文件：

```html
<!-- 动态页面链接 -->
<a href="/news?page=2">第2页</a>

<!-- 静态页面链接（生成时替换） -->
<a href="/zh/news/page-2/">第2页</a>
```

在模板中使用条件判断：

```jinja2
{% if is_static_generation %}
    <a href="{{ url_prefix }}/news/page-{{ page_num }}/">第{{ page_num }}页</a>
{% else %}
    <a href="/news?page={{ page_num }}">第{{ page_num }}页</a>
{% endif %}
```

### 挑战 4: 相对 URL vs 绝对 URL

**问题**：静态文件中的链接可能使用相对路径导致错误

**解决方案**：

1. **使用 `<base>` 标签**：

```html
<!-- 在 base.html 的 <head> 中添加 -->
<base href="/">
```

2. **模板中使用绝对路径**：

```jinja2
<!-- 不推荐：相对路径 -->
<a href="../products/chess">

<!-- 推荐：绝对路径 -->
<a href="/zh/tuition/chess">
```

3. **后处理 HTML（可选）**：

```python
def post_process_html(html: str, base_url: str) -> str:
    """后处理 HTML，转换相对链接为绝对链接"""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, 'html.parser')

    # 处理所有 <a> 标签
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.startswith(('http://', 'https://', '/', '#')):
            a['href'] = f"{base_url}/{href}"

    return str(soup)
```

### 挑战 5: 搜索功能

**问题**：静态站点无法实现动态搜索

**解决方案**：

**方案 A：客户端搜索（Lunr.js）**

1. 生成搜索索引 JSON：

```python
def generate_search_index(self):
    """生成搜索索引"""
    import json

    index = []

    # 添加所有产品
    products = self.db.query(Product).filter(Product.status == 'online').all()
    for product in products:
        index.append({
            'id': f'product-{product.id}',
            'title': product.name,
            'title_en': product.name_en,
            'summary': product.summary,
            'summary_en': product.summary_en,
            'url': f'/zh/tuition/{product.slug}',
            'url_en': f'/en/tuition/{product.slug}',
            'type': 'product'
        })

    # 添加所有文章
    posts = self.db.query(Post).filter(Post.status == 'online').all()
    for post in posts:
        index.append({
            'id': f'post-{post.id}',
            'title': post.title,
            'title_en': post.title_en,
            'summary': post.summary,
            'summary_en': post.summary_en,
            'url': f'/zh/news/{post.slug}',
            'url_en': f'/en/news/{post.slug}',
            'type': 'post'
        })

    # 保存为 JSON
    search_json_path = self.output_dir / 'search-index.json'
    search_json_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
```

2. 前端使用 Lunr.js：

```html
<script src="https://unpkg.com/lunr/lunr.js"></script>
<script>
fetch('/search-index.json')
    .then(res => res.json())
    .then(data => {
        // 构建 Lunr 索引
        const idx = lunr(function () {
            this.ref('id');
            this.field('title');
            this.field('summary');

            data.forEach(doc => this.add(doc));
        });

        // 搜索
        const results = idx.search(query);
    });
</script>
```

**方案 B：使用搜索服务（Algolia/Meilisearch）**

集成第三方搜索服务，定期同步数据。

### 挑战 6: 404 页面处理

**问题**：静态站点如何处理不存在的页面

**解决方案**：

1. **生成通用 404 页面**：

```python
def _generate_404_page(self, lang: str):
    """生成 404 页面"""
    context = {
        'request': create_mock_request('/404'),
        'lang': lang,
        'page_title': '页面未找到' if lang == 'zh' else 'Page Not Found'
    }

    html = self._render_template('404.html', context, lang)

    file_path = self.output_dir / '404.html' if lang == 'zh' else self.output_dir / 'en' / '404.html'
    self._save_html(html, file_path)
```

2. **Nginx 配置**：

```nginx
error_page 404 /404.html;
location = /404.html {
    root /path/to/public;
    internal;
}
```

### 挑战 7: 缓存失效

**问题**：静态文件更新后浏览器缓存旧内容

**解决方案**：

1. **HTML 页面使用短缓存**：

```nginx
location ~ \.html$ {
    add_header Cache-Control "public, max-age=3600";  # 1小时
}
```

2. **CSS/JS 使用版本号**：

```html
<link rel="stylesheet" href="/static/css/style.css?v=20250117">
<script src="/static/js/main.js?v=20250117"></script>
```

3. **自动添加版本号**：

```python
# 在生成时添加时间戳
import time
version = str(int(time.time()))

html = html.replace('/static/css/style.css', f'/static/css/style.css?v={version}')
```

---

## ✅ 七、验收标准

### 7.1 功能验收

- [ ] 管理后台可一键生成全站（~132页）
- [ ] 生成的 HTML 与动态页面内容完全一致
- [ ] 中英文页面均正确生成
- [ ] 双语导航菜单正确显示
- [ ] 所有链接正确（无 404）
- [ ] 表单 AJAX 提交正常
- [ ] 内容更新自动重新生成（可配置）
- [ ] 生成历史可查询
- [ ] 生成失败有错误日志

### 7.2 性能验收

- [ ] 全站生成时间 < 30 秒
- [ ] 单页生成时间 < 0.3 秒
- [ ] 静态页面加载速度 < 200ms（本地测试）
- [ ] 静态页面加载速度 < 500ms（生产环境）

### 7.3 兼容性验收

- [ ] Chrome 浏览器正常显示
- [ ] Firefox 浏览器正常显示
- [ ] Safari 浏览器正常显示
- [ ] 移动端正常显示
- [ ] SEO 元标签正确

### 7.4 安全验收

- [ ] CORS 配置正确（仅允许必要源）
- [ ] 表单验证（前端 + 后端）
- [ ] 无敏感信息泄露
- [ ] 管理后台需要登录才能访问

---

## 📚 八、参考文档

### 8.1 相关技术文档

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Jinja2 文档](https://jinja.palletsprojects.com/)
- [Nginx 文档](https://nginx.org/en/docs/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)

### 8.2 类似项目参考

- **DedeCMS**: 经典的 PHP CMS，静态化功能完善
- **Frozen-Flask**: Python 静态站点生成库
- **Pelican**: Python 静态博客生成器
- **Hugo**: Go 语言静态站点生成器

---

## 📝 九、总结

### 9.1 核心优势

1. **性能提升**：静态页面加载速度比动态页面快 5-10 倍
2. **服务器压力降低**：无需数据库查询，降低 CPU 和内存使用
3. **SEO 友好**：搜索引擎更易抓取静态页面
4. **可靠性**：即使数据库故障，静态页面仍可访问
5. **CDN 加速**：静态文件易于部署到 CDN

### 9.2 适用场景

✅ **适合使用静态生成的场景**：
- 内容更新不频繁（每天 < 10 次）
- 访问量较大（> 1000 PV/天）
- 对性能要求高
- 内容为主，交互较少

⚠️ **不适合使用静态生成的场景**：
- 内容实时更新（如股票、天气）
- 大量个性化内容（如用户中心）
- 复杂交互功能（如聊天、实时评论）

### 9.3 博文教育 CMS 评估

**适用性**: ⭐⭐⭐⭐⭐（非常适合）

**理由**：
- ✅ 内容更新频率低（教育机构内容相对稳定）
- ✅ 以展示为主（课程介绍、新闻、单页）
- ✅ 交互少（仅联系表单）
- ✅ 双语支持（可同时生成中英文）
- ✅ 管理后台独立（不受静态化影响）

**预期效果**：
- 页面加载速度提升 **80%**（从 500ms → 100ms）
- 服务器负载降低 **70%**
- SEO 排名提升（更快的页面速度）
- 用户体验显著改善

---

## 🎯 十、下一步行动

### 立即执行

1. **确认方案**：审阅此计划文档，确认技术方案
2. **准备环境**：确保开发环境正常（Python、数据库等）
3. **创建分支**：`git checkout -b feature/static-generation`

### 按阶段实施

按照本计划的 5 个阶段依次实施：
1. 阶段一：核心生成器（3-4 天）
2. 阶段二：管理后台（2 天）
3. 阶段三：自动生成 Hook（1 天）
4. 阶段四：表单 AJAX 化（1 天）
5. 阶段五：部署与优化（1 天）

### 持续优化

完成初版后，根据实际使用情况持续优化：
- 监控生成性能
- 收集用户反馈
- 优化缓存策略
- 添加更多页面类型

---

**文档编制**: 系统架构师
**审核日期**: 2025-11-17
**下次审阅**: 实施完成后
**联系方式**: architecture@boweneducation.org

---

**附录**：
- 附录 A：生成器完整代码示例
- 附录 B：Nginx 完整配置
- 附录 C：测试用例清单
- 附录 D：性能基准测试结果

---

*本计划文档基于博文教育曼彻斯特 CMS v1.2.0 版本编制，适用于 FastAPI + SQLAlchemy + Jinja2 技术栈。*
