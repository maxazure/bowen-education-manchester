# 模块 03: 媒体库管理

**模块编号**: 03  
**模块名称**: Media Library Management  
**优先级**: P0 (最高)  
**预计工时**: 3 天  
**负责 Subagent**: media-library-tdd  
**依赖**: 模块 01 (Infrastructure Setup), 模块 02 (User Management)

---

## 📋 任务概述

开发媒体文件上传和管理系统,支持图片上传、缩略图生成、媒体列表展示、媒体选择器组件等功能。

---

## 🎯 任务目标

1. ✅ 实现文件上传功能(支持多种图片格式)
2. ✅ 实现缩略图自动生成
3. ✅ 实现媒体文件 CRUD 操作
4. ✅ 实现媒体选择器组件(供其他模块使用)
5. ✅ 实现文件删除保护(检查引用)
6. ✅ 实现媒体搜索和筛选

---

## 💾 数据库设计

### media_file 表(已存在,需扩展)

```sql
-- 已有字段
-- id, file_name, file_path, file_url, file_type, file_size, 
-- mime_type, width, height, created_at, updated_at

-- 需要添加的字段
ALTER TABLE media_file ADD COLUMN thumbnail_url VARCHAR(500);
ALTER TABLE media_file ADD COLUMN usage_count INTEGER DEFAULT 0;
ALTER TABLE media_file ADD COLUMN title VARCHAR(255);
ALTER TABLE media_file ADD COLUMN alt_text VARCHAR(255);
ALTER TABLE media_file ADD COLUMN caption TEXT;
```

**新增字段说明**:
- `thumbnail_url`: 缩略图URL(用于列表展示)
- `usage_count`: 使用次数(被引用次数)
- `title`: 媒体标题
- `alt_text`: 图片 Alt 文本(SEO)
- `caption`: 说明文字

---

## ✅ TDD 测试用例

### 测试文件 1: `tests/admin/test_media_upload.py`

#### 类: TestMediaUpload

```python
def test_upload_jpg_image():
    """测试上传 JPG 图片成功"""
    # 创建测试图片文件
    # POST /admin/media/upload
    # 验证返回 201
    # 验证文件保存到磁盘
    # 验证数据库记录创建

def test_upload_png_image():
    """测试上传 PNG 图片成功"""
    # 类似 test_upload_jpg_image

def test_upload_gif_image():
    """测试上传 GIF 图片成功"""
    # 类似 test_upload_jpg_image

def test_upload_webp_image():
    """测试上传 WebP 图片成功"""
    # 类似 test_upload_jpg_image

def test_upload_unsupported_format():
    """测试上传不支持格式失败"""
    # 上传 .exe 文件
    # 验证返回 400
    # 验证错误消息

def test_upload_oversized_file():
    """测试上传超大文件失败 (>5MB)"""
    # 创建 6MB 的测试图片
    # POST /admin/media/upload
    # 验证返回 400
    # 验证错误消息

def test_thumbnail_generation():
    """测试生成缩略图"""
    # 上传图片
    # 验证 thumbnail_url 不为空
    # 验证缩略图文件存在
    # 验证缩略图尺寸正确(300x300)

def test_filename_sanitization():
    """测试文件名清洗(移除特殊字符)"""
    # 上传文件名包含特殊字符的图片
    # 验证保存的文件名安全
    # 验证没有路径遍历风险

def test_duplicate_filename_handling():
    """测试重复文件名处理"""
    # 上传同名文件两次
    # 验证第二次文件名自动添加后缀
    # 验证两个文件都保存成功
```

**测试统计**: 9 个测试用例

---

### 测试文件 2: `tests/admin/test_media_query.py`

#### 类: TestMediaQuery

```python
def test_get_media_list():
    """测试获取媒体列表"""
    # 创建多个测试媒体
    # GET /admin/media
    # 验证返回列表
    # 验证分页信息

def test_media_list_pagination():
    """测试媒体列表分页"""
    # 创建 25 个媒体
    # GET /admin/media?page=1&per_page=20
    # 验证返回 20 条
    # GET /admin/media?page=2&per_page=20
    # 验证返回 5 条

def test_filter_by_type():
    """测试按类型筛选"""
    # 创建图片和文档
    # GET /admin/media?type=image
    # 验证只返回图片

def test_search_by_filename():
    """测试按文件名搜索"""
    # 创建多个媒体
    # GET /admin/media?search=logo
    # 验证只返回文件名包含 logo 的媒体

def test_get_single_media():
    """测试获取单个媒体详情"""
    # 创建媒体
    # GET /admin/media/{id}
    # 验证返回完整信息

def test_get_nonexistent_media():
    """测试获取不存在的媒体返回 404"""
    # GET /admin/media/99999
    # 验证返回 404
```

**测试统计**: 6 个测试用例

---

### 测试文件 3: `tests/admin/test_media_update.py`

#### 类: TestMediaUpdate

```python
def test_update_media_title():
    """测试更新媒体标题"""
    # 创建媒体
    # PUT /admin/media/{id} {title: "new title"}
    # 验证更新成功

def test_update_media_alt_text():
    """测试更新 Alt 文本"""
    # 创建媒体
    # PUT /admin/media/{id} {alt_text: "alt"}
    # 验证更新成功

def test_update_media_caption():
    """测试更新说明"""
    # 创建媒体
    # PUT /admin/media/{id} {caption: "caption"}
    # 验证更新成功

def test_update_all_metadata():
    """测试更新所有元数据"""
    # 创建媒体
    # PUT /admin/media/{id} {title, alt_text, caption}
    # 验证全部更新成功
```

**测试统计**: 4 个测试用例

---

### 测试文件 4: `tests/admin/test_media_delete.py`

#### 类: TestMediaDelete

```python
def test_delete_unused_media():
    """测试删除未使用的媒体成功"""
    # 创建媒体(usage_count=0)
    # DELETE /admin/media/{id}
    # 验证返回 204
    # 验证文件被删除
    # 验证数据库记录被删除

def test_delete_used_media_fails():
    """测试删除被引用的媒体失败"""
    # 创建媒体(usage_count>0)
    # DELETE /admin/media/{id}
    # 验证返回 400
    # 验证错误消息
    # 验证文件未被删除

def test_delete_with_file_cleanup():
    """测试删除时清理文件"""
    # 创建媒体
    # 记录文件路径
    # DELETE /admin/media/{id}
    # 验证原图和缩略图都被删除

def test_delete_nonexistent_media():
    """测试删除不存在的媒体"""
    # DELETE /admin/media/99999
    # 验证返回 404
```

**测试统计**: 4 个测试用例

---

## 总测试统计

- **测试文件**: 4 个
- **测试类**: 4 个  
- **测试用例**: 23 个
- **预期全部通过**

---

## 📝 开发步骤（TDD）

### Step 1: 编写测试 (Red)

```bash
# 创建测试文件
touch tests/admin/test_media_upload.py
touch tests/admin/test_media_query.py
touch tests/admin/test_media_update.py
touch tests/admin/test_media_delete.py

# 编写所有测试用例

# 运行测试（预期失败）
pytest tests/admin/test_media_*.py -v
```

### Step 2: 扩展数据模型 (Green)

```bash
# 编辑 app/models/media.py
# 添加新字段: thumbnail_url, usage_count, title, alt_text, caption
```

### Step 3: 创建数据库迁移

```bash
alembic revision --autogenerate -m "add media metadata fields"
alembic upgrade head
```

### Step 4: 实现文件上传 (Green)

```bash
# 创建 app/admin/routers/media.py
# 实现 POST /admin/media/upload
# - 验证文件类型
# - 验证文件大小
# - 清洗文件名
# - 保存原图
# - 生成缩略图(PIL)
# - 创建数据库记录
```

### Step 5: 实现媒体查询 (Green)

```bash
# 实现 GET /admin/media (列表,支持分页、筛选、搜索)
# 实现 GET /admin/media/{id} (详情)
```

### Step 6: 实现媒体更新 (Green)

```bash
# 实现 PUT /admin/media/{id}
# - 更新 title, alt_text, caption
```

### Step 7: 实现媒体删除 (Green)

```bash
# 实现 DELETE /admin/media/{id}
# - 检查 usage_count
# - 删除文件
# - 删除数据库记录
```

### Step 8: 创建媒体选择器组件

```bash
# 创建 templates/admin/components/media_picker.html
# 创建 static/admin/js/media-picker.js
# - 模态框UI
# - 上传功能
# - 搜索和筛选
# - 图片选择
# - 事件触发
```

### Step 9: 创建媒体管理页面

```bash
# 创建 templates/admin/media/list.html
# - 网格布局
# - 搜索框
# - 类型筛选
# - 分页器
# - 详情侧边栏
```

### Step 10: 运行测试验证 (Green)

```bash
pytest tests/admin/test_media_*.py -v
pytest tests/admin/test_media_*.py --cov=app/admin/routers/media --cov-report=html
```

### Step 11: 重构和优化 (Refactor)

```bash
black app/admin/routers/media.py app/models/media.py
isort app/admin/routers/media.py app/models/media.py
mypy app/admin/routers/media.py
ruff check app/admin/routers/media.py
```

---

## ✅ 完成标准

### 功能性要求

- [ ] 文件上传功能正常
- [ ] 支持 JPG、PNG、GIF、WebP 格式
- [ ] 自动生成缩略图
- [ ] 媒体列表显示正常
- [ ] 分页功能正常
- [ ] 搜索和筛选功能正常
- [ ] 媒体详情显示正常
- [ ] 媒体元数据更新正常
- [ ] 删除保护功能正常
- [ ] 媒体选择器组件可用
- [ ] 所有测试通过 (23/23)

### 质量要求

- [ ] 代码符合 PEP 8 规范
- [ ] 所有函数有类型提示
- [ ] 所有函数有文档字符串
- [ ] 测试覆盖率 >= 85%

### 安全要求

- [ ] 文件类型验证有效
- [ ] 文件大小限制有效
- [ ] 文件名清洗有效
- [ ] 无路径遍历漏洞
- [ ] 删除检查引用

### 文档要求

- [ ] 更新 TODO.md
- [ ] 所有代码有注释
- [ ] API 文档完整

---

## 📊 验证命令

```bash
# 1. 数据库迁移
alembic revision --autogenerate -m "add media metadata fields"
alembic upgrade head

# 2. 运行测试
pytest tests/admin/test_media_*.py -v

# 3. 查看覆盖率
pytest tests/admin/test_media_*.py --cov=app/admin/routers/media --cov-report=term-missing

# 4. 代码质量检查
black app/admin/routers/media.py --check
mypy app/admin/routers/media.py

# 5. 启动服务器测试
uvicorn main:app --reload
# 访问 http://localhost:8000/admin/media
```

---

## 🔄 交付物

1. ✅ 扩展的 MediaFile 模型
2. ✅ 文件上传路由
3. ✅ 媒体 CRUD 路由
4. ✅ 媒体选择器组件(HTML+JS)
5. ✅ 媒体管理页面
6. ✅ 23 个通过的测试用例
7. ✅ 更新的 TODO.md

---

## 📝 注意事项

1. **文件存储**: 上传文件存储在 `uploads/images/` 目录
2. **缩略图**: 存储在 `uploads/thumbnails/` 目录
3. **文件命名**: 使用时间戳+原文件名避免冲突
4. **权限检查**: 上传和删除需要认证
5. **错误处理**: 上传失败要回滚数据库操作

---

## 🔗 相关文档

- [admin-system-design.md](../../admin-system-design.md) - 系统设计文档 (第 65-99 行)
- [admin-development-plan.md](../../admin-development-plan.md) - Week 1-2: 媒体库管理
- [TODO.md](./TODO.md) - 本模块待办事项
- [模块 02](../02-user-management/TASK.md) - 依赖的用户管理模块
