-- Migration: Add menu_location field to site_column table
-- Date: 2025-11-05
-- Description: Add menu_location enum field to support different menu positions (header, footer, both, none)

-- Step 1: Add the menu_location column with default value 'header'
ALTER TABLE site_column
ADD COLUMN menu_location VARCHAR(20) NOT NULL DEFAULT 'header';

-- Step 2: Update existing data - set all current columns to 'header' by default
-- You can manually update specific columns to 'footer' if needed

-- Step 3: Create index for better query performance
CREATE INDEX idx_site_column_menu_location ON site_column(menu_location);

-- Verification query
SELECT id, name, slug, menu_location, show_in_nav
FROM site_column
ORDER BY sort_order;
