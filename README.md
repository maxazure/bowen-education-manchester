# Bowen Education Group Website / 博文教育集团网站

[![Python](https://img.shields.io/badge/python-3.13.2-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.44-red)](https://www.sqlalchemy.org/)

Official website for Bowen Education Group (博文教育集团) - Manchester's premier Chinese language school.

**官方网站** - 曼彻斯特领先的中文学校

---

## 🌟 Features / 功能特性

- ✅ **Bilingual Support** / **双语支持** (English + 中文)
- ✅ **Unified Admin & Frontend** / **统一管理后台与前台**
- ✅ **Responsive Design** / **响应式设计**
- ✅ **Modern UI/UX** / **现代化界面**
- ✅ **SEO Optimized** / **SEO优化**
- ✅ **Content Management** / **内容管理系统**

---

## 🚀 Quick Start / 快速开始

### Prerequisites / 前置要求

- Python 3.13+
- SQLite 3
- Virtual Environment (venv)

### Installation / 安装

```bash
# 1. 克隆项目
git clone https://github.com/maxazure/bowen-education-manchester.git
cd bowen-education-manchester

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用 (前台 + 管理后台)
uvicorn app.main:app --reload --port 8000
```

### Access / 访问

- **前台网站**: http://localhost:8000
  - 中文首页: http://localhost:8000/zh/
  - 英文首页: http://localhost:8000/en/

- **管理后台**: http://localhost:8000/admin
  - 登录页: http://localhost:8000/admin/login
  - 产品管理: http://localhost:8000/admin/products
  - 文章管理: http://localhost:8000/admin/posts
  - 单页管理: http://localhost:8000/admin/pages

---

## 📁 Project Structure / 项目结构

```
bowen-education-manchester/
├── app/                       # 应用主目录
│   ├── main.py               # FastAPI 主应用 (前台+后台统一入口)
│   ├── database.py           # 数据库配置
│   ├── models/               # SQLAlchemy 模型
│   ├── routes/               # 前台路由
│   └── services/             # 业务逻辑
├── admin/                     # 管理后台
│   ├── app/                  # 后台应用
│   │   ├── routers/         # 后台路由
│   │   └── blocks/          # 页面区块管理
│   └── templates/           # 后台模板
├── templates/                 # 前台模板
│   ├── zh/                   # 中文模板
│   ├── en/                   # 英文模板
│   ├── components/           # 组件
│   └── static/               # 静态资源
│       ├── css/
│       ├── js/
│       └── images/
├── instance/                  # 实例文件夹
│   └── database.db           # SQLite 数据库
├── upload/                    # 上传文件目录
├── requirements.txt          # Python 依赖
├── TODO.md                   # 任务清单
└── README.md                 # 本文件
```

---

## 🗄️ Database / 数据库

### Core Models / 核心模型

1. **Site** - 站点设置和栏目
2. **Product** - 课程/产品管理 (支持双语)
3. **Post** - 文章/新闻 (支持双语)
4. **SinglePage** - 单页管理 (支持双语)
5. **Event** - 活动管理 (支持双语)
6. **TeamMember** - 团队成员
7. **FAQ** - 常见问题
8. **Media** - 媒体文件
9. **Contact** - 联系消息
10. **PageLayout** - 页面布局系统

### Bilingual Support / 双语支持

已实现双语字段的模型:
- ✅ **Product** - 产品/课程 (6个英文字段)
- ✅ **Post** - 文章/新闻 (6个英文字段)
- ✅ **SinglePage** - 单页内容 (6个英文字段)
- ✅ **Event** - 活动 (6个英文字段)

所有英文字段使用 `_en` 后缀命名,如 `name_en`, `summary_en`, `description_html_en` 等。

---

## 🎨 Design System / 设计系统

### Colors / 颜色

- **Primary**: `#c8102e` (Chinese Red / 中国红)
- **Secondary**: `#1e3a8a` (Deep Blue / 深蓝)
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

## 🌐 Deployment / 部署

### Development / 开发环境

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动开发服务器 (支持热重载)
uvicorn app.main:app --reload --port 8000
```

### Production / 生产环境

```bash
# 使用 Gunicorn + Uvicorn Worker
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 🔧 Admin Features / 管理后台功能

### Content Management / 内容管理

- ✅ **产品管理** - 双语 Tab 编辑界面
- ✅ **文章管理** - 双语 Tab 编辑界面
- ✅ **单页管理** - 双语 Tab 编辑界面
- ✅ **媒体管理** - 图片上传和管理
- ✅ **栏目管理** - 网站结构管理
- ✅ **页面布局** - 可视化布局编辑器

### Admin Interface Features / 后台界面特性

- Bootstrap 5 响应式设计
- Markdown 编辑器 (EasyMDE)
- 双语内容分离编辑
- 图片上传和选择
- 表单验证
- 自动保存功能

---

## 🌍 Internationalization / 国际化

### Language Support / 语言支持

- **English** - 完整英文界面
- **简体中文** - 完整中文界面

### Fallback Pattern / 回退模式

前台模板使用自动回退:
```jinja2
{{ product.name_en or product.name }}
{{ post.title_en or post.title }}
```

如果英文内容不存在,自动显示中文内容。

---

## 📞 Contact Information / 联系信息

**Bowen Education Group / 博文教育集团**

- **Address / 地址**: 1/F, 2A Curzon Road, Sale, Manchester M33 7DR, UK
- **Phone / 电话**: 0161 969 3071
- **Email / 邮箱**: info@boweneducation.co.uk
- **Hours / 营业时间**: Mon-Fri 9:00-18:00, Sat 9:00-17:00

---

## 🐛 Troubleshooting / 故障排除

### Common Issues / 常见问题

#### Port already in use / 端口被占用

```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
uvicorn app.main:app --port 8001
```

#### Database not found / 数据库未找到

```bash
# 确保在正确的目录
cd bowen-education-manchester

# 检查数据库文件
ls -la instance/database.db
```

#### Import errors / 导入错误

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

---

## 🔄 Updates / 更新历史

### Latest Updates / 最新更新

- **v1.2.0** (2025-11-16) - Bilingual Content Support
  - ✅ Product 模型双语支持 (6个英文字段)
  - ✅ Event 模型双语支持 (6个英文字段)
  - ✅ 产品管理后台 Tab 双语编辑界面
  - ✅ 英文模板自动回退逻辑
  - ✅ 数据库迁移脚本
  - ✅ 统一"博文教育集团"品牌名称

- **v1.1.0** (2025-11-11) - Project Optimization
  - ✅ 前台后台应用合并
  - ✅ 静态资源统一管理
  - ✅ 上传目录优化

- **v1.0.0** (2025-11-04) - Initial Release
  - ✅ 基础功能实现
  - ✅ 14 个模块启用
  - ✅ 响应式设计

---

## 📚 Documentation / 文档

- [TODO.md](TODO.md) - 项目任务清单和开发历史

---

## 📄 License / 许可证

Copyright © 2025 Bowen Education Group. All rights reserved.

---

**Built with ❤️ using FastAPI, SQLAlchemy, and modern web technologies.**

**使用 FastAPI、SQLAlchemy 和现代 Web 技术精心打造。**
