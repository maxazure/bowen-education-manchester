# TODO - 模块 06: 文章管理

**模块**: Post Management  
**开始时间**: 待定  
**完成时间**: 待定  
**负责人**: 06_post_management subagent

---

## 🔄 进行中

暂无

---

## ✅ 已完成

暂无

---

## 📋 待办事项

### Phase 1: 编写测试 (TDD - Red)

- [ ] 创建测试文件 `tests/admin/test_post_crud.py`
  - [ ] test_create_post
  - [ ] test_set_column
  - [ ] test_set_categories
  - [ ] test_set_cover
  - [ ] test_update_post
  - [ ] test_delete_post
- [ ] 创建测试文件 `tests/admin/test_post_filter.py`
  - [ ] test_filter_by_column
  - [ ] test_filter_by_category
  - [ ] test_filter_by_status
  - [ ] test_keyword_search
  - [ ] test_pagination
- [ ] 创建测试文件 `tests/admin/test_post_publish.py`
  - [ ] test_publish
  - [ ] test_unpublish
  - [ ] test_recommend
  - [ ] test_pin
- [ ] 运行测试验证失败

### Phase 2: 实现服务层 (TDD - Green)

- [ ] 创建服务文件
- [ ] 实现核心业务逻辑
- [ ] 添加类型提示和文档字符串

### Phase 3: 创建路由 (TDD - Green)

- [ ] 实现 GET /admin/posts - 列表页(支持筛选)
- [ ] 实现 GET /admin/posts/new - 新建页
- [ ] 实现 POST /admin/posts - 创建
- [ ] 实现 GET /admin/posts/{id}/edit - 编辑页
- [ ] 实现 PUT /admin/posts/{id} - 更新
- [ ] 实现 DELETE /admin/posts/{id} - 删除
- [ ] 实现 POST /admin/posts/{id}/publish - 发布/取消发布

### Phase 4: 创建模板

- [ ] 创建模板目录
- [ ] 创建列表页模板
- [ ] 创建表单页模板
- [ ] 创建详情页模板 (如需要)

### Phase 5: 创建前端脚本

- [ ] 创建 JavaScript 文件
- [ ] 实现数据绑定
- [ ] 实现 AJAX 请求
- [ ] 添加交互动画

### Phase 6: 运行测试验证 (TDD - Green)

- [ ] 运行所有测试
- [ ] 验证 15 个测试全部通过
- [ ] 查看测试覆盖率
- [ ] 确认覆盖率 >= 85%

### Phase 7: 代码质量检查 (TDD - Refactor)

- [ ] 运行 Black 格式化
- [ ] 运行 isort 排序
- [ ] 运行 mypy 类型检查
- [ ] 运行 ruff 代码检查
- [ ] 修复所有警告

### Phase 8: 手动测试

- [ ] 测试文章 CRUD
- [ ] 测试Markdown 编辑器
- [ ] 测试封面图设置
- [ ] 测试分类多选
- [ ] 测试推荐/置顶
- [ ] 测试高级筛选

### Phase 9: 文档与提交

- [ ] 更新本 TODO.md
- [ ] 截图功能演示
- [ ] 创建 Git commit
- [ ] 验证所有文件已提交

---

## 📊 任务统计

- **总任务数**: 60+
- **已完成**: 0
- **进行中**: 0
- **待办**: 60+
- **完成率**: 0%

---

## ✅ 完成标准检查清单

### 功能完整性
- [ ] 文章 CRUD功能完整
- [ ] Markdown 编辑器功能完整
- [ ] 封面图设置功能完整
- [ ] 分类多选功能完整
- [ ] 推荐/置顶功能完整
- [ ] 高级筛选功能完整

### 测试覆盖
- [ ] 15 个测试全部通过
- [ ] 测试覆盖率 >= 85%

### 代码质量
- [ ] Black 格式化通过
- [ ] isort 排序通过
- [ ] mypy 类型检查通过
- [ ] ruff 代码检查通过

### 用户体验
- [ ] 界面直观易用
- [ ] 操作流畅
- [ ] 错误提示清晰
- [ ] 响应速度快

---

## 📝 备注

- 文章 CRUD是核心功能
- Markdown 编辑器是核心功能
- 封面图设置是核心功能

---

## ❓ 问题与解决

暂无

---

**最后更新**: 2025-11-13  
**状态**: 待开始
