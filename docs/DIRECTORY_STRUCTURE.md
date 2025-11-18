# 博文教育曼彻斯特 CMS 项目目录结构说明

**文档版本**: v1.0
**更新日期**: 2025-11-17
**项目版本**: v1.2.0

---

## 目录结构总览

```
bowen-education-manchester/
├── app/                          # 核心应用代码（前端 + 业务逻辑）
├── admin/                        # 管理后台代码
├── templates/                    # 前端模板和静态资源
├── instance/                     # 实例数据（数据库、上传文件）
├── migrations/                   # 数据库迁移文件
├── logs/                         # 应用日志
├── scripts/                      # 工具脚本
├── docs/                         # 项目文档
├── backup/                       # 备份文件
├── venv/                         # Python 虚拟环境
├── requirements.txt              # Python 依赖
├── alembic.ini                   # 数据库迁移配置
├── .env                          # 环境变量（未纳入版本控制）
├── .gitignore                    # Git 忽略文件
├── README.md                     # 项目说明
└── CLAUDE.md                     # 项目开发指南
```

---

## 1. `app/` - 核心应用目录

**用途**: 包含前端网站的核心业务逻辑、数据模型、路由和服务层。

### 目录结构

```
app/
├── __init__.py                   # 包初始化
├── main.py                       # FastAPI 应用工厂（205 行）
├── config.py                     # 配置管理（133 行）
├── database.py                   # 数据库连接与会话管理（37 行）
│
├── models/                       # 数据库模型（ORM）
│   ├── __init__.py
│   ├── base.py                   # 基础模型类（TimestampMixin）
│   ├── site.py                   # 站点栏目、单页、设置（146 行）
│   ├── product.py                # 产品/课程模型（119 行）
│   ├── post.py                   # 文章/新闻模型（135 行）
│   ├── media.py                  # 媒体文件模型（108 行）
│   ├── event.py                  # 活动管理模型（275 行）
│   ├── gallery.py                # 图库模型（90 行）
│   ├── layout.py                 # 页面布局模型（61 行）
│   ├── admin_user.py             # 管理员用户（55 行）
│   ├── contact.py                # 联系消息
│   ├── team.py                   # 团队成员
│   └── faq.py                    # 常见问题
│
├── routes/                       # 路由处理
│   ├── __init__.py
│   ├── frontend.py               # 前端页面路由（~300 行）
│   ├── frontend_i18n.py          # 双语路由辅助（语言检测）
│   └── health.py                 # 健康检查端点
│
├── services/                     # 业务逻辑层
│   ├── __init__.py
│   ├── product_service.py        # 产品查询服务（带缓存）
│   ├── post_service.py           # 文章查询服务（带缓存）
│   ├── site_service.py           # 导航、栏目、设置服务
│   ├── single_page_service.py    # 单页管理服务
│   ├── event_service.py          # 活动管理服务
│   ├── gallery_service.py        # 图库管理服务
│   ├── team_service.py           # 团队成员服务
│   ├── faq_service.py            # FAQ 服务
│   ├── site_settings_service.py  # 站点设置服务
│   ├── media_service.py          # 媒体文件服务
│   ├── column_service.py         # 栏目操作服务
│   └── layout_service.py         # 页面布局服务
│
├── middleware/                   # 中间件
│   ├── __init__.py
│   └── error_handlers.py         # 全局异常处理
│
├── utils/                        # 工具函数
│   ├── __init__.py
│   ├── cache.py                  # TTL 缓存实现（140 行）
│   ├── template_helpers.py       # 模板全局函数
│   ├── template_filters.py       # 模板过滤器（双语处理）
│   └── logger.py                 # 日志配置
│
└── schemas/                      # Pydantic 数据验证
    ├── __init__.py
    ├── schemas.py                # 数据传输对象（DTO）
    └── requests.py               # 请求验证模型
```

### 关键文件说明

#### `app/main.py` - 应用入口

**职责**: 创建 FastAPI 应用实例，注册路由、中间件、异常处理器。

```python
def create_app() -> FastAPI:
    """应用工厂函数"""
    app = FastAPI(title="Bowen Education Manchester")

    # 1. 注册中间件
    register_middlewares(app)

    # 2. 注册路由
    register_routes(app)

    # 3. 注册异常处理
    register_exception_handlers(app)

    # 4. 配置模板全局函数
    configure_jinja(app)

    return app
```

#### `app/config.py` - 配置管理

**职责**: 加载环境变量、站点配置。

```python
# 环境变量加载
load_dotenv()

# 站点配置
SITE_NAME = os.getenv("SITE_NAME", "Bowen Education")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./instance/database.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
```

#### `app/models/` - 数据模型

**核心模型**：
- `SiteColumn`: 导航栏目（支持嵌套）
- `Product`: 产品/课程（双语支持）
- `Post`: 文章/新闻（双语支持）
- `SinglePage`: 静态页面（双语支持）
- `Event`: 活动管理（报名、票务）
- `MediaFile`: 媒体资源（图片、视频）

**双语字段命名规则**：
```python
name = Column(String(200))      # 中文
name_en = Column(String(200))   # 英文
```

#### `app/services/` - 服务层

**设计模式**: Repository Pattern + Caching

```python
@cache_content  # 缓存装饰器
def get_products(db: Session, column_id: int = None) -> List[Product]:
    """获取产品列表"""
    query = db.query(Product).filter(Product.status == 'online')
    if column_id:
        query = query.filter(Product.column_id == column_id)
    return query.all()
```

#### `app/utils/cache.py` - 缓存系统

**实现**: TTL（Time-To-Live）内存缓存

```python
class TTLCache:
    """时间过期缓存"""
    def __init__(self, ttl: int = 300):
        self.ttl = ttl  # 过期时间（秒）
        self.cache = {}

    def get(self, key: str) -> Any:
        """获取缓存（检查是否过期）"""
        ...
```

**缓存装饰器**：
- `@cache_navigation` - 导航菜单缓存（10 分钟）
- `@cache_content` - 内容列表缓存（5 分钟）
- `@cache_settings` - 站点设置缓存（10 分钟）

---

## 2. `admin/` - 管理后台目录

**用途**: 独立的管理后台应用，提供内容管理、用户管理、媒体管理等功能。

### 目录结构

```
admin/
├── __init__.py
├── app/                          # 管理后台应用
│   ├── __init__.py
│   ├── main.py                   # 管理后台入口
│   ├── middleware.py             # 认证中间件
│   ├── database.py               # 数据库会话管理
│   │
│   ├── routers/                  # 管理路由
│   │   ├── __init__.py
│   │   ├── auth.py               # 登录/登出
│   │   ├── dashboard.py          # 仪表板
│   │   ├── products.py           # 产品管理（CRUD）
│   │   ├── posts.py              # 文章管理（CRUD）
│   │   ├── single_pages.py       # 单页管理（CRUD）
│   │   ├── columns.py            # 栏目管理
│   │   ├── media.py              # 媒体库管理
│   │   ├── events.py             # 活动管理
│   │   ├── galleries.py          # 图库管理
│   │   ├── team.py               # 团队管理
│   │   ├── faq.py                # FAQ 管理
│   │   ├── contacts.py           # 联系消息查看
│   │   └── settings.py           # 站点设置
│   │
│   ├── services/                 # 管理后台服务
│   │   ├── media_service.py      # 图片上传、处理
│   │   ├── column_service.py     # 栏目操作
│   │   └── layout_service.py     # 布局编辑
│   │
│   └── blocks/                   # 页面布局块定义
│       └── [Block definitions]
│
├── templates/                    # 管理后台模板
│   ├── base.html                 # 基础布局（侧边栏、顶栏）
│   ├── login.html                # 登录页
│   ├── dashboard.html            # 仪表板
│   │
│   ├── products/                 # 产品管理模板
│   │   ├── list.html             # 产品列表
│   │   └── form.html             # 产品编辑表单
│   │
│   ├── posts/                    # 文章管理模板
│   │   ├── list.html
│   │   └── form.html
│   │
│   ├── pages/                    # 单页管理模板
│   │   ├── list.html
│   │   └── form.html
│   │
│   ├── columns/                  # 栏目管理模板
│   │   └── index.html
│   │
│   ├── media/                    # 媒体库模板
│   │   ├── index.html
│   │   └── upload.html
│   │
│   ├── events/                   # 活动管理模板
│   ├── galleries/                # 图库模板
│   ├── team/                     # 团队模板
│   ├── faq/                      # FAQ 模板
│   ├── contacts/                 # 联系消息模板
│   └── settings/                 # 设置模板
│
└── admin-static/                 # 管理后台静态资源
    └── css/
        └── admin.css             # 管理后台样式
```

### 关键特性

#### 1. 认证中间件

```python
# admin/app/middleware.py
class AdminAuthMiddleware(BaseHTTPMiddleware):
    """管理员认证中间件"""
    async def dispatch(self, request: Request, call_next):
        # 检查 session 中的 admin_user_id
        if request.url.path.startswith("/admin"):
            user_id = request.session.get("admin_user_id")
            if not user_id and request.url.path != "/admin/login":
                return RedirectResponse(url="/admin/login")
        return await call_next(request)
```

#### 2. 双语编辑界面

所有内容编辑表单使用 **Bootstrap Tab** 分离中英文：

```html
<!-- 示例：产品编辑表单 -->
<ul class="nav nav-tabs">
    <li><a href="#chinese">中文内容</a></li>
    <li><a href="#english">English Content</a></li>
</ul>

<div class="tab-content">
    <div id="chinese" class="tab-pane active">
        <!-- 中文字段 -->
    </div>
    <div id="english" class="tab-pane">
        <!-- 英文字段（_en 后缀） -->
    </div>
</div>
```

#### 3. 媒体管理

- 图片上传与预览
- 多尺寸自动生成（原图、中等、缩略图）
- 文件夹分类
- 使用统计（引用次数）

---

## 3. `templates/` - 前端模板目录

**用途**: 前端网站的 Jinja2 模板和静态资源（CSS、JS、图片）。

### 目录结构

```
templates/
├── static/                       # 静态资源
│   ├── css/                      # 样式表
│   │   ├── main.css              # 主样式
│   │   ├── responsive.css        # 响应式
│   │   └── components.css        # 组件样式
│   │
│   ├── js/                       # JavaScript
│   │   ├── main.js               # 主脚本
│   │   ├── interactive.js        # 交互功能
│   │   └── forms.js              # 表单处理
│   │
│   └── images/                   # 图片资源
│       ├── heroes/               # Hero 区域背景
│       ├── courses/              # 课程图片
│       ├── news/                 # 新闻图片
│       ├── services/             # 服务图片
│       ├── teachers/             # 教师照片
│       └── gallery/              # 图库
│
├── zh/                           # 中文模板
│   ├── base.html                 # 基础布局
│   ├── index.html                # 首页
│   │
│   ├── components/               # 可复用组件
│   │   ├── navbar.html           # 导航栏
│   │   ├── footer.html           # 页脚
│   │   ├── hero_standard.html    # 标准 Hero 区域
│   │   └── sidebar_nav.html      # 侧边栏导航
│   │
│   ├── partials/                 # 页面片段
│   │   ├── featured_products.html    # 推荐产品
│   │   ├── latest_news.html          # 最新新闻
│   │   └── testimonials.html         # 用户评价
│   │
│   ├── albums/                   # 图库模板
│   │   └── photo_gallery.html
│   │
│   ├── products/                 # 产品相关
│   │   ├── list.html             # 产品列表页
│   │   └── detail.html           # 产品详情页
│   │
│   ├── posts/                    # 文章相关
│   │   ├── list.html             # 文章列表
│   │   └── detail.html           # 文章详情
│   │
│   ├── events/                   # 活动相关
│   │   ├── list.html
│   │   └── detail.html
│   │
│   ├── single_page.html          # 单页模板
│   ├── post_list.html            # 通用文章列表
│   ├── post_list_universal.html  # 通用列表（带侧边栏）
│   ├── post_list_with_sidebar.html
│   ├── contact.html              # 联系页
│   ├── events.html               # 活动页
│   └── tuition.html              # 学费页
│
└── en/                           # 英文模板（结构同 zh/）
    ├── base.html
    ├── index.html
    ├── components/
    ├── partials/
    └── ... (与 zh/ 平行结构)
```

### 模板继承结构

```
base.html (基础布局)
    ├── navbar.html (组件)
    ├── hero_standard.html (组件)
    │
    └── 页面模板（继承 base.html）
        ├── index.html (首页)
        ├── single_page.html (单页)
        ├── post_list.html (文章列表)
        └── products/detail.html (产品详情)
```

### 模板全局函数

通过 `Jinja2Templates.env.globals` 注入：

```python
# app/utils/template_helpers.py
jinja_env.globals.update({
    "product_list": get_products_for_template,  # 获取产品列表
    "post_list": get_posts_for_template,        # 获取文章列表
    "site_info": get_site_info,                 # 获取站点信息
    "get_navigation": get_navigation_menu,      # 获取导航菜单
})
```

**使用示例**：
```jinja2
<!-- 在模板中直接调用 -->
{% for product in product_list(is_recommended=True) %}
    <div class="product-card">
        <h3>{{ product.name_en or product.name }}</h3>
    </div>
{% endfor %}
```

### 双语模板策略

#### 目录分离
- `/zh/` - 中文模板
- `/en/` - 英文模板

#### 路由映射
```python
# app/routes/frontend.py
if lang == "en":
    template_dir = "en/"
else:
    template_dir = "zh/"

return templates.TemplateResponse(
    f"{template_dir}index.html",
    {"request": request}
)
```

#### 模板回退逻辑
```jinja2
{# 英文模板使用 or 运算符回退 #}
{{ product.name_en or product.name }}
{{ post.title_en or post.title }}
```

---

## 4. `instance/` - 实例数据目录

**用途**: 存储运行时数据，不纳入版本控制。

```
instance/
├── database.db                   # SQLite 数据库（生产数据）
└── database.db.backup.*          # 数据库备份文件
```

**备份命名规则**：
```bash
database.db.backup.20251117_143052  # 格式：YYYYMMDD_HHMMSS
```

**备份策略**：
- 手动备份：部署前执行
- 自动备份：建议设置定时任务（cron）
- 保留周期：建议保留最近 30 天

---

## 5. `migrations/` - 数据库迁移目录

**用途**: Alembic 数据库迁移版本控制。

```
migrations/
├── versions/                     # 迁移版本文件
│   ├── 21fd3e69434b_core_modules.py      # 核心模型迁移
│   ├── 3c60c9ca6db1_admin_users.py       # 管理员表
│   └── 86c0c7875540_content_markdown.py  # 内容字段
│
├── env.py                        # Alembic 环境配置
├── README                        # 迁移说明
└── script.py.mako                # 迁移脚本模板
```

### 常用命令

```bash
# 生成新迁移
alembic revision --autogenerate -m "Add new field"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看历史
alembic history
```

---

## 6. `logs/` - 日志目录

**用途**: 存储应用运行日志。

```
logs/
├── access.log                    # 访问日志（Gunicorn）
├── error.log                     # 错误日志（Gunicorn）
└── app.log                       # 应用日志（Python logging）
```

### 日志配置

```python
# app/utils/logger.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### 日志查看

```bash
# 实时查看访问日志
tail -f logs/access.log

# 实时查看错误日志
tail -f logs/error.log

# 查看最近 100 行
tail -n 100 logs/app.log
```

---

## 7. `scripts/` - 工具脚本目录

**用途**: 数据处理、迁移、维护脚本。

```
scripts/
└── archive/                      # 归档脚本
    ├── add_bilingual_content_fields.py   # 添加双语字段
    ├── add_english_column_names.py       # 添加英文栏目名
    ├── add_event_bilingual_fields.py     # 添加活动双语字段
    ├── add_product_bilingual_fields.py   # 添加产品双语字段
    ├── fix_database.py                   # 数据库修复
    ├── fix_english_translations.py       # 修复英文翻译
    ├── translate_content_to_english.py   # 内容翻译
    └── update_about_content.py           # 更新关于页面
```

**使用方式**：
```bash
# 激活虚拟环境
source venv/bin/activate

# 运行脚本
python scripts/archive/fix_database.py
```

---

## 8. `docs/` - 文档目录

**用途**: 项目技术文档。

```
docs/
├── ARCHITECTURE_ASSESSMENT.md    # 系统架构评估报告（本文档配套）
├── DIRECTORY_STRUCTURE.md        # 目录结构说明（本文档）
├── BILINGUAL_SYSTEM.md           # 双语系统设计文档
└── DATABASE_FIX_REPORT.md        # 数据库修复报告
```

---

## 9. `backup/` - 备份目录

**用途**: 临时备份文件（不纳入版本控制）。

```
backup/
├── database_*.db                 # 数据库备份
└── single_page_en_backup_*.txt   # 单页英文内容备份
```

**清理建议**：
- 定期清理超过 30 天的备份
- 重要备份转移到外部存储

---

## 10. 配置文件

### `requirements.txt` - Python 依赖

**关键依赖**：
```
# Web 框架
fastapi==0.109.0
uvicorn==0.27.0
gunicorn==latest

# ORM 和数据库
sqlalchemy==2.0.36
alembic==1.14.0

# 模板引擎
jinja2==3.1.3

# 认证与安全
bcrypt==4.1.2
python-dotenv==1.0.0

# 图片处理
pillow==11.0.0

# Markdown
mistune==3.0.2

# 其他工具
python-slugify==8.0.3
email-validator==2.1.0
```

### `alembic.ini` - 数据库迁移配置

**关键配置**：
```ini
[alembic]
script_location = migrations
sqlalchemy.url = sqlite:///./instance/database.db
```

### `.env` - 环境变量

**示例**（实际文件不纳入版本控制）：
```bash
APP_ENV=production
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./instance/database.db
SITE_NAME=Bowen Education Manchester
```

### `bowen-education.service` - Systemd 服务

**位置**: `/etc/systemd/system/bowen-education.service`

```ini
[Unit]
Description=Bowen Education Manchester Website
After=network.target

[Service]
Type=notify
User=maxazure
WorkingDirectory=/home/maxazure/projects/bowen-education-manchester
Environment="APP_ENV=production"
ExecStart=/path/to/venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:10034

[Install]
WantedBy=multi-user.target
```

---

## 11. 重要文件说明

### 根目录文件

| 文件 | 用途 |
|------|------|
| `README.md` | 项目说明、快速开始指南 |
| `CLAUDE.md` | Claude AI 开发指南（服务器配置、部署流程） |
| `TODO.md` | 开发任务跟踪、历史记录 |
| `requirements.txt` | Python 依赖列表 |
| `alembic.ini` | Alembic 配置 |
| `.gitignore` | Git 忽略规则 |
| `.env.example` | 环境变量模板 |
| `deploy_to_production.sh` | 生产部署脚本 |

### 核心应用文件

| 文件 | 行数 | 用途 |
|------|------|------|
| `app/main.py` | 205 | FastAPI 应用工厂 |
| `app/config.py` | 133 | 配置管理 |
| `app/database.py` | 37 | 数据库会话 |
| `app/models/site.py` | 146 | 站点模型 |
| `app/models/product.py` | 119 | 产品模型 |
| `app/models/post.py` | 135 | 文章模型 |
| `app/models/event.py` | 275 | 活动模型 |
| `app/utils/cache.py` | 140 | 缓存系统 |

---

## 12. 文件命名规范

### Python 文件

- **模型**: 单数名词（`product.py`, `post.py`）
- **服务**: `*_service.py`（`product_service.py`）
- **路由**: 功能名称（`auth.py`, `frontend.py`）
- **工具**: 功能名称（`cache.py`, `logger.py`）

### 模板文件

- **布局**: `base.html`
- **组件**: 描述性名称（`navbar.html`, `footer.html`）
- **页面**: 功能名称（`index.html`, `contact.html`）
- **列表**: `list.html`
- **详情**: `detail.html`
- **表单**: `form.html`

### 静态资源

- **CSS**: 功能名称（`main.css`, `responsive.css`）
- **JS**: 功能名称（`main.js`, `forms.js`）
- **图片**: 描述性名称（`hero-bg.jpg`, `course-chess.jpg`）

---

## 13. 版本控制规则

### `.gitignore` 配置

```gitignore
# 虚拟环境
venv/
env/

# 数据库
instance/
*.db

# 日志
logs/
*.log

# 环境变量
.env

# 备份
backup/

# Python
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/

# 操作系统
.DS_Store
Thumbs.db

# 上传文件
upload/
```

### Git 分支策略

```
main (生产分支)
  └── develop (开发分支)
      ├── feature/双语支持
      ├── feature/活动系统
      └── bugfix/修复登录问题
```

---

## 14. 目录权限建议

### 开发环境

```bash
# 所有文件默认权限
chmod 644 *

# 脚本执行权限
chmod +x scripts/*.py
chmod +x deploy_to_production.sh

# 虚拟环境
chmod -R 755 venv/
```

### 生产环境

```bash
# 应用目录
chmod -R 755 /home/maxazure/projects/bowen-education-manchester/

# 日志目录（写权限）
chmod -R 775 logs/

# 上传目录（写权限）
chmod -R 775 upload/

# 实例目录（写权限）
chmod -R 775 instance/

# 配置文件（只读）
chmod 600 .env
```

---

## 15. 开发工作流程

### 新功能开发

```bash
# 1. 创建功能分支
git checkout -b feature/新功能

# 2. 添加模型（如果需要）
# 编辑 app/models/new_model.py

# 3. 生成迁移
alembic revision --autogenerate -m "Add new model"
alembic upgrade head

# 4. 添加服务层
# 编辑 app/services/new_service.py

# 5. 添加路由
# 编辑 app/routes/ 或 admin/app/routers/

# 6. 添加模板
# 编辑 templates/zh/ 和 templates/en/

# 7. 测试
pytest tests/

# 8. 提交
git add .
git commit -m "feat: 添加新功能"

# 9. 合并到开发分支
git checkout develop
git merge feature/新功能

# 10. 部署到生产
git checkout main
git merge develop
./deploy_to_production.sh
```

### Bug 修复流程

```bash
# 1. 创建修复分支
git checkout -b bugfix/修复问题

# 2. 修复代码

# 3. 测试
pytest tests/test_specific.py

# 4. 提交
git commit -m "fix: 修复具体问题"

# 5. 合并并部署
git checkout main
git merge bugfix/修复问题
./deploy_to_production.sh
```

---

## 16. 常见目录操作

### 清理临时文件

```bash
# 清理 Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 清理日志（保留最近 7 天）
find logs/ -type f -name "*.log" -mtime +7 -delete

# 清理备份（保留最近 30 天）
find backup/ -type f -mtime +30 -delete
```

### 统计代码行数

```bash
# 统计 Python 代码
find app/ -name "*.py" | xargs wc -l
find admin/ -name "*.py" | xargs wc -l

# 统计模板
find templates/ -name "*.html" | xargs wc -l

# 统计总代码量
cloc app/ admin/ templates/
```

### 搜索特定内容

```bash
# 搜索 TODO 注释
grep -r "TODO" app/ admin/

# 搜索数据库查询
grep -r "db.query" app/services/

# 搜索模板引用
grep -r "{% extends" templates/
```

---

## 17. 目录扩展建议

### 短期（当前 → 6 个月）

**建议添加**：
```
project/
├── tests/                        # 测试目录（当前几乎为空）
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   └── fixtures/                 # 测试数据
│
├── docker/                       # Docker 配置
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── ci/                           # CI/CD 配置
    └── .github/workflows/
```

### 长期（6-12 个月）

**微服务架构演进**：
```
bowen-education/
├── services/
│   ├── content-service/          # 内容管理服务
│   ├── event-service/            # 活动服务
│   ├── media-service/            # 媒体处理服务
│   └── auth-service/             # 认证服务
│
├── frontend/                     # 前端 SPA
│   ├── src/
│   ├── public/
│   └── package.json
│
└── api-gateway/                  # API 网关
```

---

## 18. 总结

### 目录组织优势

✅ **清晰分层**：
- 前端应用（`app/`）
- 管理后台（`admin/`）
- 模板资源（`templates/`）

✅ **模块化**：
- 模型、服务、路由分离
- 双语模板目录分离

✅ **可维护性**：
- 一致的命名规范
- 清晰的文件组织

### 改进建议

⚠️ **测试目录**：
- 当前测试覆盖不足
- 建议完善 `tests/` 目录结构

⚠️ **文档完善**：
- API 文档生成
- 数据库 ER 图

⚠️ **容器化**：
- 添加 Docker 支持
- 简化部署流程

---

**文档维护**: 系统架构师
**最后更新**: 2025-11-17
**审核周期**: 每月更新
**联系方式**: architecture@boweneducation.org
