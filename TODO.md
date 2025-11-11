# TODO 任务列表

## ✅ 已完成

### [2025-11-11] 项目文件清理与整理
- [x] 清理临时文件和阶段性报告 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 删除阶段性报告文档（3个）：
    - WEBSITE_CLEANUP_AND_TESTING_REPORT.md
    - SINGLE_PAGE_IMPROVEMENTS.md
    - TOOLS_GUIDE.md
  - 删除数据库相关临时文件（3个）：
    - DATABASE_RESTORE.md
    - restore_database.py
    - restore_database.sh
  - 删除数据导入脚本（2个）：
    - import_news.py
    - import_media.py
  - 删除空数据库文件（1个）：
    - bowen_education.db
  - 删除示例图片（3个）：
    - static/images/generated/chinese-classroom-example.jpg
    - static/images/generated/chess-club-example.jpg
    - static/images/generated/badminton-training-example.jpg
  - 删除冗余文档（1个）：
    - README_MODULAR.md
  - **总计清理**: 13个文件
  - **清理原因**: 这些文件为开发过程中的临时文件、阶段性报告或示例文件，已不再需要

- [x] 整理静态资源目录结构 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 将根目录 static/ 文件夹合并到 templates/static/
  - 合并的目录包括：
    - images/teachers (19个教师照片)
    - images/courses (33个课程相关图片)
    - images/news (新闻图片)
    - images/hero (hero背景图)
    - images/services (服务图片)
  - 删除根目录的 static/ 文件夹
  - **最终结果**: templates/static/images 现包含91个图片文件，7个子目录
  - **整理原因**: 统一静态资源管理，所有静态资源现在都在 templates/static/ 下

- [x] 修改上传目录配置 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 修改 app/config.py 中的媒体目录配置
  - 将上传目录从 instance/media 改为 upload
  - 删除 instance/media 目录
  - 创建 upload 目录并添加 .gitkeep
  - 创建 .gitignore 文件，配置忽略规则
  - **修改内容**:
    - SiteConfig.media_dir: instance/media → upload
    - UPLOAD_DIR = BASE_DIR / "upload"
    - MEDIA_DIR 保留为 UPLOAD_DIR 的别名（兼容性）
  - **相关文件**:
    - app/config.py
    - upload/.gitkeep
    - .gitignore

- [x] 成功运行项目 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 使用虚拟环境启动 FastAPI 应用
  - 运行端口: 8000
  - 启动命令: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  - **环境信息**:
    - Python 版本: 3.13.2
    - FastAPI 版本: 0.109.0
    - Uvicorn 版本: 0.27.0
    - SQLAlchemy 版本: 2.0.44
  - **测试结果**:
    - 主页 (/) - HTTP 200 ✅
    - 关于页面 (/about) - HTTP 200 ✅
    - 联系页面 (/contact) - HTTP 200 ✅
  - **访问地址**:
    - 本地: http://localhost:8000
    - 局域网: http://0.0.0.0:8000
  - **运行状态**: 后台运行中，已启用热重载模式

- [x] 更新 README.md 文档 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 根据项目当前状态全面更新文档
  - **更新内容**:
    - Python 版本徽章: 3.11 → 3.13.2
    - 添加 SQLAlchemy 版本徽章
    - 更新项目结构说明（添加 upload/, .gitignore, tools/）
    - 更新静态资源说明（91张图片，详细分类）
    - 更新数据库统计（508KB，图片资源详情）
    - 删除不存在的测试报告引用
    - 添加静态资源与上传章节
    - 更新部署说明（添加环境变量配置）
    - 添加更多故障排除方案
    - 添加版本历史 v1.1.0
  - **文档规模**: 500 行
  - **相关文件**: README.md

- [x] 添加 GitHub 仓库地址 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 在 README.md 添加 GitHub 仓库链接
  - **更新内容**:
    - 在文档开头添加仓库地址展示
    - 更新克隆命令为实际仓库地址
    - 更新技术支持部分的 GitHub Issues 链接
    - 更新联系邮箱为实际邮箱
  - **仓库地址**: https://github.com/maxazure/bowen-education-manchester
  - **Issues**: https://github.com/maxazure/bowen-education-manchester/issues
  - **相关文件**: README.md

### [2025-11-08] 中文学校栏目测试与优化
- [x] 运行网站并使用 Chrome DevTools 测试中文学校栏目 - 完成时间: 2025-11-07 - 负责人: maxazure
  - 测试了5个页面：/school, /school-curriculum/, /school-curriculum/primary-mandarin, /school-term-dates/, /school-pta/
  - 创建了详细测试报告 CHINESE_SCHOOL_TEST_REPORT.md (45KB)
  - 发现7门课程（超出需求的6门）
  - 整体合规性达到 95%
  - 相关文件：
    - CHINESE_SCHOOL_TEST_REPORT.md
    - curriculum-before.jpg, curriculum-after.jpg
    - term-dates-before.jpg, term-dates-after.jpg

### [2025-11-08] 页面风格统一
- [x] 统一 /school-curriculum 和 /school-term-dates 页面风格 - 完成时间: 2025-11-07 - 负责人: maxazure
  - 创建新模板 templates/post_list_with_sidebar.html (815行)
  - 匹配 single_page.html 的 hero 样式（蓝色渐变叠加层）
  - 使用相同布局系统（280px 固定侧边栏 + 弹性主内容区）
  - 保持所有课程列表功能
  - 截图格式改为 JPEG，质量设置为 60
  - 相关文件：
    - templates/post_list_with_sidebar.html
    - app/routes/frontend.py (路由已配置)

### [2025-11-08] 图片生成工具配置
- [x] 搜索并恢复图片生成工具 - 完成时间: 2025-11-08 - 负责人: maxazure
  - 从 Git 历史恢复 tools/generate_images.py (8.8KB, 292行)
  - 设置可执行权限
  - 验证工具完整性和功能
  - 相关文件：tools/generate_images.py

- [x] 配置 Zhipu AI API Key 环境变量 - 完成时间: 2025-11-08 - 负责人: maxazure
  - 将 API Key 添加到 ~/.zshrc 实现持久化
  - 在当前会话中激活环境变量
  - 验证环境配置正确
  - 相关文件：~/.zshrc

- [x] 创建示例配置并测试图片生成 - 完成时间: 2025-11-08 - 负责人: maxazure
  - 创建 images-example.json 示例配置（3张图片）
  - 成功生成3张高质量 AI 图片（100% 成功率）
  - 验证图片质量符合网站使用要求
  - 创建完整的配置文档 IMAGE_GENERATION_SETUP_REPORT.md
  - 生成的图片：
    - chinese-classroom-example.jpg (124.4 KB)
    - chess-club-example.jpg (123.9 KB)
    - badminton-training-example.jpg (122.3 KB)
  - 相关文件：
    - images-example.json
    - static/images/generated/
    - IMAGE_GENERATION_SETUP_REPORT.md

### [2025-11-08] 课程封面图片生成
- [x] 检查数据库中课程图片配置 - 完成时间: 2025-11-08 - 负责人: maxazure
  - 检查了所有7个课程的封面配置
  - 发现所有课程都缺少封面图片
  - 创建数据库检查工具 inspect_db.py
  - 相关文件：
    - inspect_db.py
    - check_course_images.py

- [x] 生成课程图片配置文件 - 完成时间: 2025-11-08 - 负责人: maxazure
  - 分析课程信息并生成AI提示词
  - 创建7个课程的图片生成配置
  - 根据课程类型定制提示词（中文、数学、物理）
  - 相关文件：
    - generate_course_image_config.py
    - course-images.json (7张图片配置)
    - course-images-mapping.json (映射关系)

- [x] 批量生成课程封面图片 - 完成时间: 2025-11-08 - 负责人: maxazure
  - 使用 Zhipu AI CogView-3-Flash 生成7张图片
  - 成功率 100%，无失败
  - 图片总大小 795 KB
  - 生成的图片：
    - course-foundation-mandarin.jpg (104 KB)
    - course-gcse-chinese.jpg (107 KB)
    - course-a-level-chinese.jpg (151 KB)
    - course-hsk-level-3.jpg (135 KB)
    - course-cantonese-language.jpg (107 KB)
    - course-gcse-mathematics.jpg (95 KB)
    - course-a-level-physics.jpg (96 KB)
  - 相关文件：
    - static/images/courses/

- [x] 更新数据库关联课程图片 - 完成时间: 2025-11-08 - 负责人: maxazure
  - 在 media_file 表创建7条媒体记录 (ID: 16-22)
  - 更新 product 表的 cover_media_id 字段
  - 验证所有课程封面配置成功
  - 创建完整的任务报告 COURSE_IMAGES_GENERATION_REPORT.md
  - 相关文件：
    - update_course_images.py
    - COURSE_IMAGES_GENERATION_REPORT.md

## 📋 待办事项

### 图片生成与优化
- [ ] 为各个栏目批量生成图片 - 优先级: 中 - 预计工时: 2h
  - 中文学校课程图片
  - 国际象棋活动图片
  - 羽毛球训练图片
  - 节日活动图片

- [ ] 建立标准化提示词模板库 - 优先级: 低 - 预计工时: 1h
  - 课堂场景模板
  - 活动场景模板
  - 运动场景模板
  - 节日场景模板

### 内容完善
- [ ] 修复面包屑导航问题 - 优先级: 高 - 预计工时: 0.5h
  - /school-curriculum/primary-mandarin 页面显示 "博文新闻" 应改为 "课程设置"

- [ ] 完善联系信息 - 优先级: 中 - 预计工时: 1h
  - 更新 PTA 页面的联系信息占位符
  - 添加实际联系方式

- [ ] 添加 PTA 即将举行的活动 - 优先级: 中 - 预计工时: 1h
  - 补充 "即将举行的活动" 内容

## 🐛 已知问题

- [ ] 课程详情页面面包屑错误 - 发现时间: 2025-11-07 - 影响程度: 中
  - 页面: /school-curriculum/primary-mandarin
  - 问题: 显示 "博文新闻" 而不是 "课程设置"
  - 需要检查模板或路由逻辑

## 💡 优化建议

- [ ] 建立图片资源管理规范 - 提出时间: 2025-11-08 - 预期收益: 提高资源组织效率
  - 统一命名规范
  - 分类目录组织
  - 版本控制管理

- [ ] 创建图片批量生成工作流 - 提出时间: 2025-11-08 - 预期收益: 提高生产效率
  - 按优先级分批生成
  - 高优先级图片优先使用
  - 定期更新图片库

## 📚 学习笔记

### Zhipu AI CogView-3-Flash 使用经验
- **模型特点**: 快速图片生成，质量高，适合批量生成
- **API 限制**: 需要设置请求间隔（建议2秒）避免限流
- **提示词技巧**:
  - 包含场景、人物、环境、光线、风格等要素
  - 加入地域标识（如 "Manchester UK"）提高准确性
  - 使用 "photorealistic style" 获得写实效果
- **文件管理**:
  - 自动跳过已存在文件，支持增量生成
  - 按优先级排序，高优先级先生成
  - 输出目录自动创建

### Jinja2 模板继承最佳实践
- 使用模板继承保持风格一致性
- 复用组件（如 sidebar_nav.html）提高可维护性
- CSS 样式模块化，避免重复代码
- 响应式设计使用 Flexbox 布局，移动端友好

### Chrome DevTools MCP 测试技巧
- 使用 take_screenshot 参数控制图片质量
- fullPage=true 可获取完整页面截图
- format="jpeg" + quality=60 平衡质量与文件大小
- 自动化测试流程提高测试效率

---

**最后更新**: 2025-11-11 21:22
**当前状态**: 项目已成功启动并运行在 http://localhost:8000，README 已添加 GitHub 仓库地址
