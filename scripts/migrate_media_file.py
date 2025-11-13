"""
Migration script to add missing columns to media_file table
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import text
from app.database import engine


def migrate():
    """Add missing columns to media_file table"""

    migrations = [
        # Add usage_count column
        "ALTER TABLE media_file ADD COLUMN usage_count INTEGER DEFAULT 0 NOT NULL",

        # Add title column
        "ALTER TABLE media_file ADD COLUMN title VARCHAR(255)",

        # Add alt_text column
        "ALTER TABLE media_file ADD COLUMN alt_text VARCHAR(255)",

        # Add caption column
        "ALTER TABLE media_file ADD COLUMN caption TEXT",
    ]

    with engine.connect() as conn:
        for migration_sql in migrations:
            try:
                print(f"Executing: {migration_sql}")
                conn.execute(text(migration_sql))
                conn.commit()
                print("✅ Success")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠️  Column already exists, skipping")
                else:
                    print(f"❌ Error: {e}")
                    raise

    print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    migrate()
