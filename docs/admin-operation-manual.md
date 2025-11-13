# 博文教育管理后台 - 操作手册

**版本**: v1.0.0
**更新日期**: 2025-11-13
**作者**: maxazure

---

## 📖 目录

1. [快速开始](#快速开始)
2. [系统要求](#系统要求)
3. [安装配置](#安装配置)
4. [启动应用](#启动应用)
5. [功能使用](#功能使用)
6. [常见问题](#常见问题)
7. [故障排除](#故障排除)
8. [维护指南](#维护指南)

---

## 🚀 快速开始

### 最快5分钟上手

```bash
# 1. 进入项目目录
cd /path/to/bowen-education-manchester

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 运行数据库迁移（仅首次）
python scripts/migrate_media_file.py

# 4. 设置环境变量并启动
export PYTHONPATH=$(pwd)
export TESTING=1  # 临时跳过认证
python -m uvicorn admin.app.main:app --host 0.0.0.0 --port 8001 --reload

# 5. 访问管理后台
# 浏览器打开: http://localhost:8001/admin/
```

---

## 💻 系统要求

### 硬件要求

- **CPU**: 2核心及以上
- **内存**: 4GB 及以上
- **磁盘**: 10GB 可用空间

### 软件要求

- **操作系统**: macOS / Linux / Windows
- **Python**: 3.10 或更高版本（推荐 3.13）
- **数据库**: SQLite（开发）/ PostgreSQL（生产）
- **浏览器**: Chrome / Firefox / Safari / Edge（最新版本）

---

## 📦 安装配置

### 1. 克隆项目

```bash
git clone <repository-url>
cd bowen-education-manchester
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件（或使用环境变量）：

```bash
# 必需配置
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///./bowen_education.db

# 可选配置
DEBUG=True
TESTING=1  # 跳过认证（开发环境）
```

### 5. 初始化数据库

```bash
# 运行迁移脚本
python scripts/migrate_media_file.py
```

### 6. 创建管理员账户（待实现）

```bash
# TODO: 创建管理员账户脚本
# python scripts/create_admin.py --username admin --password admin123
```

---

## 🎯 启动应用

### 开发环境启动

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 设置环境变量
export PYTHONPATH=/path/to/bowen-education-manchester
export TESTING=1

# 3. 启动应用（自动重载）
python -m uvicorn admin.app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 生产环境启动

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 设置环境变量
export PYTHONPATH=/path/to/bowen-education-manchester
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:password@localhost/dbname

# 3. 启动应用（使用 Gunicorn）
gunicorn admin.app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001 \
  --access-logfile - \
  --error-logfile -
```

### 验证启动成功

```bash
# 检查健康状态
curl http://localhost:8001/health

# 预期输出: {"status":"ok"}
```

---

## 📱 功能使用

### 1. 登录系统

**URL**: http://localhost:8001/admin/login

**默认账号**（待创建）:
- 用户名: `admin`
- 密码: `admin123`

**临时方案**: 设置 `TESTING=1` 环境变量跳过登录

---

### 2. 仪表板

**URL**: http://localhost:8001/admin/

**功能**:
- 查看系统统计数据
- 快速访问各功能模块
- 显示最近操作记录

**显示数据**:
- 用户总数
- 文章总数
- 相册总数

---

### 3. 媒体库管理

**URL**: http://localhost:8001/admin/media

#### 3.1 上传文件

**操作步骤**:
1. 点击"上传文件"按钮
2. 选择一个或多个文件
3. 等待上传完成
4. 查看上传结果

**支持格式**:
- 图片: JPG, PNG, GIF, WebP
- 文档: PDF, DOC, DOCX
- 其他: 根据配置

**大小限制**: 默认 10MB

#### 3.2 管理文件

**操作**:
- **查看详情**: 点击文件查看完整信息
- **编辑信息**: 修改标题、Alt文本、说明
- **删除文件**: 删除不需要的文件
- **复制URL**: 获取文件访问链接

**批量操作**:
- 批量选择文件
- 批量删除

---

### 4. 栏目管理

**URL**: http://localhost:8001/admin/columns

#### 4.1 创建栏目

**操作步骤**:
1. 点击"新建栏目"按钮
2. 填写栏目信息:
   - **栏目名称**: 必填
   - **Slug**: 自动生成或手动输入
   - **栏目类型**: CUSTOM / SINGLE_PAGE / POST
   - **父级栏目**: 可选
   - **图标**: 可选
   - **排序**: 数字，越小越靠前
3. 设置显示选项:
   - 显示在导航
   - 显示在底部
   - 是否启用
4. 配置Hero区域（可选）:
   - Hero 标题
   - Hero 标语
   - Hero 按钮
5. 点击"保存"

#### 4.2 管理栏目树

**拖拽排序**:
1. 拖动栏目项的"⋮⋮"图标
2. 移动到目标位置
3. 释放鼠标完成排序

**父子关系**:
- 子栏目会缩进显示
- 可以通过编辑修改父级

**批量操作**:
- 批量启用/禁用
- 批量删除

---

### 5. 单页管理

**URL**: http://localhost:8001/admin/pages

#### 5.1 创建单页

**操作步骤**:
1. 点击"新建单页"
2. 填写基本信息:
   - **标题**: 必填
   - **Slug**: 自动生成
   - **所属栏目**: 选择栏目
3. 编辑内容:
   - 使用 Markdown 编辑器
   - 支持实时预览
   - 插入图片和链接
4. 设置SEO:
   - SEO标题
   - SEO描述
   - 关键词
5. 选择发布状态:
   - 草稿
   - 已发布
6. 点击"保存"

#### 5.2 Markdown 语法

```markdown
# 一级标题
## 二级标题
### 三级标题

**粗体** *斜体*

- 列表项1
- 列表项2

[链接文字](https://example.com)

![图片描述](图片URL)

`代码`

​```
代码块
​```
```

---

### 6. 文章管理

**URL**: http://localhost:8001/admin/posts

#### 6.1 创建文章

**操作步骤**:
1. 点击"新建文章"
2. 填写文章信息:
   - **标题**: 必填
   - **作者**: 自动填充
   - **摘要**: 可选
   - **封面图**: 从媒体库选择
3. 选择分类:
   - 支持多栏目分类
   - 至少选择一个
4. 编辑正文:
   - Markdown 编辑器
   - 实时预览
5. 设置发布:
   - **状态**: 草稿/已发布
   - **发布时间**: 可定时发布
   - **置顶**: 是/否
6. 点击"保存"

#### 6.2 文章筛选

**筛选条件**:
- 按栏目筛选
- 按状态筛选（草稿/已发布）
- 按作者筛选
- 关键词搜索

**排序方式**:
- 按创建时间
- 按更新时间
- 按发布时间
- 按浏览量

---

### 7. 产品管理

**URL**: http://localhost:8001/admin/products

#### 7.1 创建产品

**操作步骤**:
1. 点击"新建产品"
2. 填写基本信息:
   - **产品名称**: 必填
   - **简介**: 可选
   - **详细介绍**: Markdown
3. 设置价格:
   - **原价**: 可选
   - **现价**: 必填
   - **促销价**: 可选
4. 选择分类:
   - 支持多分类
5. 配置属性:
   - 供货状态
   - 库存数量
   - SKU
6. 上传图片:
   - 产品主图
   - 详情图（多张）
7. 点击"保存"

#### 7.2 价格管理

**价格类型**:
- **原价**: 划线价
- **现价**: 售价
- **促销价**: 限时特价

**显示规则**:
- 有促销价时显示促销价
- 无促销价时显示现价
- 原价用于对比

---

### 8. 站点设置

**URL**: http://localhost:8001/admin/settings

#### 8.1 基本设置

**配置项**:
- 网站名称
- 网站标题
- 网站描述
- 关键词
- ICP备案号
- 版权信息

#### 8.2 联系信息

**配置项**:
- 联系电话
- 联系邮箱
- 公司地址
- 营业时间

#### 8.3 社交媒体

**配置项**:
- 微信公众号
- 微博账号
- Facebook
- Instagram

#### 8.4 高级设置

**配置项**:
- 统计代码（Google Analytics）
- 自定义头部代码
- 自定义底部代码

---

### 9. 相册管理

**URL**: http://localhost:8001/admin/galleries

#### 9.1 创建相册

**操作步骤**:
1. 点击"新建相册"
2. 填写相册信息:
   - **相册名称**: 必填
   - **Slug**: 自动生成
   - **描述**: 可选
   - **分类**: 可选
3. 选择封面图
4. 设置显示模式:
   - 网格
   - 瀑布流
   - 轮播
5. 点击"保存"

#### 9.2 添加图片

**操作步骤**:
1. 进入相册详情
2. 点击"批量添加图片"
3. 从媒体库选择图片
4. 批量选择多张图片
5. 点击"添加"

#### 9.3 管理图片

**拖拽排序**:
- 拖动图片调整顺序
- 支持批量重排序

**编辑图片信息**:
- 图片标题
- 图片说明
- Alt文本

**显示控制**:
- 显示/隐藏图片
- 设置精选图片

---

### 10. 留言管理

**URL**: http://localhost:8001/admin/contacts

#### 10.1 查看留言

**列表显示**:
- ID
- 姓名
- 联系方式
- 留言内容（预览）
- 状态
- 创建时间

**状态标识**:
- 🟡 未读
- 🟢 已处理

#### 10.2 处理留言

**操作步骤**:
1. 点击"查看"查看详情
2. 阅读完整留言内容
3. 点击"标记已处理"
4. 或通过联系方式回复客户

**批量操作**:
1. 勾选多条留言
2. 点击"批量操作"
3. 选择操作类型:
   - 标记已处理
   - 标记未读
4. 确认操作

#### 10.3 导出留言

**操作步骤**:
1. 可选: 设置筛选条件
2. 点击"导出 CSV"
3. 浏览器自动下载文件

**导出字段**:
- ID
- 姓名
- 联系方式
- 留言内容
- 状态
- 来源页面
- 创建时间
- 处理时间

---

## 🔧 常见问题

### Q1: 无法启动应用

**错误**: `ModuleNotFoundError: No module named 'admin'`

**解决方案**:
```bash
# 确保设置了 PYTHONPATH
export PYTHONPATH=/path/to/bowen-education-manchester

# 从项目根目录启动
cd /path/to/bowen-education-manchester
python -m uvicorn admin.app.main:app --port 8001
```

---

### Q2: 导入循环错误

**错误**: `ImportError: cannot import name 'Base' from partially initialized module`

**解决方案**:
- 已在 `admin/app/database.py` 中修复
- 确保使用最新版本代码

---

### Q3: 登录后立即退出

**错误**: Session 无法持久化

**临时方案**:
```bash
export TESTING=1  # 跳过认证中间件
```

**永久解决** (待实现):
- 检查 SECRET_KEY 配置
- 检查 cookie 设置

---

### Q4: 媒体库报错

**错误**: `no such column: media_file.usage_count`

**解决方案**:
```bash
# 运行数据库迁移
python scripts/migrate_media_file.py
```

---

### Q5: 栏目管理页面错误

**错误**: `TemplateSyntaxError: expected token 'end of statement block'`

**解决方案**:
- 已在模板中修复
- 确保使用最新版本代码

---

### Q6: 端口被占用

**错误**: `Address already in use`

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :8001

# 终止进程
kill -9 <PID>

# 或使用其他端口
python -m uvicorn admin.app.main:app --port 8002
```

---

### Q7: 权限错误

**错误**: `PermissionError: [Errno 13] Permission denied`

**解决方案**:
```bash
# 检查文件权限
ls -la

# 修改权限
chmod +x script.sh
chmod 755 directory/
```

---

## 🛠️ 故障排除

### 查看日志

**应用日志**:
```bash
# Uvicorn 会输出到控制台
# 检查启动终端的输出
```

**数据库日志**:
```python
# 在 admin/app/database.py 中启用 echo
engine = create_engine(
    database_url,
    echo=True  # 输出所有 SQL 语句
)
```

---

### 测试端点

**健康检查**:
```bash
curl http://localhost:8001/health
```

**API 文档**:
```bash
# 访问 FastAPI 自动生成的文档
open http://localhost:8001/docs
```

---

### 重置数据库

```bash
# 备份数据库
cp bowen_education.db bowen_education.db.backup

# 删除数据库（谨慎操作）
rm bowen_education.db

# 重新初始化
python scripts/init_database.py
```

---

### 清理缓存

```bash
# 清理 Python 缓存
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# 重启应用
```

---

## 🔄 维护指南

### 日常维护

**每日检查**:
- 检查应用运行状态
- 查看错误日志
- 备份数据库

**每周检查**:
- 检查磁盘空间
- 清理临时文件
- 更新依赖包

**每月检查**:
- 审查系统性能
- 优化数据库
- 更新安全补丁

---

### 备份策略

**数据库备份**:
```bash
# 每日自动备份
0 2 * * * /path/to/backup_database.sh

# 手动备份
cp bowen_education.db backup/bowen_education_$(date +%Y%m%d).db
```

**代码备份**:
```bash
# Git 提交
git add .
git commit -m "backup: $(date)"
git push
```

**媒体文件备份**:
```bash
# 同步到备份服务器
rsync -avz static/uploads/ backup@server:/backup/uploads/
```

---

### 性能优化

**数据库优化**:
```sql
-- 添加索引
CREATE INDEX idx_media_created_at ON media_file(created_at);
CREATE INDEX idx_column_parent_id ON site_column(parent_id);
CREATE INDEX idx_post_status ON post(status);

-- 定期清理
VACUUM;
```

**应用优化**:
- 启用生产模式（关闭 DEBUG）
- 使用多进程部署（Gunicorn）
- 配置反向代理（Nginx）
- 启用静态文件缓存

---

### 安全检查

**定期更新**:
```bash
# 更新依赖包
pip list --outdated
pip install --upgrade package-name
```

**安全扫描**:
```bash
# 检查已知漏洞
pip install safety
safety check
```

**访问日志审计**:
- 定期查看访问日志
- 检查异常登录
- 监控API调用

---

## 📞 技术支持

### 获取帮助

**文档**:
- [项目结构文档](./admin-project-structure.md)
- [测试报告](./admin-system-test-report.md)
- [模块开发文档](./admin-modules/)

**在线资源**:
- FastAPI 文档: https://fastapi.tiangolo.com/
- SQLAlchemy 文档: https://docs.sqlalchemy.org/
- Jinja2 文档: https://jinja.palletsprojects.com/

**问题反馈**:
- GitHub Issues: <repository-url>/issues
- 邮箱: maxazure@gmail.com

---

## 📊 性能指标

### 目标指标

| 指标 | 目标值 | 当前值 |
|------|--------|--------|
| 页面加载时间 | < 2秒 | TBD |
| API 响应时间 | < 500ms | TBD |
| 数据库查询 | < 100ms | TBD |
| 并发用户数 | > 100 | TBD |
| 内存占用 | < 500MB | TBD |

---

## 🎓 培训资源

### 新用户培训

**第一步**: 熟悉界面
- 浏览各个功能模块
- 了解菜单结构
- 掌握基本操作

**第二步**: 内容管理
- 创建测试栏目
- 发布测试文章
- 上传测试图片

**第三步**: 高级功能
- 使用 Markdown 编辑器
- 设置SEO信息
- 配置站点设置

---

## 📋 更新日志

### v1.0.0 (2025-11-13)

**新功能**:
- ✅ 完成10个核心模块开发
- ✅ 实现完整的测试覆盖（97%）
- ✅ 修复数据库schema问题
- ✅ 修复模板语法错误

**已知问题**:
- ⚠️ Session 持久化问题
- ⚠️ 缺少初始管理员账户

**下一版本计划**:
- 修复Session持久化
- 添加初始化脚本
- 完善文档
- 添加更多测试

---

**文档维护者**: maxazure
**最后更新**: 2025-11-13
**版本**: v1.0.0
