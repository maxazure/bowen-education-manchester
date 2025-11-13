# Admin.css 更新说明

## 更新日期
2025-11-13

## 更新概述
基于 `docs/ui-design/bootstrap5-styles.css` 的设计规范，完全重写了 `admin/static/css/admin.css` 文件，确保与 Bootstrap 5 和 base.html 的完美集成。

## 主要更新内容

### 1. CSS 变量系统
- **配色方案**: 中国红 (#c8102e) + 深蓝 (#1e3a8a) + 现代灰
- **完整的设计令牌**: 包括主色、次要色、中性色、功能色、背景色、阴影、尺寸、过渡效果
- **可维护性**: 使用 CSS 变量便于全局主题调整

### 2. 组件样式增强

#### 卡片组件 (Card)
- 圆角边框: 12px
- 柔和阴影: 悬停效果
- 统计卡片变体: 支持多种背景渐变色
- stat-icon: 60x60px 圆角图标容器
- stat-value: 大号数字显示 (32px)

#### 按钮组件 (Button)
- 统一的圆角: 8px
- 完整的按钮变体: primary, secondary, success, danger, outline 等
- 焦点状态: 4px 阴影环
- 按钮组: 边缘圆角处理

#### 表单组件 (Form)
- 输入框圆角: 8px
- 焦点状态: 主色边框 + 阴影环
- 表单验证: 成功/错误状态样式
- 开关按钮: 44x24px 圆角样式
- 输入组: 完整的组合样式

#### 表格组件 (Table)
- 表头背景: 浅灰色
- 悬停效果: 行高亮
- 响应式包装: 圆角容器 + 阴影
- 表格操作按钮: 专用样式类

#### 徽章组件 (Badge)
- 圆角: 6px
- 多种颜色变体: primary, success, danger, warning, info
- 浅色变体: 用于背景显示

### 3. 页面布局组件

#### 页面标题区 (Page Header)
- page-title: 28px 大标题
- page-subtitle: 14px 副标题
- 底部边框分隔

#### 面包屑导航 (Breadcrumb)
- 透明背景
- 斜杠分隔符
- 链接颜色: 次要文本色

### 4. 交互组件

#### 模态框 (Modal)
- 圆角: 12px
- 大阴影效果
- 头部/底部: 浅灰背景

#### 下拉菜单 (Dropdown)
- 圆角: 8px
- 项目悬停: 浅灰背景
- 图标对齐: 20px 宽度

#### 分页组件 (Pagination)
- 独立圆角按钮: 8px
- 间距: 4px gap
- 活动状态: 主色背景

#### Toast 提示
- 固定位置: 右上角
- 最小宽度: 300px
- 颜色变体: success, danger, warning, info

### 5. 特定页面组件

#### 登录页面
- login-container: 居中布局 + 渐变背景
- login-box: 白色卡片 + 大阴影
- 最大宽度: 420px

#### 仪表板
- dashboard-stats: 响应式网格布局
- 自动适配: 最小 250px 列宽

#### 空状态 (Empty State)
- 居中布局
- 64px 大图标
- 引导文案

#### 上传区域 (Upload Area)
- 虚线边框
- 悬停/拖拽: 主色边框 + 浅色背景
- 48px 大图标

#### 图片网格 (Image Grid)
- 响应式网格: 最小 150px
- 1:1 宽高比
- 悬停: 遮罩层显示

#### 标签输入 (Tag Input)
- 弹性布局
- 标签项: 主色浅背景
- 焦点: 边框高亮

### 6. 动画效果

#### 内置动画
- fadeIn: 淡入 + 向上移动
- slideInRight: 从右滑入
- slideInLeft: 从左滑入
- scaleIn: 缩放淡入
- hover-lift: 悬停提升效果

#### 过渡效果
- 快速: 0.15s
- 基础: 0.3s
- 缓慢: 0.5s

### 7. 响应式设计

#### 断点适配
- **1200px 以下**: 标题 24px, 统计卡片 220px
- **992px 以下**: 标题 22px, 卡片 16px padding, 表格 13px
- **768px 以下**: 标题 20px, 按钮全宽, 统计卡片单列
- **576px 以下**: 统计图标 50px, 统计值 28px

#### 移动端优化
- Toast 容器: 左右 10px
- 图片网格: 最小 100px
- 按钮组: 保持原宽度

### 8. 辅助功能

#### 工具类
- 圆角: rounded-lg, rounded-md
- 阴影: shadow-sm, shadow-md, shadow-lg, shadow-xl
- 文本: text-muted, text-dark
- 背景: bg-light-gray
- 间距: gap-2, gap-3, gap-4

#### 无障碍支持
- sr-only: 屏幕阅读器专用
- focus-visible: 焦点轮廓
- skip-link: 跳过导航链接

### 9. 打印样式
- 隐藏: 侧边栏、顶栏、按钮、分页等
- 优化: 卡片边框、表格分页
- 白色背景: 打印友好

### 10. 暗色模式支持
- 预留暗色模式媒体查询
- 可在未来扩展

## 移除的旧样式
- 移除了旧的基础样式和简单布局
- 移除了冲突的登录页面样式
- 移除了过时的仪表板样式

## 与 base.html 的协调
- CSS 变量与 base.html 中的 `<style>` 标签完全一致
- 不影响 base.html 中定义的布局结构（topbar, sidebar, main-content）
- 只提供增强样式，不覆盖核心布局逻辑

## 文件统计
- **总行数**: 1430 行
- **CSS 变量**: 26 个
- **样式分类**: 24 个主要部分
- **组件样式**: 覆盖所有 Bootstrap 5 组件

## 使用建议

### 1. 引入顺序
```html
<!-- Bootstrap CSS -->
<link href="bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap Icons -->
<link href="bootstrap-icons.css" rel="stylesheet">

<!-- 自定义样式 (admin.css) -->
<link rel="stylesheet" href="/static/css/admin.css">
```

### 2. 常用组件示例

#### 统计卡片
```html
<div class="card stat-card bg-primary-light">
  <div class="card-body d-flex align-items-center">
    <div class="stat-icon bg-primary text-white">
      <i class="bi bi-people"></i>
    </div>
    <div class="ms-3">
      <div class="stat-value">1,234</div>
      <div class="stat-label">总用户数</div>
      <div class="stat-change text-success">
        <i class="bi bi-arrow-up"></i> 12.5%
      </div>
    </div>
  </div>
</div>
```

#### 按钮组合
```html
<div class="d-flex gap-2">
  <button class="btn btn-primary">保存</button>
  <button class="btn btn-outline-secondary">取消</button>
  <button class="btn btn-outline-danger">删除</button>
</div>
```

#### 空状态
```html
<div class="empty-state">
  <i class="bi bi-inbox"></i>
  <h3>暂无数据</h3>
  <p>还没有添加任何内容</p>
  <button class="btn btn-primary">添加内容</button>
</div>
```

## 注意事项

1. **CSS 变量优先**: 尽量使用 CSS 变量而不是硬编码颜色
2. **Bootstrap 优先**: 优先使用 Bootstrap 5 类，自定义样式作为补充
3. **响应式优先**: 所有组件都考虑了移动端适配
4. **动画节制**: 只在必要时使用动画，避免过度
5. **可访问性**: 保持良好的对比度和键盘导航

## 兼容性
- Bootstrap 5.3.0+
- 现代浏览器 (Chrome, Firefox, Safari, Edge)
- 移动设备完全支持

## 下一步计划
- [ ] 添加暗色模式完整支持
- [ ] 扩展更多自定义组件
- [ ] 优化打印样式
- [ ] 添加更多动画效果
