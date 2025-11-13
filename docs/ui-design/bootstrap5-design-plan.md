# 博文教育管理后台 - Bootstrap 5 现代化设计方案

**文档版本**: v1.0
**创建日期**: 2025-11-13
**设计师**: maxazure
**技术栈**: Bootstrap 5.3 + Bootstrap Icons + FastAPI + Jinja2

---

## 📑 目录

1. [设计概览](#一设计概览)
2. [整体布局结构](#二整体布局结构)
3. [配色方案](#三配色方案)
4. [导航系统设计](#四导航系统设计)
5. [组件库规范](#五组件库规范)
6. [响应式设计](#六响应式设计)
7. [实施计划](#七实施计划)

---

## 一、设计概览

### 1.1 设计目标

- ✅ **现代化**: 采用 Bootstrap 5 最新设计语言
- ✅ **专业性**: 适合教育机构的品牌形象
- ✅ **易用性**: 清晰的信息层级和操作流程
- ✅ **响应式**: 完美适配桌面端、平板和移动端
- ✅ **高效率**: 快速加载，流畅交互

### 1.2 设计原则

1. **内容优先**: 突出核心管理功能，减少视觉干扰
2. **一致性**: 统一的色彩、字体、间距、组件风格
3. **反馈清晰**: 操作后即时反馈，状态明确
4. **渐进增强**: 基础功能优先，高级功能可选
5. **无障碍**: 遵循 WCAG 2.1 AA 标准

### 1.3 技术选型

| 技术 | 版本 | 用途 |
|------|------|------|
| Bootstrap | 5.3.0 | UI 框架 |
| Bootstrap Icons | 1.11.0 | 图标系统 |
| FastAPI | 0.109.0 | 后端框架 |
| Jinja2 | 3.1.2 | 模板引擎 |
| Alpine.js | 3.13.0 | 轻量级 JS 框架（可选） |

---

## 二、整体布局结构

### 2.1 布局架构

采用经典的 **三栏布局**：

```
┌─────────────────────────────────────────────────────────┐
│  Topbar (固定顶部导航栏)                                   │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ Sidebar  │  Main Content Area                          │
│ (左侧导航)│  (主内容区)                                   │
│          │                                              │
│ 可折叠    │  - 面包屑导航                                 │
│ 200px   │  - 页面标题                                   │
│          │  - 功能内容                                   │
│          │  - 底部分页                                   │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

### 2.2 尺寸规范

| 区域 | 宽度 | 高度 | 说明 |
|------|------|------|------|
| Topbar | 100% | 60px | 固定顶部 |
| Sidebar (展开) | 240px | 100vh - 60px | 可折叠 |
| Sidebar (折叠) | 70px | 100vh - 60px | 仅显示图标 |
| Main Content | 自适应 | 100vh - 60px | 可滚动 |
| 内容最大宽度 | 1400px | - | 居中显示 |

### 2.3 间距系统

采用 Bootstrap 5 的间距标准（基于 4px）：

```css
$spacer: 1rem; /* 16px */

/* 间距等级 */
0: 0
1: 0.25rem  (4px)
2: 0.5rem   (8px)
3: 1rem     (16px)
4: 1.5rem   (24px)
5: 3rem     (48px)
```

---

## 三、配色方案

### 3.1 主题色彩

基于博文教育的品牌色（中国红 + 深蓝）设计配色方案：

#### 主色（Primary）
```css
--bs-primary: #c8102e;        /* 中国红（品牌主色） */
--bs-primary-rgb: 200, 16, 46;
--bs-primary-hover: #a00d25;  /* 深红 */
--bs-primary-light: #fdeaec;  /* 浅红背景 */
```

#### 次要色（Secondary）
```css
--bs-secondary: #1e3a8a;      /* 深蓝 */
--bs-secondary-rgb: 30, 58, 138;
--bs-secondary-hover: #1e40af;
--bs-secondary-light: #dbeafe;
```

#### 中性色（Neutral）
```css
--bs-dark: #1f2937;           /* 深灰（标题） */
--bs-body-color: #4b5563;     /* 正文灰色 */
--bs-secondary: #6b7280;      /* 次要文字 */
--bs-light: #f9fafb;          /* 浅灰背景 */
--bs-border: #e5e7eb;         /* 边框灰 */
```

#### 功能色（Functional）
```css
--bs-success: #10b981;        /* 成功（绿） */
--bs-danger: #ef4444;         /* 危险（红） */
--bs-warning: #f59e0b;        /* 警告（黄） */
--bs-info: #3b82f6;           /* 信息（蓝） */
```

#### 背景色（Backgrounds）
```css
--bg-body: #ffffff;           /* 主背景（白） */
--bg-sidebar: #1f2937;        /* 侧边栏（深灰） */
--bg-topbar: #ffffff;         /* 顶栏（白） */
--bg-content: #f9fafb;        /* 内容区（浅灰） */
--bg-card: #ffffff;           /* 卡片（白） */
```

### 3.2 色彩应用场景

| 场景 | 颜色 | 用途 |
|------|------|------|
| 主操作按钮 | Primary Red | 添加、保存、确认 |
| 次要按钮 | Secondary Blue | 编辑、查看详情 |
| 危险操作 | Danger Red | 删除、下线 |
| 成功提示 | Success Green | 操作成功反馈 |
| 侧边栏背景 | Dark Gray | 导航菜单背景 |
| 内容区背景 | Light Gray | 主内容区背景 |

### 3.3 阴影系统

```css
/* 卡片阴影 */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

/* 悬浮效果 */
.card:hover {
  box-shadow: var(--shadow-lg);
  transition: box-shadow 0.3s ease;
}
```

---

## 四、导航系统设计

### 4.1 顶部导航栏 (Topbar)

**高度**: 60px
**背景**: 白色 (#ffffff)
**边框**: 底部 1px 灰色边框

#### 布局结构
```html
<nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom fixed-top">
  <div class="container-fluid px-4">
    <!-- 左侧：Logo + 折叠按钮 -->
    <div class="d-flex align-items-center">
      <button class="btn btn-link" id="sidebarToggle">
        <i class="bi bi-list"></i>
      </button>
      <a class="navbar-brand ms-3" href="/admin/">
        <img src="/static/images/logo.png" height="30" alt="博文教育">
        <span class="ms-2">管理后台</span>
      </a>
    </div>

    <!-- 右侧：用户信息 + 操作菜单 -->
    <div class="d-flex align-items-center">
      <!-- 通知图标（可选） -->
      <button class="btn btn-link position-relative me-3">
        <i class="bi bi-bell"></i>
        <span class="badge bg-danger rounded-pill position-absolute top-0 start-100">
          3
        </span>
      </button>

      <!-- 用户下拉菜单 -->
      <div class="dropdown">
        <button class="btn btn-link dropdown-toggle" data-bs-toggle="dropdown">
          <i class="bi bi-person-circle me-2"></i>
          <span>管理员</span>
        </button>
        <ul class="dropdown-menu dropdown-menu-end">
          <li><a class="dropdown-item" href="/admin/profile">
            <i class="bi bi-person me-2"></i>个人资料
          </a></li>
          <li><a class="dropdown-item" href="/admin/change-password">
            <i class="bi bi-key me-2"></i>修改密码
          </a></li>
          <li><hr class="dropdown-divider"></li>
          <li><a class="dropdown-item text-danger" href="/admin/logout">
            <i class="bi bi-box-arrow-right me-2"></i>退出登录
          </a></li>
        </ul>
      </div>
    </div>
  </div>
</nav>
```

### 4.2 左侧导航栏 (Sidebar)

**宽度**: 240px (展开) / 70px (折叠)
**背景**: 深灰色 (#1f2937)
**文字**: 白色/灰色

#### 功能模块分组

```
📊 Dashboard 仪表板
  └─ /admin/

📁 内容管理
  ├─ 栏目管理 /admin/columns
  ├─ 单页管理 /admin/pages
  ├─ 文章管理 /admin/posts
  └─ 产品管理 /admin/products

🖼️ 媒体资源
  ├─ 媒体库 /admin/media
  └─ 相册管理 /admin/galleries

💬 用户互动
  └─ 留言管理 /admin/contacts

⚙️ 系统设置
  └─ 站点设置 /admin/settings
```

#### HTML 结构

```html
<aside class="sidebar bg-dark text-white" id="sidebar">
  <div class="sidebar-content">
    <!-- 仪表板 -->
    <div class="sidebar-section">
      <a href="/admin/" class="sidebar-link">
        <i class="bi bi-speedometer2"></i>
        <span class="sidebar-text">仪表板</span>
      </a>
    </div>

    <!-- 内容管理 -->
    <div class="sidebar-section">
      <div class="sidebar-header">内容管理</div>
      <a href="/admin/columns" class="sidebar-link">
        <i class="bi bi-folder"></i>
        <span class="sidebar-text">栏目管理</span>
      </a>
      <a href="/admin/pages" class="sidebar-link">
        <i class="bi bi-file-text"></i>
        <span class="sidebar-text">单页管理</span>
      </a>
      <a href="/admin/posts" class="sidebar-link">
        <i class="bi bi-newspaper"></i>
        <span class="sidebar-text">文章管理</span>
      </a>
      <a href="/admin/products" class="sidebar-link">
        <i class="bi bi-box-seam"></i>
        <span class="sidebar-text">产品管理</span>
      </a>
    </div>

    <!-- 媒体资源 -->
    <div class="sidebar-section">
      <div class="sidebar-header">媒体资源</div>
      <a href="/admin/media" class="sidebar-link">
        <i class="bi bi-images"></i>
        <span class="sidebar-text">媒体库</span>
      </a>
      <a href="/admin/galleries" class="sidebar-link">
        <i class="bi bi-collection"></i>
        <span class="sidebar-text">相册管理</span>
      </a>
    </div>

    <!-- 用户互动 -->
    <div class="sidebar-section">
      <div class="sidebar-header">用户互动</div>
      <a href="/admin/contacts" class="sidebar-link">
        <i class="bi bi-chat-dots"></i>
        <span class="sidebar-text">留言管理</span>
        <span class="badge bg-danger">5</span>
      </a>
    </div>

    <!-- 系统设置 -->
    <div class="sidebar-section">
      <div class="sidebar-header">系统设置</div>
      <a href="/admin/settings" class="sidebar-link">
        <i class="bi bi-gear"></i>
        <span class="sidebar-text">站点设置</span>
      </a>
    </div>
  </div>
</aside>
```

### 4.3 主内容区 (Main Content)

#### 标准页面结构

```html
<main class="main-content" id="mainContent">
  <!-- 面包屑导航 -->
  <nav aria-label="breadcrumb" class="mb-3">
    <ol class="breadcrumb">
      <li class="breadcrumb-item"><a href="/admin/">首页</a></li>
      <li class="breadcrumb-item"><a href="/admin/posts">文章管理</a></li>
      <li class="breadcrumb-item active">编辑文章</li>
    </ol>
  </nav>

  <!-- 页面标题区 -->
  <div class="page-header mb-4">
    <div class="row align-items-center">
      <div class="col">
        <h1 class="page-title mb-0">文章管理</h1>
        <p class="text-muted mt-1">管理网站的所有文章内容</p>
      </div>
      <div class="col-auto">
        <a href="/admin/posts/new" class="btn btn-primary">
          <i class="bi bi-plus-lg me-2"></i>新建文章
        </a>
      </div>
    </div>
  </div>

  <!-- 内容区 -->
  <div class="content-wrapper">
    <!-- 这里是具体的页面内容 -->
  </div>
</main>
```

---

## 五、组件库规范

### 5.1 按钮 (Buttons)

#### 主要按钮
```html
<!-- 主操作按钮（红色） -->
<button class="btn btn-primary">
  <i class="bi bi-plus-lg me-2"></i>新建
</button>

<!-- 次要按钮（蓝色） -->
<button class="btn btn-secondary">
  <i class="bi bi-pencil me-2"></i>编辑
</button>

<!-- 危险操作（红色描边） -->
<button class="btn btn-outline-danger">
  <i class="bi bi-trash me-2"></i>删除
</button>

<!-- 文本按钮 -->
<button class="btn btn-link">取消</button>
```

#### 按钮尺寸
```html
<button class="btn btn-primary btn-lg">大按钮</button>
<button class="btn btn-primary">标准按钮</button>
<button class="btn btn-primary btn-sm">小按钮</button>
```

### 5.2 表单 (Forms)

#### 标准表单项
```html
<div class="mb-3">
  <label for="title" class="form-label">标题 <span class="text-danger">*</span></label>
  <input type="text" class="form-control" id="title" 
         placeholder="请输入文章标题" required>
  <div class="form-text">标题将显示在文章列表和详情页</div>
</div>

<!-- 带图标的输入框 -->
<div class="input-group mb-3">
  <span class="input-group-text"><i class="bi bi-search"></i></span>
  <input type="text" class="form-control" placeholder="搜索...">
</div>

<!-- 选择框 -->
<select class="form-select" aria-label="栏目选择">
  <option selected>请选择栏目</option>
  <option value="1">中文学校</option>
  <option value="2">国际象棋</option>
</select>

<!-- 文本域 -->
<textarea class="form-control" rows="4" 
          placeholder="请输入内容..."></textarea>

<!-- 开关按钮 -->
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" id="isPublished">
  <label class="form-check-label" for="isPublished">立即发布</label>
</div>
```

### 5.3 卡片 (Cards)

#### 标准卡片
```html
<div class="card">
  <div class="card-header">
    <h5 class="card-title mb-0">基本信息</h5>
  </div>
  <div class="card-body">
    <p class="card-text">卡片内容</p>
  </div>
  <div class="card-footer text-muted">
    最后更新: 2025-11-13
  </div>
</div>
```

#### 统计卡片
```html
<div class="card stat-card">
  <div class="card-body">
    <div class="d-flex align-items-center">
      <div class="stat-icon bg-primary text-white rounded-3 me-3">
        <i class="bi bi-file-text fs-3"></i>
      </div>
      <div>
        <h6 class="text-muted mb-1">文章总数</h6>
        <h2 class="mb-0">128</h2>
        <small class="text-success">
          <i class="bi bi-arrow-up"></i> 12% 比上月
        </small>
      </div>
    </div>
  </div>
</div>
```

### 5.4 表格 (Tables)

#### 响应式表格
```html
<div class="table-responsive">
  <table class="table table-hover">
    <thead class="table-light">
      <tr>
        <th width="5%">
          <input type="checkbox" class="form-check-input">
        </th>
        <th width="10%">ID</th>
        <th width="30%">标题</th>
        <th width="15%">栏目</th>
        <th width="10%">状态</th>
        <th width="15%">更新时间</th>
        <th width="15%">操作</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="checkbox" class="form-check-input"></td>
        <td>1</td>
        <td>文章标题</td>
        <td><span class="badge bg-info">中文学校</span></td>
        <td><span class="badge bg-success">已发布</span></td>
        <td>2025-11-13 10:30</td>
        <td>
          <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-secondary">
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-outline-danger">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

### 5.5 徽章 (Badges)

```html
<!-- 状态徽章 -->
<span class="badge bg-success">已发布</span>
<span class="badge bg-warning text-dark">草稿</span>
<span class="badge bg-danger">已下线</span>
<span class="badge bg-info">待审核</span>

<!-- 数字徽章 -->
<span class="badge rounded-pill bg-danger">5</span>

<!-- 标签徽章 -->
<span class="badge bg-light text-dark me-1">标签1</span>
<span class="badge bg-light text-dark me-1">标签2</span>
```

### 5.6 提示框 (Alerts)

```html
<!-- 成功提示 -->
<div class="alert alert-success alert-dismissible fade show" role="alert">
  <i class="bi bi-check-circle me-2"></i>
  操作成功！文章已保存。
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>

<!-- 警告提示 -->
<div class="alert alert-warning" role="alert">
  <i class="bi bi-exclamation-triangle me-2"></i>
  此操作可能影响已发布的内容，请谨慎操作。
</div>

<!-- 危险提示 -->
<div class="alert alert-danger" role="alert">
  <i class="bi bi-x-circle me-2"></i>
  删除后无法恢复，确定要继续吗？
</div>
```

### 5.7 模态框 (Modals)

```html
<!-- 确认删除对话框 -->
<div class="modal fade" id="deleteModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">确认删除</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <p>确定要删除这篇文章吗？此操作无法撤销。</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          取消
        </button>
        <button type="button" class="btn btn-danger">
          <i class="bi bi-trash me-2"></i>确认删除
        </button>
      </div>
    </div>
  </div>
</div>
```

### 5.8 分页 (Pagination)

```html
<nav aria-label="Page navigation">
  <ul class="pagination justify-content-center">
    <li class="page-item disabled">
      <a class="page-link" href="#" tabindex="-1">
        <i class="bi bi-chevron-left"></i>
      </a>
    </li>
    <li class="page-item active"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item">
      <a class="page-link" href="#">
        <i class="bi bi-chevron-right"></i>
      </a>
    </li>
  </ul>
</nav>

<!-- 带信息的分页 -->
<div class="d-flex justify-content-between align-items-center">
  <div class="text-muted">
    显示第 1-10 条，共 128 条记录
  </div>
  <nav>
    <ul class="pagination mb-0">
      <!-- 分页按钮 -->
    </ul>
  </nav>
</div>
```

---

## 六、响应式设计

### 6.1 断点系统

采用 Bootstrap 5 标准断点：

```css
/* Extra small devices (phones, less than 576px) */
@media (max-width: 575.98px) { }

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) { }

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) { }

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) { }

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) { }

/* Extra extra large devices (1400px and up) */
@media (min-width: 1400px) { }
```

### 6.2 布局适配

#### 移动端 (<768px)
- Sidebar 默认隐藏，通过汉堡菜单打开
- Topbar 高度保持 60px
- 表格横向滚动或卡片化展示
- 按钮全宽显示
- 字体大小适当缩小

#### 平板端 (768px - 991px)
- Sidebar 可折叠为图标模式（70px）
- 表格可正常显示
- 表单两列布局

#### 桌面端 (≥992px)
- Sidebar 默认展开（240px）
- 完整功能展示
- 多列布局

### 6.3 移动优化

```html
<!-- 移动端菜单按钮 -->
<button class="btn btn-link d-lg-none" id="mobileSidebarToggle">
  <i class="bi bi-list fs-4"></i>
</button>

<!-- 移动端遮罩层 -->
<div class="sidebar-overlay d-lg-none" id="sidebarOverlay"></div>

<!-- 响应式表格 -->
<div class="table-responsive">
  <table class="table">
    <!-- 表格内容 -->
  </table>
</div>

<!-- 移动端卡片式列表 -->
<div class="d-block d-md-none">
  <div class="card mb-3">
    <div class="card-body">
      <h6>文章标题</h6>
      <p class="text-muted small">栏目: 中文学校</p>
      <div class="d-flex justify-content-between">
        <span class="badge bg-success">已发布</span>
        <div>
          <button class="btn btn-sm btn-outline-secondary">编辑</button>
          <button class="btn btn-sm btn-outline-danger">删除</button>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## 七、实施计划

### 7.1 阶段一：核心框架搭建（1-2天）

**任务**:
- [ ] 创建 Bootstrap 5 基础模板
- [ ] 实现 Topbar 组件
- [ ] 实现 Sidebar 组件
- [ ] 实现主内容区布局
- [ ] 添加响应式适配

**文件**:
- `admin/templates/bootstrap_base.html` - 新的基础模板
- `admin/templates/components/topbar.html` - 顶部导航栏
- `admin/templates/components/sidebar_v2.html` - 左侧导航栏
- `admin/static/css/bootstrap-admin.css` - 自定义样式

### 7.2 阶段二：页面迁移（3-5天）

**优先级 P0**:
- [ ] Dashboard 仪表板
- [ ] 登录页面（已有 Bootstrap）
- [ ] 媒体库列表页

**优先级 P1**:
- [ ] 文章列表页
- [ ] 文章编辑页
- [ ] 栏目管理页

**优先级 P2**:
- [ ] 产品管理页
- [ ] 相册管理页
- [ ] 留言管理页
- [ ] 站点设置页

### 7.3 阶段三：组件优化（2-3天）

- [ ] 统一表格组件
- [ ] 统一表单组件
- [ ] 统一模态框组件
- [ ] 统一分页组件
- [ ] 图片选择器组件

### 7.4 阶段四：交互优化（2-3天）

- [ ] 侧边栏折叠动画
- [ ] Toast 提示组件
- [ ] 加载状态组件
- [ ] 确认对话框
- [ ] 拖拽上传组件

### 7.5 阶段五：测试与调优（2天）

- [ ] 响应式测试（手机、平板、桌面）
- [ ] 浏览器兼容测试
- [ ] 性能优化
- [ ] 无障碍测试
- [ ] 用户体验优化

### 7.6 交付物清单

#### 模板文件
```
admin/templates/
├── bootstrap_base.html          # Bootstrap 5 基础模板
├── bootstrap_dashboard.html     # 仪表板页面
├── components/
│   ├── topbar.html              # 顶部导航栏
│   ├── sidebar_v2.html          # 左侧导航栏
│   ├── breadcrumb.html          # 面包屑
│   ├── page_header.html         # 页面标题组件
│   ├── data_table.html          # 数据表格组件
│   ├── pagination_v2.html       # 分页组件
│   └── toast.html               # Toast 提示组件
├── posts/
│   ├── list_v2.html             # 文章列表（Bootstrap版）
│   └── form_v2.html             # 文章表单（Bootstrap版）
└── ... (其他模块)
```

#### 样式文件
```
admin/static/css/
├── bootstrap-admin.css          # 主样式文件
├── components/
│   ├── sidebar.css              # 侧边栏样式
│   ├── topbar.css               # 顶栏样式
│   ├── tables.css               # 表格样式
│   └── forms.css                # 表单样式
└── themes/
    ├── light.css                # 亮色主题（默认）
    └── dark.css                 # 暗色主题（可选）
```

#### JavaScript 文件
```
admin/static/js/
├── bootstrap-admin.js           # 主JS文件
├── components/
│   ├── sidebar.js               # 侧边栏交互
│   ├── toast.js                 # Toast 提示
│   ├── modal.js                 # 模态框管理
│   └── table.js                 # 表格交互
└── utils/
    ├── api.js                   # API 请求封装
    └── helpers.js               # 工具函数
```

---

## 八、附录

### 8.1 Bootstrap Icons 图标映射

| 功能 | 图标 | 代码 |
|------|------|------|
| 仪表板 | 📊 | `bi-speedometer2` |
| 栏目管理 | 📁 | `bi-folder` |
| 单页管理 | 📄 | `bi-file-text` |
| 文章管理 | 📰 | `bi-newspaper` |
| 产品管理 | 📦 | `bi-box-seam` |
| 媒体库 | 🖼️ | `bi-images` |
| 相册管理 | 🖼️ | `bi-collection` |
| 留言管理 | 💬 | `bi-chat-dots` |
| 站点设置 | ⚙️ | `bi-gear` |
| 用户信息 | 👤 | `bi-person-circle` |
| 通知 | 🔔 | `bi-bell` |
| 搜索 | 🔍 | `bi-search` |
| 编辑 | ✏️ | `bi-pencil` |
| 删除 | 🗑️ | `bi-trash` |
| 添加 | ➕ | `bi-plus-lg` |
| 保存 | 💾 | `bi-check-lg` |
| 取消 | ❌ | `bi-x-lg` |

### 8.2 参考资源

- [Bootstrap 5 官方文档](https://getbootstrap.com/docs/5.3/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Material Design Guidelines](https://material.io/design)
- [WCAG 2.1 无障碍标准](https://www.w3.org/WAI/WCAG21/quickref/)

---

**文档结束**

如有问题或建议，请联系：maxazure@gmail.com
