## 背景与现状确认
- 前台首页渲染：`app/routes/frontend.py:78-102` 通过模板 `home.html` 组合特定数据（精选活动、最新文章、推荐产品）。
- 栏目页渲染：`app/routes/frontend.py:105-354` 按 `ColumnType` 分发，`CUSTOM` 类型靠 `slug` 匹配自定义模板或渲染概览页（有子栏目时走 `overview.html`）。
- 后台栏目管理：`admin/app/routers/columns.py` 提供完整 CRUD 与排序；模板行操作在 `admin/templates/columns/_column_row.html`，当前未为 `CUSTOM` 提供“页面编辑”入口。
- 模型：`app/models/site.py:20-28` 定义 `ColumnType（含 CUSTOM）`；`SinglePage` 仅绑定 `SINGLE_PAGE`。

## 目标
- 新增后台「首页管理」：区块化编辑首页布局，支持插入、配置、拖拽排序、预览与发布。
- 扩展到 `CUSTOM` 类型栏目：为每个自定义栏目提供同样的区块化页面编辑能力，前台优先使用布局渲染，无布局时保持现有模板/概览行为不变。

## 统一布局数据模型（MVP）
- `page_layout`：`id`, `scope{home|column}`, `scope_id(nullable for home)`, `status{draft|published}`, `updated_at`。
- `page_layout_section`：`id`, `layout_id`, `title`, `sort_order`, `is_enabled`。
- `page_layout_block`：`id`, `section_id`, `block_type`, `attributes_json`, `sort_order`, `is_enabled`。
- 说明：
  - `scope=home` 表示首页（不需要 `scope_id`）。
  - `scope=column` + `scope_id=site_column.id` 表示某个自定义栏目。
  - `attributes_json` 用 Pydantic 校验；支持轻量嵌套（未来扩展 children）。

## 区块注册与渲染管线
- 区块注册表：集中定义区块元信息、属性 Schema、服务端渲染器。
  - 建议位置：`admin/app/blocks/registry.py`（注册）、`admin/app/blocks/types/*.py`（具体区块）。
- 首批内置区块：
  - `HeroBanner`（背景、标题、副标题、CTA，媒体库/站点设置）
  - `FeatureList`（图标+标题+描述卡片）
  - `PostList`（文章列表，分类/数量/排序，动态）
  - `ProductGrid`（产品网格，分类/数量/排序）
  - `GalleryGrid`（相册缩略图集合）
  - `RichText`（Markdown→HTML）
  - `MediaText`（图文混排，图位置/比率）
  - `ContactCTA`（行动召唤）
  - `Spacer/Divider`（静态装饰）
- 渲染流程：
  - 服务层 `admin/app/services/home_service.py` 与 `admin/app/services/column_page_builder_service.py` 读取布局树，按 `sort_order` 迭代调用区块渲染器生成 HTML 片段。
  - 前台模板 `app/templates/home/index.html` 与 `app/templates/columns/builder.html` 拼装片段（`|safe` 输出），确保 SEO 友好。

## 后台功能设计
- 新增栏目「首页管理」：
  - 路由：`GET /admin/home` 管理界面；`GET /admin/home/data` 读取布局；CRUD / reorder / preview / publish 一组接口。
  - 模板与脚本：`admin/templates/home/manager.html`、`admin/admin-static/js/home.js`；使用 `Sortable.js` 实现 Section 与 Block 两层拖拽排序。
- 为 `CUSTOM` 栏目提供「页面编辑」入口：
  - 在 `admin/templates/columns/_column_row.html` 增加按钮 `编辑页面`（当 `column.column_type == CUSTOM`），跳转 `GET /admin/columns/{id}/builder`。
  - 路由：`GET /admin/columns/{id}/builder` 打开页面构建器；接口与首页一致但 `scope=column`、`scope_id={id}`。
- 属性编辑：右侧表单面板由区块 Schema 驱动；支持实时预览（可选）。
- 模板锁定：提供锁定策略（允许移动但禁止插入/删除或全部锁定），参考 Gutenberg `template_lock` 行为。

## 接口一览（FastAPI）
- 通用：
  - `GET /admin/{scope}/data`（`scope in {home, columns/{id}}`）：读取布局
  - `POST /admin/{scope}/sections`：新增/编辑 Section
  - `POST /admin/{scope}/sections/reorder`：批量排序
  - `POST /admin/{scope}/blocks`：新增区块
  - `PUT /admin/{scope}/blocks/{id}`：更新属性
  - `POST /admin/{scope}/blocks/reorder`：批量排序
  - `DELETE /admin/{scope}/blocks/{id}`：删除区块
  - `POST /admin/{scope}/publish`：发布草稿
  - `GET /admin/{scope}/preview`：服务端渲染预览

## 前台渲染集成
- 首页：在 `app/routes/frontend.py:78-102` 增加“布局优先”逻辑；存在已发布布局则渲染区块，否则保持当前 `home.html` 拼装行为。
- `CUSTOM` 栏目：在 `app/routes/frontend.py:262-351` 的分支开头检查是否存在 `scope=column` 的布局；如有则渲染布局，否则继续现有自定义模板/概览页逻辑。
- 其他类型栏目：保持现状；后续可逐步引入区块化（例如 `SINGLE_PAGE` 通过区块生成 `content_html`）。

## 安全与一致性
- 认证：跟随现有 Admin Session 与中间件；仅管理员可访问布局编辑接口。
- 校验：区块属性 Pydantic 校验；媒体类型与大小沿用既有白名单与清洗策略。
- XSS：渲染时默认转义，富文本严格受控 Markdown→HTML。
- 兼容性：无布局数据时完全回退到现有模板分派逻辑，避免破坏当前线上表现。

## 测试计划
- 接口测试：CRUD、拖拽批量、预览与发布、权限控制。
- 渲染测试：典型区块组合的 Jinja2 片段快照比对；数据区块（文章/产品/相册）正确性。
- 回归测试：确保 `app/routes/frontend.py` 在无布局时所有原有分支仍返回同样模板与上下文。

## 迁移与上线
- 数据库迁移：新增三表，提供迁移脚本（风格同现有 `scripts/migrate_media_file.py`）。
- 数据初始化：为首页创建默认布局与演示区块；为常见 `CUSTOM` 栏目（如 `school/chess/badminton/programmes/contact`）可选初始化模板锁定布局。
- 渐进上线：先发布首页管理；第二阶段开启指定 `CUSTOM` 栏目的页面编辑。

## 时间线（MVP）
- Week 1：统一数据模型与后端接口（含注册表、服务层）。
- Week 2：后台 UI（首页管理、栏目页面编辑）与交互逻辑（区块库、表单、拖拽）。
- Week 3：前台渲染接入（首页与 CUSTOM 栏目），动态区块联动文章/产品/相册。
- Week 4：测试完善、迁移与文档汇总，灰度上线。

## 参考与一致性对标
- 动态区块与属性仅保存、服务端渲染：[Creating dynamic blocks](https://developer.wordpress.org/block-editor/how-to-guides/block-tutorial/creating-dynamic-blocks/)
- 区块层级组合与复用：`InnerBlocks` 与 Patterns 概念：[Key Concepts](https://developer.wordpress.org/block-editor/explanations/architecture/key-concepts/)
- 模板与锁定策略：`template_lock` 行为：[Templates](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-templates/)
- 静态/动态渲染策略与回退：[Static vs Dynamic](https://developer.wordpress.org/block-editor/getting-started/fundamentals/static-dynamic-rendering/)