-- =========================================
-- Bowen-Education-Manchester - Database Seed Data Template
-- Generated: 2025-11-02 11:06:19
-- =========================================

-- Clean existing data (optional - comment out if appending)
DELETE FROM product_category_link;
DELETE FROM post_category_link;
DELETE FROM product;
DELETE FROM post;
DELETE FROM product_category;
DELETE FROM post_category;
DELETE FROM single_page;
DELETE FROM site_column;
DELETE FROM site_setting;

-- =========================================
-- 1. SITE SETTINGS
-- =========================================
INSERT INTO site_setting (`key`, value, created_at, updated_at) VALUES
('site_name', 'Bowen-Education-Manchester', datetime('now'), datetime('now')),
('site_description', 'A professional website for Bowen-Education-Manchester', datetime('now'), datetime('now')),
('phone', '+64 9 123 4567', datetime('now'), datetime('now')),
('email', 'info@bowen-education-manchester.com', datetime('now'), datetime('now')),
('address', 'Your Address Here', datetime('now'), datetime('now')),
('business_hours', 'Monday-Friday 9:00am-5:00pm', datetime('now'), datetime('now')),
('copyright', '© 2025 Bowen-Education-Manchester. All rights reserved.', datetime('now'), datetime('now'));

-- =========================================
-- 2. SITE COLUMNS (Navigation Structure)
-- =========================================
INSERT INTO site_column (id, name, slug, type, description, is_visible, `order`, created_at, updated_at) VALUES
(1, 'Home', 'home', 'CUSTOM', 'Homepage', 1, 1, datetime('now'), datetime('now')),
(2, 'About Us', 'about', 'SINGLE_PAGE', 'About page', 1, 2, datetime('now'), datetime('now')),
(3, 'Services', 'services', 'SINGLE_PAGE', 'Services page', 1, 3, datetime('now'), datetime('now')),
(4, 'Blog', 'blog', 'POST', 'Blog posts and articles', 1, 4, datetime('now'), datetime('now')),
(5, 'Contact', 'contact', 'SINGLE_PAGE', 'Contact information and form', 1, 5, datetime('now'), datetime('now'));
