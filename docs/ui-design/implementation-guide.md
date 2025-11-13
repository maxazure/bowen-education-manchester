# Bootstrap 5 UI 实施指南

**版本**: v1.0
**日期**: 2025-11-13
**负责人**: maxazure

---

## 📋 实施清单

### 第一步：准备工作（Day 1 上午）

#### 1.1 CDN 资源确认
```html
<!-- Bootstrap 5.3.0 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap Icons 1.11.0 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">

<!-- Bootstrap 5.3.0 JS (包含 Popper) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

#### 1.2 创建目录结构
```bash
cd /Users/maxazure/projects/bowen-education-manchester/admin

# 创建新的静态资源目录
mkdir -p static/css/bootstrap5
mkdir -p static/js/bootstrap5
mkdir -p static/js/components

# 创建新的模板目录
mkdir -p templates/bootstrap5
mkdir -p templates/bootstrap5/components
mkdir -p templates/bootstrap5/pages
```

#### 1.3 复制设计文件
```bash
# 复制样式文件
cp docs/ui-design/bootstrap5-styles.css admin/static/css/bootstrap5/admin.css

# 创建 JavaScript 文件
touch admin/static/js/bootstrap5/main.js
touch admin/static/js/bootstrap5/sidebar.js
```

---

### 第二步：创建基础模板（Day 1 下午）

#### 2.1 创建 Bootstrap 5 基础模板

**文件**: `admin/templates/bootstrap5/base.html`

```jinja2
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}博文教育管理后台{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    
    <!-- 自定义样式 -->
    <link href="/static/css/bootstrap5/admin.css" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- 顶部导航栏 -->
    {% include 'bootstrap5/components/topbar.html' %}
    
    <!-- 布局容器 -->
    <div class="admin-wrapper">
        <!-- 左侧导航栏 -->
        {% include 'bootstrap5/components/sidebar.html' %}
        
        <!-- 主内容区 -->
        <main class="main-content" id="mainContent">
            {% block content %}{% endblock %}
        </main>
    </div>
    
    <!-- 移动端遮罩 -->
    <div class="sidebar-overlay" id="sidebarOverlay"></div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- 自定义 JS -->
    <script src="/static/js/bootstrap5/main.js"></script>
    <script src="/static/js/bootstrap5/sidebar.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### 2.2 创建顶部导航栏组件

**文件**: `admin/templates/bootstrap5/components/topbar.html`

```jinja2
<nav class="navbar topbar navbar-expand-lg navbar-light bg-white border-bottom fixed-top">
    <div class="container-fluid px-4">
        <!-- 左侧：折叠按钮 + Logo -->
        <div class="d-flex align-items-center">
            <button class="btn btn-link p-0 me-3" id="sidebarToggle" type="button">
                <i class="bi bi-list fs-3"></i>
            </button>
            <a class="navbar-brand d-flex align-items-center" href="/admin/">
                <img src="/static/images/logo.png" height="30" alt="博文教育">
                <span class="ms-2 d-none d-md-inline">管理后台</span>
            </a>
        </div>

        <!-- 右侧：用户菜单 -->
        <div class="d-flex align-items-center">
            <div class="dropdown user-dropdown">
                <button class="btn dropdown-toggle d-flex align-items-center" type="button" 
                        id="userDropdown" data-bs-toggle="dropdown">
                    <i class="bi bi-person-circle fs-5 me-2"></i>
                    <span class="d-none d-md-inline">{{ session.get('username', '管理员') }}</span>
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li>
                        <a class="dropdown-item" href="/admin/change-password">
                            <i class="bi bi-key me-2"></i>修改密码
                        </a>
                    </li>
                    <li><hr class="dropdown-divider"></li>
                    <li>
                        <a class="dropdown-item text-danger" href="/admin/logout">
                            <i class="bi bi-box-arrow-right me-2"></i>退出登录
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</nav>
```

#### 2.3 创建侧边栏组件

**文件**: `admin/templates/bootstrap5/components/sidebar.html`

```jinja2
<aside class="sidebar" id="sidebar">
    <div class="sidebar-content">
        <!-- 仪表板 -->
        <a href="/admin/" class="sidebar-link {% if request.path == '/admin/' %}active{% endif %}">
            <i class="bi bi-speedometer2"></i>
            <span class="sidebar-text">仪表板</span>
        </a>

        <!-- 内容管理 -->
        <div class="sidebar-section mt-3">
            <div class="sidebar-header">内容管理</div>
            <a href="/admin/columns" class="sidebar-link {% if '/columns' in request.path %}active{% endif %}">
                <i class="bi bi-folder"></i>
                <span class="sidebar-text">栏目管理</span>
            </a>
            <a href="/admin/pages" class="sidebar-link {% if '/pages' in request.path %}active{% endif %}">
                <i class="bi bi-file-text"></i>
                <span class="sidebar-text">单页管理</span>
            </a>
            <a href="/admin/posts" class="sidebar-link {% if '/posts' in request.path %}active{% endif %}">
                <i class="bi bi-newspaper"></i>
                <span class="sidebar-text">文章管理</span>
            </a>
            <a href="/admin/products" class="sidebar-link {% if '/products' in request.path %}active{% endif %}">
                <i class="bi bi-box-seam"></i>
                <span class="sidebar-text">产品管理</span>
            </a>
        </div>

        <!-- 媒体资源 -->
        <div class="sidebar-section mt-3">
            <div class="sidebar-header">媒体资源</div>
            <a href="/admin/media" class="sidebar-link {% if '/media' in request.path %}active{% endif %}">
                <i class="bi bi-images"></i>
                <span class="sidebar-text">媒体库</span>
            </a>
            <a href="/admin/galleries" class="sidebar-link {% if '/galleries' in request.path %}active{% endif %}">
                <i class="bi bi-collection"></i>
                <span class="sidebar-text">相册管理</span>
            </a>
        </div>

        <!-- 用户互动 -->
        <div class="sidebar-section mt-3">
            <div class="sidebar-header">用户互动</div>
            <a href="/admin/contacts" class="sidebar-link {% if '/contacts' in request.path %}active{% endif %}">
                <i class="bi bi-chat-dots"></i>
                <span class="sidebar-text">留言管理</span>
            </a>
        </div>

        <!-- 系统设置 -->
        <div class="sidebar-section mt-3">
            <div class="sidebar-header">系统设置</div>
            <a href="/admin/settings" class="sidebar-link {% if '/settings' in request.path %}active{% endif %}">
                <i class="bi bi-gear"></i>
                <span class="sidebar-text">站点设置</span>
            </a>
        </div>
    </div>
</aside>
```

---

### 第三步：创建 JavaScript 功能（Day 2 上午）

#### 3.1 主 JavaScript 文件

**文件**: `admin/static/js/bootstrap5/main.js`

```javascript
/**
 * 博文教育管理后台 - 主 JavaScript
 */

// ====================================
// 1. 工具函数
// ====================================

/**
 * 显示 Toast 提示
 */
function showToast(type, message, title = '提示') {
    const toastHTML = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <i class="bi bi-${getToastIcon(type)} me-2"></i>
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHTML;
    container.appendChild(toastElement.firstElementChild);
    
    const toast = new bootstrap.Toast(toastElement.firstElementChild);
    toast.show();
    
    // 3秒后自动移除
    setTimeout(() => {
        toastElement.remove();
    }, 3500);
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'x-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * 显示确认对话框
 */
function confirmAction(title, message, onConfirm) {
    const modalHTML = `
        <div class="modal fade" id="confirmModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-exclamation-triangle text-warning me-2"></i>
                            ${title}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${message}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-danger" id="confirmBtn">确认</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 移除旧的模态框
    const oldModal = document.getElementById('confirmModal');
    if (oldModal) oldModal.remove();
    
    // 添加新的模态框
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
    
    document.getElementById('confirmBtn').addEventListener('click', function() {
        modal.hide();
        if (typeof onConfirm === 'function') {
            onConfirm();
        }
    });
}

/**
 * API 请求封装
 */
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API 请求失败:', error);
        throw error;
    }
}

// ====================================
// 2. 全局事件监听
// ====================================

document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有 tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 初始化所有 popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// ====================================
// 3. 表单处理
// ====================================

/**
 * 表单验证
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    form.classList.add('was-validated');
    return form.checkValidity();
}

/**
 * 重置表单
 */
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.reset();
    form.classList.remove('was-validated');
}

// 导出到全局
window.showToast = showToast;
window.confirmAction = confirmAction;
window.apiRequest = apiRequest;
window.validateForm = validateForm;
window.resetForm = resetForm;
```

#### 3.2 侧边栏 JavaScript

**文件**: `admin/static/js/bootstrap5/sidebar.js`

```javascript
/**
 * 博文教育管理后台 - 侧边栏功能
 */

(function() {
    'use strict';
    
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const mainContent = document.getElementById('mainContent');
    
    if (!sidebar || !sidebarToggle) return;
    
    // ====================================
    // 侧边栏切换
    // ====================================
    sidebarToggle.addEventListener('click', function() {
        if (window.innerWidth < 992) {
            // 移动端：显示/隐藏侧边栏
            sidebar.classList.toggle('show');
            if (sidebarOverlay) {
                sidebarOverlay.classList.toggle('show');
            }
        } else {
            // 桌面端：折叠/展开侧边栏
            sidebar.classList.toggle('collapsed');
            document.body.classList.toggle('sidebar-collapsed');
            
            // 保存状态到 localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
        }
    });
    
    // ====================================
    // 点击遮罩关闭侧边栏（移动端）
    // ====================================
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        });
    }
    
    // ====================================
    // 窗口大小改变时的处理
    // ====================================
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992) {
            // 桌面端：移除移动端的 show 类
            sidebar.classList.remove('show');
            if (sidebarOverlay) {
                sidebarOverlay.classList.remove('show');
            }
        } else {
            // 移动端：移除桌面端的 collapsed 类
            sidebar.classList.remove('collapsed');
            document.body.classList.remove('sidebar-collapsed');
        }
    });
    
    // ====================================
    // 恢复侧边栏折叠状态
    // ====================================
    if (window.innerWidth >= 992) {
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
            document.body.classList.add('sidebar-collapsed');
        }
    }
    
    // ====================================
    // 当前菜单项高亮
    // ====================================
    const currentPath = window.location.pathname;
    const sidebarLinks = sidebar.querySelectorAll('.sidebar-link');
    
    sidebarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath === href || (href !== '/admin/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });
})();
```

---

### 第四步：迁移现有页面（Day 2-3）

#### 4.1 Dashboard 仪表板

**文件**: `admin/templates/bootstrap5/pages/dashboard.html`

```jinja2
{% extends "bootstrap5/base.html" %}

{% block title %}仪表板 - 博文教育管理后台{% endblock %}

{% block content %}
<div class="container-fluid">
    <!-- 页面标题 -->
    <div class="page-header mb-4">
        <h1 class="page-title">仪表板</h1>
        <p class="page-subtitle mb-0">欢迎回来！这是您的管理后台概览</p>
    </div>

    <!-- 统计卡片 -->
    <div class="row g-3 mb-4">
        <div class="col-md-3">
            <div class="card stat-card border-0 shadow-sm">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="stat-icon bg-primary text-white rounded-3 me-3">
                            <i class="bi bi-file-text fs-3"></i>
                        </div>
                        <div>
                            <h6 class="stat-label mb-1">文章总数</h6>
                            <h2 class="stat-value mb-0">{{ stats.posts_count or 0 }}</h2>
                            <small class="text-success">
                                <i class="bi bi-arrow-up"></i> 12% 比上月
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card stat-card border-0 shadow-sm">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="stat-icon bg-success text-white rounded-3 me-3">
                            <i class="bi bi-box-seam fs-3"></i>
                        </div>
                        <div>
                            <h6 class="stat-label mb-1">产品总数</h6>
                            <h2 class="stat-value mb-0">{{ stats.products_count or 0 }}</h2>
                            <small class="text-success">
                                <i class="bi bi-arrow-up"></i> 8% 比上月
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card stat-card border-0 shadow-sm">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="stat-icon bg-warning text-white rounded-3 me-3">
                            <i class="bi bi-chat-dots fs-3"></i>
                        </div>
                        <div>
                            <h6 class="stat-label mb-1">留言总数</h6>
                            <h2 class="stat-value mb-0">{{ stats.contacts_count or 0 }}</h2>
                            <small class="text-danger">
                                <span class="badge bg-danger">{{ stats.unread_contacts or 0 }}</span> 未读
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card stat-card border-0 shadow-sm">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="stat-icon bg-info text-white rounded-3 me-3">
                            <i class="bi bi-images fs-3"></i>
                        </div>
                        <div>
                            <h6 class="stat-label mb-1">媒体文件</h6>
                            <h2 class="stat-value mb-0">{{ stats.media_count or 0 }}</h2>
                            <small class="text-muted">
                                共 {{ stats.media_size or '0 MB' }}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 快速操作 -->
    <div class="row g-3 mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">快速操作</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="/admin/posts/new" class="btn btn-outline-primary">
                            <i class="bi bi-plus-lg me-2"></i>新建文章
                        </a>
                        <a href="/admin/products/new" class="btn btn-outline-success">
                            <i class="bi bi-plus-lg me-2"></i>新建产品
                        </a>
                        <a href="/admin/media" class="btn btn-outline-info">
                            <i class="bi bi-upload me-2"></i>上传媒体文件
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">最新留言</h5>
                </div>
                <div class="card-body">
                    {% if recent_contacts %}
                        <div class="list-group list-group-flush">
                            {% for contact in recent_contacts[:5] %}
                            <a href="/admin/contacts" class="list-group-item list-group-item-action">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ contact.name }}</h6>
                                    <small>{{ contact.created_at.strftime('%m-%d %H:%M') }}</small>
                                </div>
                                <p class="mb-1 text-truncate">{{ contact.message }}</p>
                            </a>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-muted text-center my-3">暂无留言</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

### 第五步：更新路由（Day 3）

#### 5.1 修改 main.py

```python
# admin/app/main.py

from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func

@app.get("/admin/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """管理后台仪表板 - Bootstrap 5 版本"""
    
    # 统计数据
    from app.models import Post, Product, Contact, MediaFile
    
    stats = {
        'posts_count': db.query(func.count(Post.id)).scalar(),
        'products_count': db.query(func.count(Product.id)).scalar(),
        'contacts_count': db.query(func.count(Contact.id)).scalar(),
        'unread_contacts': db.query(func.count(Contact.id)).filter(Contact.status == 'unread').scalar(),
        'media_count': db.query(func.count(MediaFile.id)).scalar(),
    }
    
    # 最新留言
    recent_contacts = db.query(Contact).order_by(Contact.created_at.desc()).limit(5).all()
    
    return templates.TemplateResponse(
        "bootstrap5/pages/dashboard.html",
        {
            "request": request,
            "stats": stats,
            "recent_contacts": recent_contacts
        }
    )
```

---

### 第六步：测试验证（Day 4）

#### 6.1 功能测试清单

- [ ] 顶部导航栏显示正常
- [ ] 侧边栏展开/折叠功能正常
- [ ] 移动端侧边栏显示/隐藏正常
- [ ] 用户下拉菜单功能正常
- [ ] 仪表板统计数据显示正确
- [ ] 页面响应式布局正常
- [ ] 所有图标显示正常
- [ ] 按钮和链接功能正常
- [ ] Toast 提示功能正常
- [ ] 模态框功能正常

#### 6.2 浏览器兼容性测试

- [ ] Chrome (最新版本)
- [ ] Firefox (最新版本)
- [ ] Safari (最新版本)
- [ ] Edge (最新版本)

#### 6.3 响应式测试

- [ ] 桌面端 (≥1200px)
- [ ] 笔记本 (992px - 1199px)
- [ ] 平板竖屏 (768px - 991px)
- [ ] 平板横屏 (576px - 767px)
- [ ] 手机 (<576px)

---

## 📝 开发注意事项

### 1. Git 提交规范

```bash
# 提交消息格式
git commit -m "feat(ui): 添加 Bootstrap 5 基础模板"
git commit -m "refactor(ui): 重构侧边栏组件"
git commit -m "fix(ui): 修复移动端菜单显示问题"
git commit -m "style(ui): 优化按钮样式"
git commit -m "docs(ui): 更新 UI 设计文档"
```

### 2. 代码规范

- HTML: 使用 2 空格缩进
- CSS: 使用 2 空格缩进，遵循 BEM 命名规范
- JavaScript: 使用 2 空格缩进，使用 ES6+ 语法
- Jinja2: 使用 4 空格缩进（与 Python 一致）

### 3. 性能优化

- 使用 CDN 加载 Bootstrap 和 Icons
- 压缩自定义 CSS 和 JS 文件
- 图片使用 WebP 格式（提供 JPEG 回退）
- 启用 Gzip 压缩
- 合理使用浏览器缓存

### 4. 无障碍性

- 为所有图标添加 `aria-label`
- 为交互元素添加适当的 ARIA 属性
- 确保键盘导航可用
- 保持良好的颜色对比度

---

## 🔗 相关文档

- [Bootstrap 5 设计方案](./bootstrap5-design-plan.md)
- [Bootstrap 5 样式文件](./bootstrap5-styles.css)
- [Bootstrap 5 模板示例](./bootstrap5-templates-example.html)
- [Bootstrap 5 官方文档](https://getbootstrap.com/docs/5.3/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

---

## ✅ 完成标准

### Phase 1: 基础框架 ✅
- [x] Bootstrap 5 基础模板
- [x] 顶部导航栏组件
- [x] 左侧导航栏组件
- [x] 主内容区布局
- [x] 响应式适配

### Phase 2: 核心页面 🔄
- [ ] Dashboard 仪表板
- [ ] 登录页面（已有）
- [ ] 文章列表页
- [ ] 文章编辑页

### Phase 3: 全面迁移 ⏳
- [ ] 栏目管理
- [ ] 单页管理
- [ ] 产品管理
- [ ] 媒体库
- [ ] 相册管理
- [ ] 留言管理
- [ ] 站点设置

### Phase 4: 优化完善 ⏳
- [ ] 动画效果
- [ ] 交互优化
- [ ] 性能优化
- [ ] 文档完善

---

**祝开发顺利！** 🎉

如有问题，请联系：maxazure@gmail.com
