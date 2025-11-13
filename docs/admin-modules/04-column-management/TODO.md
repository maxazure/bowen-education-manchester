# TODO - 模块 04: 栏目管理

**模块**: Column Management  
**开始时间**: 待定  
**完成时间**: 待定  
**负责人**: column-management subagent

---

## 🔄 进行中

暂无

---

## ✅ 已完成

暂无

---

## 📋 待办事项

### Phase 1: 编写测试 (TDD - Red)

- [ ] 创建测试文件 `tests/admin/test_column_crud.py`
- [ ] 编写 TestColumnCreate 类 (4个测试)
  - [ ] test_create_basic_column
  - [ ] test_create_column_with_parent
  - [ ] test_slug_auto_generation
  - [ ] test_slug_uniqueness
- [ ] 编写 TestColumnRead 类 (3个测试)
  - [ ] test_get_column_by_id
  - [ ] test_get_column_by_slug
  - [ ] test_get_all_columns
- [ ] 编写 TestColumnUpdate 类 (3个测试)
  - [ ] test_update_basic_info
  - [ ] test_update_hero_config
  - [ ] test_toggle_active_status
- [ ] 编写 TestColumnDelete 类 (2个测试)
  - [ ] test_delete_empty_column
  - [ ] test_cannot_delete_column_with_content
- [ ] 创建 `tests/admin/test_column_sorting.py`
- [ ] 编写 TestColumnSorting 类 (3个测试)
  - [ ] test_default_sort_order
  - [ ] test_manual_sort_order
  - [ ] test_batch_update_sort_order
- [ ] 创建 `tests/admin/test_column_tree.py`
- [ ] 编写 TestColumnTree 类 (3个测试)
  - [ ] test_build_tree_structure
  - [ ] test_get_nav_columns
  - [ ] test_get_footer_columns
- [ ] 运行测试验证失败 `pytest tests/admin/test_column_*.py -v`

### Phase 2: 创建 Service 层 (TDD - Green)

- [ ] 创建 `app/services/column_service.py`
- [ ] 实现 `generate_slug()` 函数
- [ ] 实现 `can_delete_column()` 函数
- [ ] 实现 `build_tree()` 函数
- [ ] 实现 `get_nav_columns()` 函数
- [ ] 实现 `get_footer_columns()` 函数
- [ ] 实现 `get_breadcrumbs()` 函数
- [ ] 添加类型提示和文档字符串

### Phase 3: 创建路由 (TDD - Green)

- [ ] 创建 `app/admin/routers/columns.py`
- [ ] 实现 `GET /admin/columns` (列表页)
- [ ] 实现 `GET /admin/columns/new` (新建页)
- [ ] 实现 `POST /admin/columns` (创建)
- [ ] 实现 `GET /admin/columns/{id}/edit` (编辑页)
- [ ] 实现 `PUT /admin/columns/{id}` (更新)
- [ ] 实现 `DELETE /admin/columns/{id}` (删除)
- [ ] 实现 `POST /admin/columns/reorder` (排序)

### Phase 4: 创建模板

- [ ] 创建目录 `templates/admin/columns/`
- [ ] 创建 `list.html` (列表页)
  - [ ] 顶部操作栏 (新建按钮)
  - [ ] 树形结构展示区域
  - [ ] 栏目卡片 (名称、类型、状态、操作)
  - [ ] 拖拽排序功能区域
- [ ] 创建 `form.html` (表单页)
  - [ ] 基础信息 Tab (名称、Slug、类型、描述)
  - [ ] Hero 配置 Tab (标题、副标题、背景图、CTA)
  - [ ] 高级设置 Tab (父栏目、显示控制、图标)
  - [ ] 保存和取消按钮

### Phase 5: 创建前端脚本

- [ ] 创建 `static/admin/js/columns.js`
- [ ] 实现树形结构渲染
- [ ] 集成 SortableJS 库
- [ ] 实现拖拽排序功能
- [ ] 实现 AJAX 保存排序
- [ ] 实现删除确认对话框
- [ ] 实现启用/禁用切换
- [ ] 添加加载动画

### Phase 6: 注册路由和中间件

- [ ] 在 `app/admin/__init__.py` 注册 columns 路由
- [ ] 在 `main.py` 中挂载路由
- [ ] 测试路由访问权限
- [ ] 更新侧边栏导航链接

### Phase 7: 运行测试验证 (TDD - Green)

- [ ] 运行所有测试 `pytest tests/admin/test_column_*.py -v`
- [ ] 验证 18 个测试全部通过
- [ ] 查看覆盖率 `--cov=app/admin/routers/columns --cov=app/services/column_service --cov-report=html`
- [ ] 确认覆盖率 >= 85%

### Phase 8: 代码质量检查 (TDD - Refactor)

- [ ] 运行 Black 格式化
- [ ] 运行 isort 排序
- [ ] 运行 mypy 类型检查
- [ ] 运行 ruff 代码检查
- [ ] 修复所有警告

### Phase 9: 手动测试

- [ ] 测试创建顶级栏目
- [ ] 测试创建子栏目
- [ ] 测试编辑栏目基本信息
- [ ] 测试编辑 Hero 配置
- [ ] 测试拖拽排序
- [ ] 测试启用/禁用
- [ ] 测试删除空栏目
- [ ] 测试删除包含内容的栏目 (应该失败)
- [ ] 测试树形结构展示
- [ ] 测试导航栏目筛选

### Phase 10: 文档与提交

- [ ] 更新本 TODO.md 标记完成任务
- [ ] 截图功能演示
- [ ] 创建 Git commit
  - 提交信息: "feat: 实现栏目管理系统(树形结构+拖拽排序)"
- [ ] 验证所有文件已提交

---

## 📊 任务统计

- **总任务数**: 75+
- **已完成**: 0
- **进行中**: 0
- **待办**: 75+
- **完成率**: 0%

---

## ✅ 完成标准检查清单

### 功能完整性
- [ ] 栏目 CRUD 功能完整
- [ ] 树形结构显示正常
- [ ] 拖拽排序功能正常
- [ ] Hero 配置功能正常
- [ ] 启用/禁用控制正常
- [ ] 导航显示控制正常
- [ ] 底部显示控制正常
- [ ] Slug 自动生成正常
- [ ] 删除保护机制正常

### 测试覆盖
- [ ] 18 个测试全部通过
- [ ] 测试覆盖率 >= 85%
- [ ] 无失败的测试

### 代码质量
- [ ] Black 格式化通过
- [ ] isort 排序通过
- [ ] mypy 类型检查通过
- [ ] ruff 代码检查通过
- [ ] 无代码质量警告

### 用户体验
- [ ] 界面直观易用
- [ ] 拖拽操作流畅
- [ ] 错误提示清晰
- [ ] 加载速度快
- [ ] 响应式设计良好

---

## 📝 备注

- site_column 表已存在,无需创建
- 栏目类型: SINGLE_PAGE, POST, PRODUCT, CUSTOM, GALLERY
- 树形结构需要递归算法
- 拖拽排序使用 SortableJS 库
- Hero 配置影响前台页面 header 显示

---

## ❓ 问题与解决

暂无

---

**最后更新**: 2025-11-13  
**状态**: 待开始
