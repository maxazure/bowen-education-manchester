-- 为主栏目配置 Hero 数据
-- 日期: 2025-11-12
-- 说明: 根据现有模板内容为各主栏目配置 Hero 标题、标语、CTA等信息

-- 1. 中文学校 (school)
UPDATE site_column SET
    hero_title = '博文中文学校',
    hero_title_en = 'Bowen Chinese School',
    hero_tagline = '传承中华文化 · 培养双语人才',
    hero_cta_text = '查看课程',
    hero_cta_url = '/school-curriculum/'
WHERE slug = 'school';

-- 2. 国际象棋俱乐部 (chess)
UPDATE site_column SET
    hero_title = '博文国际象棋俱乐部',
    hero_title_en = 'Bowen Chess Club',
    hero_tagline = 'ECF注册俱乐部 · 专业教练团队 · 竞赛平台',
    hero_cta_text = '预约免费试课',
    hero_cta_url = '/contact'
WHERE slug = 'chess';

-- 3. 羽毛球俱乐部 (badminton)
UPDATE site_column SET
    hero_title = '博文羽毛球俱乐部',
    hero_title_en = 'Bowen Badminton Club',
    hero_tagline = '专业羽毛球训练 · 培养运动技能 · 健康成长',
    hero_cta_text = '了解课程',
    hero_cta_url = '#programs'
WHERE slug = 'badminton';

-- 4. 政府项目 (programmes)
UPDATE site_column SET
    hero_title = '政府项目',
    hero_title_en = 'Government Programmes',
    hero_tagline = '参与政府合作项目 · 服务社区发展',
    hero_cta_text = '联系我们',
    hero_cta_url = '/contact'
WHERE slug = 'programmes';

-- 5. 博文活动 (events)
UPDATE site_column SET
    hero_title = '博文活动',
    hero_title_en = 'Bowen Events',
    hero_tagline = '丰富多彩的文化活动 · 专业培训 · 精彩赛事',
    hero_cta_text = '查看近期活动',
    hero_cta_url = '#upcoming-events'
WHERE slug = 'events';

-- 6. 联系我们 (contact)
UPDATE site_column SET
    hero_title = '联系我们',
    hero_title_en = 'Contact Us',
    hero_tagline = '我们期待与您沟通 · 解答您的疑问',
    hero_cta_text = NULL,
    hero_cta_url = NULL
WHERE slug = 'contact';

-- 验证更新结果
SELECT
    slug,
    hero_title,
    hero_title_en,
    hero_tagline,
    hero_cta_text,
    hero_cta_url
FROM site_column
WHERE slug IN ('school', 'chess', 'badminton', 'programmes', 'events', 'contact')
ORDER BY
    CASE slug
        WHEN 'school' THEN 1
        WHEN 'chess' THEN 2
        WHEN 'badminton' THEN 3
        WHEN 'programmes' THEN 4
        WHEN 'events' THEN 5
        WHEN 'contact' THEN 6
    END;
