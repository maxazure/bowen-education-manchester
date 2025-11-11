-- 为 site_column 表添加 hero 背景图片和描述字段
-- 执行时间: 2025-11-12

-- 添加描述字段（用于hero区域的副标题）
ALTER TABLE site_column ADD COLUMN description TEXT;

-- 添加hero背景图片ID字段
ALTER TABLE site_column ADD COLUMN hero_media_id INTEGER;

-- 添加外键约束（如果需要）
-- 注意：SQLite的ALTER TABLE不支持添加外键，需要重建表才能添加外键约束
-- 这里先添加字段，外键约束可以在应用层面控制
