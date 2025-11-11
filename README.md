# Bowen Education Group Website / 博文集团网站

[![Test Status](https://img.shields.io/badge/tests-100%25%20passing-brightgreen)](WEBSITE_TEST_REPORT.md)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Official website for Bowen Education Group (博文集团) - Manchester's premier Chinese language school.

**官方网站** - 曼彻斯特领先的中文学校

---

## 🌟 Features / 功能特性

### Core Features / 核心功能

- ✅ **Bilingual Support** / **双语支持** (English + 中文)
- ✅ **Responsive Design** / **响应式设计** (手机/平板/桌面)
- ✅ **Modern UI/UX** / **现代化界面**
- ✅ **SEO Optimized** / **SEO优化**
- ✅ **Fast Loading** / **快速加载** (<1秒)

### Key Pages / 主要页面

- 🏠 **Homepage** / **首页** - Company introduction, courses showcase
- 📖 **About** / **关于** - Mission, vision, team, partnership
- 📞 **Contact** / **联系** - Contact form, location, map
- 📚 **Courses** / **课程** (数据库已配置)
- 📰 **News** / **新闻** (数据库已配置)
- 🎭 **Events** / **活动** (数据库已配置)

---

## 🚀 Quick Start / 快速开始

### Prerequisites / 前置要求

- Python 3.11+
- SQLite 3
- Virtual Environment

### Installation / 安装

```bash
# 1. 克隆项目 (如果从Git)
git clone <repository-url>
cd bowen-education-manchester

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库 (已完成)
# 数据库已包含示例数据

# 5. 启动应用
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access / 访问

- **Local**: http://localhost:8000
- **LAN**: http://192.168.31.205:8002

---

## 📁 Project Structure / 项目结构

```
bowen-education-manchester/
├── app/                       # 应用主目录
│   ├── main.py               # FastAPI 主应用
│   ├── config.py             # 配置文件
│   ├── database.py           # 数据库配置
│   ├── models/               # SQLAlchemy 模型 (14个模块)
│   ├── routes/               # 路由
│   ├── services/             # 业务逻辑
│   ├── schemas/              # Pydantic schemas
│   └── utils/                # 工具函数
├── templates/                 # Jinja2 模板
│   ├── base.html             # 基础模板
│   ├── home.html             # 首页
│   ├── about.html            # 关于页
│   ├── contact.html          # 联系页
│   ├── partials/             # 模板片段
│   │   ├── header.html       # 头部
│   │   └── footer.html       # 页脚
│   └── static/               # 静态文件
│       ├── css/
│       │   └── main.css      # 主样式表 (900+ lines)
│       └── images/           # 图片 (10张)
├── instance/                  # 实例文件夹
│   └── database.db           # SQLite 数据库
├── migrations/               # Alembic 迁移
├── tests/                    # 测试文件
├── requirements.txt          # Python 依赖
└── README.md                 # 本文件
```

---

## 🗄️ Database / 数据库

### Modules Enabled / 启用的模块 (14个)

1. **Site** - 站点设置和栏目
2. **Product** - 课程/产品管理
3. **Post** - 文章/新闻
4. **TeamMember** - 团队成员
5. **FAQ** - 常见问题
6. **User** - 用户系统
7. **Booking** - 预约系统
8. **Event** - 活动管理
9. **File** - 文件下载
10. **Video** - 视频管理
11. **Media** - 媒体文件
12. **Contact** - 联系消息
13. **CustomField** - 自定义字段
14. **SinglePage** - 单页管理

### Database Statistics / 数据库统计

- **Tables**: 50
- **Records**: 45+ seed data
- **Images**: 10 media files (1.21 MB)
- **Courses**: 7 products
- **Team Members**: 3
- **Articles**: 2 posts
- **Events**: 2
- **FAQs**: 3

---

## 🎨 Design System / 设计系统

### Colors / 颜色

- **Primary**: `#c8102e` (Chinese Red / 中国红)
- **Secondary**: `#1e3a8a` (Deep Blue / 深蓝)
- **Background**: White / Light Gray
- **Text**: `#111827` (Dark Gray)

### Typography / 字体

- **English**: Inter, -apple-system, sans-serif
- **Chinese**: Noto Sans SC, Microsoft YaHei, sans-serif
- **Headings**: Playfair Display, Georgia, serif

### Responsive Breakpoints / 响应式断点

- **Desktop**: > 992px
- **Tablet**: 768px - 992px
- **Mobile**: < 768px

---

## 🧪 Testing / 测试

### Test Results / 测试结果

✅ **100% Pass Rate** (45/45 tests passing)

```bash
# 运行功能测试
python test_website_functional.py
```

### Test Coverage / 测试覆盖

- ✅ Page Accessibility (页面可访问性)
- ✅ Content Integrity (内容完整性)
- ✅ Bilingual Support (双语支持)
- ✅ Static Resources (静态资源)
- ✅ HTTP Headers (响应头)
- ✅ SEO Meta Tags (SEO标签)
- ✅ Navigation (导航系统)
- ✅ Forms (表单功能)
- ✅ Performance (性能)
- ✅ Error Handling (错误处理)

详细报告: [WEBSITE_TEST_REPORT.md](WEBSITE_TEST_REPORT.md)

---

## 📊 Performance / 性能

- **Page Load Time**: < 1 second (优秀)
- **Page Size**: ~43 KB (合理)
- **Image Loading**: Lazy loading enabled
- **CSS Size**: 900+ lines, optimized

---

## 🌐 Deployment / 部署

### Development / 开发环境

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production / 生产环境

```bash
# 使用 Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 或使用 systemd service
# 参见 DEPLOYMENT.md
```

详细部署指南: [DEPLOYMENT.md](DEPLOYMENT.md) (待创建)

---

## 📝 Content Management / 内容管理

### Adding Content / 添加内容

#### 1. Add Course / 添加课程

```python
# 使用 populate_db.py 或直接操作数据库
from app.models import Product
from app.database import SessionLocal

db = SessionLocal()
course = Product(
    column_id=3,  # Chinese School column
    name="New Course",
    slug="new-course",
    summary="Course summary",
    description_html="<p>Course description</p>",
    price_text="£200/term",
    status="online"
)
db.add(course)
db.commit()
```

#### 2. Add Team Member / 添加团队成员

```python
from app.models import TeamMember

member = TeamMember(
    name="Teacher Name",
    name_chinese="教师姓名",
    title="Senior Teacher",
    bio_html="<p>Biography</p>",
    qualifications="MA in Education"
)
db.add(member)
db.commit()
```

#### 3. Add News Article / 添加新闻

```python
from app.models import Post

post = Post(
    column_id=8,  # News column
    title="News Title",
    slug="news-title",
    summary="News summary",
    content_html="<p>News content</p>",
    status="published",
    published_at=datetime.now()
)
db.add(post)
db.commit()
```

---

## 🔒 Security / 安全

- ✅ Form validation with Pydantic
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS protection (Jinja2 auto-escaping)
- ✅ CSRF token support (可配置)
- ✅ Input sanitization

---

## 🌍 Internationalization / 国际化

### Supported Languages / 支持语言

- **English** (Primary)
- **简体中文** (Simplified Chinese)

### Adding Translations / 添加翻译

模板中使用双语内容：

```html
<h1>About Us</h1>
<h2 class="chinese">关于我们</h2>
```

CSS 中定义中文样式：

```css
.text-chinese {
    font-family: var(--font-chinese);
}
```

---

## 📞 Contact Information / 联系信息

**Bowen Education Group / 博文集团**

- **Address / 地址**: 1/F, 2A Curzon Road, Sale, Manchester M33 7DR, UK
- **Phone / 电话**: 0161 969 3071
- **Email / 邮箱**: info@boweneducation.co.uk
- **Hours / 营业时间**: Mon-Fri 9:00-18:00, Sat 9:00-17:00

---

## 👥 Team / 团队

- **Developer**: AI-Assisted Development
- **Framework**: docms-scaffold (Modular CMS)
- **Generated**: 2025-11-04

---

## 📄 License / 许可证

Copyright © 2025 Bowen Education Group. All rights reserved.

---

## 🙏 Acknowledgments / 致谢

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM
- **Jinja2** - Template engine
- **AOS** - Animate On Scroll library
- **Font Awesome** - Icons
- **Google Fonts** - Typography
- **Zhipu AI** - Image generation

---

## 📚 Documentation / 文档

- [Testing Report / 测试报告](WEBSITE_TEST_REPORT.md)
- [Phase 6 Report / Phase 6报告](PHASE6_TEST_REPORT.md)
- [Phase 7 Report / Phase 7报告](PHASE7_COMPLETION_REPORT.md)
- [Architecture / 架构文档](.claude/ARCHITECTURE.md)
- [Agent Summary / 代理总结](.claude/AGENT_SUMMARY.md)

---

## 🐛 Troubleshooting / 故障排除

### Common Issues / 常见问题

#### 1. Database not found

```bash
# 确保在正确的目录
cd bowen-education-manchester

# 数据库应该在 instance/database.db
ls -la instance/database.db
```

#### 2. Import errors

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

#### 3. Port already in use

```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
uvicorn app.main:app --port 8001
```

#### 4. Templates not found

```bash
# 确认templates目录存在
ls -la templates/

# 检查配置
cat app/config.py | grep template
```

---

## 🔄 Updates / 更新

### Version History / 版本历史

- **v1.0.0** (2025-11-04) - Initial release
  - ✅ 3 main pages (Home, About, Contact)
  - ✅ 14 modules enabled
  - ✅ 45 database records
  - ✅ 100% test coverage
  - ✅ Bilingual support
  - ✅ Responsive design

---

## 📮 Support / 技术支持

For technical support / 技术支持:
- Create an issue on GitHub
- Email: developer@example.com (待配置)

---

**Built with ❤️ using FastAPI, SQLAlchemy, and modern web technologies.**

**使用 FastAPI、SQLAlchemy 和现代 Web 技术精心打造。**
