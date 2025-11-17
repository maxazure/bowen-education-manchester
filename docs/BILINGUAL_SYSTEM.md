# 双模板系统文档

## 📋 系统概述

博文教育网站现已支持**双模板系统**，提供中英文独立版本：

- **中英混排版** (`/` 或 `/zh/`): 面向华人社区，保留中英文双语内容
- **纯英文版** (`/en/`): 面向英语社区，完全英文界面

## 🏗️ 架构设计

### 目录结构

```
templates/
├── zh/                    # 中英混排模板
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   └── partials/
│       ├── header.html
│       └── footer.html
├── en/                    # 纯英文模板
│   ├── base.html          (移除了中文字体)
│   ├── home.html
│   ├── about.html
│   └── partials/
│       ├── header.html    (移除了中文站点名称)
│       └── footer.html
└── static/                # 共享静态资源
    ├── css/
    ├── js/
    └── images/
```

### URL 路由规则

| URL 路径 | 模板目录 | 语言 | 描述 |
|---------|---------|------|------|
| `/` | `templates/zh/` | zh | 首页（中英混排） |
| `/zh/` | `templates/zh/` | zh | 首页（显式中文） |
| `/about` | `templates/zh/` | zh | 关于页面（中英混排） |
| `/en/` | `templates/en/` | en | 英文首页 |
| `/en/about` | `templates/en/` | en | 英文关于页面 |
| `/en/school` | `templates/en/` | en | 英文学校页面 |

### 数据库设计

- **单一数据源**: 只维护一份数据库内容
- **字段策略**: 利用现有的中英文字段（如 `title`, `title_chinese`）
- **内容过滤**: 英文版自动过滤中文内容标记

## 🔧 技术实现

### 1. 模板引擎选择

```python
# app/routes/frontend_i18n.py

def get_template_engine(lang: str = "zh") -> Jinja2Templates:
    """根据语言代码返回对应的模板引擎"""
    template_base = Path(settings.template_dir)
    lang_dir = template_base / lang

    templates = Jinja2Templates(directory=str(lang_dir))

    # 为英文模板添加过滤器
    if lang == "en":
        templates.env.filters["remove_chinese"] = remove_chinese
        templates.env.filters["format_title"] = lambda title: format_bilingual_title(title, "en")

    return templates
```

### 2. 内容过滤器

```python
# app/utils/template_filters.py

def remove_chinese(html: str) -> str:
    """从HTML内容中移除中文内容"""
    # 移除带有 chinese 类名的标签
    html = re.sub(r'<([a-z][a-z0-9]*)\s+[^>]*class=["\'][^"\']*chinese[^"\']*["\'][^>]*>.*?</\1>', '', html, flags=re.DOTALL)

    # 移除独立中文段落
    html = re.sub(r'<br\s*/?\s*>[\s\r\n]*<span[^>]*>[\u4e00-\u9fff\s]+</span>', '', html)

    return html.strip()
```

### 3. 路由处理

```python
# app/routes/frontend.py

@router.get("/", response_class=HTMLResponse)
@router.get("/zh/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    """中英混排版首页"""
    lang = "zh"
    context = get_base_context(request, db, lang=lang)
    templates_engine = get_template_engine(lang)
    # ...
    return templates_engine.TemplateResponse("home.html", context)


@router.get("/en/", response_class=HTMLResponse)
async def homepage_en(request: Request, db: Session = Depends(get_db)):
    """纯英文版首页"""
    lang = "en"
    context = get_base_context(request, db, lang=lang)
    templates_engine = get_template_engine(lang)
    # ...
    return templates_engine.TemplateResponse("home.html", context)
```

## 🎨 模板差异

### 中英混排版 (`templates/zh/`)

#### base.html
```html
<!-- 包含中文字体 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">

<!-- 显示中英文站点名称 -->
<span class="logo-text">
    <strong>{{ site.site_name }}</strong>
    <small>{{ site.site_name_chinese }}</small>
</span>

<!-- 语言切换到英文 -->
<a href="/en{{ request.url.path }}">English</a>
```

#### header.html
- 显示完整的中英文品牌信息
- "English" 切换按钮

### 纯英文版 (`templates/en/`)

#### base.html
```html
<!-- 只使用英文字体 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- 只显示英文站点名称 -->
<span class="logo-text">
    <strong>{{ site.site_name }}</strong>
</span>

<!-- 语言切换到中文 -->
<a href="{{ request.url.path|replace('/en', '') }}">中文</a>
```

#### header.html
- 移除中文品牌名称
- "中文" 切换按钮

## 🔍 SEO 优化

### Hreflang 标签

两个版本都包含完整的 hreflang 标签：

```html
<!-- 在 base.html 中 -->
<link rel="alternate" hreflang="en" href="https://boweneducation.co.uk/en{{ request.url.path }}" />
<link rel="alternate" hreflang="zh" href="https://boweneducation.co.uk{{ request.url.path }}" />
<link rel="alternate" hreflang="x-default" href="https://boweneducation.co.uk{{ request.url.path }}" />
```

### 优势

1. **搜索引擎识别**: Google 能正确识别语言版本
2. **避免重复内容惩罚**: 明确标记语言关系
3. **改善用户体验**: 搜索结果显示正确语言版本

## 📱 管理后台

### 零改动策略

管理后台**完全不需要修改**，继续使用现有方式：

1. **编辑内容**: 管理员按现有方式编辑中英文内容
2. **自动适配**: 前台根据模板版本自动显示对应内容
3. **统一管理**: 一处编辑，两个版本同步更新

### 内容管理建议

在管理后台编辑时：

- **标题**: 英文标题作为主要字段
- **中文内容**: 使用带 `class="text-chinese"` 的标签包裹
- **双语段落**: 英文在前，中文标记为 `chinese` 类

示例：
```html
<h2>About Us</h2>
<p class="text-chinese">关于我们</p>

<p>We provide professional Chinese education.</p>
<p class="text-chinese">我们提供专业的中文教育。</p>
```

## 🚀 使用指南

### 访问不同版本

- **中英混排版**: `https://boweneducation.co.uk/`
- **纯英文版**: `https://boweneducation.co.uk/en/`

### 语言切换

- 在页面右上角点击语言切换按钮
- 自动保持当前页面路径

### 开发环境测试

```bash
# 启动开发服务器
source venv/bin/activate
uvicorn app.main:app --reload

# 访问测试
# 中文版: http://localhost:8000/
# 英文版: http://localhost:8000/en/
```

## 📊 性能考虑

### 优化措施

1. **共享静态资源**: CSS、JS、图片只加载一次
2. **模板缓存**: Jinja2 自动缓存编译后的模板
3. **按需加载字体**: 英文版不加载中文字体，减少加载时间

### 预期效果

- **中英混排版**: 页面大小与原版相同
- **纯英文版**: 减少约100KB（中文字体）

## 🔧 扩展性

### 添加新页面

1. 在 `templates/zh/` 创建中英混排模板
2. 复制到 `templates/en/` 并移除中文内容
3. 路由会自动支持两个版本

### 添加新语言

如需添加其他语言（如法语）：

1. 创建 `templates/fr/` 目录
2. 在 `frontend_i18n.py` 添加语言支持
3. 添加对应的路由：`@router.get("/fr/")`

## 📝 维护注意事项

1. **同步更新**: 修改模板时记得同步更新 zh/ 和 en/ 版本
2. **中文标记**: 新增中文内容时使用 `class="text-chinese"` 标记
3. **测试两个版本**: 发布前测试中英文版本都正常工作
4. **URL一致性**: 确保中英文版本的URL结构一致

## 🎯 未来改进

- [ ] 使用内容过滤器自动处理更多HTML模板
- [ ] 添加语言偏好Cookie记住用户选择
- [ ] 实现更智能的内容过滤算法
- [ ] 支持更多语言版本
- [ ] 添加管理后台预览不同语言版本功能

## 📞 技术支持

如有问题，请参考：
- 路由配置: `app/routes/frontend.py`
- 过滤器: `app/utils/template_filters.py`
- 模板: `templates/zh/` 和 `templates/en/`

---

**实施日期**: 2025-11-16
**开发者**: maxazure
**Git Commit**: 22cf108
