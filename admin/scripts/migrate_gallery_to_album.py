#!/usr/bin/env python3
"""
数据迁移脚本：将旧的 Gallery 系统迁移到新的 Album 系统

执行方式：
    python admin/scripts/migrate_gallery_to_album.py
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.album import Album, AlbumCategory, AlbumPhoto
from app.models.gallery import Gallery, GalleryImage


def migrate_galleries_to_albums(database_url: str = "sqlite:///./bowen_cms.db"):
    """
    将 Gallery 数据迁移到 Album 系统

    迁移映射：
    - Gallery -> Album
    - GalleryImage -> AlbumPhoto
    - Gallery.category -> AlbumCategory (通过分类名称匹配)
    """
    # 创建数据库连接
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        print("=" * 60)
        print("开始迁移 Gallery 数据到 Album 系统")
        print("=" * 60)

        # 1. 获取所有 Gallery
        galleries = db.query(Gallery).all()
        print(f"\n找到 {len(galleries)} 个相册需要迁移")

        if len(galleries) == 0:
            print("没有需要迁移的数据")
            return

        # 2. 统计信息
        migrated_albums = 0
        migrated_photos = 0
        errors = []

        # 3. 迁移每个 Gallery
        for gallery in galleries:
            try:
                print(f"\n迁移相册: {gallery.title}")

                # 检查是否已经迁移过（通过 slug 判断）
                existing_album = db.query(Album).filter_by(slug=gallery.slug).first()
                if existing_album:
                    print(f"  ⚠️  相册已存在，跳过: {gallery.slug}")
                    continue

                # 获取或创建分类
                category = None
                if gallery.category:
                    # 尝试通过分类名称匹配
                    category = db.query(AlbumCategory).filter_by(name=gallery.category).first()
                    if not category:
                        print(f"  ⚠️  未找到匹配的分类: {gallery.category}，使用默认分类")

                # 创建新的 Album
                album = Album(
                    title=gallery.title,
                    slug=gallery.slug,
                    description=gallery.description,
                    category_id=category.id if category else None,
                    tags=gallery.tags,
                    cover_media_id=gallery.cover_media_id,
                    status="published" if gallery.is_public else "draft",
                    seo_title=gallery.seo_title,
                    seo_description=gallery.seo_description,
                    view_count=gallery.view_count,
                    photo_count=0,  # 将在添加照片后更新
                    sort_order=gallery.sort_order,
                    created_at=gallery.created_at,
                    updated_at=gallery.updated_at,
                )

                # 如果是公开的，设置发布时间
                if gallery.is_public:
                    album.published_at = gallery.created_at

                db.add(album)
                db.flush()  # 获取 album.id

                print(f"  ✓ 创建相册: ID={album.id}, Slug={album.slug}")
                migrated_albums += 1

                # 4. 迁移相册中的图片
                images = db.query(GalleryImage).filter_by(gallery_id=gallery.id).all()
                print(f"  找到 {len(images)} 张照片")

                # 使用集合来跟踪已添加的 media_id，避免重复
                added_media_ids = set()
                actual_added = 0
                skipped = 0

                for image in images:
                    # 跳过重复的 media_id
                    if image.media_id in added_media_ids:
                        skipped += 1
                        print(f"    ⚠️  跳过重复的 media_id: {image.media_id}")
                        continue

                    # 创建 AlbumPhoto
                    album_photo = AlbumPhoto(
                        album_id=album.id,
                        media_id=image.media_id,
                        caption=image.caption or image.title,  # 优先使用 caption
                        sort_order=image.sort_order,
                        created_at=image.created_at,
                        updated_at=image.updated_at,
                    )
                    db.add(album_photo)
                    added_media_ids.add(image.media_id)
                    actual_added += 1
                    migrated_photos += 1

                # 更新相册的照片数量
                album.photo_count = actual_added

                print(f"  ✓ 迁移 {actual_added} 张照片" + (f" (跳过 {skipped} 张重复)" if skipped > 0 else ""))

            except Exception as e:
                error_msg = f"迁移相册 {gallery.title} (ID={gallery.id}) 时出错: {str(e)}"
                errors.append(error_msg)
                print(f"  ✗ {error_msg}")
                db.rollback()
                continue

        # 5. 提交所有更改
        db.commit()

        # 6. 输出统计信息
        print("\n" + "=" * 60)
        print("迁移完成！")
        print("=" * 60)
        print(f"✓ 成功迁移相册: {migrated_albums}")
        print(f"✓ 成功迁移照片: {migrated_photos}")

        if errors:
            print(f"\n⚠️  遇到 {len(errors)} 个错误:")
            for error in errors:
                print(f"  - {error}")

        print("\n" + "=" * 60)
        print("下一步操作建议：")
        print("=" * 60)
        print("1. 访问 http://localhost:8001/admin/albums 查看迁移的相册")
        print("2. 检查相册分类是否正确")
        print("3. 确认照片排序是否正确")
        print("4. 备份原数据后，可以删除旧的 Gallery 表")

    except Exception as e:
        print(f"\n✗ 迁移过程中发生错误: {str(e)}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="迁移 Gallery 数据到 Album 系统")
    parser.add_argument(
        "--database",
        default="sqlite:///./bowen_cms.db",
        help="数据库 URL (默认: sqlite:///./bowen_cms.db)",
    )
    parser.add_argument(
        "--frontend-db",
        action="store_true",
        help="同时迁移前台数据库 (instance/database.db)",
    )

    args = parser.parse_args()

    # 迁移管理后台数据库
    print("\n📦 迁移管理后台数据库...")
    migrate_galleries_to_albums(args.database)

    # 如果指定，也迁移前台数据库
    if args.frontend_db:
        print("\n📦 迁移前台数据库...")
        migrate_galleries_to_albums("sqlite:///./instance/database.db")

    print("\n✅ 所有迁移完成！\n")
