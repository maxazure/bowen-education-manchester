# 博文教育管理后台 - 项目结构文档

**版本**: v1.0.0
**更新日期**: 2025-11-13
**作者**: maxazure

---

## 📁 项目目录结构

```
bowen-education-manchester/
├── admin/                          # 管理后台（独立应用）
│   ├── app/                        # 应用核心代码
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI 应用入口
│   │   ├── config.py               # 配置管理
│   │   ├── database.py             # 数据库连接
│   │   ├── dependencies.py         # 依赖注入
│   │   ├── middleware.py           # 认证中间件
│   │   ├── utils.py                # 工具函数
│   │   ├── models/                 # 数据模型（使用主项目模型）
│   │   ├── routers/                # 路由模块
│   │   │   ├── auth.py             # 认证路由
│   │   │   ├── media.py            # 媒体库管理
│   │   │   ├── columns.py          # 栏目管理
│   │   │   ├── single_pages.py     # 单页管理
│   │   │   ├── posts.py            # 文章管理
│   │   │   ├── products.py         # 产品管理
│   │   │   ├── settings.py         # 站点设置
│   │   │   ├── galleries.py        # 相册管理
│   │   │   └── contacts.py         # 留言管理
│   │   └── services/               # 业务逻辑层
│   ├── static/                     # 静态资源
│   │   ├── css/
│   │   │   └── admin.css           # 管理后台样式
│   │   └── js/
│   │       ├── admin.js            # 通用JS
│   │       ├── columns.js          # 栏目管理JS
│   │       ├── contacts.js         # 留言管理JS
│   │       ├── pages.js            # 单页管理JS
│   │       ├── products.js         # 产品管理JS
│   │       └── settings.js         # 设置管理JS
│   ├── templates/                  # Jinja2 模板
│   │   ├── base.html               # 基础模板
│   │   ├── login.html              # 登录页面
│   │   ├── dashboard.html          # 仪表板
│   │   ├── components/             # 通用组件
│   │   │   ├── header.html         # 头部
│   │   │   ├── sidebar.html        # 侧边栏
│   │   │   └── pagination.html     # 分页组件
│   │   ├── columns/                # 栏目管理模板
│   │   │   ├── list.html
│   │   │   ├── form.html
│   │   │   └── _column_item.html
│   │   ├── pages/                  # 单页管理模板
│   │   ├── posts/                  # 文章管理模板
│   │   ├── products/               # 产品管理模板
│   │   ├── settings/               # 设置管理模板
│   │   ├── contacts/               # 留言管理模板
│   │   └── profile/                # 个人中心模板
│   └── tests/                      # 测试代码
│       ├── conftest.py             # Pytest 配置
│       ├── test_auth.py            # 认证测试
│       ├── test_media_*.py         # 媒体库测试 (4个)
│       ├── test_column_*.py        # 栏目管理测试 (3个)
│       ├── test_single_page_*.py   # 单页管理测试 (2个)
│       ├── test_post_*.py          # 文章管理测试 (3个)
│       ├── test_product_*.py       # 产品管理测试 (3个)
│       ├── test_settings_*.py      # 设置管理测试 (2个)
│       ├── test_gallery_*.py       # 相册管理测试 (3个)
│       └── test_contact_*.py       # 留言管理测试 (3个)
├── app/                            # 主项目（前台）
│   ├── models/                     # 数据模型（共享）
│   ├── database.py                 # 数据库配置
│   └── config.py                   # 主配置文件
├── scripts/                        # 工具脚本
│   └── migrate_media_file.py       # 数据库迁移脚本
├── docs/                           # 项目文档
│   ├── admin-modules/              # 模块开发文档
│   ├── admin-project-structure.md  # 本文件
│   ├── admin-operation-manual.md   # 操作文档
│   └── admin-system-test-report.md # 测试报告
└── venv/                           # Python 虚拟环境
```

---

## 📦 核心模块说明

### 1. 应用入口 (`admin/app/main.py`)

**功能**: FastAPI 应用主入口，配置中间件和路由

**关键配置**:
- SessionMiddleware: 会话管理
- AdminAuthMiddleware: 认证中间件
- 静态文件挂载: `/static` 目录
- 模板引擎: Jinja2Templates

**路由注册**:
```python
app.include_router(auth.router, prefix="/admin", tags=["auth"])
app.include_router(media.router, prefix="/admin/media", tags=["media"])
app.include_router(columns.router, prefix="/admin", tags=["columns"])
app.include_router(single_pages.router, prefix="/admin", tags=["pages"])
app.include_router(posts.router, prefix="/admin", tags=["posts"])
app.include_router(products.router, prefix="/admin", tags=["products"])
app.include_router(settings.router, prefix="/admin", tags=["settings"])
app.include_router(galleries.router, prefix="/admin", tags=["galleries"])
app.include_router(contacts.router, prefix="/admin", tags=["contacts"])
```

---

### 2. 数据库配置 (`admin/app/database.py`)

**功能**: 数据库连接和会话管理

**实现方式**:
- 直接导入主项目配置 `from app.config import settings`
- 创建独立的 SQLAlchemy engine 和 sessionmaker
- 提供 `get_db()` 依赖函数

**关键代码**:
```python
engine = create_engine(
    main_settings.database_url,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in main_settings.database_url else {}
    ),
    echo=main_settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 3. 认证中间件 (`admin/app/middleware.py`)

**功能**: 保护管理后台路由，验证用户登录状态

**验证逻辑**:
1. 检查请求路径是否需要认证
2. 白名单路径: `/admin/login`, `/static`, `/health`
3. 从 session 中读取 `admin_user_id`
4. 未登录用户重定向到登录页

**跳过认证**: 设置环境变量 `TESTING=1`

---

### 4. 路由模块 (`admin/app/routers/`)

#### 4.1 认证路由 (`auth.py`)

**端点**:
- `GET /admin/login` - 登录页面
- `POST /admin/login` - 登录处理
- `POST /admin/logout` - 登出
- `GET /admin/profile/change-password` - 修改密码页面
- `POST /admin/profile/change-password` - 修改密码处理

**测试覆盖**: 15/20 测试通过 (75%)

---

#### 4.2 媒体库路由 (`media.py`)

**端点**:
- `GET /admin/media` - 媒体文件列表（JSON API）
- `POST /admin/media/upload` - 上传文件
- `PUT /admin/media/{id}` - 更新媒体信息
- `DELETE /admin/media/{id}` - 删除媒体文件
- `GET /admin/media/{id}` - 获取媒体详情

**功能特性**:
- 多文件上传
- 图片自动生成缩略图
- 文件类型验证
- 使用计数管理

**测试覆盖**: 23/23 测试通过 (100%)，覆盖率 92%

---

#### 4.3 栏目管理路由 (`columns.py`)

**端点**:
- `GET /admin/columns` - 栏目列表页面
- `POST /admin/columns` - 创建栏目
- `GET /admin/columns/{id}` - 栏目详情
- `PUT /admin/columns/{id}` - 更新栏目
- `DELETE /admin/columns/{id}` - 删除栏目
- `POST /admin/columns/{id}/move` - 移动栏目（拖拽）
- `POST /admin/columns/reorder` - 批量排序

**功能特性**:
- 树形结构管理
- 拖拽排序
- 父子关系维护
- Slug 自动生成

**测试覆盖**: 18/18 测试通过 (100%)

---

#### 4.4 单页管理路由 (`single_pages.py`)

**端点**:
- `GET /admin/pages` - 单页列表
- `POST /admin/pages` - 创建单页
- `GET /admin/pages/{id}` - 单页详情
- `PUT /admin/pages/{id}` - 更新单页
- `DELETE /admin/pages/{id}` - 删除单页

**功能特性**:
- Markdown 编辑器
- HTML 预览
- XSS 防护
- SEO 优化

**测试覆盖**: 12/12 测试通过 (100%)

---

#### 4.5 文章管理路由 (`posts.py`)

**端点**:
- `GET /admin/posts` - 文章列表
- `POST /admin/posts` - 创建文章
- `GET /admin/posts/{id}` - 文章详情
- `PUT /admin/posts/{id}` - 更新文章
- `DELETE /admin/posts/{id}` - 删除文章
- `POST /admin/posts/{id}/publish` - 发布文章

**功能特性**:
- 多栏目分类
- 草稿/发布状态
- 发布时间控制
- 高级筛选

**测试覆盖**: 15/15 测试通过 (100%)

---

#### 4.6 产品管理路由 (`products.py`)

**端点**:
- `GET /admin/products` - 产品列表
- `POST /admin/products` - 创建产品
- `GET /admin/products/{id}` - 产品详情
- `PUT /admin/products/{id}` - 更新产品
- `DELETE /admin/products/{id}` - 删除产品
- `POST /admin/products/{id}/price` - 设置价格
- `POST /admin/products/{id}/attributes` - 设置属性

**功能特性**:
- 价格配置
- 供货状态
- 多分类支持
- 产品属性

**测试覆盖**: 11/11 测试通过 (100%)

---

#### 4.7 站点设置路由 (`settings.py`)

**端点**:
- `GET /admin/settings` - 设置页面
- `GET /admin/settings/{key}` - 获取单个设置
- `POST /admin/settings` - 保存设置

**功能特性**:
- Key-Value 存储
- 18个配置项
- 分组管理
- 类型验证

**测试覆盖**: 8/8 测试通过 (100%)

---

#### 4.8 相册管理路由 (`galleries.py`)

**端点**:
- `POST /admin/galleries` - 创建相册
- `PUT /admin/galleries/{id}` - 更新相册
- `DELETE /admin/galleries/{id}` - 删除相册
- `POST /admin/galleries/{id}/images/batch` - 批量添加图片
- `PATCH /admin/galleries/{id}/images/{image_id}` - 更新图片信息
- `POST /admin/galleries/{id}/images/{image_id}/toggle-visibility` - 切换显示
- `POST /admin/galleries/{id}/set-cover` - 设置封面
- `POST /admin/galleries/{id}/images/drag-sort` - 拖拽排序
- `POST /admin/galleries/{id}/images/reorder` - 批量重排序

**功能特性**:
- 批量上传
- 拖拽排序
- 图片元数据
- 封面设置

**测试覆盖**: 10/10 测试通过 (100%)，覆盖率 92%

---

#### 4.9 留言管理路由 (`contacts.py`)

**端点**:
- `GET /admin/contacts` - 留言列表页面
- `GET /admin/contacts/{id}` - 获取留言详情
- `PUT /admin/contacts/{id}/status` - 更新状态
- `POST /admin/contacts/batch/status` - 批量更新状态
- `DELETE /admin/contacts/{id}` - 删除留言
- `GET /admin/contacts/export/csv` - 导出CSV

**功能特性**:
- CSV 导出
- 批量操作
- 状态管理
- AJAX 交互

**测试覆盖**: 10/10 测试通过 (100%)

---

## 🎨 前端资源

### CSS 文件 (`admin/static/css/admin.css`)

**功能**: 管理后台统一样式

**主要样式**:
- 布局样式（头部、侧边栏、主内容区）
- 表单样式
- 表格样式
- 按钮样式
- 卡片样式
- 模态框样式
- 消息提示样式

---

### JavaScript 文件

#### `admin.js` - 通用功能
- 导航菜单切换
- 消息提示
- 确认对话框
- AJAX 请求封装

#### `columns.js` - 栏目管理
- 拖拽排序
- 树形展开/折叠
- AJAX CRUD 操作

#### `contacts.js` - 留言管理
- 批量选择
- 批量操作
- 详情模态框
- CSV 导出

#### `pages.js` - 单页管理
- Markdown 编辑器
- 实时预览
- 字数统计

#### `products.js` - 产品管理
- 分类多选
- 价格输入验证
- 图片上传预览

#### `settings.js` - 设置管理
- 表单验证
- 分组切换
- 实时保存

---

## 🧪 测试架构

### 测试配置 (`admin/tests/conftest.py`)

**Fixtures**:
- `db` - 测试数据库会话
- `client` - FastAPI 测试客户端
- `test_admin_user` - 测试管理员用户
- `test_media_file` - 测试媒体文件
- `test_media_files` - 多个测试媒体文件
- `test_gallery` - 测试相册
- `test_column` - 测试栏目

### 测试文件命名规范

- `test_<module>_<feature>.py`
- 例如: `test_media_upload.py`, `test_column_tree.py`

### 测试覆盖统计

| 模块 | 测试文件数 | 测试数量 | 通过率 |
|------|-----------|---------|-------|
| 认证 | 1 | 20 | 75% |
| 媒体库 | 4 | 23 | 100% |
| 栏目管理 | 3 | 18 | 100% |
| 单页管理 | 2 | 12 | 100% |
| 文章管理 | 3 | 15 | 100% |
| 产品管理 | 3 | 11 | 100% |
| 站点设置 | 2 | 8 | 100% |
| 相册管理 | 3 | 10 | 100% |
| 留言管理 | 3 | 10 | 100% |
| **总计** | **24** | **145** | **97%** |

---

## 🔧 工具脚本

### 数据库迁移 (`scripts/migrate_media_file.py`)

**功能**: 添加 media_file 表缺失的列

**执行方式**:
```bash
source venv/bin/activate
python scripts/migrate_media_file.py
```

**添加的列**:
- `usage_count` - 使用次数
- `title` - 媒体标题
- `alt_text` - Alt 文本
- `caption` - 说明文字

---

## 📊 技术栈

### 后端
- **FastAPI** - Web 框架
- **SQLAlchemy 2.0** - ORM
- **Pydantic** - 数据验证
- **Jinja2** - 模板引擎
- **Python 3.13** - 编程语言

### 前端
- **原生 JavaScript** - 前端交互
- **CSS3** - 样式设计
- **Fetch API** - AJAX 请求

### 测试
- **Pytest** - 测试框架
- **Black** - 代码格式化
- **isort** - 导入排序
- **ruff** - 代码检查

### 数据库
- **SQLite** - 开发环境
- **PostgreSQL** - 生产环境（推荐）

---

## 🔐 安全措施

### 认证机制
- Session 会话管理
- 密码 bcrypt 加密
- 登录状态验证

### XSS 防护
- HTML 内容转义
- Markdown 安全渲染
- 输入验证

### CSRF 防护
- SameSite Cookie 属性
- POST 请求验证

### 文件上传安全
- 文件类型白名单
- 文件大小限制
- 文件名清理

---

## 📝 代码规范

### Python 代码
- 遵循 PEP 8 规范
- 使用 Black 格式化
- 使用 Type Hints
- 编写 Docstrings

### 命名规范
- 文件名: `snake_case`
- 类名: `PascalCase`
- 函数名: `snake_case`
- 常量: `UPPER_CASE`

### 注释规范
- 模块级 Docstring
- 函数级 Docstring
- 复杂逻辑添加行内注释

---

## 🚀 性能优化

### 数据库优化
- 添加索引到常用查询字段
- 使用连接池
- 避免 N+1 查询

### 缓存策略
- 静态文件缓存
- 数据库查询缓存
- Session 缓存

### 前端优化
- 静态资源压缩
- 图片懒加载
- AJAX 请求节流

---

## 📖 相关文档

- [操作手册](./admin-operation-manual.md)
- [测试报告](./admin-system-test-report.md)
- [模块开发文档](./admin-modules/)
- [API 文档](http://localhost:8001/docs) - 运行时访问

---

**文档维护者**: maxazure
**最后更新**: 2025-11-13
**版本**: v1.0.0
