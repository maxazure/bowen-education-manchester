# 博文教育管理后台开发计划

**制定时间**: 2025-11-13
**开发模式**: TDD (测试驱动开发)
**预计总工期**: 6 周

---

## 开发原则

### 1. TDD 开发流程
对于每个模块,严格遵循以下步骤:
1. **Red (红)**: 先写测试,运行失败 (因为功能还未实现)
2. **Green (绿)**: 编写最小代码使测试通过
3. **Refactor (重构)**: 优化代码,保持测试通过

### 2. 测试覆盖率要求
- 单元测试覆盖率 ≥ 80%
- 关键业务逻辑覆盖率 = 100%
- API 接口全覆盖

### 3. 代码质量要求
- 遵循 PEP 8 规范
- 使用 Black 格式化代码
- 使用 mypy 进行类型检查
- 所有函数必须有类型提示
- 关键逻辑必须有注释

---

## 模块依赖关系图

```
用户管理 (无依赖)
    ↓
媒体库管理 (依赖: 用户管理)
    ↓
栏目管理 (依赖: 用户管理)
    ↓
单页管理 (依赖: 媒体库, 栏目管理)
文章管理 (依赖: 媒体库, 栏目管理)
产品管理 (依赖: 媒体库, 栏目管理)
相册管理 (依赖: 媒体库, 栏目管理)
    ↓
站点设置 (依赖: 媒体库)
留言管理 (无特殊依赖)
```

---

## Week 1: 基础框架与用户管理

### Day 1-2: 项目基础设施 (基础模块)

#### Subagent 任务: infrastructure-setup
**任务描述**: 搭建管理后台基础架构

**开发任务**:
1. 创建项目目录结构
   ```
   app/admin/
   ├── __init__.py
   ├── routers/
   ├── middleware.py
   ├── dependencies.py
   └── utils.py
   templates/admin/
   ├── base.html
   ├── components/
   static/admin/
   ├── css/
   ├── js/
   tests/admin/
   ```

2. 配置依赖包 (更新 requirements.txt)
   - bcrypt==4.1.2
   - itsdangerous==2.1.2
   - Pillow==10.2.0
   - mistune==3.0.2
   - python-slugify==8.0.1 (已有)

3. 配置测试环境
   - pytest==8.0.0
   - pytest-asyncio==0.23.0
   - pytest-cov==4.1.0
   - httpx==0.26.0 (用于测试 FastAPI)

**TDD 测试用例**:
- ✅ 测试项目结构创建
- ✅ 测试依赖包安装
- ✅ 测试 pytest 配置

**完成标准**:
- 所有目录结构创建完成
- 依赖包安装成功
- pytest 运行正常

---

### Day 3-4: 用户管理模块 (模块1)

#### Subagent 任务: user-management-tdd
**任务描述**: 开发管理员认证系统 (TDD)

**数据库设计**:
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
```

**TDD 测试用例** (先写这些测试):

1. 模型测试 (`tests/admin/test_admin_user_model.py`)
   - ✅ 测试创建管理员用户
   - ✅ 测试用户名唯一性约束
   - ✅ 测试邮箱唯一性约束
   - ✅ 测试密码哈希存储
   - ✅ 测试密码验证成功
   - ✅ 测试密码验证失败
   - ✅ 测试 `set_password()` 方法
   - ✅ 测试 `verify_password()` 方法

2. 认证中间件测试 (`tests/admin/test_auth_middleware.py`)
   - ✅ 测试未登录访问管理页面重定向到登录页
   - ✅ 测试已登录访问管理页面正常
   - ✅ 测试访问公开路径不需要认证
   - ✅ 测试 session 过期处理

3. 登录 API 测试 (`tests/admin/test_auth_routes.py`)
   - ✅ 测试登录页面渲染
   - ✅ 测试正确凭据登录成功
   - ✅ 测试错误用户名登录失败
   - ✅ 测试错误密码登录失败
   - ✅ 测试登录后创建 session
   - ✅ 测试登出清除 session

**开发任务** (测试通过后编写):
1. 创建 `app/models/admin_user.py`
2. 创建数据库迁移
3. 创建 `app/admin/middleware.py`
4. 创建 `app/admin/routers/auth.py`
5. 创建登录模板 `templates/admin/login.html`
6. 创建初始化脚本 `scripts/init_admin.py`

**完成标准**:
- 所有测试通过 (12+ 测试用例)
- 测试覆盖率 ≥ 90%
- 可以登录管理后台
- Session 管理正常工作

---

## Week 1-2: 媒体库管理

### Day 5-7: 媒体库模块 (模块2)

#### Subagent 任务: media-library-tdd
**任务描述**: 开发媒体文件上传和管理系统 (TDD)

**数据库扩展**:
```sql
ALTER TABLE media_file ADD COLUMN thumbnail_url VARCHAR(500);
ALTER TABLE media_file ADD COLUMN usage_count INTEGER DEFAULT 0;
```

**TDD 测试用例** (先写):

1. 文件上传测试 (`tests/admin/test_media_upload.py`)
   - ✅ 测试上传 JPG 图片成功
   - ✅ 测试上传 PNG 图片成功
   - ✅ 测试上传不支持格式失败
   - ✅ 测试上传超大文件失败 (>5MB)
   - ✅ 测试生成缩略图
   - ✅ 测试文件名清洗 (移除特殊字符)
   - ✅ 测试重复文件名处理

2. 媒体查询测试 (`tests/admin/test_media_query.py`)
   - ✅ 测试获取媒体列表 (分页)
   - ✅ 测试按类型筛选
   - ✅ 测试按文件名搜索
   - ✅ 测试获取单个媒体详情
   - ✅ 测试媒体不存在返回 404

3. 媒体更新测试 (`tests/admin/test_media_update.py`)
   - ✅ 测试更新媒体标题
   - ✅ 测试更新 Alt 文本
   - ✅ 测试更新说明

4. 媒体删除测试 (`tests/admin/test_media_delete.py`)
   - ✅ 测试删除未使用的媒体成功
   - ✅ 测试删除被引用的媒体失败
   - ✅ 测试删除时清理文件

**开发任务**:
1. 扩展 `app/models/media.py` 模型
2. 创建 `app/admin/routers/media.py`
3. 实现文件上传功能 (Pillow 生成缩略图)
4. 实现媒体 CRUD API
5. 创建媒体列表模板
6. 创建媒体选择器组件 `templates/admin/components/media_picker.html`
7. 创建前端 JS `static/admin/js/media-picker.js`

**完成标准**:
- 所有测试通过 (15+ 测试用例)
- 测试覆盖率 ≥ 85%
- 可以上传、查看、编辑、删除图片
- 媒体选择器组件可复用

---

## Week 2: 栏目管理与单页管理

### Day 1-3: 栏目管理 (模块3)

#### Subagent 任务: column-management-tdd
**任务描述**: 开发栏目管理系统 (TDD)

**TDD 测试用例**:

1. 栏目 CRUD 测试 (`tests/admin/test_column_crud.py`)
   - ✅ 测试创建栏目
   - ✅ 测试 Slug 自动生成
   - ✅ 测试 Slug 唯一性约束
   - ✅ 测试更新栏目基本信息
   - ✅ 测试更新 Hero 配置
   - ✅ 测试删除空栏目成功
   - ✅ 测试删除包含内容的栏目失败

2. 栏目排序测试 (`tests/admin/test_column_sorting.py`)
   - ✅ 测试手动设置排序值
   - ✅ 测试批量更新排序
   - ✅ 测试父子栏目排序

3. 栏目查询测试 (`tests/admin/test_column_query.py`)
   - ✅ 测试获取树形结构
   - ✅ 测试筛选启用的栏目
   - ✅ 测试筛选导航显示的栏目

**开发任务**:
1. 创建 `app/admin/routers/columns.py`
2. 创建栏目列表模板 (树形结构)
3. 创建栏目编辑表单
4. 实现拖拽排序 (SortableJS)

**完成标准**:
- 所有测试通过 (12+ 测试用例)
- 树形结构显示正常
- 拖拽排序功能正常

---

### Day 4-7: 单页管理 (模块4)

#### Subagent 任务: single-page-management-tdd
**任务描述**: 开发单页内容管理系统 (TDD)

**数据库扩展**:
```sql
ALTER TABLE single_page ADD COLUMN content_markdown TEXT;
```

**TDD 测试用例**:

1. Markdown 转换测试 (`tests/admin/test_markdown_convert.py`)
   - ✅ 测试基本 Markdown 转 HTML
   - ✅ 测试代码高亮
   - ✅ 测试 XSS 防护
   - ✅ 测试图片链接转换

2. 单页 CRUD 测试 (`tests/admin/test_single_page_crud.py`)
   - ✅ 测试创建单页
   - ✅ 测试保存草稿
   - ✅ 测试发布单页
   - ✅ 测试取消发布
   - ✅ 测试更新内容
   - ✅ 测试删除单页

3. SEO 配置测试 (`tests/admin/test_single_page_seo.py`)
   - ✅ 测试设置 Meta 描述
   - ✅ 测试设置 Meta 关键词

**开发任务**:
1. 扩展 `app/models/site.py` (SinglePage)
2. 创建 `app/admin/routers/pages.py`
3. 集成 EasyMDE 编辑器
4. 实现 Markdown 到 HTML 转换 (mistune)
5. 创建单页列表模板
6. 创建单页编辑模板

**完成标准**:
- 所有测试通过 (12+ 测试用例)
- Markdown 编辑器正常工作
- 实时预览功能正常
- 可以插入媒体库图片

---

## Week 3: 文章管理与站点设置

### Day 1-4: 文章管理 (模块5)

#### Subagent 任务: post-management-tdd
**任务描述**: 开发文章管理系统 (TDD)

**TDD 测试用例**:

1. 文章 CRUD 测试 (`tests/admin/test_post_crud.py`)
   - ✅ 测试创建文章
   - ✅ 测试设置栏目
   - ✅ 测试设置分类 (多选)
   - ✅ 测试设置封面图
   - ✅ 测试更新文章
   - ✅ 测试删除文章

2. 文章筛选测试 (`tests/admin/test_post_filter.py`)
   - ✅ 测试按栏目筛选
   - ✅ 测试按分类筛选
   - ✅ 测试按状态筛选
   - ✅ 测试关键词搜索
   - ✅ 测试分页功能

3. 文章发布测试 (`tests/admin/test_post_publish.py`)
   - ✅ 测试发布文章
   - ✅ 测试取消发布
   - ✅ 测试推荐标记
   - ✅ 测试置顶标记
   - ✅ 测试定时发布 (可选)

**开发任务**:
1. 扩展 `app/models/post.py`
2. 创建 `app/admin/routers/posts.py`
3. 创建文章列表模板 (Alpine.js)
4. 创建文章编辑模板
5. 实现高级筛选功能

**完成标准**:
- 所有测试通过 (15+ 测试用例)
- 筛选和搜索功能正常
- 批量操作功能正常

---

### Day 5-7: 站点设置 (模块6)

#### Subagent 任务: site-settings-tdd
**任务描述**: 开发站点设置管理 (TDD)

**TDD 测试用例**:

1. 设置存储测试 (`tests/admin/test_site_settings.py`)
   - ✅ 测试保存基本信息
   - ✅ 测试保存联系方式
   - ✅ 测试保存社交媒体
   - ✅ 测试保存高级设置
   - ✅ 测试键值对存储

2. 设置读取测试 (`tests/admin/test_settings_read.py`)
   - ✅ 测试读取单个设置
   - ✅ 测试读取设置组
   - ✅ 测试默认值处理

**开发任务**:
1. 创建 `app/admin/routers/settings.py`
2. 创建设置页面模板 (分组表单)
3. 实现 Logo 上传

**完成标准**:
- 所有测试通过 (8+ 测试用例)
- 设置保存和读取正常

---

## Week 4: 产品管理

### Day 1-4: 产品管理 (模块7)

#### Subagent 任务: product-management-tdd
**任务描述**: 开发产品/课程管理系统 (TDD)

**TDD 测试用例**:

1. 产品 CRUD 测试 (`tests/admin/test_product_crud.py`)
   - ✅ 测试创建产品
   - ✅ 测试设置价格
   - ✅ 测试设置属性
   - ✅ 测试更新产品
   - ✅ 测试删除产品

2. 产品分类测试 (`tests/admin/test_product_category.py`)
   - ✅ 测试创建分类
   - ✅ 测试关联产品
   - ✅ 测试多选分类

**开发任务**:
1. 创建 `app/admin/routers/products.py`
2. 创建产品列表模板
3. 创建产品编辑表单

**完成标准**:
- 所有测试通过 (10+ 测试用例)
- 产品管理功能完整

---

## Week 4-5: 相册管理与留言管理

### Day 1-3: 相册管理 (模块8)

#### Subagent 任务: gallery-management-tdd
**任务描述**: 开发相册管理系统 (TDD)

**TDD 测试用例**:

1. 相册 CRUD 测试 (`tests/admin/test_gallery_crud.py`)
   - ✅ 测试创建相册
   - ✅ 测试批量添加图片
   - ✅ 测试更新相册
   - ✅ 测试删除相册

2. 图片排序测试 (`tests/admin/test_gallery_sorting.py`)
   - ✅ 测试拖拽排序
   - ✅ 测试批量更新排序

3. 图片元数据测试 (`tests/admin/test_gallery_metadata.py`)
   - ✅ 测试设置图片标题
   - ✅ 测试设置图片说明
   - ✅ 测试显示/隐藏控制

**开发任务**:
1. 创建 `app/admin/routers/galleries.py`
2. 创建相册列表模板
3. 创建相册编辑模板 (拖拽排序)

**完成标准**:
- 所有测试通过 (10+ 测试用例)
- 拖拽排序功能正常

---

### Day 4-7: 留言管理 (模块9)

#### Subagent 任务: contact-management-tdd
**任务描述**: 开发留言管理系统 (TDD)

**TDD 测试用例**:

1. 留言查询测试 (`tests/admin/test_contact_query.py`)
   - ✅ 测试获取留言列表
   - ✅ 测试按状态筛选
   - ✅ 测试关键词搜索
   - ✅ 测试分页

2. 留言状态测试 (`tests/admin/test_contact_status.py`)
   - ✅ 测试标记为已读
   - ✅ 测试标记为已回复
   - ✅ 测试标记为已归档
   - ✅ 测试批量标记

3. 留言导出测试 (`tests/admin/test_contact_export.py`)
   - ✅ 测试导出 CSV
   - ✅ 测试导出字段完整性

**开发任务**:
1. 创建 `app/admin/routers/contacts.py`
2. 创建留言列表模板
3. 实现 CSV 导出功能

**完成标准**:
- 所有测试通过 (10+ 测试用例)
- CSV 导出功能正常

---

## Week 6: 集成测试与优化

### Day 1-2: 系统集成测试

**测试任务**:
1. 端到端测试
2. 性能测试
3. 安全测试
4. 兼容性测试

### Day 3-4: 性能优化

**优化任务**:
1. 数据库查询优化
2. 图片加载优化
3. JavaScript 优化
4. 添加加载动画

### Day 5-7: 文档与部署

**文档任务**:
1. 编写管理员使用手册
2. 编写开发文档
3. 编写 API 文档
4. 准备部署方案

---

## 测试命令

```bash
# 运行所有测试
pytest tests/admin/

# 运行特定模块测试
pytest tests/admin/test_admin_user_model.py

# 运行测试并显示覆盖率
pytest tests/admin/ --cov=app/admin --cov-report=html

# 运行测试并显示详细输出
pytest tests/admin/ -v

# 运行失败的测试
pytest tests/admin/ --lf

# 运行特定测试
pytest tests/admin/test_auth_routes.py::test_login_success
```

---

## 质量检查命令

```bash
# 代码格式化
black app/admin/
isort app/admin/

# 类型检查
mypy app/admin/

# 代码规范检查
ruff check app/admin/
```

---

## 总结

这份开发计划确保:
1. ✅ 严格遵循 TDD 原则
2. ✅ 每个模块都有完整的测试覆盖
3. ✅ 按依赖关系有序开发
4. ✅ 测试先行,代码后写
5. ✅ 持续重构,保持代码质量
6. ✅ 每个阶段都有明确的完成标准

**预期成果**:
- 9 个功能模块全部完成
- 100+ 测试用例
- 测试覆盖率 ≥ 85%
- 代码质量符合规范
- 文档完整齐全
