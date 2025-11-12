-- 为主栏目 Hero 添加额外配置字段
-- 日期: 2025-11-12
-- 说明: 添加标题、英文标题、标语、CTA按钮等字段，以支持主栏目的统一 Hero 组件

-- 添加新字段
ALTER TABLE site_column ADD COLUMN hero_title TEXT;
ALTER TABLE site_column ADD COLUMN hero_title_en TEXT;
ALTER TABLE site_column ADD COLUMN hero_tagline TEXT;
ALTER TABLE site_column ADD COLUMN hero_cta_text TEXT;
ALTER TABLE site_column ADD COLUMN hero_cta_url TEXT;

-- 验证字段添加
SELECT name FROM pragma_table_info('site_column') WHERE name LIKE 'hero%';
