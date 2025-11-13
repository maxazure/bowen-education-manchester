# TODO - 模块 10: 留言管理

**模块**: Contact Management  
**开始时间**: 待定  
**完成时间**: 待定  
**负责人**: 10_contact_management subagent

---

## 🔄 进行中

暂无

---

## ✅ 已完成

暂无

---

## 📋 待办事项

### Phase 1: 编写测试 (TDD - Red)

- [ ] 创建测试文件 `tests/admin/test_contact_query.py`
  - [ ] test_get_list
  - [ ] test_filter_by_status
  - [ ] test_keyword_search
  - [ ] test_pagination
- [ ] 创建测试文件 `tests/admin/test_contact_status.py`
  - [ ] test_mark_as_read
  - [ ] test_mark_as_replied
  - [ ] test_mark_as_archived
  - [ ] test_batch_mark
- [ ] 创建测试文件 `tests/admin/test_contact_export.py`
  - [ ] test_export_csv
  - [ ] test_export_fields_completeness
- [ ] 运行测试验证失败

### Phase 2: 实现服务层 (TDD - Green)

- [ ] 创建服务文件
- [ ] 实现核心业务逻辑
- [ ] 添加类型提示和文档字符串

### Phase 3: 创建路由 (TDD - Green)

- [ ] 实现 GET /admin/contacts - 列表页
- [ ] 实现 GET /admin/contacts/{id} - 详情(AJAX)
- [ ] 实现 PUT /admin/contacts/{id}/status - 更新状态(AJAX)
- [ ] 实现 DELETE /admin/contacts/{id} - 删除
- [ ] 实现 GET /admin/contacts/export - 导出CSV

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
- [ ] 验证 10 个测试全部通过
- [ ] 查看测试覆盖率
- [ ] 确认覆盖率 >= 85%

### Phase 7: 代码质量检查 (TDD - Refactor)

- [ ] 运行 Black 格式化
- [ ] 运行 isort 排序
- [ ] 运行 mypy 类型检查
- [ ] 运行 ruff 代码检查
- [ ] 修复所有警告

### Phase 8: 手动测试

- [ ] 测试留言查询
- [ ] 测试状态管理
- [ ] 测试筛选搜索
- [ ] 测试批量操作
- [ ] 测试CSV 导出
- [ ] 测试留言详情

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
- [ ] 留言查询功能完整
- [ ] 状态管理功能完整
- [ ] 筛选搜索功能完整
- [ ] 批量操作功能完整
- [ ] CSV 导出功能完整
- [ ] 留言详情功能完整

### 测试覆盖
- [ ] 10 个测试全部通过
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

- 留言查询是核心功能
- 状态管理是核心功能
- 筛选搜索是核心功能

---

## ❓ 问题与解决

暂无

---

**最后更新**: 2025-11-13  
**状态**: 待开始
