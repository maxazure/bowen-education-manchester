# TODO 任务列表

## ✅ 已完成

### [2025-11-12] 生成主栏目 Hero 背景图片
- [x] 为8个主栏目生成高质量 Hero 背景图片 - 完成时间: 2025-11-12 17:16 - 负责人: maxazure
  - **生成脚本**:
    - 创建 tools/generate_hero_images.py
    - 使用 Image Generator Service 的 Python 客户端
    - 每张图片规格: 1920 × 1088 (16:9, JPG 格式)
    - 质量等级: HIGH_COMMERCIAL (0.06元/张)
    - 用途类别: HERO_BG
  - **生成的图片**（8张）:
    - hero-school.jpg (173 KB) - 中文学校
    - hero-chess.jpg (195 KB) - 国际象棋俱乐部
    - hero-badminton.jpg (216 KB) - 羽毛球俱乐部
    - hero-tuition.jpg (215 KB) - 补习中心
    - hero-programmes.jpg (179 KB) - 政府项目
    - hero-events.jpg (300 KB) - 博文活动
    - hero-contact.jpg (169 KB) - 联系我们
    - hero-about.jpg (234 KB) - 关于博文
  - **数据库更新**:
    - 添加 8 条 media_file 记录 (id: 33-40)
    - 更新 8 个栏目的 hero_media_id 字段
    - 所有图片尺寸: 1920 × 1088 ✓
  - **生成统计**:
    - 总耗时: 159.20 秒 (约 2.6 分钟)
    - 总成本: ¥0.48 (8张 × ¥0.06)
    - 成功率: 100% (8/8)
  - **Prompt 设计**:
    - 每个栏目的 prompt 包含: 主题、风格、色彩、光线、构图要求
    - 统一使用蓝色系作为主色调（符合品牌色）
    - 明亮、专业、积极向上的氛围
    - 适合作为网站 hero banner 的构图

### [2025-11-12] 创建统一的主栏目 Hero 组件
- [x] 为主栏目创建统一 Hero 组件系统 - 完成时间: 2025-11-12 - 负责人: maxazure
  - **数据库扩展**:
    - 创建迁移脚本 tools/add_main_column_hero_fields.sql
    - 为 site_column 表添加5个新字段：
      - hero_title (TEXT): Hero主标题（中文）
      - hero_title_en (TEXT): Hero英文副标题
      - hero_tagline (TEXT): Hero标语/口号
      - hero_cta_text (TEXT): CTA按钮文字（可选）
      - hero_cta_url (TEXT): CTA按钮链接（可选）
    - 已有字段：description, hero_media_id
  - **模型更新**:
    - 更新 app/models/site.py 中的 SiteColumn 模型
    - 添加全部新字段的 Column 定义和注释
  - **创建 hero_main_column.html 组件**:
    - 路径：templates/components/hero_main_column.html
    - 支持双语标题结构（中文主标题 + 英文副标题）
    - 支持 tagline/标语
    - 支持可选的 CTA 按钮
    - 有动画效果（使用 data-aos 属性）
    - 背景图从 column.hero_media 读取
    - 不包含统计数据栏
    - 响应式设计（450px → 350px → 300px）
  - **配置主栏目数据**:
    - 创建脚本 tools/configure_main_column_hero.sql
    - 为6个主栏目配置 Hero 数据：
      - school: 博文中文学校 / Bowen Chinese School
      - chess: 博文国际象棋俱乐部 / Bowen Chess Club
      - badminton: 博文羽毛球俱乐部 / Bowen Badminton Club
      - programmes: 政府项目 / Government Programmes
      - events: 博文活动 / Bowen Events
      - contact: 联系我们 / Contact Us
  - **更新模板文件**（6个）:
    - templates/school.html - 使用新组件 + 保留统计数据栏
    - templates/chess.html - 使用新组件 + 保留统计数据栏
    - templates/badminton.html - 使用新组件
    - templates/events.html - 使用新组件
    - templates/programmes.html - 使用新组件
    - templates/contact.html - 使用新组件
    - 删除重复的 Hero CSS 代码
    - school 和 chess 保留独立的统计数据区域
  - **验证结果**:
    - /school - HTTP 200 ✅
    - /chess - HTTP 200 ✅
    - /badminton - HTTP 200 ✅
    - /programmes - HTTP 200 ✅
    - /events - HTTP 200 ✅
    - /contact - HTTP 200 ✅
  - **相关文件**:
    - tools/add_main_column_hero_fields.sql
    - tools/configure_main_column_hero.sql
    - app/models/site.py
    - templates/components/hero_main_column.html
    - templates/school.html, chess.html, badminton.html
    - templates/events.html, programmes.html, contact.html

### [2025-11-12] 相册模块（Gallery）开发
- [x] 创建相册模块类型 - 完成时间: 2025-11-12 - 负责人: maxazure
  - **数据库扩展**:
    - 在 app/models/site.py 的 ColumnType 枚举中添加 GALLERY 类型
    - 用于展示照片相册的栏目类型
  - **模板创建**:
    - 创建 templates/gallery.html 模板
    - 使用 hero_standard.html 组件（与 chess-about 相同）
    - 支持左侧边栏导航（当有父栏目时）
    - 响应式网格布局展示照片
    - 集成 Lightbox2 实现全屏图片查看
    - 空状态提示："暂无照片，敬请期待"
  - **路由配置**:
    - 在 app/routes/frontend.py 添加 GALLERY 类型处理
    - 使用 GalleryService 获取相册数据
    - 加载相册图片并过滤可见项
    - 增加浏览计数
  - **栏目转换**:
    - 将 badminton-gallery 栏目从 CUSTOM 改为 GALLERY 类型
    - 配置 Hero 数据：标题"精彩瞬间"，副标题"记录羽毛球俱乐部的精彩时刻"
    - 关联 hero_media_id = 35
  - **相关文件**:
    - app/models/site.py
    - templates/gallery.html
    - app/routes/frontend.py
    - Commit: cbe653b, fcb030c

- [x] 生成羽毛球俱乐部相册照片 - 完成时间: 2025-11-12 - 负责人: maxazure
  - **使用工具**: Image Generator Service (CogView-4)
  - **生成参数**:
    - 尺寸: 1920 × 1088 (16:9)
    - 格式: JPG
    - 质量: HIGH_COMMERCIAL (¥0.06/张)
    - 类别: ILLUSTRATION
    - 风格: 写实摄影
  - **生成的照片**（4张）:
    - badminton-001.jpg (180KB) - 儿童专注击球瞬间
    - badminton-002.jpg (175KB) - 教练指导训练
    - badminton-003.jpg (145KB) - 双打比赛
    - badminton-004.jpg (253KB) - 训练后的欢乐时刻
  - **存储位置**: templates/static/images/gallery/
  - **数据库更新**:
    - media_file 表: 添加 4 条记录 (ID: 41-44)
    - gallery_image 表: 添加 4 条记录，关联 gallery_id=2
    - 每张照片包含：title, caption, alt_text, tags, location
    - 更新 gallery.image_count = 4
  - **生成统计**:
    - 总耗时: 约 40 秒
    - 总成本: ¥0.24 (4张 × ¥0.06)
    - 成功率: 100% (4/4)
  - **Prompt 设计**:
    - 真实感照片风格
    - Manchester 地区儿童羽毛球训练场景
    - 专业室内羽毛球场馆背景
    - 明亮、积极向上的氛围
  - **相关文件**:
    - templates/static/images/gallery/badminton-*.jpg
    - Commit: a7ab553

- [x] 测试并修复相册页面 - 完成时间: 2025-11-12 - 负责人: maxazure
  - **测试页面**: http://localhost:8000/badminton-gallery
  - **发现的问题**:
    - 页面显示"暂无照片，敬请期待"
    - 4张照片已在数据库中，但未显示
  - **问题原因**:
    - GALLERY 路由处理器中 media_files 初始化为空数组
    - 未调用 GalleryService 获取相册图片
    - 未从 gallery_image 表读取数据
  - **修复方案**:
    - 导入并使用 GalleryService
    - 通过 slug 获取 gallery 对象
    - 调用 get_gallery_images() 获取图片列表
    - 过滤 is_visible=True 的图片
    - 增加 gallery 浏览计数
    - 将 media_files 传递到模板上下文
  - **测试验证**:
    - 使用 Chrome DevTools 重新加载页面 ✅
    - 4张照片正确显示在响应式网格中 ✅
    - Lightbox2 全屏查看功能正常 ✅
    - 左侧边栏导航正常 ✅
    - Hero 区域显示正确 ✅
  - **修改的文件**:
    - app/routes/frontend.py (lines 231-256)
    - Commit: ebb8f5e
  - **最终状态**: 相册页面完全正常，所有功能测试通过

### [2025-11-12] 统一所有模板的 Hero 和侧边栏布局
- [x] 添加栏目级别 Hero 背景图片支持 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 创建数据库迁移脚本 tools/add_column_hero_fields.sql
  - 为 site_column 表添加两个新字段：
    - description (TEXT): 栏目描述，用作 Hero 副标题
    - hero_media_id (INTEGER): Hero 背景图片ID（外键关联 media_file）
  - 成功执行 SQL 迁移，字段添加成功
  - 相关文件：tools/add_column_hero_fields.sql

- [x] 更新 SiteColumn 模型支持 Hero 配置 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 修改 app/models/site.py 中的 SiteColumn 类
  - 添加模型字段定义：
    - description = Column(Text, nullable=True, comment="栏目描述（Hero副标题）")
    - hero_media_id = Column(Integer, ForeignKey("media_file.id"), nullable=True)
    - hero_media = relationship("MediaFile", foreign_keys=[hero_media_id])
  - SQLAlchemy 关系配置正确
  - 相关文件：app/models/site.py

- [x] 创建统一 Hero 组件 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 创建 templates/components/hero_standard.html 组件
  - **核心特性**:
    - 支持 page 和 column 两种上下文（使用 `is defined` 检查）
    - 自动选择标题：hero_title → page.title → column.name
    - 自动选择副标题：hero_subtitle → page.subtitle → column.description
    - 自动选择背景图：hero_image → page.hero_media → column.hero_media → 默认图
    - 包含完整 CSS 样式（400px 高度，蓝色渐变叠加层）
  - **修复的问题**:
    - 初始版本在列表页报错 `'page' is undefined`
    - 使用 Jinja2 条件表达式修复：`if page is defined else`
  - 适用于所有页面类型：单页、列表页、详情页
  - 相关文件：templates/components/hero_standard.html

- [x] 更新侧边栏注册按钮为可选 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 修改 templates/components/sidebar_nav.html
  - **修改内容**:
    - 注册按钮改为条件显示：`{% if show_register_button and parent_column %}`
    - 不再自动为 chess 栏目显示
    - 需要在模板中显式传递 show_register_button 变量
    - 按钮文本、URL、副文本均可自定义：
      - register_button_text (默认: "立即报名")
      - register_button_url (默认: "/contact")
      - register_button_subtext (默认: "联系我们")
  - **设计原因**: 根据用户要求，默认不显示注册按钮
  - 相关文件：templates/components/sidebar_nav.html

- [x] 批量更新模板使用统一 Hero 和侧边栏 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 使用 Task subagent 更新4个模板文件
  - **更新的模板**:
    - templates/post_list_universal.html
    - templates/post_detail.html
    - templates/product_list.html
    - templates/product_detail.html
  - **统一的修改**:
    - 使用 `{% include 'components/hero_standard.html' %}` 替代硬编码 Hero
    - 使用左侧边栏布局（280px sidebar + flex main）
    - 移除重复的 Hero CSS（组件自带）
    - 移除重复的面包屑 CSS（组件自带）
    - 保持 CTA 区块样式一致
  - 所有页面视觉风格统一

- [x] 验证所有更新页面正常运行 - 完成时间: 2025-11-12 - 负责人: maxazure
  - **测试结果**:
    - /chess-news (列表页) - HTTP 200 ✅
    - /chess-events (列表页) - HTTP 200 ✅
    - /chess-news/chess-tactics-double-attack (详情页) - HTTP 200 ✅
    - /tuition (产品列表) - HTTP 200 ✅
  - **Hero 组件验证**:
    - 列表页正确显示栏目名称和描述 ✅
    - 详情页正确显示页面标题和副标题 ✅
    - 未定义 page 变量不会报错 ✅
    - Hero 背景图支持从数据库配置 ✅
  - **侧边栏验证**:
    - 左侧边栏导航正常显示 ✅
    - 注册按钮默认不显示 ✅
    - 页面布局响应式正常 ✅
  - **总结**: 所有页面（除首页和 CUSTOM 类型）现已使用统一的 Hero 和侧边栏布局

### [2025-11-12] 象棋俱乐部POST栏目添加左侧导航
- [x] 为chess-events和chess-news添加左侧导航菜单 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 修改 app/routes/frontend.py 路由配置
  - **列表页修改**:
    - 在POST类型路由处理中已有parent_column和sibling_columns支持
    - 添加chess-events和chess-news到特殊模板处理列表
    - 使用post_list_with_sidebar.html模板（与school-curriculum相同）
  - **详情页修改**:
    - 修改post_detail.html模板，添加条件布局
    - 有parent_column时使用左侧导航栏布局
    - 无parent_column时保持传统右侧边栏布局
    - 在两个详情路由函数中添加parent_column和sibling_columns上下文
  - **CSS样式**:
    - 添加page-layout相关CSS类（280px左侧栏 + 弹性主内容）
    - 响应式支持：移动端自动纵向堆叠
  - **测试验证**:
    - /chess-events 列表页 - HTTP 200 ✅
    - /chess-news 列表页 - HTTP 200 ✅
    - /chess-events/autumn-chess-tournament-2024 详情页 - 左侧导航显示 ✅
    - /chess-news/chess-tactics-double-attack 详情页 - 左侧导航显示 ✅
    - 注册按钮在所有页面正确显示 ✅
  - **修改的文件**:
    - app/routes/frontend.py (3处修改)
    - templates/post_detail.html (布局和CSS)
  - **功能特性**:
    - 左侧导航显示5个象棋俱乐部子栏目
    - 当前页面高亮显示
    - 底部显示绿色注册按钮（仅chess栏目）
    - 移动端响应式友好

### [2025-11-12] 象棋俱乐部栏目重组
- [x] 收集英国国际象棋学习资源 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 使用 WebSearch 搜索英国本地象棋资源
  - **收集的资源**（20+项）:
    - 官方组织：ECF (English Chess Federation), Chess in Schools and Communities
    - 在线平台：Lichess.org, Chess.com, ChessTempo, LearningChess.net UK
    - 教练服务：UK Chess Academy, Chess Rising Stars, First Move Chess
    - 学习材料：Irving Chernev 书籍, ChessBase 软件
    - 视频资源：ChessNetwork, John Bartholomew, GothamChess 等 YouTube 频道
  - 所有资源附带详细描述和直接链接
  - 相关文件：tools/reorganize_chess_club.sql

- [x] 创建象棋俱乐部重组 SQL 脚本 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 创建 tools/reorganize_chess_club.sql（2000+行）
  - **栏目结构**（5个子栏目）:
    - 俱乐部简介 (chess-about, SINGLE_PAGE, sort_order=1)
    - 课程设置 (chess-courses, SINGLE_PAGE, sort_order=2)
    - 活动与赛事 (chess-events, POST, sort_order=3) - 从原"我们的比赛"更新
    - 学习资源 (chess-resources, SINGLE_PAGE, sort_order=4)
    - 新闻与精彩回顾 (chess-news, POST, sort_order=5)
  - **内容创建**:
    - 3个 single_page 记录（俱乐部简介、课程设置、学习资源）
    - 3个 post 记录（新闻文章）
    - 课程设置包含完整的 HTML 注册表单，带客户端验证
    - 学习资源整合了所有收集的英国象棋资源
  - **修复的问题**:
    - 列名错误：is_visible → show_in_nav + is_enabled
    - 使用 sed 命令批量替换修复
  - 相关文件：tools/reorganize_chess_club.sql

- [x] 执行 SQL 脚本重组数据库 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 执行 reorganize_chess_club.sql 脚本
  - **数据库更新**:
    - 创建4个新栏目（id: 26, 27, 28, 29）
    - 更新1个现有栏目（id: 16 - 活动与赛事）
    - 删除2个旧栏目（id: 17 - 棋手信息, id: 18 - 相册）
    - 插入3条 single_page 内容（id: 19, 20, 21）
    - 插入3条 post 新闻文章（id: 19, 20, 21）
  - **验证结果**:
    - 所有子栏目正确显示 ✅
    - 排序顺序正确 ✅
    - 导航菜单显示正确 ✅

- [x] 修改侧边栏模板添加注册按钮 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 修改 templates/components/sidebar_nav.html
  - **添加的功能**:
    - 条件注册按钮（仅在象棋俱乐部页面显示）
    - 检查条件：parent_column.slug == 'chess'
    - 按钮链接：/chess-courses#registration-form
    - SVG 图标：用户添加图标
    - 双行文本：注册象棋俱乐部 / 成为新会员
  - **CSS 样式**:
    - 绿色渐变背景（#10b981 → #059669）
    - 悬停效果：上升动画 + 阴影增强
    - 响应式设计：移动端友好
    - 分隔线：与菜单区域分隔
    - 自动定位：margin-top: auto 推到底部
  - **代码统计**:
    - HTML：16行（lines 62-77）
    - CSS：47行（lines 181-227）
  - 相关文件：templates/components/sidebar_nav.html

- [x] 验证所有更新 - 完成时间: 2025-11-12 - 负责人: maxazure
  - **页面可访问性测试**:
    - /chess-about - HTTP 200 ✅
    - /chess-courses - HTTP 200 ✅
    - /chess-resources - HTTP 200 ✅
    - /chess-news - HTTP 200 ✅
  - **侧边栏注册按钮验证**:
    - 按钮HTML正确渲染 ✅
    - CSS样式正确应用 ✅
    - 出现在所有象棋俱乐部页面 ✅
    - 链接指向正确位置 ✅
  - **数据库验证**:
    - 5个子栏目正确创建 ✅
    - 3个单页内容存在 ✅
    - 3篇新闻文章存在 ✅
    - 排序顺序正确 ✅
  - **应用运行状态**:
    - FastAPI 成功重载 ✅
    - 无错误或警告 ✅
    - 端口 8000 正常运行 ✅

### [2025-11-11] 代码模块优化
- [x] 删除未使用的数据库模块 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 通过分析数据库使用情况，识别并删除未使用的模块
  - **数据库分析结果**:
    - 实际使用的栏目类型仅4种：SINGLE_PAGE(10), CUSTOM(9), POST(5), PRODUCT(1)
    - 发现30+个空表（记录数为0），涉及预订、餐厅、作品集、用户等模块
  - **删除的模型文件**（5个）:
    - app/models/booking.py
    - app/models/user.py
    - app/models/file_download.py
    - app/models/custom_field.py
    - app/models/video.py
  - **删除的服务文件**（4个）:
    - app/services/booking_service.py
    - app/services/user_service.py
    - app/services/file_download_service.py
    - app/services/video_service.py
  - **更新的文件**:
    - app/models/__init__.py - 移除未使用模块的导入，保留10个核心模型
    - app/services/__init__.py - 移除未使用服务的导入，保留7个核心服务
    - app/models/event.py - 移除对已删除User模型的引用
  - **代码优化统计**:
    - 模型文件: 15 → 10 (减少33%)
    - 服务文件: 13 → 7 (减少46%)
    - 代码库更精简，维护性更好
  - **验证结果**:
    - 应用成功启动在端口 8000 ✅
    - 所有核心路由测试通过 (/, /about, /contact) ✅
    - 无导入错误，无关系错误 ✅

- [x] 清理数据库中未使用的表 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 创建数据库清理工具 tools/clean_database_tables.py
  - 分析50个数据库表，识别30个未使用的表
  - **删除的表**（30个）:
    - booking 模块：booking, booking_service, booking_time_slot
    - user 模块：user
    - file_download 模块：file_download, file_download_log, file_category
    - video 模块：video, video_category, video_playlist, video_playlist_link
    - custom_field 模块：custom_field_def, custom_field_option, product_custom_field_value
    - cart 模块：cart, cart_item
    - order 模块：order, order_item
    - portfolio 模块：portfolio, portfolio_category, portfolio_category_link, portfolio_image
    - restaurant 模块：restaurant_order, restaurant_order_item, menu_category, menu_item
    - newsletter 模块：newsletter_campaign, newsletter_subscriber
    - 其他：review, comment
  - **保留的表**（20个）:
    - alembic_version（数据库版本）
    - contact_message（联系消息）
    - event, event_registration, event_ticket_type（活动）
    - faq, faq_category（FAQ）
    - gallery, gallery_image（图库）
    - media_file（媒体文件）
    - post, post_category, post_category_link（文章）
    - product, product_category, product_category_link（产品/课程）
    - single_page（单页）
    - site_column, site_setting（站点设置）
    - team_member（团队成员）
  - **数据库优化统计**:
    - 表数量: 50 → 20 (减少60%)
    - 文件大小: 508KB → 324KB (减少36%)
    - 执行 VACUUM 命令回收空间
  - **验证结果**:
    - 应用运行正常 ✅
    - 所有核心功能测试通过 ✅
    - 数据完整性保持 ✅

- [x] 删除清理过程中的临时文件 - 完成时间: 2025-11-11 - 负责人: maxazure
  - 删除临时检查脚本：/tmp/check_tables.sh
  - 删除数据库清理工具：tools/clean_database_tables.py（已完成使命）
  - **保留的工具文件**:
    - tools/generate_images.py（图片生成工具）
    - tools/README.md（工具说明文档）
  - **清理原因**: 这些临时文件仅用于一次性清理任务，已无保留价值

- [x] 重新导出清理后的数据库 SQL - 完成时间: 2025-11-11 - 负责人: maxazure
  - 使用 sqlite3 .dump 命令导出完整数据库
  - 覆盖现有的 database_backup.sql 文件
  - **导出统计**:
    - 包含表数量: 20 个
    - CREATE TABLE 语句: 20 条
    - INSERT INTO 语句: 144 条
    - 文件行数: 507 行
    - 文件大小: 224K → 219K（减少 5K）
  - **验证结果**:
    - SQL 语法正确 ✅
    - 可成功导入新数据库 ✅
    - 所有20个核心表完整导出 ✅
    - 数据完整性保持 ✅
  - **用途**: 用于数据库恢复、迁移或部署新环境

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

## ✅ 已完成

### [2025-11-12] 批量统一剩余模板使用标准 Hero 组件
- [x] 修复 4 个模板的 Hero 区域 - 完成时间: 2025-11-12 - 负责人: maxazure
  - **修改的模板**:
    - templates/post_list.html (新闻列表)
    - templates/events.html (博文活动)
    - templates/badminton.html (羽毛球俱乐部)
    - templates/programmes.html (政府项目)
  - **统一改进**:
    - 所有模板使用 `{% include 'components/hero_standard.html' %}`
    - 通过变量传递 hero_title、hero_subtitle、hero_image
    - 支持数据库配置背景图片
  - **代码优化**:
    - 删除重复的 Hero CSS：57 行
    - 替换硬编码 HTML：64 行 → 12 行
    - 净减少代码：约 85 行
  - **功能优化**:
    - events 和 badminton：将 Hero 内按钮移到独立的"快速导航"区域
    - 视觉层次更清晰，用户体验更好
    - 新增 .quick-nav 和 .quick-nav__buttons CSS
  - **测试验证**:
    - /news - HTTP 200 ✅
    - /events - HTTP 200 ✅
    - /badminton - HTTP 200 ✅
    - /programmes - HTTP 200 ✅

- [x] 修复模板统一性问题 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 更新 post_list_with_sidebar.html 使用统一 hero 组件
  - 移除重复的 Hero CSS 定义（约 50 行）
  - 更新路由配置：news 页面使用 post_list_universal.html
  - 删除弃用的 post_list_with_sidebar_news.html 模板
  - **测试验证**:
    - /news 页面侧边栏正常，无"联系我们"自定义内容 ✅
    - /school-curriculum Hero 正常显示 ✅

### [2025-11-12] 修复 About 页面时间线样式问题
- [x] 修复年份徽章遮挡文字的问题 - 完成时间: 2025-11-12 - 负责人: maxazure
  - 问题页面：http://localhost:8000/about
  - **问题分析**：
    - 时间线部分的年份徽章（2018、2019、2020等）遮挡了下方的文字内容
    - 原因是年份徽章 z-index: 2，而内容卡片没有设置 z-index
    - 年份徽章使用绝对定位，位于中间线上，导致与内容卡片重叠
  - **修复方案**：
    - 将 .timeline-item__year 的 z-index 从 2 改为 1（降低层级）
    - 为 .timeline-item__content 添加 position: relative 和 z-index: 2（提高层级）
    - 确保内容卡片始终显示在年份徽章上方
  - **测试验证**：
    - 桌面视图（1920x1080）- 年份不再遮挡文字 ✅
    - 移动视图（375x667）- 布局正常，年份位于左侧 ✅
    - 所有时间线条目（2018、2019、2020、2021-2025）均正常显示 ✅
  - **修改的文件**：
    - templates/about.html（第1132-1158行）
  - **CSS 修改**：
    ```css
    .timeline-item__year {
        z-index: 1;  /* 从 2 改为 1 */
    }
    .timeline-item__content {
        position: relative;  /* 新增 */
        z-index: 2;  /* 新增 */
    }
    ```
  - **效果**：页面美观度提升，用户体验改善，桌面和移动端均完美显示

### [2025-11-13] 管理后台开发 - 基础设施搭建完成
- [x] 制定管理后台开发总体计划 - 完成时间: 2025-11-13 - 负责人: maxazure
  - **规划文档**:
    - 创建 docs/admin-system-design.md (1957行，系统设计文档)
    - 创建 docs/admin-development-plan.md (完整的6周TDD开发计划)
    - 定义9个核心模块和依赖关系
    - 明确TDD开发流程: Red → Green → Refactor

- [x] 为所有10个模块创建任务文档 - 完成时间: 2025-11-13 - 负责人: maxazure
  - **文档结构**:
    - 创建 docs/admin-modules/ 目录结构
    - 为每个模块创建 TASK.md（任务说明）和 TODO.md（详细待办）
    - 模块01-03: 完整文档已完成
    - 模块04-10: 完整文档已完成
    - 总计23个文档文件，约2500+行内容
  - **文档规范**:
    - 每个TASK.md包含: 数据库设计、TDD测试用例（20+个）、开发步骤、完成标准
    - 每个TODO.md包含: 13个Phase、70+详细任务、完成检查清单
    - 测试用例总计: 100+ 个

- [x] 模块01基础设施搭建完成 - 完成时间: 2025-11-13 - 负责人: infrastructure-setup subagent
  - **目录结构** (8个目录):
    - app/admin/ - 管理后台主目录
    - app/admin/routers/ - 路由模块
    - templates/admin/ - 管理后台模板
    - templates/admin/components/ - 公共组件
    - static/admin/css/ - 管理后台样式
    - static/admin/js/ - 管理后台脚本
    - static/admin/images/ - 后台图片
    - tests/admin/ - 测试目录

  - **Python文件** (5个):
    - app/admin/__init__.py - 包初始化（含版本信息）
    - app/admin/middleware.py - 认证中间件（占位）
    - app/admin/dependencies.py - 依赖注入（占位）
    - app/admin/utils.py - 工具函数（format_datetime, success_response, error_response）
    - app/admin/routers/__init__.py - 路由包

  - **测试文件** (3个):
    - tests/admin/test_infrastructure.py - 基础设施测试（15个测试用例）
    - tests/admin/conftest.py - pytest配置（fixtures）
    - pytest.ini - pytest全局配置

  - **模板文件** (6个):
    - templates/admin/base.html - Bootstrap 5基础布局
    - templates/admin/login.html - 登录页占位
    - templates/admin/dashboard.html - 仪表板占位
    - templates/admin/components/header.html - 顶部组件
    - templates/admin/components/sidebar.html - 侧边栏组件
    - templates/admin/components/pagination.html - 分页组件

  - **静态资源** (2个):
    - static/admin/css/admin.css - 基础样式
    - static/admin/js/admin.js - 基础脚本

  - **依赖更新** (11个新增):
    - bcrypt==4.1.2 - 密码加密
    - itsdangerous==2.1.2 - Session管理
    - Pillow==11.0.0 - 图片处理（升级支持Python 3.13）
    - mistune==3.0.2 - Markdown处理
    - pytest==8.3.4 - 测试框架（升级）
    - pytest-asyncio==0.25.2 - 异步测试（升级）
    - pytest-cov==6.0.0 - 测试覆盖率（升级）
    - httpx==0.28.1 - HTTP客户端（升级）
    - ruff==0.1.11 - 代码检查
    - sqlalchemy==2.0.36 - ORM（升级支持Python 3.13）
    - alembic==1.14.0 - 数据库迁移（升级）

  - **测试结果**:
    - 15/15 测试全部通过 ✅
    - 测试覆盖率: 100%
    - 代码质量检查通过: Black ✅, isort ✅, ruff ✅

  - **解决的问题**:
    - Pillow 10.2.0 → 11.0.0（修复Python 3.13兼容性）
    - SQLAlchemy 2.0.25 → 2.0.36（修复Python 3.13兼容性）
    - pytest-asyncio 0.23.0 → 0.25.2（修复Python 3.13兼容性）
    - 虚拟环境路径错误（重新创建venv）

  - **Git提交**:
    - Commit: c1cb974
    - 文件变更: 20个文件
    - 新增代码: 983行
    - 提交信息: "feat: 搭建管理后台基础设施"

  - **总结**:
    - TDD流程完整执行: Red → Green → Refactor ✅
    - 26个文件/目录创建完成
    - 为后续9个模块开发奠定基础

## 📋 待办事项

### 管理后台开发（优先级最高）
- [ ] 模块02: 用户管理系统 - 优先级: P0 - 预计工时: 2天
  - 管理员模型、登录/登出、Session管理、认证中间件
  - 26个测试用例
  - 依赖: 模块01

- [ ] 模块03: 媒体库管理 - 优先级: P0 - 预计工时: 3天
  - 文件上传、缩略图生成、媒体选择器、CRUD操作
  - 15个测试用例
  - 依赖: 模块01, 02

- [ ] 模块04: 栏目管理 - 优先级: P0 - 预计工时: 3天
  - 栏目CRUD、树形结构、拖拽排序、Hero配置
  - 18个测试用例
  - 依赖: 模块01, 02

- [ ] 模块05: 单页管理 - 优先级: P0 - 预计工时: 4天
  - Markdown编辑器、单页CRUD、SEO配置、草稿发布
  - 12个测试用例
  - 依赖: 模块02, 03

- [ ] 模块06: 文章管理 - 优先级: P0 - 预计工时: 4天
  - 文章CRUD、分类管理、高级筛选、推荐置顶
  - 15个测试用例
  - 依赖: 模块02, 03, 04

- [ ] 模块07: 站点设置 - 优先级: P0 - 预计工时: 3天
  - 站点配置、联系方式、社交媒体、高级设置
  - 8个测试用例
  - 依赖: 模块02, 03

- [ ] 模块08: 产品管理 - 优先级: P1 - 预计工时: 4天
  - 产品CRUD、价格配置、产品属性、分类管理
  - 10个测试用例
  - 依赖: 模块02, 03, 04

- [ ] 模块09: 相册管理 - 优先级: P1 - 预计工时: 4天
  - 相册CRUD、批量上传、拖拽排序、图片元数据
  - 10个测试用例
  - 依赖: 模块02, 03, 04

- [ ] 模块10: 留言管理 - 优先级: P1 - 预计工时: 3天
  - 留言查询、状态管理、筛选搜索、CSV导出
  - 10个测试用例
  - 依赖: 模块02

- [ ] 系统集成测试与优化 - 优先级: P1 - 预计工时: 5天
  - 端到端测试、性能优化、文档编写、部署准备

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

### SQLite 数据库优化经验
- **表清理策略**: 分析实际使用情况，删除零记录表
- **SQL关键字处理**: "order" 等关键字需要用引号转义 `"order"`
- **VACUUM命令**: 删除表后必须执行 VACUUM 回收空间
- **效果显著**: 本次优化减少60%的表，数据库文件减少36%
- **清理工具**: 创建自动化脚本提高效率和安全性
- **验证流程**: 清理后必须验证应用运行和数据完整性

### 代码模块清理最佳实践
- **从数据库反推**: 通过数据库使用情况识别未使用模块
- **逐步删除**: 先删除模型文件，再删除服务文件
- **处理关系**: 注意 ForeignKey 和 relationship 的依赖关系
- **更新导入**: 及时更新 __init__.py 中的导入语句
- **完整测试**: 每次删除后验证应用启动和核心功能

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

### 内容管理系统栏目重组经验
- **资源收集**：使用 WebSearch 工具收集特定地域的在线资源
- **内容结构设计**：
  - 单页内容（SINGLE_PAGE）适合固定内容：简介、课程、资源
  - 列表内容（POST）适合动态更新：新闻、活动、赛事
  - 合理使用 sort_order 控制显示顺序
- **SQL 脚本编写**：
  - 注意列名准确性（show_in_nav, is_enabled）
  - 使用事务确保数据一致性
  - 先更新再删除，避免外键冲突
  - 使用 sed 批量修复列名错误
- **条件组件显示**：
  - 使用 Jinja2 条件判断（{% if parent_column.slug == 'chess' %}）
  - 实现特定栏目的定制化功能
  - CSS 类名要语义化（sidebar-cta, sidebar-register-btn）
- **表单设计**：
  - HTML5 表单验证（required, type="email", pattern）
  - JavaScript 客户端验证增强用户体验
  - 锚点链接（#registration-form）实现页面内跳转

### Jinja2 模板条件渲染技巧
- 使用对象属性判断：parent_column.slug == 'value'
- 条件块包裹可选内容：{% if condition %} ... {% endif %}
- CSS 类结合条件判断实现不同页面的差异化显示
- margin-top: auto 配合 flexbox 实现底部对齐

---

### [2025-11-13] 更新管理后台样式系统
- [x] 基于 Bootstrap 5 设计规范更新 admin.css - 完成时间: 2025-11-13 - 负责人: maxazure
  - **更新概述**:
    - 完全重写 admin/static/css/admin.css 文件（1430行）
    - 基于 docs/ui-design/bootstrap5-styles.css 的设计规范
    - 与 admin/templates/base.html 完美协调
  - **主要更新内容**:
    - CSS 变量系统: 26个设计令牌（颜色、尺寸、过渡等）
    - 组件样式增强: 卡片、按钮、表单、表格、徽章等
    - 页面布局组件: 页面标题、面包屑、Hero区域
    - 交互组件: 模态框、下拉菜单、分页、Toast提示
    - 特定页面组件: 登录页面、仪表板、空状态、上传区域等
    - 动画效果: fadeIn, slideInRight, slideInLeft, scaleIn, hover-lift
    - 响应式设计: 4个断点适配（1200px, 992px, 768px, 576px）
    - 辅助功能: 工具类、无障碍支持、打印样式
  - **配色方案**:
    - 主色: 中国红 #c8102e
    - 次要色: 深蓝 #1e3a8a
    - 中性色: 现代灰系列
    - 功能色: 成功、危险、警告、信息
  - **组件统计**:
    - 卡片组件: 标准卡片 + 统计卡片（4种渐变背景）
    - 按钮组件: 7种变体（primary, secondary, success, danger, outline等）
    - 表单组件: 输入框、选择器、开关、验证样式
    - 表格组件: 响应式包装、悬停效果、操作按钮
    - 徽章组件: 6种颜色 + 浅色变体
  - **移除内容**:
    - 旧的基础样式（110行）
    - 冲突的登录页面样式
    - 过时的仪表板样式
  - **文档支持**:
    - 创建 docs/ui-design/admin-css-update-summary.md
    - 包含完整的使用说明和示例代码
    - 组件使用指南和注意事项
  - **兼容性**:
    - Bootstrap 5.3.0+
    - 现代浏览器（Chrome, Firefox, Safari, Edge）
    - 移动设备完全支持
  - **相关文件**:
    - admin/static/css/admin.css (完全重写)
    - docs/ui-design/admin-css-update-summary.md (新增)
    - admin/templates/base.html (参考)
    - docs/ui-design/bootstrap5-styles.css (参考)

---

**最后更新**: 2025-11-13 16:45
**当前状态**: 管理后台样式系统更新完成 - admin.css 完全重写（1430行），基于 Bootstrap 5 设计规范，26个CSS变量，24个样式分类，完整的响应式支持，已创建使用文档
