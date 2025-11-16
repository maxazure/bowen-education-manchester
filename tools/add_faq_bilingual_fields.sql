-- 为 FAQ 表添加中英双语字段
-- 执行时间: 2025-11-16
-- 说明: 扩展 FAQ 支持中英双语问答

-- 添加英文字段
ALTER TABLE faq ADD COLUMN question_en VARCHAR(500);
ALTER TABLE faq ADD COLUMN answer_en TEXT;

-- 添加中文字段
ALTER TABLE faq ADD COLUMN question_zh VARCHAR(500);
ALTER TABLE faq ADD COLUMN answer_zh TEXT;

-- 将现有数据迁移到英文字段
UPDATE faq SET
  question_en = question,
  answer_en = answer;

-- 注释说明:
-- question: 保留作为主问题（向后兼容）
-- answer: 保留作为主答案（向后兼容）
-- question_en: 英文问题
-- answer_en: 英文答案
-- question_zh: 中文问题
-- answer_zh: 中文答案
