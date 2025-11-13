# 模块 05: 单页管理

**模块编号**: 05
**模块名称**: Single Page Management
**优先级**: P0
**预计工时**: 4 天
**负责 Subagent**: 05_single_page
**依赖**: 模块 02 (用户管理), 模块 03 (媒体库)

---

## 📋 任务概述

实现单页管理系统,包括单页 CRUD、Markdown 编辑器、实时预览、Hero 配置、SEO 设置、草稿/发布等核心功能。

---

## 🎯 任务目标

1. ✅ 实现单页 CRUD功能
2. ✅ 实现Markdown 编辑器功能
3. ✅ 实现实时预览功能
4. ✅ 实现Hero 配置功能
5. ✅ 实现SEO 设置功能
6. ✅ 实现草稿/发布功能

---

## 🗄️ 数据库设计

### 数据库变更

ALTER TABLE single_page ADD COLUMN content_markdown TEXT;

---

## ✅ TDD 测试用例

### 测试文件 1: `tests/admin/test_single_page_crud.py`

```python
def test_create_page()
def test_save_draft()
def test_publish_page()
def test_update_page()
def test_delete_page()
```
### 测试文件 2: `tests/admin/test_markdown_convert.py`

```python
def test_markdown_to_html()
def test_code_highlighting()
def test_xss_防护()
def test_image_links()
```
### 测试文件 3: `tests/admin/test_single_page_seo.py`

```python
def test_set_meta_description()
def test_set_meta_keywords()
def test_slug_generation()
```

**测试统计**: 共 12 个测试用例

---

## 📝 开发步骤（TDD）

### Phase 1: 编写测试 (Red)
- 创建 3 个测试文件
- 编写所有 12 个测试用例
- 运行测试确认失败

### Phase 2-3: 实现功能 (Green)
- 创建路由文件
- 创建服务层
- 实现核心业务逻辑

### Phase 4-5: 创建模板和脚本
- 创建 HTML 模板
- 创建 JavaScript 脚本
- 集成前端组件

### Phase 6: 测试验证 (Green)
- 运行所有测试
- 确认覆盖率 >= 85%

### Phase 7: 重构 (Refactor)
- 代码格式化
- 类型检查
- 优化性能

---

## 📄 API 路由设计

- GET /admin/pages - 列表页
- GET /admin/pages/new - 新建页
- POST /admin/pages - 创建
- GET /admin/pages/{id}/edit - 编辑页
- PUT /admin/pages/{id} - 更新
- DELETE /admin/pages/{id} - 删除
- POST /admin/pages/{id}/publish - 发布/取消发布

---

## ✅ 完成标准

### 功能性要求
- [ ] 单页 CRUD功能正常
- [ ] Markdown 编辑器功能正常
- [ ] 实时预览功能正常
- [ ] Hero 配置功能正常
- [ ] SEO 设置功能正常
- [ ] 草稿/发布功能正常
- [ ] 所有测试通过 (12/12)

### 质量要求
- [ ] 代码符合 PEP 8 规范
- [ ] 所有函数有类型提示
- [ ] 测试覆盖率 >= 85%
- [ ] 无代码质量警告

### 用户体验
- [ ] 界面直观易用
- [ ] 操作流畅
- [ ] 错误提示清晰
- [ ] 响应式设计良好

---

## 📊 验证命令

```bash
# 运行测试
pytest tests/admin/test_single_page_crud*.py -v

# 查看覆盖率
pytest tests/admin/test_single_page_crud*.py --cov=app/admin --cov-report=html

# 代码质量检查
black app/admin/ --check
mypy app/admin/
```

---

## 🔄 交付物

1. ✅ 路由文件（完整 CRUD 或查询功能）
2. ✅ 服务层（业务逻辑）
3. ✅ 模板文件
4. ✅ JavaScript 脚本
5. ✅ 12 个通过的测试用例
6. ✅ 更新的 TODO.md

---

## 📝 注意事项

1. **单页 CRUD**: 确保功能完整且用户友好
2. **Markdown 编辑器**: 确保功能完整且用户友好
3. **实时预览**: 确保功能完整且用户友好

---

## 🔗 相关文档

- [admin-system-design.md](../../admin-system-design.md) - 系统设计文档 (第 138-182 行)
- [admin-development-plan.md](../../admin-development-plan.md) - 总体开发计划
- [TODO.md](./TODO.md) - 本模块待办事项
