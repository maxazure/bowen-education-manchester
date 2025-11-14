-- ============================================================
-- 相册管理数据库迁移脚本
-- 创建日期: 2025-11-14
-- 描述: 创建相册管理所需的数据库表
-- ============================================================

-- ============================================================
-- 1. 相册分类表 (album_category)
-- ============================================================
CREATE TABLE IF NOT EXISTS album_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE,
    description TEXT,
    sort_order INTEGER DEFAULT 0,
    is_enabled BOOLEAN DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认分类
INSERT INTO album_category (name, slug, description, sort_order) VALUES
('学校活动', 'school-activities', '学校各类活动照片', 1),
('课堂风采', 'classroom-moments', '课堂教学精彩瞬间', 2),
('学生作品', 'student-works', '学生优秀作品展示', 3),
('校园风景', 'campus-scenery', '校园美丽风景', 4),
('获奖荣誉', 'awards-honors', '获奖证书和荣誉', 5);

-- ============================================================
-- 2. 相册表 (album)
-- ============================================================
CREATE TABLE IF NOT EXISTS album (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 基本信息
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE,
    description TEXT,
    cover_media_id INTEGER,

    -- 分类和标签
    category_id INTEGER,
    tags VARCHAR(500),

    -- 统计信息
    photo_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,

    -- 排序和状态
    sort_order INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft',

    -- SEO 信息
    seo_title VARCHAR(200),
    seo_description TEXT,
    seo_keywords VARCHAR(500),

    -- 时间戳
    published_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (cover_media_id) REFERENCES media_file(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES album_category(id) ON DELETE SET NULL
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_album_status ON album(status);
CREATE INDEX IF NOT EXISTS idx_album_created_at ON album(created_at);
CREATE INDEX IF NOT EXISTS idx_album_category ON album(category_id);
CREATE INDEX IF NOT EXISTS idx_album_slug ON album(slug);

-- ============================================================
-- 3. 相册照片关联表 (album_photo)
-- ============================================================
CREATE TABLE IF NOT EXISTS album_photo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    media_id INTEGER NOT NULL,
    caption TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (album_id) REFERENCES album(id) ON DELETE CASCADE,
    FOREIGN KEY (media_id) REFERENCES media_file(id) ON DELETE CASCADE,

    -- 唯一约束：同一相册不能重复添加同一照片
    UNIQUE(album_id, media_id)
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_album_photo_album ON album_photo(album_id);
CREATE INDEX IF NOT EXISTS idx_album_photo_media ON album_photo(media_id);
CREATE INDEX IF NOT EXISTS idx_album_photo_sort ON album_photo(album_id, sort_order);

-- ============================================================
-- 4. 插入示例数据（用于测试）
-- ============================================================

-- 示例相册 1
INSERT INTO album (
    title,
    slug,
    description,
    category_id,
    tags,
    status,
    sort_order,
    seo_title,
    seo_description,
    published_at
) VALUES (
    '2024年春季运动会',
    '2024-spring-sports-day',
    '博文教育2024年春季运动会精彩瞬间，记录孩子们在赛场上的拼搏与欢乐。',
    1,
    '["运动会", "2024", "春季", "体育"]',
    'published',
    1,
    '2024年春季运动会 - 博文教育',
    '博文教育2024年春季运动会精彩瞬间，展现学生们的运动风采和团队精神。',
    CURRENT_TIMESTAMP
);

-- 示例相册 2
INSERT INTO album (
    title,
    slug,
    description,
    category_id,
    tags,
    status,
    sort_order,
    seo_title,
    seo_description,
    published_at
) VALUES (
    '优秀学生作品展',
    'excellent-student-works',
    '展示学生们的优秀作品，包括绘画、手工、书法等多种形式。',
    3,
    '["学生作品", "艺术", "创作"]',
    'published',
    2,
    '优秀学生作品展 - 博文教育',
    '博文教育学生优秀作品展示，包括绘画、手工、书法等多种艺术形式。',
    CURRENT_TIMESTAMP
);

-- 示例相册 3
INSERT INTO album (
    title,
    slug,
    description,
    category_id,
    tags,
    status,
    sort_order
) VALUES (
    '校园四季风光',
    'campus-four-seasons',
    '记录校园一年四季的美丽景色，感受时光流转中的校园变化。',
    4,
    '["校园", "风景", "四季"]',
    'draft',
    3
);

-- ============================================================
-- 5. 触发器：自动更新 updated_at 字段
-- ============================================================

-- album_category 表触发器
CREATE TRIGGER IF NOT EXISTS update_album_category_timestamp
AFTER UPDATE ON album_category
FOR EACH ROW
BEGIN
    UPDATE album_category SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- album 表触发器
CREATE TRIGGER IF NOT EXISTS update_album_timestamp
AFTER UPDATE ON album
FOR EACH ROW
BEGIN
    UPDATE album SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ============================================================
-- 6. 触发器：自动更新 photo_count
-- ============================================================

-- 添加照片时增加计数
CREATE TRIGGER IF NOT EXISTS album_photo_count_insert
AFTER INSERT ON album_photo
FOR EACH ROW
BEGIN
    UPDATE album SET photo_count = photo_count + 1 WHERE id = NEW.album_id;
END;

-- 删除照片时减少计数
CREATE TRIGGER IF NOT EXISTS album_photo_count_delete
AFTER DELETE ON album_photo
FOR EACH ROW
BEGIN
    UPDATE album SET photo_count = photo_count - 1 WHERE id = OLD.album_id;
END;

-- ============================================================
-- 迁移完成
-- ============================================================
