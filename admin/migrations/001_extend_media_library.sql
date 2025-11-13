-- 媒体库扩展迁移脚本
-- 创建时间: 2025-11-14
-- 说明: 扩展媒体文件表，添加文件夹管理功能

-- ============================================================
-- 第 1 步：创建媒体文件夹表
-- ============================================================

CREATE TABLE IF NOT EXISTS media_folder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,               -- 文件夹名称
    parent_id INTEGER,                        -- 父文件夹 ID（支持嵌套）
    path VARCHAR(500) NOT NULL,               -- 文件夹路径
    description TEXT,                         -- 描述
    sort_order INTEGER DEFAULT 0,             -- 排序
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (parent_id) REFERENCES media_folder(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_media_folder_parent ON media_folder(parent_id);

-- ============================================================
-- 第 2 步：扩展 media_file 表（添加新字段）
-- ============================================================

-- 添加文件类型字段
ALTER TABLE media_file ADD COLUMN file_type VARCHAR(50) DEFAULT 'image';

-- 添加文件夹关联
ALTER TABLE media_file ADD COLUMN folder_id INTEGER;

-- 添加标签字段
ALTER TABLE media_file ADD COLUMN tags VARCHAR(500);

-- 添加描述字段
ALTER TABLE media_file ADD COLUMN description TEXT;

-- 添加上传者字段
ALTER TABLE media_file ADD COLUMN uploaded_by VARCHAR(100);

-- 添加公开状态
ALTER TABLE media_file ADD COLUMN is_public BOOLEAN DEFAULT 1;

-- 添加下载次数
ALTER TABLE media_file ADD COLUMN download_count INTEGER DEFAULT 0;

-- 添加查看次数
ALTER TABLE media_file ADD COLUMN view_count INTEGER DEFAULT 0;

-- 添加视频专用字段
ALTER TABLE media_file ADD COLUMN duration INTEGER;  -- 视频时长（秒）
ALTER TABLE media_file ADD COLUMN video_thumbnail_path VARCHAR(500);  -- 视频缩略图

-- 添加 SEO 字段
ALTER TABLE media_file ADD COLUMN seo_keywords VARCHAR(500);

-- ============================================================
-- 第 3 步：创建索引
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_media_file_type ON media_file(file_type);
CREATE INDEX IF NOT EXISTS idx_media_file_folder ON media_file(folder_id);
CREATE INDEX IF NOT EXISTS idx_media_file_created_at ON media_file(created_at);

-- ============================================================
-- 第 4 步：插入默认文件夹
-- ============================================================

INSERT INTO media_folder (name, path, description, sort_order) VALUES
('全部文件', '/', '所有媒体文件', 0),
('图片', '/images', '图片文件', 1),
('视频', '/videos', '视频文件', 2),
('文档', '/documents', '文档文件', 3),
('其他', '/others', '其他文件', 4);

-- ============================================================
-- 第 5 步：更新现有数据
-- ============================================================

-- 将现有文件的 file_type 设置为 'image'（基于 mime_type）
UPDATE media_file
SET file_type = CASE
    WHEN mime_type LIKE 'image/%' THEN 'image'
    WHEN mime_type LIKE 'video/%' THEN 'video'
    WHEN mime_type LIKE 'application/pdf%' THEN 'document'
    WHEN mime_type LIKE 'application/%' THEN 'document'
    ELSE 'other'
END
WHERE file_type IS NULL OR file_type = '';

-- 将现有图片文件分配到"图片"文件夹
UPDATE media_file
SET folder_id = (SELECT id FROM media_folder WHERE name = '图片' LIMIT 1)
WHERE file_type = 'image' AND folder_id IS NULL;

-- 将现有视频文件分配到"视频"文件夹
UPDATE media_file
SET folder_id = (SELECT id FROM media_folder WHERE name = '视频' LIMIT 1)
WHERE file_type = 'video' AND folder_id IS NULL;

-- 将现有文档文件分配到"文档"文件夹
UPDATE media_file
SET folder_id = (SELECT id FROM media_folder WHERE name = '文档' LIMIT 1)
WHERE file_type = 'document' AND folder_id IS NULL;

-- 将其他文件分配到"其他"文件夹
UPDATE media_file
SET folder_id = (SELECT id FROM media_folder WHERE name = '其他' LIMIT 1)
WHERE file_type = 'other' AND folder_id IS NULL;

-- ============================================================
-- 迁移完成
-- ============================================================
