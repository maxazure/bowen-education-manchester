# 博文教育集团管理后台设计方案

**文档版本**: v1.0
**创建日期**: 2025-11-13
**项目**: Bowen Education Group CMS

---

## 目录

1. [项目概述](#一项目概述)
2. [业务逻辑方案](#二业务逻辑方案)
3. [技术实现方案](#三技术实现方案)
4. [数据库设计](#四数据库设计)
5. [API接口设计](#五api接口设计)
6. [开发计划](#六开发计划)
7. [安全性考虑](#七安全性考虑)

---

## 一、项目概述

### 1.1 背景
博文教育集团网站目前已完成前台开发，包含首页、关于、中文学校、国际象棋、羽毛球、政府项目等完整功能模块。现需开发配套的管理后台系统，实现内容的动态管理和维护。

### 1.2 目标
- 提供直观易用的内容管理界面
- 支持 Markdown 格式的内容编辑
- 实现媒体文件的上传和管理
- 保证系统安全性和稳定性
- 与现有前台系统无缝集成

### 1.3 用户角色
- **管理员**: 拥有所有功能的完全访问权限（单用户模式）

---

## 二、业务逻辑方案

### 2.1 核心模块划分

#### 优先级 P0（核心功能，Week 1-3）

##### 模块 1：用户管理
**功能描述**: 管理员账号的创建、登录、修改密码

**核心功能**:
- 管理员登录/登出
- 密码修改
- Session 管理

**数据模型**:
```python
admin_user:
  - id (主键)
  - username (唯一)
  - password_hash
  - email
  - last_login_at
  - created_at
```

---

##### 模块 2：媒体库管理
**功能描述**: 图片、文件的上传、管理、预览和删除

**核心功能**:
- 文件上传（支持拖拽上传）
- 图片预览（Grid 网格布局）
- 文件筛选（按类型、日期）
- 文件搜索（按文件名）
- 文件删除（带使用检查）
- 文件信息编辑（标题、Alt文本、说明）
- 图片选择器（供其他模块使用）

**业务规则**:
- 支持的图片格式: JPG, PNG, GIF, WebP
- 单文件大小限制: 5MB
- 删除前检查是否被引用
- 自动生成缩略图（用于列表显示）

**界面设计**:
```
媒体库
├── 顶部操作栏
│   ├── 上传按钮
│   ├── 搜索框
│   └── 类型筛选（全部/图片/文档）
├── 网格视图
│   ├── 图片卡片（缩略图 + 文件名 + 操作）
│   └── 分页器
└── 详情侧边栏（选中文件时显示）
    ├── 预览
    ├── 文件信息
    └── 编辑表单
```

---

##### 模块 3：栏目管理
**功能描述**: 网站栏目结构的配置和管理

**核心功能**:
- 栏目列表展示（树形结构）
- 栏目创建/编辑/删除
- 栏目排序（拖拽排序）
- 栏目启用/禁用
- Hero 区域配置
- 导航显示控制

**数据字段**:
- 基础信息: 名称、Slug、描述
- 类型: SINGLE_PAGE, POST, PRODUCT, CUSTOM, GALLERY
- Hero 配置: 标题、副标题、背景图、CTA
- 显示控制: 是否启用、是否显示在导航、是否显示在底部

**业务规则**:
- Slug 必须唯一
- 不能删除包含内容的栏目
- 父栏目不能是自己
- 排序值自动生成，可手动调整

**界面设计**:
```
栏目管理
├── 左侧树形结构
│   ├── 可折叠的父子关系
│   └── 拖拽排序
└── 右侧编辑表单
    ├── 基础信息 Tab
    ├── Hero 配置 Tab
    └── 高级设置 Tab
```

---

##### 模块 4：单页管理
**功能描述**: 单页面内容的编辑和发布

**核心功能**:
- 单页列表展示
- Markdown 编辑器（带实时预览）
- 图片插入（调用媒体库选择器）
- Hero 背景图设置
- SEO 信息配置
- 发布状态控制
- 保存草稿

**编辑器功能**:
- Markdown 语法高亮
- 实时预览（左右分屏或上下分屏）
- 工具栏（加粗、斜体、标题、列表、链接、图片等）
- 全屏编辑模式
- 图片上传（粘贴上传）

**业务规则**:
- Slug 自动生成，可手动修改
- Slug 必须唯一
- 保存草稿不影响前台显示
- 发布时自动更新 published_at

**界面设计**:
```
单页编辑
├── 顶部操作栏
│   ├── 保存草稿
│   ├── 发布
│   └── 返回列表
├── 基础信息区域
│   ├── 标题
│   ├── Slug
│   └── 副标题
├── Markdown 编辑器（左右分屏）
│   ├── 左侧: 编辑区（带工具栏）
│   └── 右侧: 实时预览
└── 侧边栏
    ├── 发布状态
    ├── Hero 背景图选择
    └── SEO 设置（可折叠）
```

---

##### 模块 5：文章管理
**功能描述**: 新闻、博客、活动等文章内容的管理

**核心功能**:
- 文章列表（支持筛选、搜索、分页）
- 文章创建/编辑/删除
- Markdown 编辑器（带预览）
- 封面图设置
- 分类选择（多选）
- 文章状态管理（草稿/已发布）
- 推荐/置顶标记
- 定时发布（可选）

**列表筛选**:
- 按状态筛选（全部/草稿/已发布）
- 按栏目筛选
- 按分类筛选
- 按发布日期筛选
- 关键词搜索（标题、摘要）

**业务规则**:
- 文章必须归属于一个栏目
- 可以选择多个分类
- 摘要为可选，如果为空则自动提取正文前 200 字
- Slug 自动从标题生成，支持手动修改
- 发布时间可以设置为未来时间（定时发布）

**界面设计**:
```
文章列表
├── 顶部操作栏
│   ├── 新建文章按钮
│   ├── 搜索框
│   └── 筛选器（栏目、分类、状态）
├── 表格视图
│   ├── 列: 标题、栏目、分类、状态、发布时间、操作
│   └── 行操作: 编辑、删除、快速发布/取消发布
└── 分页器

文章编辑
├── 顶部操作栏
│   ├── 保存草稿
│   ├── 发布/取消发布
│   └── 返回列表
├── 基础信息
│   ├── 标题
│   ├── Slug
│   ├── 摘要
│   ├── 所属栏目（下拉选择）
│   └── 分类（多选标签）
├── Markdown 编辑器（带预览）
└── 侧边栏
    ├── 封面图选择
    ├── 发布状态
    ├── 发布时间
    ├── 推荐/置顶开关
    └── SEO 设置
```

---

##### 模块 6：站点设置
**功能描述**: 全局站点配置管理

**核心功能**:
- 站点基本信息（名称、Logo、Slogan）
- 联系方式（电话、邮箱、地址、营业时间）
- 社交媒体链接（微信、WhatsApp、Facebook 等）
- 其他设置（ICP 备案、统计代码等）

**设置分组**:
1. **基本信息**:
   - 站点名称（中文/英文）
   - Logo（上传）
   - Favicon（上传）
   - 站点描述

2. **联系方式**:
   - 电话
   - 邮箱
   - 地址（中文/英文）
   - 营业时间

3. **社交媒体**:
   - 微信二维码
   - WhatsApp
   - Facebook
   - Instagram

4. **高级设置**:
   - Google Analytics ID
   - ICP 备案号
   - 版权信息

**业务规则**:
- 所有设置以键值对形式存储
- 支持多语言字段
- Logo 和图片通过媒体库选择

**界面设计**:
```
站点设置
├── 左侧导航
│   ├── 基本信息
│   ├── 联系方式
│   ├── 社交媒体
│   └── 高级设置
└── 右侧表单
    ├── 分组表单字段
    └── 保存按钮（固定在底部）
```

---

#### 优先级 P1（重要功能，Week 4-5）

##### 模块 7：产品/课程管理
**功能描述**: 课程产品的信息管理

**核心功能**:
- 产品列表（表格视图）
- 产品创建/编辑/删除
- Markdown 编辑器（产品描述）
- 封面图设置
- 价格配置
- 分类管理
- 产品属性（等级、时长、容量、教师）
- 推荐/热门标记

**业务规则**:
- 产品必须归属于一个栏目（如"补习中心"）
- 价格支持数字或文本（如"免费"、"面议"）
- 可以设置原价和现价（显示折扣）
- 分类可多选

**界面设计**:
```
产品列表
├── 顶部操作栏（新建、搜索、筛选）
├── 表格（产品名称、价格、分类、状态、操作）
└── 分页器

产品编辑
├── 基础信息（名称、Slug、摘要）
├── 价格信息（现价、原价、价格文本）
├── Markdown 编辑器（产品描述）
├── 产品属性（等级、时长、容量、教师）
└── 侧边栏（封面图、分类、状态、标记）
```

---

##### 模块 8：相册管理
**功能描述**: 图片相册的批量管理

**核心功能**:
- 相册列表
- 相册创建/编辑/删除
- 批量图片上传
- 图片排序（拖拽）
- 图片元数据编辑（标题、说明、Alt文本）
- 图片显示/隐藏控制
- 封面图设置

**业务规则**:
- 一个相册可以包含多张图片
- 图片可以单独设置元数据
- 图片排序影响前台展示顺序
- 相册必须归属于一个栏目

**界面设计**:
```
相册列表
├── 顶部操作栏（新建相册、搜索）
├── 卡片视图（相册封面、名称、图片数量、操作）
└── 分页器

相册编辑
├── 基础信息（名称、Slug、描述）
├── 图片管理区域
│   ├── 批量上传按钮
│   ├── 图片网格（可拖拽排序）
│   └── 图片卡片（缩略图、编辑、删除）
└── 图片详情编辑（点击图片弹出）
    ├── 标题
    ├── 说明
    ├── Alt 文本
    └── 显示/隐藏开关
```

---

##### 模块 9：留言管理
**功能描述**: 联系表单提交消息的查看和处理

**核心功能**:
- 留言列表（表格视图）
- 留言详情查看
- 状态标记（新消息/已读/已回复/已归档）
- 留言搜索和筛选
- 留言删除
- 导出功能（CSV）

**列表字段**:
- 姓名
- 邮箱
- 电话
- 主题/感兴趣项目
- 提交时间
- 状态
- 操作

**业务规则**:
- 新提交的消息状态为"新消息"
- 可以批量标记状态
- 已归档的消息可以批量删除
- 导出包含所有字段

**界面设计**:
```
留言列表
├── 顶部操作栏
│   ├── 状态筛选（全部/新消息/已读/已回复/已归档）
│   ├── 搜索框
│   └── 导出按钮
├── 表格视图
│   ├── 列: 姓名、邮箱、主题、提交时间、状态
│   ├── 行操作: 查看详情、标记状态、删除
│   └── 批量操作: 标记为已读、删除
└── 分页器

留言详情（模态框）
├── 联系人信息（姓名、邮箱、电话）
├── 主题/项目
├── 留言内容
├── 提交时间
├── IP 地址
└── 操作按钮（标记状态、删除）
```

---

### 2.2 功能优先级总结

| 模块 | 优先级 | 开发周期 | 依赖关系 |
|-----|-------|---------|---------|
| 用户管理 | P0 | Week 1 | 无 |
| 媒体库管理 | P0 | Week 1-2 | 用户管理 |
| 栏目管理 | P0 | Week 2 | 用户管理 |
| 单页管理 | P0 | Week 2-3 | 媒体库、栏目 |
| 文章管理 | P0 | Week 3 | 媒体库、栏目 |
| 站点设置 | P0 | Week 3 | 媒体库 |
| 产品管理 | P1 | Week 4 | 媒体库、栏目 |
| 相册管理 | P1 | Week 4-5 | 媒体库、栏目 |
| 留言管理 | P1 | Week 5 | 无 |

---

## 三、技术实现方案

### 3.1 技术栈选型

#### 后端技术
- **Web 框架**: FastAPI 0.109.0（已有）
- **ORM**: SQLAlchemy 2.0.44（已有）
- **数据库**: SQLite（开发）/ PostgreSQL（生产推荐）
- **模板引擎**: Jinja2（与前台一致）
- **认证**: Session-based Authentication
- **密码加密**: bcrypt

#### 前端技术
- **CSS 框架**: Bootstrap 5.3
- **JavaScript**: Alpine.js 3.x（轻量级响应式）
- **Markdown 编辑器**: EasyMDE（MIT 许可，带预览）
- **图片上传**: Dropzone.js
- **图标**: Font Awesome 6
- **HTTP 客户端**: Axios（用于 AJAX）

#### 开发工具
- **代码格式化**: Black, isort
- **代码检查**: Ruff
- **类型检查**: mypy
- **测试**: pytest

---

### 3.2 项目结构设计

```
bowen-education-manchester/
├── app/
│   ├── admin/                    # 管理后台模块（新增）
│   │   ├── __init__.py
│   │   ├── routers/              # 路由
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # 登录/登出
│   │   │   ├── dashboard.py     # 仪表板
│   │   │   ├── columns.py       # 栏目管理
│   │   │   ├── pages.py         # 单页管理
│   │   │   ├── posts.py         # 文章管理
│   │   │   ├── products.py      # 产品管理
│   │   │   ├── galleries.py     # 相册管理
│   │   │   ├── media.py         # 媒体库
│   │   │   ├── contacts.py      # 留言管理
│   │   │   └── settings.py      # 站点设置
│   │   ├── middleware.py         # 认证中间件
│   │   ├── dependencies.py       # 依赖注入
│   │   └── utils.py             # 工具函数
│   ├── models/                   # 数据模型（已有，需扩展）
│   │   └── admin_user.py        # 管理员模型（新增）
│   ├── services/                 # 业务逻辑（已有，复用）
│   └── ...
├── templates/
│   ├── admin/                    # 管理后台模板（新增）
│   │   ├── base.html            # 基础布局
│   │   ├── login.html           # 登录页
│   │   ├── dashboard.html       # 仪表板
│   │   ├── columns/             # 栏目管理模板
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   ├── pages/               # 单页管理模板
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   ├── posts/               # 文章管理模板
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   ├── products/            # 产品管理模板
│   │   ├── galleries/           # 相册管理模板
│   │   ├── media/               # 媒体库模板
│   │   ├── contacts/            # 留言管理模板
│   │   ├── settings/            # 站点设置模板
│   │   └── components/          # 公共组件
│   │       ├── header.html
│   │       ├── sidebar.html
│   │       ├── pagination.html
│   │       └── media_picker.html
│   └── frontend/                 # 前台模板（已有）
├── static/
│   ├── admin/                    # 管理后台静态资源（新增）
│   │   ├── css/
│   │   │   └── admin.css        # 管理后台自定义样式
│   │   ├── js/
│   │   │   ├── admin.js         # 通用脚本
│   │   │   ├── media-picker.js  # 媒体选择器
│   │   │   └── markdown-editor.js  # Markdown 编辑器配置
│   │   └── images/              # 后台用图片
│   └── frontend/                 # 前台静态资源（已有）
├── uploads/                      # 用户上传文件（已有）
│   ├── images/                  # 图片
│   ├── documents/               # 文档
│   └── thumbnails/              # 缩略图（新增）
├── migrations/                   # 数据库迁移（已有）
├── tests/                        # 测试文件
│   ├── admin/                   # 管理后台测试（新增）
│   └── ...
├── main.py                       # 应用入口（已有，需注册管理后台路由）
└── requirements.txt              # 依赖列表（需更新）
```

---

### 3.3 路由设计

#### 管理后台路由前缀: `/admin`

```python
# 认证路由
GET  /admin/login              # 登录页面
POST /admin/login              # 登录提交
GET  /admin/logout             # 登出

# 仪表板
GET  /admin/                   # 仪表板（需认证）

# 栏目管理
GET  /admin/columns            # 栏目列表
GET  /admin/columns/new        # 新建栏目页面
POST /admin/columns            # 创建栏目
GET  /admin/columns/{id}/edit  # 编辑栏目页面
PUT  /admin/columns/{id}       # 更新栏目
DELETE /admin/columns/{id}     # 删除栏目
POST /admin/columns/reorder    # 栏目排序（AJAX）

# 单页管理
GET  /admin/pages              # 单页列表
GET  /admin/pages/new          # 新建单页页面
POST /admin/pages              # 创建单页
GET  /admin/pages/{id}/edit    # 编辑单页页面
PUT  /admin/pages/{id}         # 更新单页
DELETE /admin/pages/{id}       # 删除单页
POST /admin/pages/{id}/publish # 发布/取消发布（AJAX）

# 文章管理
GET  /admin/posts              # 文章列表（支持筛选）
GET  /admin/posts/new          # 新建文章页面
POST /admin/posts              # 创建文章
GET  /admin/posts/{id}/edit    # 编辑文章页面
PUT  /admin/posts/{id}         # 更新文章
DELETE /admin/posts/{id}       # 删除文章
POST /admin/posts/{id}/publish # 发布/取消发布（AJAX）

# 产品管理
GET  /admin/products           # 产品列表
GET  /admin/products/new       # 新建产品页面
POST /admin/products           # 创建产品
GET  /admin/products/{id}/edit # 编辑产品页面
PUT  /admin/products/{id}      # 更新产品
DELETE /admin/products/{id}    # 删除产品

# 相册管理
GET  /admin/galleries          # 相册列表
GET  /admin/galleries/new      # 新建相册页面
POST /admin/galleries          # 创建相册
GET  /admin/galleries/{id}/edit # 编辑相册页面
PUT  /admin/galleries/{id}     # 更新相册
DELETE /admin/galleries/{id}   # 删除相册
POST /admin/galleries/{id}/images # 添加图片（AJAX）
DELETE /admin/galleries/{id}/images/{image_id} # 删除图片（AJAX）
POST /admin/galleries/{id}/reorder # 图片排序（AJAX）

# 媒体库
GET  /admin/media              # 媒体列表（AJAX返回JSON）
POST /admin/media/upload       # 上传文件（AJAX）
GET  /admin/media/{id}         # 获取媒体详情（AJAX）
PUT  /admin/media/{id}         # 更新媒体信息（AJAX）
DELETE /admin/media/{id}       # 删除媒体（AJAX）
GET  /admin/media/picker       # 媒体选择器（模态框）

# 留言管理
GET  /admin/contacts           # 留言列表
GET  /admin/contacts/{id}      # 留言详情（AJAX）
PUT  /admin/contacts/{id}/status # 更新留言状态（AJAX）
DELETE /admin/contacts/{id}    # 删除留言
GET  /admin/contacts/export    # 导出CSV

# 站点设置
GET  /admin/settings           # 设置页面
PUT  /admin/settings           # 更新设置
```

---

### 3.4 认证系统设计

#### 认证方式
- **Session-based Authentication**: 使用 FastAPI 的 session middleware
- **密码加密**: bcrypt 哈希算法
- **Session 存储**: 服务器端 Session（使用 `starlette-session`）

#### 认证流程
```
1. 用户访问 /admin/login
2. 输入用户名和密码
3. 后端验证凭据
4. 验证成功: 创建 session，重定向到 /admin/
5. 验证失败: 返回错误消息
6. 后续请求: 通过 middleware 检查 session
7. 登出: 清除 session，重定向到 /admin/login
```

#### 中间件实现
```python
# app/admin/middleware.py

from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 公开路径（无需认证）
        public_paths = ["/admin/login"]

        # 如果是管理后台路径且不是公开路径
        if request.url.path.startswith("/admin") and request.url.path not in public_paths:
            # 检查 session 中是否有用户信息
            user_id = request.session.get("admin_user_id")
            if not user_id:
                # 未登录，重定向到登录页
                return RedirectResponse(url="/admin/login", status_code=302)

        response = await call_next(request)
        return response
```

#### 管理员模型
```python
# app/models/admin_user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
import bcrypt

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password: str):
        """设置密码（自动哈希）"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
```

---

### 3.5 Markdown 编辑器集成

#### 选择方案: EasyMDE
- **特点**: 简单易用、自带预览、MIT 许可
- **功能**: 工具栏、快捷键、实时预览、图片上传
- **大小**: ~100KB (gzipped)

#### 集成方式
```html
<!-- templates/admin/components/markdown_editor.html -->

<!-- 引入 EasyMDE CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css">

<!-- 编辑器容器 -->
<textarea id="markdown-content" name="content">{{ content }}</textarea>

<!-- 引入 EasyMDE JS -->
<script src="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js"></script>

<!-- 初始化编辑器 -->
<script>
const easyMDE = new EasyMDE({
    element: document.getElementById("markdown-content"),
    autofocus: true,
    spellChecker: false,
    placeholder: "请输入内容（支持 Markdown 语法）...",
    toolbar: [
        "bold", "italic", "heading", "|",
        "quote", "unordered-list", "ordered-list", "|",
        "link", {
            name: "image",
            action: function(editor) {
                // 打开媒体选择器
                openMediaPicker(function(url) {
                    // 插入图片链接
                    const cm = editor.codemirror;
                    const output = '![图片](' + url + ')';
                    cm.replaceSelection(output);
                });
            },
            className: "fa fa-image",
            title: "插入图片"
        }, "|",
        "preview", "side-by-side", "fullscreen", "|",
        "guide"
    ],
    previewRender: function(plainText) {
        // 自定义预览渲染（可以使用 marked.js）
        return marked.parse(plainText);
    }
});
</script>
```

#### 图片上传集成
```javascript
// static/admin/js/markdown-editor.js

function openMediaPicker(callback) {
    // 打开媒体选择器模态框
    const modal = new bootstrap.Modal(document.getElementById('media-picker-modal'));
    modal.show();

    // 监听图片选择事件
    window.addEventListener('media-selected', function(event) {
        callback(event.detail.url);
        modal.hide();
    }, { once: true });
}

// 也支持直接粘贴上传
easyMDE.codemirror.on('paste', function(cm, event) {
    const items = event.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
            event.preventDefault();
            const file = items[i].getAsFile();
            uploadImage(file, function(url) {
                cm.replaceSelection('![图片](' + url + ')');
            });
        }
    }
});
```

---

### 3.6 媒体库实现

#### 文件上传
```python
# app/admin/routers/media.py

from fastapi import UploadFile, File
from PIL import Image
import os
from datetime import datetime

@router.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    # 验证文件大小（5MB）
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小超过限制")

    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"

    # 保存原图
    file_path = f"uploads/images/{filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(contents)

    # 生成缩略图
    thumbnail_path = f"uploads/thumbnails/{filename}"
    os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img.save(thumbnail_path)

    # 保存到数据库
    media_file = MediaFile(
        file_name=file.filename,
        file_path=file_path,
        file_url=f"/{file_path}",
        thumbnail_url=f"/{thumbnail_path}",
        file_type="image",
        file_size=len(contents),
        mime_type=file.content_type,
        width=img.width,
        height=img.height
    )

    db.add(media_file)
    db.commit()
    db.refresh(media_file)

    return {"id": media_file.id, "url": media_file.file_url}
```

#### 媒体选择器
```html
<!-- templates/admin/components/media_picker.html -->

<!-- 媒体选择器模态框 -->
<div class="modal fade" id="media-picker-modal" tabindex="-1">
    <div class="modal-dialog modal-xl">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">选择图片</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <!-- 上传区域 -->
                <div class="upload-zone mb-3">
                    <button type="button" class="btn btn-primary" id="upload-btn">
                        <i class="fas fa-upload"></i> 上传图片
                    </button>
                    <input type="file" id="file-input" accept="image/*" style="display:none">
                </div>

                <!-- 搜索和筛选 -->
                <div class="filters mb-3">
                    <input type="text" class="form-control" placeholder="搜索图片..." id="media-search">
                </div>

                <!-- 图片网格 -->
                <div class="media-grid" id="media-grid">
                    <!-- 动态加载图片 -->
                </div>

                <!-- 分页 -->
                <nav>
                    <ul class="pagination justify-content-center" id="media-pagination"></ul>
                </nav>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" id="select-media-btn" disabled>选择</button>
            </div>
        </div>
    </div>
</div>

<style>
.media-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
    max-height: 400px;
    overflow-y: auto;
}

.media-item {
    position: relative;
    cursor: pointer;
    border: 2px solid transparent;
    border-radius: 4px;
    overflow: hidden;
}

.media-item.selected {
    border-color: #0d6efd;
}

.media-item img {
    width: 100%;
    height: 150px;
    object-fit: cover;
}

.media-item .media-info {
    padding: 5px;
    font-size: 12px;
    text-align: center;
    background: #f8f9fa;
}
</style>
```

```javascript
// static/admin/js/media-picker.js

class MediaPicker {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.selectedMedia = null;
        this.currentPage = 1;
        this.init();
    }

    init() {
        // 加载媒体列表
        this.loadMedia();

        // 上传按钮
        document.getElementById('upload-btn').addEventListener('click', () => {
            document.getElementById('file-input').click();
        });

        // 文件选择
        document.getElementById('file-input').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.uploadFile(file);
            }
        });

        // 搜索
        let searchTimeout;
        document.getElementById('media-search').addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.loadMedia(1, e.target.value);
            }, 300);
        });

        // 选择按钮
        document.getElementById('select-media-btn').addEventListener('click', () => {
            if (this.selectedMedia) {
                // 触发自定义事件
                const event = new CustomEvent('media-selected', {
                    detail: this.selectedMedia
                });
                window.dispatchEvent(event);
            }
        });
    }

    async loadMedia(page = 1, search = '') {
        const response = await fetch(`/admin/media?page=${page}&search=${search}`);
        const data = await response.json();

        this.renderMediaGrid(data.items);
        this.renderPagination(data.total, data.page, data.per_page);
    }

    renderMediaGrid(items) {
        const grid = document.getElementById('media-grid');
        grid.innerHTML = items.map(item => `
            <div class="media-item" data-id="${item.id}" data-url="${item.file_url}">
                <img src="${item.thumbnail_url}" alt="${item.file_name}">
                <div class="media-info">${item.file_name}</div>
            </div>
        `).join('');

        // 绑定点击事件
        grid.querySelectorAll('.media-item').forEach(item => {
            item.addEventListener('click', () => {
                this.selectMedia(item);
            });
        });
    }

    selectMedia(element) {
        // 移除之前的选中状态
        document.querySelectorAll('.media-item.selected').forEach(el => {
            el.classList.remove('selected');
        });

        // 添加选中状态
        element.classList.add('selected');

        // 保存选中的媒体
        this.selectedMedia = {
            id: element.dataset.id,
            url: element.dataset.url
        };

        // 启用选择按钮
        document.getElementById('select-media-btn').disabled = false;
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/admin/media/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                // 重新加载媒体列表
                this.loadMedia();
                alert('上传成功');
            } else {
                alert('上传失败: ' + data.detail);
            }
        } catch (error) {
            alert('上传失败: ' + error.message);
        }
    }

    renderPagination(total, page, perPage) {
        const totalPages = Math.ceil(total / perPage);
        const pagination = document.getElementById('media-pagination');

        let html = '';
        for (let i = 1; i <= totalPages; i++) {
            html += `
                <li class="page-item ${i === page ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `;
        }

        pagination.innerHTML = html;

        // 绑定分页点击事件
        pagination.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = parseInt(e.target.dataset.page);
                this.loadMedia(page);
            });
        });
    }
}

// 初始化媒体选择器
const mediaPicker = new MediaPicker('media-picker-modal');
```

---

### 3.7 前端框架选择

#### Bootstrap 5.3 布局示例
```html
<!-- templates/admin/base.html -->

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}管理后台{% endblock %} - 博文教育集团</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- 自定义样式 -->
    <link rel="stylesheet" href="/static/admin/css/admin.css">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="wrapper">
        <!-- 侧边栏 -->
        <nav id="sidebar" class="sidebar">
            <div class="sidebar-header">
                <h3>博文教育集团</h3>
                <p class="text-muted">管理后台</p>
            </div>

            <ul class="list-unstyled components">
                <li class="{{ 'active' if request.path == '/admin/' }}">
                    <a href="/admin/">
                        <i class="fas fa-tachometer-alt"></i> 仪表板
                    </a>
                </li>

                <li class="{{ 'active' if '/columns' in request.path }}">
                    <a href="/admin/columns">
                        <i class="fas fa-sitemap"></i> 栏目管理
                    </a>
                </li>

                <li class="{{ 'active' if '/pages' in request.path }}">
                    <a href="/admin/pages">
                        <i class="fas fa-file-alt"></i> 单页管理
                    </a>
                </li>

                <li class="{{ 'active' if '/posts' in request.path }}">
                    <a href="/admin/posts">
                        <i class="fas fa-newspaper"></i> 文章管理
                    </a>
                </li>

                <li class="{{ 'active' if '/products' in request.path }}">
                    <a href="/admin/products">
                        <i class="fas fa-shopping-cart"></i> 产品管理
                    </a>
                </li>

                <li class="{{ 'active' if '/galleries' in request.path }}">
                    <a href="/admin/galleries">
                        <i class="fas fa-images"></i> 相册管理
                    </a>
                </li>

                <li class="{{ 'active' if '/media' in request.path }}">
                    <a href="/admin/media">
                        <i class="fas fa-photo-video"></i> 媒体库
                    </a>
                </li>

                <li class="{{ 'active' if '/contacts' in request.path }}">
                    <a href="/admin/contacts">
                        <i class="fas fa-envelope"></i> 留言管理
                        {% if unread_count > 0 %}
                        <span class="badge bg-danger">{{ unread_count }}</span>
                        {% endif %}
                    </a>
                </li>

                <li class="{{ 'active' if '/settings' in request.path }}">
                    <a href="/admin/settings">
                        <i class="fas fa-cog"></i> 站点设置
                    </a>
                </li>
            </ul>
        </nav>

        <!-- 主内容区域 -->
        <div id="content">
            <!-- 顶部导航栏 -->
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="container-fluid">
                    <button type="button" id="sidebarCollapse" class="btn btn-outline-secondary">
                        <i class="fas fa-bars"></i>
                    </button>

                    <div class="ms-auto d-flex align-items-center">
                        <a href="/" target="_blank" class="btn btn-outline-primary me-2">
                            <i class="fas fa-external-link-alt"></i> 查看网站
                        </a>

                        <div class="dropdown">
                            <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user"></i> {{ admin_user.username }}
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="/admin/logout">
                                    <i class="fas fa-sign-out-alt"></i> 退出登录
                                </a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </nav>

            <!-- 面包屑 -->
            {% if breadcrumbs %}
            <nav aria-label="breadcrumb" class="mt-3 mx-3">
                <ol class="breadcrumb">
                    {% for crumb in breadcrumbs %}
                    <li class="breadcrumb-item {{ 'active' if loop.last }}">
                        {% if not loop.last %}
                        <a href="{{ crumb.url }}">{{ crumb.title }}</a>
                        {% else %}
                        {{ crumb.title }}
                        {% endif %}
                    </li>
                    {% endfor %}
                </ol>
            </nav>
            {% endif %}

            <!-- 主要内容 -->
            <div class="container-fluid p-4">
                {% block content %}{% endblock %}
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <!-- Axios -->
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

    <!-- 自定义脚本 -->
    <script src="/static/admin/js/admin.js"></script>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

### 3.8 Alpine.js 使用示例

#### 文章列表筛选
```html
<!-- templates/admin/posts/list.html -->

{% extends "admin/base.html" %}

{% block content %}
<div x-data="postList()">
    <!-- 顶部操作栏 -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>文章管理</h2>
        <a href="/admin/posts/new" class="btn btn-primary">
            <i class="fas fa-plus"></i> 新建文章
        </a>
    </div>

    <!-- 筛选器 -->
    <div class="card mb-3">
        <div class="card-body">
            <div class="row g-3">
                <div class="col-md-3">
                    <label class="form-label">栏目</label>
                    <select class="form-select" x-model="filters.column_id" @change="loadPosts()">
                        <option value="">全部</option>
                        <template x-for="column in columns" :key="column.id">
                            <option :value="column.id" x-text="column.name"></option>
                        </template>
                    </select>
                </div>

                <div class="col-md-3">
                    <label class="form-label">状态</label>
                    <select class="form-select" x-model="filters.status" @change="loadPosts()">
                        <option value="">全部</option>
                        <option value="draft">草稿</option>
                        <option value="published">已发布</option>
                    </select>
                </div>

                <div class="col-md-6">
                    <label class="form-label">搜索</label>
                    <input type="text" class="form-control" placeholder="搜索标题..."
                           x-model="filters.search" @input.debounce.500ms="loadPosts()">
                </div>
            </div>
        </div>
    </div>

    <!-- 文章表格 -->
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>标题</th>
                            <th>栏目</th>
                            <th>状态</th>
                            <th>发布时间</th>
                            <th>浏览量</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <template x-for="post in posts" :key="post.id">
                            <tr>
                                <td>
                                    <div x-text="post.title"></div>
                                    <div class="text-muted small" x-text="post.slug"></div>
                                </td>
                                <td x-text="post.column_name"></td>
                                <td>
                                    <span class="badge"
                                          :class="post.status === 'published' ? 'bg-success' : 'bg-secondary'"
                                          x-text="post.status === 'published' ? '已发布' : '草稿'"></span>
                                    <span x-show="post.is_recommended" class="badge bg-warning ms-1">推荐</span>
                                    <span x-show="post.is_top" class="badge bg-danger ms-1">置顶</span>
                                </td>
                                <td x-text="formatDate(post.published_at)"></td>
                                <td x-text="post.view_count"></td>
                                <td>
                                    <a :href="`/admin/posts/${post.id}/edit`" class="btn btn-sm btn-outline-primary">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <button @click="togglePublish(post)" class="btn btn-sm btn-outline-secondary">
                                        <i :class="post.status === 'published' ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                                    </button>
                                    <button @click="deletePost(post.id)" class="btn btn-sm btn-outline-danger">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>

            <!-- 分页 -->
            <nav>
                <ul class="pagination justify-content-center">
                    <template x-for="page in totalPages" :key="page">
                        <li class="page-item" :class="{ 'active': page === currentPage }">
                            <a class="page-link" href="#" @click.prevent="loadPosts(page)" x-text="page"></a>
                        </li>
                    </template>
                </ul>
            </nav>
        </div>
    </div>
</div>

<script>
function postList() {
    return {
        posts: [],
        columns: [],
        filters: {
            column_id: '',
            status: '',
            search: ''
        },
        currentPage: 1,
        totalPages: 1,

        async init() {
            await this.loadColumns();
            await this.loadPosts();
        },

        async loadColumns() {
            const response = await axios.get('/admin/api/columns');
            this.columns = response.data;
        },

        async loadPosts(page = 1) {
            const params = new URLSearchParams({
                page: page,
                ...this.filters
            });

            const response = await axios.get(`/admin/api/posts?${params}`);
            this.posts = response.data.items;
            this.currentPage = response.data.page;
            this.totalPages = response.data.total_pages;
        },

        async togglePublish(post) {
            try {
                await axios.post(`/admin/posts/${post.id}/publish`);
                post.status = post.status === 'published' ? 'draft' : 'published';
            } catch (error) {
                alert('操作失败');
            }
        },

        async deletePost(id) {
            if (!confirm('确定要删除这篇文章吗？')) return;

            try {
                await axios.delete(`/admin/posts/${id}`);
                await this.loadPosts();
            } catch (error) {
                alert('删除失败');
            }
        },

        formatDate(dateString) {
            if (!dateString) return '-';
            return new Date(dateString).toLocaleString('zh-CN');
        }
    }
}
</script>
{% endblock %}
```

---

## 四、数据库设计

### 4.1 新增表

#### admin_users（管理员用户表）
```sql
CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 初始管理员账号（密码: admin123）
INSERT INTO admin_users (username, password_hash, email) VALUES (
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYCWqQJFwKi',
    'admin@boweneducation.org'
);
```

### 4.2 表字段扩展

#### media_file 表扩展
```sql
-- 添加缩略图字段
ALTER TABLE media_file ADD COLUMN thumbnail_url VARCHAR(500);

-- 添加使用统计
ALTER TABLE media_file ADD COLUMN usage_count INTEGER DEFAULT 0;
```

#### site_column 表（已有，无需修改）
现有字段已满足需求

#### single_page 表（已有，可能需要扩展）
```sql
-- 添加 Markdown 原始内容字段
ALTER TABLE single_page ADD COLUMN content_markdown TEXT;

-- content_html 将从 content_markdown 转换生成
```

#### post 表（已有，可能需要扩展）
```sql
-- 添加 Markdown 原始内容字段
ALTER TABLE post ADD COLUMN content_markdown TEXT;
```

#### product 表（已有，无需修改）
现有字段已满足需求

---

## 五、API 接口设计

### 5.1 RESTful API 规范

所有管理后台 API 采用以下规范：
- **成功响应**: HTTP 200，返回 JSON 数据
- **创建成功**: HTTP 201，返回创建的资源
- **更新成功**: HTTP 200，返回更新后的资源
- **删除成功**: HTTP 204，无内容
- **客户端错误**: HTTP 400，返回错误信息
- **未授权**: HTTP 401，重定向到登录页
- **禁止访问**: HTTP 403，返回错误信息
- **未找到**: HTTP 404，返回错误信息
- **服务器错误**: HTTP 500，返回错误信息

### 5.2 通用响应格式

#### 列表响应
```json
{
    "items": [...],
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
}
```

#### 错误响应
```json
{
    "detail": "错误描述信息"
}
```

### 5.3 核心接口定义

#### 文章管理 API
```python
# GET /admin/api/posts
# 参数: page, per_page, column_id, status, search
# 响应: 文章列表

# GET /admin/api/posts/{id}
# 响应: 文章详情

# POST /admin/api/posts
# 请求体: { title, slug, content_markdown, column_id, ... }
# 响应: 创建的文章

# PUT /admin/api/posts/{id}
# 请求体: { title, slug, content_markdown, ... }
# 响应: 更新后的文章

# DELETE /admin/api/posts/{id}
# 响应: HTTP 204

# POST /admin/api/posts/{id}/publish
# 响应: { status: "published" }
```

#### 媒体库 API
```python
# GET /admin/api/media
# 参数: page, per_page, type, search
# 响应: 媒体文件列表

# POST /admin/api/media/upload
# 请求体: multipart/form-data (file)
# 响应: { id, url, thumbnail_url }

# GET /admin/api/media/{id}
# 响应: 媒体文件详情

# PUT /admin/api/media/{id}
# 请求体: { title, alt_text, caption }
# 响应: 更新后的媒体文件

# DELETE /admin/api/media/{id}
# 响应: HTTP 204（检查是否被使用）
```

---

## 六、开发计划

### 6.1 总体时间规划

**总开发时间**: 5-6 周（按每天 6-8 小时计算）

```
Week 1: 基础框架 + 认证系统 + 媒体库
Week 2: 栏目管理 + 单页管理
Week 3: 文章管理 + Markdown 编辑器优化
Week 4: 产品管理 + 站点设置
Week 5: 相册管理 + 留言管理
Week 6: 测试、优化、文档
```

### 6.2 详细开发计划

#### Week 1: 基础框架（5-7 天）

**Day 1-2: 项目结构搭建**
- [ ] 创建 `app/admin/` 目录结构
- [ ] 创建 `templates/admin/` 模板目录
- [ ] 创建 `static/admin/` 静态资源目录
- [ ] 配置路由和中间件
- [ ] 集成 Bootstrap 5 和 Alpine.js

**Day 3-4: 认证系统**
- [ ] 创建 `admin_users` 表和模型
- [ ] 实现登录页面和逻辑
- [ ] 实现 Session 管理
- [ ] 实现认证中间件
- [ ] 实现登出功能
- [ ] 添加初始管理员账号

**Day 5-7: 媒体库**
- [ ] 实现文件上传功能
- [ ] 实现缩略图生成
- [ ] 实现媒体列表页面
- [ ] 实现媒体选择器组件
- [ ] 实现图片预览和编辑
- [ ] 实现文件删除（带使用检查）

**交付物**:
- ✅ 可登录的管理后台
- ✅ 完整的媒体库功能
- ✅ 可复用的媒体选择器组件

---

#### Week 2: 栏目管理 + 单页管理（5-7 天）

**Day 1-3: 栏目管理**
- [ ] 实现栏目列表页面（树形结构）
- [ ] 实现栏目创建/编辑表单
- [ ] 实现 Hero 配置功能
- [ ] 实现栏目排序（拖拽或手动）
- [ ] 实现栏目启用/禁用
- [ ] 实现栏目删除（带内容检查）

**Day 4-7: 单页管理**
- [ ] 集成 EasyMDE Markdown 编辑器
- [ ] 实现单页列表页面
- [ ] 实现单页创建/编辑表单
- [ ] 实现 Markdown 到 HTML 转换
- [ ] 实现图片插入（集成媒体选择器）
- [ ] 实现 SEO 设置
- [ ] 实现草稿和发布功能

**交付物**:
- ✅ 完整的栏目管理功能
- ✅ 带 Markdown 编辑器的单页管理
- ✅ Markdown 实时预览

---

#### Week 3: 文章管理（5-7 天）

**Day 1-3: 文章列表和筛选**
- [ ] 实现文章列表页面
- [ ] 实现多条件筛选（栏目、分类、状态）
- [ ] 实现关键词搜索
- [ ] 实现分页功能
- [ ] 实现批量操作（删除、发布）

**Day 4-7: 文章编辑**
- [ ] 实现文章创建/编辑表单
- [ ] 集成 Markdown 编辑器
- [ ] 实现分类多选
- [ ] 实现封面图选择
- [ ] 实现推荐/置顶标记
- [ ] 实现定时发布（可选）
- [ ] 优化 Markdown 编辑器体验

**交付物**:
- ✅ 完整的文章管理功能
- ✅ 高级筛选和搜索
- ✅ 优秀的编辑体验

---

#### Week 4: 产品管理 + 站点设置（5-7 天）

**Day 1-4: 产品管理**
- [ ] 实现产品列表页面
- [ ] 实现产品创建/编辑表单
- [ ] 实现价格配置
- [ ] 实现产品属性配置
- [ ] 实现分类管理
- [ ] 实现推荐/热门标记

**Day 5-7: 站点设置**
- [ ] 实现设置页面（分组表单）
- [ ] 实现基本信息设置
- [ ] 实现联系方式设置
- [ ] 实现社交媒体设置
- [ ] 实现高级设置
- [ ] 实现 Logo 上传

**交付物**:
- ✅ 完整的产品/课程管理
- ✅ 全局站点设置功能

---

#### Week 5: 相册管理 + 留言管理（5-7 天）

**Day 1-4: 相册管理**
- [ ] 实现相册列表页面
- [ ] 实现相册创建/编辑
- [ ] 实现批量图片上传
- [ ] 实现图片排序（拖拽）
- [ ] 实现图片元数据编辑
- [ ] 实现封面图设置

**Day 5-7: 留言管理**
- [ ] 实现留言列表页面
- [ ] 实现留言详情查看
- [ ] 实现状态筛选
- [ ] 实现状态标记
- [ ] 实现留言删除
- [ ] 实现 CSV 导出

**交付物**:
- ✅ 完整的相册管理功能
- ✅ 完整的留言管理功能

---

#### Week 6: 测试、优化、文档（5-7 天）

**Day 1-2: 功能测试**
- [ ] 测试所有 CRUD 操作
- [ ] 测试文件上传和删除
- [ ] 测试筛选和搜索
- [ ] 测试 Markdown 编辑和预览
- [ ] 测试响应式布局
- [ ] 修复发现的 Bug

**Day 3-4: 性能优化**
- [ ] 优化数据库查询
- [ ] 优化图片加载（懒加载）
- [ ] 优化 JavaScript 性能
- [ ] 添加加载动画
- [ ] 优化用户体验

**Day 5-7: 文档和部署**
- [ ] 编写管理员使用手册
- [ ] 编写开发文档
- [ ] 编写 API 文档
- [ ] 准备生产环境配置
- [ ] 数据库迁移脚本
- [ ] 部署测试

**交付物**:
- ✅ 稳定可用的管理后台系统
- ✅ 完整的文档
- ✅ 生产环境部署方案

---

### 6.3 里程碑

| 里程碑 | 完成时间 | 交付内容 |
|-------|---------|---------|
| M1: 基础框架 | Week 1 结束 | 登录系统 + 媒体库 |
| M2: 内容管理 | Week 3 结束 | 栏目 + 单页 + 文章管理 |
| M3: 功能完善 | Week 5 结束 | 产品 + 相册 + 留言 + 设置 |
| M4: 生产就绪 | Week 6 结束 | 测试完成 + 文档完成 |

---

## 七、安全性考虑

### 7.1 身份认证和授权
- **Session 安全**: 使用 HTTPOnly Cookie，防止 XSS 攻击
- **密码存储**: bcrypt 哈希，加盐存储
- **Session 过期**: 设置合理的过期时间（如 24 小时）
- **CSRF 防护**: 使用 CSRF Token（FastAPI 内置支持）

### 7.2 文件上传安全
- **文件类型验证**: 白名单验证，只允许图片类型
- **文件大小限制**: 单文件最大 5MB
- **文件名清洗**: 移除特殊字符，防止路径遍历
- **存储隔离**: 用户上传文件存储在独立目录
- **病毒扫描**: 可选，集成 ClamAV（生产环境推荐）

### 7.3 SQL 注入防护
- **ORM 使用**: 使用 SQLAlchemy ORM，避免直接拼接 SQL
- **参数化查询**: 所有查询使用参数化
- **输入验证**: 使用 Pydantic 进行输入验证

### 7.4 XSS 防护
- **HTML 转义**: Jinja2 自动转义 HTML
- **Markdown 渲染**: 使用安全的 Markdown 渲染器（如 mistune）
- **CSP 头**: 设置 Content-Security-Policy 头

### 7.5 其他安全措施
- **HTTPS**: 生产环境必须使用 HTTPS
- **访问日志**: 记录所有管理操作
- **备份策略**: 定期备份数据库
- **权限最小化**: 数据库用户权限最小化
- **依赖更新**: 定期更新依赖包，修复安全漏洞

---

## 八、技术栈总结

### 8.1 后端依赖
```txt
# requirements.txt 新增依赖

# Markdown 处理
mistune==3.0.2              # Markdown 解析器
Pygments==2.17.2            # 代码高亮

# 密码加密
bcrypt==4.1.2

# Session 管理
itsdangerous==2.1.2
starlette-session==0.3.0

# 图片处理
Pillow==10.2.0

# 文件上传
python-multipart==0.0.7

# 工具
python-slugify==8.0.1       # Slug 生成
```

### 8.2 前端依赖（CDN）
```html
<!-- Bootstrap 5.3 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Font Awesome 6 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Alpine.js 3 -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Axios -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

<!-- EasyMDE (Markdown 编辑器) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css">
<script src="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js"></script>

<!-- Marked.js (Markdown 渲染) -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<!-- SortableJS (拖拽排序) -->
<script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
```

---

## 九、附录

### 9.1 数据库迁移脚本

```bash
# 创建迁移
alembic revision --autogenerate -m "add admin system tables"

# 执行迁移
alembic upgrade head
```

### 9.2 初始化脚本

```python
# scripts/init_admin.py

"""
初始化管理员账号
使用方法: python scripts/init_admin.py
"""

from app.database import SessionLocal
from app.models.admin_user import AdminUser

def init_admin():
    db = SessionLocal()

    # 检查是否已有管理员
    existing = db.query(AdminUser).filter_by(username="admin").first()
    if existing:
        print("管理员账号已存在")
        return

    # 创建初始管理员
    admin = AdminUser(
        username="admin",
        email="admin@boweneducation.org"
    )
    admin.set_password("admin123")  # 请在首次登录后修改密码

    db.add(admin)
    db.commit()

    print("✅ 初始管理员账号创建成功")
    print("用户名: admin")
    print("密码: admin123")
    print("⚠️  请在首次登录后立即修改密码")

    db.close()

if __name__ == "__main__":
    init_admin()
```

### 9.3 常用命令

```bash
# 启动开发服务器
uvicorn main:app --reload --port 8000

# 创建管理员
python scripts/init_admin.py

# 运行测试
pytest tests/admin/

# 代码格式化
black app/admin/
isort app/admin/

# 类型检查
mypy app/admin/

# 生成密钥（用于 Session）
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 十、总结

### 10.1 方案优势
1. **技术栈统一**: 后端完全使用 FastAPI + SQLAlchemy，与前台一致
2. **开发效率高**: 使用 Bootstrap + Alpine.js 快速构建界面
3. **Markdown 支持**: 内容编辑使用 Markdown，编辑体验优秀
4. **模块化设计**: 各模块独立，易于维护和扩展
5. **安全可靠**: 完善的认证和授权机制
6. **用户体验好**: 响应式设计，支持移动端访问

### 10.2 未来扩展方向
1. **多用户角色**: 支持不同权限的管理员
2. **审核工作流**: 内容发布审核流程
3. **版本控制**: 内容修改历史和回滚
4. **数据分析**: 访问统计和内容分析
5. **API 对外开放**: RESTful API 供第三方使用
6. **多语言支持**: 后台界面多语言切换

### 10.3 预期成果
- **开发时间**: 5-6 周完成全部功能
- **代码质量**: 符合 PEP 8 规范，类型提示完整
- **文档完整**: 开发文档 + 使用手册 + API 文档
- **可维护性**: 模块化设计，易于维护和扩展
- **用户友好**: 直观易用的管理界面

---

**文档结束**

如有任何问题或需要进一步讨论的地方，请随时联系。