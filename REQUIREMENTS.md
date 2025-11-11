# 博文集团网站需求文档
# Bowen Education Group Website Requirements

**项目名称 Project Name:** Bowen Education Group Official Website
**客户 Client:** Bowen Education Group, Manchester, UK
**文档版本 Version:** 1.0
**最后更新 Last Updated:** 2024-12-05

---

## 目录 Table of Contents

1. [项目概述 Project Overview](#项目概述-project-overview)
2. [网站目标 Website Goals](#网站目标-website-goals)
3. [网站结构 Website Structure](#网站结构-website-structure)
4. [页面需求 Page Requirements](#页面需求-page-requirements)
5. [功能需求 Functional Requirements](#功能需求-functional-requirements)
6. [设计需求 Design Requirements](#设计需求-design-requirements)
7. [技术需求 Technical Requirements](#技术需求-technical-requirements)
8. [SEO与性能 SEO & Performance](#seo与性能-seo--performance)
9. [内容管理 Content Management](#内容管理-content-management)

---

## 项目概述 Project Overview

### 关于博文集团 About Bowen Education Group

博文集团（Bowen Education Group）是位于英国曼彻斯特的综合性教育机构，成立于2018年。集团提供多元化的教育服务，包括：

- **中文学校**：从基础到A-Level的全方位中文课程
- **国际象棋俱乐部**：ECF认证的国际象棋培训
- **羽毛球俱乐部**：青少年和成人羽毛球训练
- **政府资助项目**：Trafford Council资助的HAF项目
- **文化交流项目**：与河南大学合作的寻根之旅

### 网站目的 Website Purpose

1. **品牌展示**：展示博文集团的综合实力和多元化服务
2. **招生转化**：吸引家长和学生报名各类课程和项目
3. **信息发布**：发布最新新闻、活动和学期安排
4. **信任建立**：展示政府合作、大学合作和社区认可
5. **在线咨询**：提供便捷的联系和咨询渠道

---

## 网站目标 Website Goals

### 业务目标 Business Goals

1. **提升品牌知名度**：在曼彻斯特地区建立中文教育领导者形象
2. **增加招生数量**：网站访客转化为报名学员
3. **展示政府合作**：突出Trafford Council HAF项目合作
4. **吸引合作伙伴**：展示与河南大学等机构的合作成果
5. **服务现有学员**：提供学期日期、训练时间表等实用信息

### 用户目标 User Goals

**主要用户群体 Primary User Groups:**

1. **华裔家长**：寻找中文学校，让孩子学习中文和中华文化
2. **本地家长**：寻找课外活动（象棋、羽毛球、HAF项目）
3. **学生**：了解课程内容、活动信息
4. **教育合作伙伴**：了解合作机会
5. **社区成员**：了解免费政府项目

**用户期望 User Expectations:**

- 清晰的课程信息和价格
- 便捷的联系和报名方式
- 多语言支持（中英文）
- 移动端友好体验
- 可信的背书和证明（政府合作、大学合作）

---

## 网站结构 Website Structure

### 整体架构 Site Architecture

```
首页 Home
│
├── 关于我们 About Us
│   ├── 集团简介 Group Introduction
│   ├── 团队介绍 Our Team
│   └── 联系我们 Contact Us
│
├── 中文学校 Chinese School ⭐ 一级栏目
│   ├── 课程设置 Curriculum (POST类型 - 列表页)
│   ├── 学期日期 Term Dates (SINGLE_PAGE)
│   └── PTA家长教师协会 PTA (SINGLE_PAGE)
│
├── 国际象棋俱乐部 Chess Club ⭐ 一级栏目
│   ├── 俱乐部简介 About Club (SINGLE_PAGE)
│   ├── 棋手信息 Players Info (SINGLE_PAGE)
│   └── 比赛活动 Tournaments (POST类型 - 列表页)
│
├── 羽毛球俱乐部 Badminton Club ⭐ 一级栏目
│   ├── 俱乐部简介 About Club (SINGLE_PAGE)
│   ├── 训练时间表 Training Schedule (SINGLE_PAGE)
│   └── 教练团队 Coaches (POST类型)
│
├── 政府项目 Government Programmes ⭐ 一级栏目
│   ├── HAF项目 HAF Programme (SINGLE_PAGE)
│   └── 社区服务 Community Services (POST类型)
│
├── 博文活动 Events ⭐ 一级栏目
│   ├── 河南大学合作 Henan University Partnership (SINGLE_PAGE)
│   └── 活动回顾 Event Gallery (POST类型)
│
├── 新闻中心 News Center (POST类型 - 列表页)
│
├── 学科辅导 Academic Tutoring (PRODUCT类型)
│
└── 联系我们 Contact Us (SINGLE_PAGE)
```

### 栏目类型说明 Column Types

| 栏目类型 | 说明 | 示例 |
|---------|------|------|
| SINGLE_PAGE | 单页内容，无子页面 | 学期日期、训练时间表 |
| POST | 列表+详情页，支持多篇文章 | 新闻、课程介绍、活动回顾 |
| PRODUCT | 产品/服务列表+详情 | 学科辅导课程 |
| CUSTOM | 自定义页面逻辑 | 特殊功能页面 |

### 导航菜单结构 Navigation Menu Structure

**主导航 Primary Navigation:**

```
首页 | 关于我们 | 中文学校▼ | 国际象棋俱乐部▼ | 羽毛球俱乐部▼ | 政府项目▼ | 博文活动▼ | 新闻中心 | 学科辅导 | 联系我们
```

**二级下拉菜单 Dropdown Menus:**

- **中文学校** → 课程设置、学期日期、PTA家长教师协会
- **国际象棋俱乐部** → 俱乐部简介、棋手信息、比赛活动
- **羽毛球俱乐部** → 俱乐部简介、训练时间表、教练团队
- **政府项目** → HAF项目、社区服务
- **博文活动** → 河南大学合作、活动回顾

**交互方式 Interaction:**
- 桌面端：鼠标悬停显示下拉菜单
- 移动端：点击展开二级菜单

---

## 页面需求 Page Requirements

### 1. 首页 Homepage

**URL:** `/`

**目标 Purpose:**
- 给访客留下专业、可信的第一印象
- 快速展示集团的多元化服务
- 引导用户进入各个板块
- 突出政府合作和大学合作背书

**页面结构 Page Structure:**

#### 1.1 Hero轮播区 Hero Carousel Section

**布局 Layout:**
- 全屏高度（100vh），自动轮播，6秒切换
- 深色半透明遮罩（opacity: 0.5）
- 左右箭头导航 + 底部指示点

**轮播内容 Slides (4-5张):**

**幻灯片1：集团主形象**
```
标题：Bowen Education Group | 博文集团
副标题：Bridging East and West Through Education
中文副标题：中西融汇，博学致远
CTA按钮：探索课程 → /school/
CTA按钮：预约试听 → /contact/
背景图：学生上课场景
```

**幻灯片2：政府项目背书**
```
标题：Official HAF Programme Provider
副标题：政府认证HAF项目提供商
描述：Funded by Trafford Council - Free Holiday Activities for Eligible Children
CTA按钮：了解HAF项目 → /programmes/programmes-haf/
背景图：HAF活动照片
Logo徽章：Trafford Council Logo
```

**幻灯片3：河南大学合作**
```
标题：Strategic Partnership with Henan University
副标题：河南大学战略合作伙伴
描述：Cultural Exchange & Root-seeking Tours to China
CTA按钮：查看合作详情 → /events/events-henan/
背景图：学生访华照片
Logo徽章：河南大学校徽
```

**幻灯片4：最新推荐活动（动态内容）**
```
标题：从数据库读取（Post.is_recommended=True最新一条）
副标题：活动简介
CTA按钮：查看详情 → /news/{slug}/
背景图：活动封面图
```

**技术实现 Technical:**
- 使用 Swiper.js 或 Alpine.js + CSS transitions
- 响应式：移动端文字大小调整，高度调整为 70vh
- 图片懒加载优化首屏加载速度

#### 1.2 集团简介 Introduction Section

**布局 Layout:**
- 左右两栏（桌面）或上下（移动端）
- 左侧：文字内容 + 统计数字 + CTA按钮（60%宽度）
- 右侧：形象图片（40%宽度）

**内容 Content:**

**标题区域:**
```
小标签：About Us / 关于我们
主标题：Leading Chinese Education in Manchester
副标题：曼彻斯特领先的中文教育机构
```

**描述文字:**
```
英文描述：
Bowen Education Group is a registered educational institution in Manchester, UK,
offering comprehensive Chinese language programmes from Foundation to A-Level,
academic tutoring, chess club, badminton club, and government-funded community programmes.

We are proud to be an official partner of Trafford Council for the HAF programme
and maintain a strategic partnership with Henan University for cultural exchange.

中文描述：
博文集团是位于曼彻斯特的注册教育机构，提供从基础到A-Level的全方位中文课程、
学科辅导、国际象棋俱乐部、羽毛球俱乐部以及政府资助的社区项目。

我们是Trafford Council HAF项目的官方合作伙伴，并与河南大学保持战略合作关系，
开展文化交流活动。
```

**统计数字 Statistics (3个):**
```
[图标：日历] 2018
          成立年份 | Established

[图标：学生] 500+
          在读学生 | Active Students

[图标：奖杯] 100%
          GCSE通过率 | GCSE Pass Rate
```

**CTA按钮:**
```
了解更多 Learn More → /about/
```

**右侧图片:**
- 展示学生活动场景（中国新年庆祝、课堂照片等）
- 配有徽章："Registered Education Provider"

**数据来源 Data Source:**
- 统计数字从 `site_settings` 表读取：
  - `established_year`
  - `student_count`
  - `gcse_pass_rate`

#### 1.3 四大板块入口 Four Service Blocks

**布局 Layout:**
- 2x2网格（桌面）或 1列（移动端）
- 每个卡片高度 350px（桌面）
- 卡片间距 30px

**标题区域:**
```
小标签：Our Services / 服务项目
主标题：Comprehensive Education Solutions
副标题：为不同年龄和需求提供多元化教育服务
```

**四个板块 Four Blocks:**

**板块1：中文学校 Chinese School**
```
图标：📚 书本图标
标题（英文）：Chinese School
标题（中文）：中文学校
描述：From Foundation to A-Level Mandarin, HSK, YCT preparation
关键词标签：
  - GCSE Chinese
  - A-Level Mandarin
  - HSK Certification
CTA按钮：查看课程 View Courses → /school/
背景图：教室上课场景（50%透明度遮罩）
悬停效果：卡片上浮 5px，背景图放大 110%
```

**板块2：国际象棋俱乐部 Chess Club**
```
图标：♟️ 国际象棋图标
标题（英文）：Chess Club
标题（中文）：国际象棋俱乐部
描述：ECF-affiliated club for all levels, tournaments and coaching
关键词标签：
  - ECF Certified
  - Tournament Training
  - Youth Players
CTA按钮：了解详情 Learn More → /chess/
背景图：孩子下棋照片
小徽章：ECF (English Chess Federation) Logo
```

**板块3：羽毛球俱乐部 Badminton Club**
```
图标：🏸 羽毛球拍图标
标题（英文）：Badminton Club
标题（中文）：羽毛球俱乐部
描述：Professional coaching for juniors and adults, competitive training
关键词标签：
  - Professional Coaching
  - Competitive Training
  - Health & Fitness
CTA按钮：了解详情 Learn More → /badminton/
背景图：羽毛球训练场景
```

**板块4：政府项目 Government Programmes**
```
图标：🏛️ 政府图标
标题（英文）：Government Programmes
标题（中文）：政府项目
描述：HAF programme funded by Trafford Council - Free for eligible children
关键词标签：
  - Free Activities
  - Healthy Food
  - Community Service
CTA按钮：了解详情 Learn More → /programmes/
背景图：HAF活动照片
小徽章：Trafford Council Logo（右上角）
特殊标识：FREE 免费（醒目标签）
```

**交互效果 Interactions:**
- 鼠标悬停：卡片上浮（transform: translateY(-5px)）
- 背景图片轻微放大（transform: scale(1.1)）
- 过渡时间：0.3s ease

#### 1.4 最新新闻与活动 Latest News & Events

**布局 Layout:**
- 标题居中
- 3列网格（桌面）/ 1列（移动端）
- 每个卡片：封面图 + 日期 + 标题 + 摘要 + 阅读更多

**标题区域:**
```
小标签：Latest Updates / 最新动态
主标题：News & Events
副标题：Stay updated with our latest activities and announcements
右上角链接：查看全部 View All → /news/
```

**卡片结构 Card Structure:**
```
[封面图片 - 16:9比例，高度200px]
  - 左上角：分类标签（新闻/活动/通知）
  - 图片上悬浮效果：深色渐变遮罩

[日期标签]
  2024年3月15日 | March 15, 2024

[文章标题]
  2024 Spring Term Enrolment Now Open
  (限制2行，超出显示省略号)

[摘要]
  Join our award-winning Mandarin programmes and experience...
  (限制3行，80-100字符)

[阅读更多按钮]
  阅读更多 Read More →
```

**显示逻辑 Display Logic:**
- 显示最新 6 篇已发布文章
- 按发布时间倒序排列
- 可选：优先显示 `is_recommended=True` 的文章

**数据查询 Data Query:**
```python
# 获取新闻栏目
news_column = db.query(SiteColumn).filter_by(slug='news').first()

# 查询最新6篇文章
latest_posts = (
    db.query(Post)
    .filter_by(column_id=news_column.id, status='published')
    .order_by(Post.published_at.desc())
    .limit(6)
    .all()
)
```

**响应式 Responsive:**
- 桌面（≥992px）：3列
- 平板（768-991px）：2列
- 移动（<768px）：1列

#### 1.5 合作伙伴Logo带 Partner Logo Band

**布局 Layout:**
- 浅灰色背景（#f8f9fa）
- 内边距：60px 0
- Logo水平排列，无限循环滚动

**标题区域:**
```
主标题：Our Partners / 合作伙伴
副标题：Trusted by leading organizations and institutions
```

**合作伙伴列表 Partners (6-8个):**

1. **Trafford Council**
   - Logo文件：`/static/images/partners/trafford-council.png`
   - 关系：HAF项目合作方

2. **Henan University 河南大学**
   - Logo文件：`/static/images/partners/henan-university.png`
   - 关系：战略教育合作伙伴

3. **English Chess Federation (ECF)**
   - Logo文件：`/static/images/partners/ecf.png`
   - 关系：国际象棋认证机构

4. **Sale Sports Centre**
   - Logo文件：`/static/images/partners/sale-sports-centre.png`
   - 关系：场地合作伙伴

5. **Badminton England**
   - Logo文件：`/static/images/partners/badminton-england.png`
   - 关系：羽毛球协会

6. **Manchester Chinese Education**
   - Logo文件：`/static/images/partners/manchester-chinese-education.png`
   - 关系：教育网络成员

**显示效果 Display Effect:**
- Logo尺寸标准化：高度 60px，宽度自适应
- 默认：灰度滤镜（grayscale(100%)）
- 鼠标悬停：彩色（grayscale(0%)），轻微放大（scale(1.1)）
- 自动滚动动画：20秒完成一轮，无缝循环

**技术实现 Technical:**
```css
/* 无限滚动动画 */
@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
```

**响应式 Responsive:**
- 桌面：一行显示 6 个Logo
- 平板：一行显示 4 个Logo
- 移动：一行显示 3 个Logo

#### 1.6 快速统计与成就 Quick Stats & Achievements

**布局 Layout:**
- 深色背景（深蓝色或品牌色渐变）
- 白色文字
- 4列网格（桌面）/ 2列（移动端）

**标题区域:**
```
主标题：Our Achievements / 我们的成就
副标题：Building excellence in education since 2018
```

**四个统计数字 Four Statistics:**

```
[图标：📅 日历]
2018
成立年份
Established

[图标：👨‍🎓 学生]
500+
在读学生
Active Students

[图标：🏆 奖杯]
100%
GCSE通过率
GCSE Pass Rate

[图标：👨‍🏫 教师]
30+
专业教师
Professional Teachers
```

**动画效果 Animations:**
- 滚动进入视口时：数字从0计数到目标值（CountUp.js）
- 图标轻微缩放动画

**数据来源 Data Source:**
```python
# 从 site_settings 表读取
stats = {
    'established_year': get_site_setting(db, 'established_year'),
    'student_count': get_site_setting(db, 'student_count'),
    'gcse_pass_rate': get_site_setting(db, 'gcse_pass_rate'),
    'teacher_count': get_site_setting(db, 'teacher_count'),
}
```

#### 1.7 联系我们与地图 Contact Form & Map

**布局 Layout:**
- 左侧（50%）：联系表单
- 右侧（50%）：Google地图嵌入
- 移动端：上下堆叠，表单在上

**标题区域:**
```
主标题：Get in Touch / 联系我们
副标题：We're here to help with any questions you may have
```

**联系表单 Contact Form:**

**表单字段 Form Fields:**
```
姓名 Name * (必填)
  - 输入框类型：text
  - placeholder: "Your name / 您的姓名"
  - 验证：非空

邮箱 Email * (必填)
  - 输入框类型：email
  - placeholder: "your.email@example.com"
  - 验证：邮箱格式

电话 Phone (可选)
  - 输入框类型：tel
  - placeholder: "07xxx xxxxxx"

感兴趣的项目 Interested In (必填)
  - 下拉选择框
  - 选项：
    - 中文学校 Chinese School
    - 国际象棋俱乐部 Chess Club
    - 羽毛球俱乐部 Badminton Club
    - 政府项目 HAF Government Programmes
    - 学科辅导 Academic Tutoring
    - 其他 Other

留言 Message * (必填)
  - 文本域 textarea
  - placeholder: "Tell us about your inquiry / 告诉我们您的需求"
  - 最少20字符

提交按钮
  - 文本："发送消息 Send Message"
  - 提交中状态："发送中... Sending..."
```

**表单行为 Form Behavior:**
- 提交方式：AJAX POST → `/api/contact`
- 成功提示："感谢您的留言！我们会尽快回复您。"
- 失败提示："提交失败，请稍后重试或直接致电我们。"
- 提交后：表单重置

**Google地图 Map:**

**地图设置 Map Settings:**
- 嵌入方式：Google Maps Embed API
- 中心坐标：从 `site_settings` 读取（latitude, longitude）
- 缩放级别：14
- 标记：博文集团地址
- 样式：自定义配色与网站风格统一

**地图下方信息 Map Info:**
```
📍 地址 Address:
   [从 site_settings 读取完整地址]
   Street Address, Manchester, Postcode

📞 电话 Phone:
   [从 site_settings 读取]
   0161 xxx xxxx

📧 邮箱 Email:
   info@boweneducation.org

🕐 营业时间 Opening Hours:
   周六 Saturday: 9:00 - 17:00
   周日 Sunday: 9:00 - 17:00
```

**数据来源 Data Source:**
```python
site_info = {
    'address': get_site_setting(db, 'address'),
    'city': get_site_setting(db, 'city'),
    'postcode': get_site_setting(db, 'postcode'),
    'phone': get_site_setting(db, 'phone'),
    'email': get_site_setting(db, 'email'),
    'latitude': get_site_setting(db, 'latitude'),
    'longitude': get_site_setting(db, 'longitude'),
}
```

---

### 2. 关于我们页面 About Us Page

**URL:** `/about/`

**页面结构 Page Structure:**

#### 2.1 Page Hero
- 标题："About Bowen Education Group / 关于博文集团"
- 副标题："Building bridges between cultures through education"
- 背景图：集团形象照片

#### 2.2 集团简介 Group Introduction
- 详细介绍集团历史、使命、愿景
- 成立背景、发展历程
- 核心价值观

#### 2.3 服务板块 Service Divisions
- 四大板块详细介绍（中文学校、国际象棋、羽毛球、政府项目）
- 每个板块：图标 + 标题 + 详细描述

#### 2.4 合作伙伴 Partnerships
- Trafford Council 合作详情
- 河南大学合作详情
- ECF认证说明

#### 2.5 资质认证 Certifications
- 教育机构注册证明
- 政府项目资质
- ECF会员资格

#### 2.6 CTA Section
- "准备好加入我们了吗？" Ready to join us?
- 按钮：查看课程 / 联系我们

---

### 3. 中文学校页面 Chinese School Pages

#### 3.1 中文学校首页 (Landing Page)

**URL:** `/school/`

**页面结构:**

**Hero Section:**
- 标题："Bowen Chinese School / 博文中文学校"
- 副标题："Comprehensive Mandarin education from Foundation to A-Level"
- CTA按钮：查看课程 / 预约试听

**学校简介 School Introduction:**
- 学校特色介绍
- 教学理念
- 师资力量

**课程体系 Course System:**
- 课程层级展示（Foundation → Primary → GCSE → A-Level）
- 流程图形式展示学习路径

**三个快捷入口 Three Quick Links:**
```
[卡片1] 课程设置
        查看所有课程详情 → /school/school-curriculum/

[卡片2] 学期日期
        查看本学年学期安排 → /school/school-term-dates/

[卡片3] PTA家长教师协会
        了解如何参与 → /school/school-pta/
```

**学生成果展示 Student Achievements:**
- GCSE/A-Level成绩统计
- 学生获奖情况
- HSK/YCT考试通过率

**报名流程 Enrolment Process:**
- 4步报名流程图
- 在线咨询 → 预约试听 → 缴费注册 → 开始上课

#### 3.2 课程设置页面 Curriculum Page

**URL:** `/school/school-curriculum/`

**页面类型:** POST列表页

**内容结构:**

**课程列表 Course List (每个课程一张卡片):**

**卡片结构:**
```
[课程封面图 - 16:9]
[年龄标签] Ages 5-7

课程名称：Foundation Mandarin / 基础中文
课程描述：Playful introduction to Mandarin through songs, games, and stories

课程信息：
  📅 上课时间：每周六 10:00-11:00
  💰 学费：£180/学期（12周）
  👥 班级人数：8-12人
  📍 上课地点：Sale Sports Centre

课程特色：
  ✓ 小班教学
  ✓ 沉浸式环境
  ✓ 互动游戏

[查看详情按钮] → /school/school-curriculum/foundation-mandarin/
[立即报名按钮] → /contact/?course=foundation-mandarin
```

**课程分类 Course Categories:**
1. Foundation Mandarin (5-7岁)
2. Primary Mandarin (8-10岁)
3. GCSE Chinese (14-16岁)
4. A-Level Chinese (16-18岁)
5. HSK Preparation (各年龄段)
6. YCT Preparation (儿童)
7. Cantonese Lessons (广东话课程)

#### 3.3 学期日期页面 Term Dates Page

**URL:** `/school/school-term-dates/`

**页面类型:** SINGLE_PAGE

**内容结构:**

```markdown
# 2024-2025学年学期安排
# Academic Year 2024-2025 Term Dates

## 秋季学期 Autumn Term
- 开学日期 Start Date: 2024年9月7日 (7 September 2024)
- 期中假期 Half Term: 2024年10月26日 - 11月3日
- 学期结束 End Date: 2024年12月21日 (21 December 2024)

## 春季学期 Spring Term
- 开学日期: 2025年1月6日 (6 January 2025)
- 期中假期: 2025年2月15日 - 2月23日
- 学期结束: 2025年4月4日 (4 April 2025)

## 夏季学期 Summer Term
- 开学日期: 2025年4月21日 (21 April 2025)
- 期中假期: 2025年5月24日 - 6月1日
- 学期结束: 2025年7月18日 (18 July 2025)

## 重要提示 Important Notes
- 所有课程均在周六上午进行
- 法定假日（Bank Holidays）不上课
- 如遇特殊情况需要调整，学校将提前通知
- 缺课学生可以申请补课或观看录播
```

#### 3.4 PTA家长教师协会页面 PTA Page

**URL:** `/school/school-pta/`

**页面类型:** SINGLE_PAGE

**内容结构:**

```markdown
# PTA家长教师协会
# Parent-Teacher Association

## 关于PTA About PTA
博文中文学校家长教师协会（PTA）是一个由家长和教师组成的志愿组织...

## 我们的使命 Our Mission
- 促进家长与学校之间的沟通与合作
- 组织各类文化活动和社交活动
- 为学校筹集资金，改善教学设施
- 支持学校的教育项目和倡议

## 如何参与 How to Get Involved
- 参加每学期的PTA会议
- 协助组织学校活动（中国新年庆祝、端午节、中秋节等）
- 担任PTA委员会成员
- 提供您的专业技能和建议

## 近期活动 Upcoming Activities
- 2024春季学期家长会：2024年2月10日
- 中国新年庆祝活动：2024年2月3日
- 夏季学期末家庭日：2024年7月15日

## 联系我们 Contact Us
如有任何问题或建议，请通过以下方式联系：
- 邮箱：pta@boweneducation.org
- 微信群：扫描二维码加入PTA家长群
```

---

### 4. 国际象棋俱乐部页面 Chess Club Pages

#### 4.1 国际象棋俱乐部首页

**URL:** `/chess/`

**页面结构:**

**Hero Section:**
- 标题："Bowen Chess Club / 博文国际象棋俱乐部"
- 副标题："ECF-affiliated chess training for all ages and levels"
- 小徽章：ECF (English Chess Federation) Logo

**俱乐部简介:**
- ECF认证说明
- 教练资质
- 训练方法

**三个快捷入口:**
```
[卡片1] 俱乐部简介
        了解俱乐部历史和特色 → /chess/chess-about/

[卡片2] 棋手信息
        ECF注册和等级分体系 → /chess/chess-players/

[卡片3] 比赛活动
        查看近期比赛和报名 → /chess/chess-tournaments/
```

**成绩展示 Achievements:**
- 学员ECF等级分布图
- 近期比赛获奖情况
- 优秀学员案例

#### 4.2 俱乐部简介页面 About Club Page

**URL:** `/chess/chess-about/`

**页面类型:** SINGLE_PAGE

**内容:**
- 俱乐部历史
- ECF认证详情
- 教练团队介绍
- 训练理念和方法
- 训练时间和地点
- 收费标准

#### 4.3 棋手信息页面 Players Info Page

**URL:** `/chess/chess-players/`

**页面类型:** SINGLE_PAGE

**内容:**
```markdown
# 棋手注册与认证
# Player Registration & Certification

## ECF会员注册 ECF Membership
- 注册流程
- 会员类型和费用
- 注册优势

## 等级分体系 Rating System
- ECF等级分说明
- 如何提升等级分
- 等级分查询方法

## 相关链接 Useful Links
- English Chess Federation 官网
- ECF会员注册页面
- 等级分查询页面
```

#### 4.4 比赛活动页面 Tournaments Page

**URL:** `/chess/chess-tournaments/`

**页面类型:** POST列表页

**文章示例:**
- 2024年春季内部比赛通知
- 2023年秋季比赛结果公布
- 曼彻斯特地区青少年锦标赛报名
- 每篇文章包含：比赛时间、地点、报名方式、参赛要求

---

### 5. 羽毛球俱乐部页面 Badminton Club Pages

#### 5.1 羽毛球俱乐部首页

**URL:** `/badminton/`

**页面结构:**

**Hero Section:**
- 标题："Bowen Badminton Club / 博文羽毛球俱乐部"
- 副标题："Professional coaching for all ages and skill levels"

**俱乐部简介:**
- 教练资质
- 训练设施
- 训练理念

**三个快捷入口:**
```
[卡片1] 俱乐部简介
        了解俱乐部详情 → /badminton/badminton-about/

[卡片2] 训练时间表
        查看训练时间安排 → /badminton/badminton-schedule/

[卡片3] 教练团队
        了解教练背景 → /badminton/badminton-coaches/
```

#### 5.2 俱乐部简介页面

**URL:** `/badminton/badminton-about/`

**页面类型:** SINGLE_PAGE

**内容:**
- 俱乐部历史
- 训练设施介绍（Sale Sports Centre）
- 训练级别说明（初级、中级、高级、竞技）
- 收费标准
- 报名方式

#### 5.3 训练时间表页面 Training Schedule Page

**URL:** `/badminton/badminton-schedule/`

**页面类型:** SINGLE_PAGE

**内容:**
```markdown
# 训练时间表
# Training Schedule

## 常规训练 Regular Training

| 日期 Day | 时间 Time | 级别 Level | 地点 Venue |
|---------|----------|-----------|----------|
| 每周六 Every Sat | 10:00-12:00 | 初级班 Beginner | Sale Sports Centre |
| 每周六 Every Sat | 14:00-16:00 | 中级班 Intermediate | Sale Sports Centre |
| 每周日 Every Sun | 10:00-12:00 | 高级班 Advanced | Sale Sports Centre |
| 每周日 Every Sun | 14:00-17:00 | 竞技训练 Competitive | Sale Sports Centre |

## 训练内容 Training Content
- 初级班：基础技术（握拍、步法、基本击球）
- 中级班：技术提升、战术训练、双打配合
- 高级班：高级技战术、体能训练、心理素质培养
- 竞技训练：针对比赛的专项训练和实战演练

## 训练地点 Venue
**Sale Sports Centre**
Sale Road, Sale, Manchester M33 3SL
[查看地图]

## 注意事项 Important Notes
- 请提前10分钟到场热身
- 自备球拍和运动装备
- 如遇场馆维护或特殊情况，将提前通知
```

#### 5.4 教练团队页面 Coaches Page

**URL:** `/badminton/badminton-coaches/`

**页面类型:** POST列表页

**内容结构:**
- 每位教练一张卡片
- 包含：照片、姓名、职称、资质、教学经验、专长

---

### 6. 政府项目页面 Government Programmes Pages

#### 6.1 政府项目首页

**URL:** `/programmes/`

**页面结构:**

**Hero Section:**
- 标题："Government Programmes / 政府项目"
- 副标题："Supporting the community through funded programmes"
- 小徽章：Trafford Council Logo

**项目简介:**
- 博文集团与Trafford Council合作关系
- 政府项目的社会意义

**两个主要项目入口:**
```
[卡片1] HAF项目
        假期活动和食品项目 → /programmes/programmes-haf/
        标签：FREE 免费

[卡片2] 社区服务
        其他社区项目介绍 → /programmes/programmes-community/
```

#### 6.2 HAF项目页面 HAF Programme Page

**URL:** `/programmes/programmes-haf/`

**页面类型:** SINGLE_PAGE

**内容:**
```markdown
# HAF项目 Holiday Activities and Food Programme

## 关于HAF About HAF
Holiday Activities and Food (HAF) 项目是英国政府资助的重要社区项目...

## 项目目标 Programme Goals
- 为符合条件的儿童提供免费的健康餐食
- 组织各类教育和娱乐活动
- 促进儿童的身心健康发展
- 支持家庭减轻假期照看负担

## 活动内容 Activities
- 中华文化体验（书法、剪纸、中国结）
- 体育运动（羽毛球、国际象棋）
- 艺术创作和手工制作
- 团队游戏和户外活动
- 每日提供健康午餐和小食

## 参与资格 Eligibility
该项目面向5-16岁符合以下条件的儿童：
- 有资格享受免费校餐（Free School Meals）
- 居住在Trafford地区

## 活动安排 Schedule
HAF项目通常在以下假期期间举办：
- 复活节假期（Easter）：2周
- 暑假（Summer）：4周
- 圣诞假期（Christmas）：1周

## 如何报名 How to Apply
报名方式将通过学校和社区渠道公布。
联系邮箱：haf@boweneducation.org
咨询电话：0161 xxx xxxx

## 项目优势 Benefits
- ✓ 完全免费，包括所有活动和餐食
- ✓ 专业教练和工作人员指导
- ✓ 安全友好的环境
- ✓ 结识新朋友，学习新技能
```

#### 6.3 社区服务页面 Community Services Page

**URL:** `/programmes/programmes-community/`

**页面类型:** POST列表页

**内容:**
- 其他社区项目介绍文章
- 志愿者招募信息
- 社区活动回顾

---

### 7. 博文活动页面 Events Pages

#### 7.1 博文活动首页

**URL:** `/events/`

**页面结构:**

**Hero Section:**
- 标题:"Bowen Events / 博文活动"
- 副标题："Cultural exchange and community activities"

**活动分类:**
```
[卡片1] 河南大学合作
        寻根之旅和文化交流 → /events/events-henan/

[卡片2] 活动回顾
        查看往期活动照片和报道 → /events/events-gallery/
```

#### 7.2 河南大学合作页面 Henan University Partnership Page

**URL:** `/events/events-henan/`

**页面类型:** SINGLE_PAGE

**内容:**
```markdown
# 河南大学合作项目
# Strategic Partnership with Henan University

## 合作简介 Partnership Overview
博文集团与中国河南大学建立了长期战略合作伙伴关系...

## 合作内容 Cooperation Areas
- 师资交流：河南大学定期派遣优秀教师
- 学生交流：组织学生互访活动
- 文化活动：联合举办文化推广活动
- 资源共享：共享教学资源和研究成果

## 寻根之旅 Root-seeking Tours
每年组织"寻根之旅"活动，带领华裔青少年回到中国：
- 参观河南大学校园
- 游览历史文化名城
- 与中国学生交流
- 参加文化体验活动

## Easter访华计划 Easter China Trip
每年复活节期间，为期两周的访华活动：
- 日期：每年复活节假期
- 对象：12-18岁学生
- 行程：河南（开封、郑州、洛阳）+ 北京
- 住宿：大学宿舍和精选酒店
- 陪同：专业领队和河南大学志愿者

## 报名咨询 Enquiry
邮箱：china-trip@boweneducation.org
电话：0161 xxx xxxx
```

#### 7.3 活动回顾页面 Event Gallery Page

**URL:** `/events/events-gallery/`

**页面类型:** POST列表页

**内容:**
- 往期活动报道文章
- 照片图集
- 视频回顾
- 每篇文章包含：活动时间、地点、参与人数、活动亮点

---

### 8. 新闻中心页面 News Center

**URL:** `/news/`

**页面类型:** POST列表页

**页面结构:**

**Page Hero:**
- 标题："News Center / 新闻中心"
- 副标题："Stay updated with our latest news and announcements"

**筛选和排序 Filters & Sorting:**
```
[分类筛选] 全部 | 学校新闻 | 俱乐部动态 | 活动通知 | 政府项目

[排序方式] 最新发布 | 最多阅读
```

**新闻列表:**
- 每页显示 12 篇文章
- 卡片式布局（3列桌面，1列移动）
- 每个卡片：缩略图 + 日期 + 分类标签 + 标题 + 摘要 + 阅读更多

**侧边栏 Sidebar (可选):**
- 热门文章 Popular Posts
- 最新评论 Recent Comments (如果启用评论功能)
- 分类导航 Categories

---

### 9. 学科辅导页面 Academic Tutoring

**URL:** `/tutoring/`

**页面类型:** PRODUCT列表页

**页面结构:**

**Hero Section:**
- 标题："Academic Tutoring / 学科辅导"
- 副标题："One-to-one and small group tutoring for all subjects"

**学科分类 Subject Categories:**
- 数学 Maths
- 英语 English
- 科学 Science (Physics, Chemistry, Biology)
- 人文 Humanities (History, Geography)

**每个学科卡片:**
```
[学科图标]
学科名称：GCSE Mathematics
辅导形式：一对一 / 小组课（2-4人）
适合年龄：11-16岁
课时费用：£35/小时（一对一）/ £25/小时（小组）

课程特色：
✓ 经验丰富的教师
✓ 个性化学习计划
✓ 考试技巧培训
✓ 定期进度报告

[查看详情] [立即咨询]
```

---

### 10. 联系我们页面 Contact Us Page

**URL:** `/contact/`

**页面类型:** SINGLE_PAGE

**页面结构:**

**Page Hero:**
- 标题："Contact Us / 联系我们"
- 副标题："Get in touch and we'll get back to you soon"

**联系方式 Contact Information:**
```
📍 地址 Address:
   [完整地址]
   Manchester, Postcode

📞 电话 Phone:
   0161 xxx xxxx
   (周一至周五 9:00-17:00)

📧 邮箱 Email:
   info@boweneducation.org
   (24小时内回复)

🕐 营业时间 Opening Hours:
   周六 Saturday: 9:00-17:00
   周日 Sunday: 9:00-17:00
   周一至周五 Mon-Fri: 预约访问
```

**联系表单:**
- 与首页表单相同的字段
- 表单提交后发送确认邮件

**Google地图:**
- 嵌入地图，标记地址

**社交媒体 Social Media:**
```
关注我们 Follow Us:
[Facebook图标] [Instagram图标] [WeChat图标]
```

**常见问题快捷链接 Quick FAQs:**
- 如何报名课程？
- 学费如何支付？
- 有试听课吗？
- HAF项目如何申请？

---

## 功能需求 Functional Requirements

### 1. 导航系统 Navigation System

**主导航 Primary Navigation:**
- 固定在页面顶部（sticky header）
- 滚动后背景色变化（透明 → 白色）
- 二级下拉菜单（桌面端hover，移动端click）

**面包屑导航 Breadcrumb:**
- 所有内页都显示面包屑
- 格式：首页 > 一级栏目 > 二级栏目 > 当前页

**移动端菜单 Mobile Menu:**
- 汉堡菜单图标（三条横线）
- 从右侧滑出全屏菜单
- 支持二级菜单展开/收起

### 2. 搜索功能 Search Function

**全站搜索 Site-wide Search:**
- 顶部导航栏搜索图标
- 点击后展开搜索框
- 支持搜索：
  - 文章标题和内容
  - 课程名称和描述
  - 活动信息

**搜索结果页 Search Results Page:**
- 显示匹配结果数量
- 按相关性排序
- 高亮显示匹配关键词

### 3. 多语言支持 Multi-language Support

**语言切换 Language Switcher:**
- 位置：顶部右上角
- 支持语言：英文 English / 中文 Chinese (Simplified)
- 切换方式：下拉菜单或切换按钮

**内容翻译 Content Translation:**
- 所有界面文字双语显示
- 动态内容（文章、课程）支持双语编辑
- URL结构：
  - 英文：`/about/`
  - 中文：`/about/?lang=zh`

### 4. 表单处理 Form Handling

**联系表单 Contact Form:**
- 前端验证：必填项、邮箱格式
- 后端验证：防止恶意提交
- reCAPTCHA防止垃圾邮件（可选）
- 提交后行为：
  - 发送确认邮件给用户
  - 通知邮件给管理员
  - 数据保存到数据库

**报名表单 Enrolment Form:**
- 字段：学生姓名、年龄、家长姓名、联系方式、报名课程
- 支持文件上传（学生照片、证件等）
- 付款链接或说明

### 5. 内容管理 Content Management

**文章发布 Article Publishing:**
- 支持富文本编辑器（图片、视频、链接）
- 文章分类和标签
- 发布状态：草稿、已发布、下线
- 定时发布功能
- 推荐文章标记（显示在首页）

**媒体管理 Media Management:**
- 图片上传和管理
- 图片自动压缩和优化
- 视频嵌入（YouTube、Vimeo）
- 文件下载管理（PDF、文档）

### 6. SEO优化 SEO Optimization

**页面级SEO Page-level SEO:**
- 自定义页面标题 Title
- 自定义描述 Meta Description
- 自定义关键词 Keywords
- Open Graph标签（社交媒体分享）
- Twitter Card标签
- Canonical URL

**结构化数据 Structured Data:**
- Schema.org标记
- Organization markup（集团信息）
- EducationalOrganization markup
- Course markup（课程信息）
- Event markup（活动信息）

**站点地图 Sitemap:**
- 自动生成XML sitemap
- 提交到Google Search Console
- 更新频率：每日

### 7. 性能优化 Performance Optimization

**图片优化 Image Optimization:**
- WebP格式支持
- 懒加载（lazy loading）
- 响应式图片（srcset）
- CDN加速（可选）

**代码优化 Code Optimization:**
- CSS/JS压缩和合并
- 关键CSS内联
- 异步加载非关键资源
- 浏览器缓存配置

**数据库优化 Database Optimization:**
- 查询结果缓存（10分钟）
- 数据库索引优化
- 分页查询

### 8. 分析和追踪 Analytics & Tracking

**Google Analytics:**
- GA4集成
- 页面浏览追踪
- 事件追踪：
  - 表单提交
  - 按钮点击
  - 文件下载
  - 外部链接点击

**转化追踪 Conversion Tracking:**
- 目标设置：
  - 联系表单提交
  - 课程查看
  - 电话点击
  - 邮件点击

### 9. 社交媒体集成 Social Media Integration

**社交分享 Social Sharing:**
- 文章详情页分享按钮
- 支持：Facebook、Twitter、WeChat、WhatsApp
- 分享统计

**社交关注 Social Follow:**
- 页脚社交媒体图标
- 链接到：
  - Facebook主页
  - Instagram账号
  - WeChat公众号（二维码）

### 10. 安全性 Security

**数据安全 Data Security:**
- HTTPS加密
- 表单CSRF保护
- SQL注入防护
- XSS攻击防护

**用户隐私 User Privacy:**
- Cookie使用声明
- 隐私政策页面
- GDPR合规（可选）
- 数据保留政策

---

## 设计需求 Design Requirements

### 1. 设计风格 Design Style

**品牌色彩 Brand Colors:**
```
主色 Primary Color:
  - 深蓝色 Deep Blue: #1e3a8a (教育、信任、专业)

辅助色 Secondary Colors:
  - 中国红 Chinese Red: #dc2626 (文化、热情)
  - 金色 Gold: #f59e0b (荣誉、高端)

中性色 Neutral Colors:
  - 深灰 Dark Gray: #1f2937 (文字)
  - 中灰 Medium Gray: #6b7280 (次要文字)
  - 浅灰 Light Gray: #f3f4f6 (背景)
  - 白色 White: #ffffff
```

**排版 Typography:**
```
英文字体 English Font:
  - Headings: 'Poppins', sans-serif (600/700)
  - Body: 'Inter', sans-serif (400/500)

中文字体 Chinese Font:
  - 'Noto Sans SC', sans-serif (400/500/700)

字号 Font Sizes:
  - H1: 48px (桌面) / 32px (移动)
  - H2: 36px (桌面) / 28px (移动)
  - H3: 28px (桌面) / 24px (移动)
  - Body: 16px (桌面) / 14px (移动)
```

### 2. 响应式设计 Responsive Design

**断点 Breakpoints:**
```
- 移动端 Mobile: < 768px
- 平板 Tablet: 768px - 991px
- 桌面 Desktop: ≥ 992px
- 大屏 Large Desktop: ≥ 1200px
```

**移动端优化 Mobile Optimization:**
- 触摸友好的按钮尺寸（最小44x44px）
- 可点击区域足够大
- 简化移动端菜单
- 移动端隐藏不必要元素

### 3. UI组件 UI Components

**按钮 Buttons:**
```
主要按钮 Primary Button:
  - 背景色：主色 #1e3a8a
  - 文字色：白色
  - 悬停：背景变暗10%
  - 圆角：6px
  - 内边距：12px 24px

次要按钮 Secondary Button:
  - 背景色：透明
  - 边框：2px solid #1e3a8a
  - 文字色：#1e3a8a
  - 悬停：背景填充，文字变白
```

**卡片 Cards:**
```
标准卡片:
  - 白色背景
  - 圆角：8px
  - 阴影：0 2px 8px rgba(0,0,0,0.1)
  - 悬停：阴影加深，上浮5px
  - 内边距：24px
```

**表单元素 Form Elements:**
```
输入框 Input Fields:
  - 边框：1px solid #d1d5db
  - 圆角：6px
  - 内边距：12px
  - 聚焦：边框变为主色

下拉菜单 Select:
  - 与输入框样式一致
  - 自定义箭头图标

文本域 Textarea:
  - 最小高度：120px
  - 可调整大小
```

### 4. 动画效果 Animations

**页面加载动画 Page Load Animations:**
- AOS (Animate On Scroll) 库
- 元素从下方淡入：fade-up
- 延迟时间：100-300ms递增

**交互动画 Interaction Animations:**
- 按钮悬停：transform scale(1.05)
- 卡片悬停：transform translateY(-5px)
- 图片悬停：transform scale(1.1)
- 过渡时间：0.3s ease

**页面切换 Page Transitions:**
- 平滑滚动到锚点
- 加载状态指示器

### 5. 图标系统 Icon System

**图标库 Icon Library:**
- Feather Icons 或 Heroicons
- 统一线条宽度：2px
- 尺寸：16px、20px、24px

**自定义图标 Custom Icons:**
- 学科图标（数学、英语等）
- 活动图标（象棋、羽毛球等）
- SVG格式，可缩放

### 6. 图片规范 Image Guidelines

**图片尺寸 Image Sizes:**
```
Hero背景图：1920x1080px (16:9)
课程卡片封面：800x450px (16:9)
新闻缩略图：600x400px (3:2)
教师头像：400x400px (1:1)
Logo：高度60px，宽度自适应
```

**图片格式 Image Formats:**
- 照片：WebP格式（备用JPEG）
- Logo/图标：SVG（备用PNG）
- 压缩：保持视觉质量前提下最大压缩

---

## 技术需求 Technical Requirements

### 1. 技术栈 Technology Stack

**后端 Backend:**
- 框架：FastAPI (Python 3.9+)
- ORM：SQLAlchemy
- 数据库：SQLite (开发) / PostgreSQL (生产)
- 模板引擎：Jinja2

**前端 Frontend:**
- JavaScript框架：Alpine.js 3.x
- CSS框架：Bootstrap 5 或 Tailwind CSS
- 图标库：Feather Icons
- 动画库：AOS (Animate On Scroll)

**第三方服务 Third-party Services:**
- Google Maps API（地图）
- Google Analytics 4（分析）
- reCAPTCHA v3（表单保护）
- Swiper.js（轮播图）

### 2. 服务器要求 Server Requirements

**最低配置 Minimum Requirements:**
- CPU：2核
- 内存：2GB RAM
- 存储：20GB SSD
- 带宽：100Mbps

**推荐配置 Recommended:**
- CPU：4核
- 内存：4GB RAM
- 存储：50GB SSD
- 带宽：1Gbps

**操作系统 Operating System:**
- Linux (Ubuntu 20.04 LTS 或更高)
- Python 3.9+
- Nginx（Web服务器）
- Supervisor（进程管理）

### 3. 数据库设计 Database Design

**核心表 Core Tables:**

**site_column (栏目表):**
```
- id: 主键
- name: 栏目名称
- slug: URL别名
- parent_id: 父栏目ID（外键，支持多级）
- column_type: 栏目类型（SINGLE_PAGE/POST/PRODUCT/CUSTOM）
- sort_order: 排序序号
- is_enabled: 是否启用
- show_in_nav: 是否显示在导航菜单
- icon: 图标（可选）
- description: 描述
- created_at: 创建时间
- updated_at: 更新时间
```

**post (文章表):**
```
- id: 主键
- column_id: 关联栏目ID
- title: 文章标题
- slug: URL别名
- summary: 摘要
- content_html: 正文HTML
- cover_media_id: 封面图ID
- is_recommended: 是否推荐（显示在首页）
- status: 状态（draft/published/offline）
- published_at: 发布时间
- seo_title: SEO标题
- seo_description: SEO描述
- views: 浏览次数
- created_at: 创建时间
- updated_at: 更新时间
```

**single_page (单页表):**
```
- id: 主键
- column_id: 关联栏目ID
- title: 页面标题
- subtitle: 副标题
- content_html: 页面内容HTML
- status: 状态
- published_at: 发布时间
- seo_title: SEO标题
- seo_description: SEO描述
- created_at: 创建时间
- updated_at: 更新时间
```

**site_setting (站点设置表):**
```
- id: 主键
- setting_key: 设置键
- value_text: 文本值
- description: 描述
```

**media_file (媒体文件表):**
```
- id: 主键
- filename: 文件名
- file_path: 文件路径
- file_url: 访问URL
- file_type: 文件类型（image/video/document）
- file_size: 文件大小
- mime_type: MIME类型
- uploaded_at: 上传时间
```

### 4. API端点 API Endpoints

**公共API Public APIs:**
```
GET  /api/navigation          # 获取导航菜单
GET  /api/posts?column=news   # 获取文章列表
GET  /api/posts/{slug}        # 获取文章详情
POST /api/contact             # 提交联系表单
GET  /api/settings            # 获取站点设置
GET  /api/search?q=keyword    # 搜索
```

**管理API Admin APIs (需要认证):**
```
POST   /api/admin/posts       # 创建文章
PUT    /api/admin/posts/{id}  # 更新文章
DELETE /api/admin/posts/{id}  # 删除文章
POST   /api/admin/media       # 上传媒体文件
```

### 5. 缓存策略 Caching Strategy

**页面缓存 Page Caching:**
- 首页：缓存10分钟
- 文章列表页：缓存10分钟
- 文章详情页：缓存30分钟
- 单页内容：缓存1小时

**数据缓存 Data Caching:**
- 导航菜单：缓存10分钟
- 站点设置：缓存1小时
- 统计数字：缓存1天

**缓存清除 Cache Invalidation:**
- 发布新文章时清除相关列表缓存
- 更新站点设置时清除设置缓存
- 提供手动清除全部缓存功能

### 6. 部署要求 Deployment Requirements

**部署方式 Deployment Method:**
- Docker容器化部署（推荐）
- 或传统Nginx + Gunicorn/Uvicorn

**环境变量 Environment Variables:**
```
DATABASE_URL=sqlite:///instance/database.db
SECRET_KEY=your-secret-key
GOOGLE_MAPS_API_KEY=your-maps-key
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
```

**备份策略 Backup Strategy:**
- 数据库：每日自动备份
- 媒体文件：每周备份
- 保留最近30天备份

---

## SEO与性能 SEO & Performance

### 1. SEO优化 SEO Optimization

**页面标题格式 Page Title Format:**
```
首页: Bowen Education Group | Manchester Chinese School
内页: {页面标题} - Bowen Education Group
文章: {文章标题} | Bowen Education Group
```

**URL结构 URL Structure:**
```
清晰的层级结构:
/school/                    # 一级栏目
/school/school-curriculum/  # 二级栏目
/news/spring-term-2024/     # 文章详情

使用连字符分隔单词
全部小写
避免特殊字符
```

**Meta描述 Meta Descriptions:**
- 长度：150-160字符
- 包含关键词
- 简明扼要描述页面内容
- 每个页面独特的描述

**关键词策略 Keyword Strategy:**
```
主要关键词:
- Chinese school Manchester
- Mandarin classes Manchester
- GCSE Chinese
- A-Level Chinese
- Chess club Manchester
- Badminton club Manchester

长尾关键词:
- Chinese language courses for children Manchester
- HAF programme Trafford
- Chinese New Year celebration Manchester
```

### 2. 性能指标 Performance Metrics

**目标指标 Target Metrics:**
```
首次内容绘制 FCP: < 1.8秒
最大内容绘制 LCP: < 2.5秒
首次输入延迟 FID: < 100ms
累积布局偏移 CLS: < 0.1
总页面大小: < 2MB
请求数量: < 50个
```

**优化措施 Optimization Measures:**
- 图片懒加载
- 代码分割和按需加载
- 浏览器缓存配置
- CDN加速（可选）
- Gzip/Brotli压缩

### 3. 移动端优化 Mobile Optimization

**移动端友好 Mobile-friendly:**
- 通过Google Mobile-Friendly测试
- 响应式设计，适配所有屏幕
- 触摸目标尺寸 ≥ 44x44px
- 避免使用Flash

**移动端性能 Mobile Performance:**
- 首屏加载时间 < 3秒（3G网络）
- 优化图片大小和格式
- 减少第三方脚本

### 4. 可访问性 Accessibility

**WCAG 2.1 AA级标准:**
- 语义化HTML标签
- 图片alt属性
- 表单label标签
- 键盘导航支持
- 色彩对比度 ≥ 4.5:1
- ARIA标签（需要时）

**屏幕阅读器支持:**
- 清晰的页面结构
- 跳转到主内容链接
- 导航地标（nav, main, footer）

---

## 内容管理 Content Management

### 1. 初始内容 Initial Content

**必须准备的内容 Required Content:**

**关于集团 About Group:**
- 集团简介（500-800字）
- 历史发展
- 使命愿景
- 团队介绍（至少5位成员）

**中文学校 Chinese School:**
- 至少6个课程详细介绍
- 学期日期信息
- PTA介绍内容

**国际象棋俱乐部 Chess Club:**
- 俱乐部简介
- ECF认证说明
- 棋手注册指南

**羽毛球俱乐部 Badminton Club:**
- 俱乐部简介
- 训练时间表
- 至少3位教练介绍

**政府项目 Government Programmes:**
- HAF项目详细介绍
- 资格要求
- 报名流程

**博文活动 Events:**
- 河南大学合作介绍
- 至少5篇往期活动报道

**新闻文章 News Articles:**
- 至少10篇初始新闻文章
- 涵盖不同分类

**图片素材 Image Assets:**
- Logo（多种尺寸）
- Hero背景图（5张）
- 课程封面图（至少6张）
- 活动照片（至少20张）
- 教师/教练照片
- 合作伙伴Logo（至少6个）

### 2. 内容更新计划 Content Update Plan

**定期更新 Regular Updates:**
- 新闻文章：每周至少1篇
- 活动报道：活动后3天内发布
- 学期信息：每学期开始前2周更新
- 课程信息：有变化时及时更新

**内容审核 Content Review:**
- 每季度审核一次所有内容
- 更新过时信息
- 检查链接有效性
- 优化SEO

### 3. 多语言内容 Multi-language Content

**翻译要求 Translation Requirements:**
- 所有页面都需要中英文版本
- 专业术语保持一致
- 文化适配（日期格式、表达方式等）

**翻译优先级 Translation Priority:**
1. 高优先级：首页、课程介绍、联系页面
2. 中优先级：新闻文章、活动介绍
3. 低优先级：详细政策、内部文档

---

## 项目交付 Project Deliverables

### 1. 交付物清单 Deliverables Checklist

**代码 Code:**
- 完整的源代码
- 数据库初始化脚本
- 示例数据（seed data）
- 部署文档

**文档 Documentation:**
- 技术文档（架构、API）
- 用户手册（内容管理）
- 部署指南
- 维护指南

**培训 Training:**
- 内容管理培训（2小时）
- 系统维护培训（1小时）
- Q&A支持

### 2. 验收标准 Acceptance Criteria

**功能验收 Functional Acceptance:**
- 所有页面正常显示
- 所有表单正常提交
- 导航菜单正常工作
- 搜索功能正常
- 多语言切换正常

**性能验收 Performance Acceptance:**
- 首页加载时间 < 3秒
- 内页加载时间 < 2秒
- 通过Google PageSpeed测试（分数 > 80）

**兼容性验收 Compatibility Acceptance:**
- Chrome、Firefox、Safari、Edge最新版本
- iOS Safari、Android Chrome
- 桌面、平板、移动端

**SEO验收 SEO Acceptance:**
- 通过Google Mobile-Friendly测试
- 所有页面有正确的title和meta
- 生成并提交sitemap
- 结构化数据正确

---

## 项目时间表 Project Timeline

### 阶段1：设计和准备 (2周)
- Week 1: 需求确认、设计稿制作
- Week 2: 内容准备、图片素材收集

### 阶段2：开发 (4-6周)
- Week 3-4: 后端开发、数据库设计
- Week 5-6: 前端开发、模板制作
- Week 7-8: 功能集成、测试

### 阶段3：测试和上线 (1-2周)
- Week 9: 内容录入、测试
- Week 10: 修改完善、部署上线

### 阶段4：维护支持 (持续)
- 3个月免费维护期
- Bug修复和小调整
- 内容更新支持

---

## 附录 Appendix

### A. 术语表 Glossary

- **CMS**: Content Management System 内容管理系统
- **SEO**: Search Engine Optimization 搜索引擎优化
- **CTA**: Call To Action 行动号召
- **HAF**: Holiday Activities and Food 假期活动和食品项目
- **ECF**: English Chess Federation 英格兰国际象棋联合会
- **HSK**: 汉语水平考试
- **YCT**: 青少年汉语考试

### B. 参考资源 References

**设计参考 Design References:**
- 其他教育机构网站
- Bootstrap组件库
- Material Design指南

**技术参考 Technical References:**
- FastAPI官方文档
- SQLAlchemy文档
- Alpine.js文档

---

**文档结束 End of Document**

*本需求文档为博文集团网站项目的指导性文件，如有疑问或需要调整，请及时沟通。*
