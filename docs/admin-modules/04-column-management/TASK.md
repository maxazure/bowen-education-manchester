# 模块 04: 栏目管理

**模块编号**: 04
**模块名称**: Column Management
**优先级**: P0 (高)
**预计工时**: 3 天
**负责 Subagent**: column-management
**依赖**: 模块 01 (基础设施), 模块 02 (用户管理)

---

## 📋 任务概述

实现网站栏目结构的配置和管理,包括栏目的 CRUD 操作、树形结构展示、拖拽排序、Hero 区域配置和导航显示控制。

---

## 🎯 任务目标

1. ✅ 实现栏目 CRUD 功能
2. ✅ 实现树形结构展示
3. ✅ 实现拖拽排序功能
4. ✅ 实现 Hero 配置
5. ✅ 实现启用/禁用控制
6. ✅ 实现导航显示控制

---

## 🗄️ 数据库设计

### site_column 表 (已存在,无需修改)

现有表结构已满足需求,无需创建新表。

**字段说明**:
- `id`: 主键
- `name`: 栏目名称
- `slug`: URL 别名 (唯一)
- `description`: 栏目描述
- `parent_id`: 父栏目 ID (外键)
- `sort_order`: 排序值
- `column_type`: 栏目类型 (SINGLE_PAGE, POST, PRODUCT, CUSTOM, GALLERY)
- `is_active`: 是否启用
- `show_in_nav`: 是否显示在导航
- `show_in_footer`: 是否显示在底部
- `icon`: 图标类名
- `hero_title`: Hero 标题
- `hero_subtitle`: Hero 副标题
- `hero_background_image`: Hero 背景图
- `hero_cta_text`: CTA 按钮文本
- `hero_cta_link`: CTA 按钮链接
- `created_at`: 创建时间
- `updated_at`: 更新时间

---

## ✅ TDD 测试用例

### 测试文件 1: `tests/admin/test_column_crud.py` (12 个测试)

```python
class TestColumnCreate:
    def test_create_basic_column()
    def test_create_column_with_parent()
    def test_slug_auto_generation()
    def test_slug_uniqueness()

class TestColumnRead:
    def test_get_column_by_id()
    def test_get_column_by_slug()
    def test_get_all_columns()

class TestColumnUpdate:
    def test_update_basic_info()
    def test_update_hero_config()
    def test_toggle_active_status()

class TestColumnDelete:
    def test_delete_empty_column()
    def test_cannot_delete_column_with_content()
```

### 测试文件 2: `tests/admin/test_column_sorting.py` (3 个测试)

```python
class TestColumnSorting:
    def test_default_sort_order()
    def test_manual_sort_order()
    def test_batch_update_sort_order()
```

### 测试文件 3: `tests/admin/test_column_tree.py` (3 个测试)

```python
class TestColumnTree:
    def test_build_tree_structure()
    def test_get_nav_columns()
    def test_get_footer_columns()
```

**测试统计**: 共 18 个测试用例

---

## 📝 开发步骤（TDD）

### Phase 1: 编写测试 (Red)
- 创建 3 个测试文件
- 编写所有 18 个测试用例
- 运行测试确认失败

### Phase 2-3: 实现功能 (Green)
- 创建 `app/services/column_service.py`
- 创建 `app/admin/routers/columns.py`
- 实现 CRUD 路由
- 实现树形结构构建
- 实现排序功能

### Phase 4-5: 创建模板和脚本
- 创建 `templates/admin/columns/list.html`
- 创建 `templates/admin/columns/form.html`
- 创建 `static/admin/js/columns.js`
- 集成 SortableJS 拖拽库

### Phase 6: 测试验证 (Green)
- 运行所有测试
- 确认覆盖率 >= 85%

### Phase 7: 重构 (Refactor)
- 代码格式化
- 类型检查
- 优化性能

---

## 📄 核心代码示例

### Service 层

```python
# app/services/column_service.py

def generate_slug(name: str) -> str:
    """生成 URL Slug"""
    return slugify(name)

def can_delete_column(db: Session, column_id: int) -> bool:
    """检查栏目是否可以删除"""
    # 检查是否有内容
    post_count = db.query(Post).filter(Post.column_id == column_id).count()
    if post_count > 0:
        return False
    return True

def build_tree(db: Session) -> List[Dict]:
    """构建栏目树形结构"""
    columns = db.query(SiteColumn).order_by(SiteColumn.sort_order).all()
    # 构建树形结构逻辑
    return tree

def get_nav_columns(db: Session) -> List[SiteColumn]:
    """获取导航显示的栏目"""
    return db.query(SiteColumn).filter(
        SiteColumn.show_in_nav == True,
        SiteColumn.is_active == True
    ).order_by(SiteColumn.sort_order).all()
```

### Router 层

```python
# app/admin/routers/columns.py

@router.get("/")
async def list_columns(request: Request, db: Session = Depends(get_db)):
    """栏目列表页面"""
    columns = db.query(SiteColumn).order_by(SiteColumn.sort_order).all()
    tree = column_service.build_tree(db)
    return templates.TemplateResponse("admin/columns/list.html", {...})

@router.post("/")
async def create_column(name: str = Form(...), slug: str = Form(None), ...):
    """创建栏目"""
    if not slug:
        slug = column_service.generate_slug(name)
    column = SiteColumn(name=name, slug=slug, ...)
    db.add(column)
    db.commit()
    return RedirectResponse(url="/admin/columns", status_code=302)

@router.put("/{column_id}")
async def update_column(column_id: int, ...):
    """更新栏目"""
    column = db.query(SiteColumn).filter_by(id=column_id).first()
    # 更新字段
    db.commit()
    return RedirectResponse(...)

@router.delete("/{column_id}")
async def delete_column(column_id: int, db: Session = Depends(get_db)):
    """删除栏目"""
    if not column_service.can_delete_column(db, column_id):
        return JSONResponse({"error": "该栏目包含内容,无法删除"}, status_code=400)
    db.delete(column)
    db.commit()
    return JSONResponse({"message": "删除成功"})

@router.post("/reorder")
async def reorder_columns(request: Request, db: Session = Depends(get_db)):
    """批量更新排序"""
    data = await request.json()
    for item in data["order"]:
        column = db.query(SiteColumn).filter_by(id=item["id"]).first()
        if column:
            column.sort_order = item["sort_order"]
    db.commit()
    return JSONResponse({"message": "排序更新成功"})
```

---

## ✅ 完成标准

### 功能性要求
- [ ] 栏目列表显示正常
- [ ] 树形结构展示正常
- [ ] 创建栏目功能正常
- [ ] 编辑栏目功能正常
- [ ] 删除栏目功能正常
- [ ] Slug 自动生成功能正常
- [ ] Hero 配置功能正常
- [ ] 拖拽排序功能正常
- [ ] 启用/禁用切换正常
- [ ] 所有测试通过 (18/18)

### 质量要求
- [ ] 代码符合 PEP 8 规范
- [ ] 所有函数有类型提示
- [ ] 测试覆盖率 >= 85%
- [ ] 无代码质量警告

### 用户体验
- [ ] 树形结构直观易懂
- [ ] 拖拽操作流畅
- [ ] 错误提示清晰
- [ ] 响应式设计良好

---

## 📊 验证命令

```bash
# 运行测试
pytest tests/admin/test_column_*.py -v

# 查看覆盖率
pytest tests/admin/test_column_*.py --cov=app/admin/routers/columns --cov=app/services/column_service --cov-report=html

# 代码质量检查
black app/admin/routers/columns.py app/services/column_service.py --check
mypy app/admin/routers/columns.py app/services/column_service.py
```

---

## 🔄 交付物

1. ✅ 栏目路由（完整 CRUD）
2. ✅ 栏目服务层
3. ✅ 栏目列表模板（树形结构）
4. ✅ 栏目表单模板（Hero 配置）
5. ✅ 拖拽排序 JS
6. ✅ 18 个通过的测试用例
7. ✅ 更新的 TODO.md

---

## 📝 注意事项

1. **Slug 唯一性**: 确保生成的 slug 不重复
2. **删除保护**: 删除前必须检查是否包含内容
3. **树形结构**: 避免父子关系形成循环
4. **排序优化**: 使用合理的排序算法
5. **Hero 配置**: 验证图片 URL 的有效性

---

## 🔗 相关文档

- [admin-system-design.md](../../admin-system-design.md) - 系统设计文档 (第 101-135 行)
- [admin-development-plan.md](../../admin-development-plan.md) - 总体开发计划
- [TODO.md](./TODO.md) - 本模块待办事项
