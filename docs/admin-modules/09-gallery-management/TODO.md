# TODO - 模块 09: 相册管理

**模块**: Gallery Management  
**开始时间**: 待定  
**完成时间**: 待定  
**负责人**: 09_gallery_management subagent

---

## 🔄 进行中

暂无

---

## ✅ 已完成

暂无

---

## 📋 待办事项

### Phase 1: 编写测试 (TDD - Red)

- [ ] 创建测试文件 `tests/admin/test_gallery_crud.py`
  - [ ] test_create_gallery
  - [ ] test_batch_add_images
  - [ ] test_update_gallery
  - [ ] test_delete_gallery
- [ ] 创建测试文件 `tests/admin/test_gallery_sorting.py`
  - [ ] test_drag_sort
  - [ ] test_batch_update_order
- [ ] 创建测试文件 `tests/admin/test_gallery_metadata.py`
  - [ ] test_set_image_title
  - [ ] test_set_image_caption
  - [ ] test_toggle_visibility
  - [ ] test_set_cover_image
- [ ] 运行测试验证失败

### Phase 2: 实现服务层 (TDD - Green)

- [ ] 创建服务文件
- [ ] 实现核心业务逻辑
- [ ] 添加类型提示和文档字符串

### Phase 3: 创建路由 (TDD - Green)

- [ ] 实现 GET /admin/galleries - 列表页
- [ ] 实现 GET /admin/galleries/new - 新建页
- [ ] 实现 POST /admin/galleries - 创建
- [ ] 实现 GET /admin/galleries/{id}/edit - 编辑页
- [ ] 实现 PUT /admin/galleries/{id} - 更新
- [ ] 实现 DELETE /admin/galleries/{id} - 删除
- [ ] 实现 POST /admin/galleries/{id}/images - 添加图片
- [ ] 实现 DELETE /admin/galleries/{id}/images/{image_id} - 删除图片
- [ ] 实现 POST /admin/galleries/{id}/reorder - 图片排序

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

- [ ] 测试相册 CRUD
- [ ] 测试批量上传
- [ ] 测试拖拽排序
- [ ] 测试图片元数据
- [ ] 测试封面图设置
- [ ] 测试显示/隐藏控制

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
- [ ] 相册 CRUD功能完整
- [ ] 批量上传功能完整
- [ ] 拖拽排序功能完整
- [ ] 图片元数据功能完整
- [ ] 封面图设置功能完整
- [ ] 显示/隐藏控制功能完整

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

- 相册 CRUD是核心功能
- 批量上传是核心功能
- 拖拽排序是核心功能

---

## ❓ 问题与解决

暂无

---

**最后更新**: 2025-11-13  
**状态**: 待开始
