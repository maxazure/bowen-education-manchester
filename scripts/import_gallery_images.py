#!/usr/bin/env python3
"""
图片导入脚本 - 将upload目录中的图片导入到数据库Gallery系统
自动生成缩略图并关联到对应的相册
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from PIL import Image
import hashlib

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import SessionLocal
from app.models.media import MediaFile
from app.models.gallery import Gallery, GalleryImage

# 配置参数
UPLOAD_DIR = project_root / "upload"
STATIC_DIR = project_root / "templates" / "static"
THUMBNAIL_SIZES = {
    'thumbnail': (300, 300, 'crop'),  # 300x300 裁剪
    'medium': (800, 800, 'fit'),      # 800px 保持比例
    'large': (1920, 1920, 'fit')      # 1920px 保持比例
}

# 图片分类映射规则（目录路径 -> Gallery slug + tags）
GALLERY_MAPPING = {
    # 节日庆典
    'chinese-new-year-2025': {
        'gallery_slug': 'cny-2025',
        'tags': ['2025', '春节', 'Chinese New Year']
    },
    'christmas-concert': {
        'gallery_slug': 'christmas-concert',
        'tags': ['2024', '圣诞', 'Christmas']
    },
    'website-photos/christmas-concert': {
        'gallery_slug': 'christmas-concert',
        'tags': ['2024', '圣诞', 'Christmas']
    },

    # 政府资助项目
    'government-haf-camp': {
        'gallery_slug': 'haf-camps',
        'tags': ['2024', 'HAF', '政府项目']
    },
    'website-photos/government-camp/2021': {
        'gallery_slug': 'haf-camps',
        'tags': ['2021', 'HAF', '政府项目']
    },
    'website-photos/government-camp/2022': {
        'gallery_slug': 'haf-camps',
        'tags': ['2022', 'HAF', '政府项目']
    },
    'website-photos/government-camp/2023': {
        'gallery_slug': 'haf-camps',
        'tags': ['2023', 'HAF', '政府项目']
    },
    'website-photos/government-camp/2024': {
        'gallery_slug': 'haf-camps',
        'tags': ['2024', 'HAF', '政府项目']
    },
    'website-photos/government-camp/2025': {
        'gallery_slug': 'haf-camps',
        'tags': ['2025', 'HAF', '政府项目']
    },
    'website-photos/camp-highlights': {
        'gallery_slug': 'haf-highlights',
        'tags': ['精彩瞬间', 'HAF', 'highlights']
    },
    'parktastic-activities': {
        'gallery_slug': 'park-activities',
        'tags': ['2024', '公园活动', 'Parktastic']
    },

    # 俱乐部活动
    'chess-club': {
        'gallery_slug': 'chess-club-photos',
        'tags': ['2024', '国际象棋', 'Chess']
    },
    'website-photos/Chess club': {
        'gallery_slug': 'chess-club-photos',
        'tags': ['2023', '国际象棋', 'Chess']
    },

    # 夏令营
    'middleton-summer-camp': {
        'gallery_slug': 'middleton-camp',
        'tags': ['2024', '夏令营', 'Summer Camp']
    },
    'website-photos/middleton-summer-camp': {
        'gallery_slug': 'middleton-camp',
        'tags': ['2023', '夏令营', 'Summer Camp']
    }
}

# 排除目录
EXCLUDE_DIRS = ['chinese-school']


def get_file_md5(file_path):
    """计算文件MD5值用于去重"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def generate_thumbnail(source_path, output_path, size_tuple):
    """生成缩略图

    Args:
        source_path: 源图片路径
        output_path: 输出路径
        size_tuple: (width, height, method)
                   method可以是'crop'(裁剪)或'fit'(适应)
    """
    try:
        width, height, method = size_tuple

        with Image.open(source_path) as img:
            # 转换RGBA为RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            if method == 'crop':
                # 裁剪为正方形（居中裁剪）
                img_width, img_height = img.size
                if img_width > img_height:
                    left = (img_width - img_height) // 2
                    img = img.crop((left, 0, left + img_height, img_height))
                else:
                    top = (img_height - img_width) // 2
                    img = img.crop((0, top, img_width, top + img_width))
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            else:  # fit
                # 保持比例，最大边不超过指定尺寸
                img.thumbnail((width, height), Image.Resampling.LANCZOS)

            # 创建输出目录
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 保存
            img.save(output_path, 'JPEG', quality=90, optimize=True)
            return True
    except Exception as e:
        print(f"  ✗ 生成缩略图失败: {e}")
        return False


def get_image_dimensions(image_path):
    """获取图片尺寸"""
    try:
        with Image.open(image_path) as img:
            return img.size  # (width, height)
    except:
        return (0, 0)


def find_gallery_mapping(relative_path):
    """根据相对路径查找Gallery映射

    Args:
        relative_path: 相对于upload目录的路径

    Returns:
        dict: {'gallery_slug': str, 'tags': list} 或 None
    """
    # 标准化路径（移除开头的upload/）
    path = str(relative_path).replace('\\', '/')

    # 精确匹配
    if path in GALLERY_MAPPING:
        return GALLERY_MAPPING[path]

    # 模糊匹配（从最长路径开始）
    sorted_keys = sorted(GALLERY_MAPPING.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if path.startswith(key):
            return GALLERY_MAPPING[key]

    return None


def import_images():
    """主导入函数"""
    db = SessionLocal()

    try:
        print("=" * 70)
        print("图片导入脚本启动")
        print("=" * 70)
        print(f"源目录: {UPLOAD_DIR}")
        print(f"静态目录: {STATIC_DIR}")
        print(f"排除目录: {', '.join(EXCLUDE_DIRS)}")
        print("=" * 70)

        # 统计信息
        stats = {
            'total_files': 0,
            'imported': 0,
            'skipped': 0,
            'failed': 0,
            'by_gallery': {}
        }

        # 获取所有Gallery（slug -> id映射）
        galleries = {}
        for gallery in db.query(Gallery).all():
            galleries[gallery.slug] = gallery
        print(f"\n已加载 {len(galleries)} 个Gallery相册")

        # 遍历upload目录
        for root, dirs, files in os.walk(UPLOAD_DIR):
            # 过滤排除目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for filename in files:
                # 只处理图片文件
                ext = os.path.splitext(filename)[1].lower()
                if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    continue

                stats['total_files'] += 1

                # 获取相对路径
                full_path = Path(root) / filename
                relative_path = full_path.relative_to(UPLOAD_DIR)
                rel_dir = str(relative_path.parent).replace('\\', '/')

                print(f"\n[{stats['total_files']}] {relative_path}")

                # 查找Gallery映射
                mapping = find_gallery_mapping(rel_dir)
                if not mapping:
                    print(f"  ⚠ 未找到映射规则，跳过")
                    stats['skipped'] += 1
                    continue

                gallery_slug = mapping['gallery_slug']
                tags = mapping['tags']

                if gallery_slug not in galleries:
                    print(f"  ✗ Gallery '{gallery_slug}' 不存在")
                    stats['failed'] += 1
                    continue

                gallery = galleries[gallery_slug]
                print(f"  → Gallery: {gallery.title} ({gallery_slug})")
                print(f"  → Tags: {', '.join(tags)}")

                # 检查是否已导入（通过文件名查重）
                existing = db.query(MediaFile).filter(
                    MediaFile.filename_original == filename
                ).first()

                if existing:
                    # 检查是否已关联到此Gallery
                    existing_link = db.query(GalleryImage).filter(
                        GalleryImage.gallery_id == gallery.id,
                        GalleryImage.media_id == existing.id
                    ).first()

                    if existing_link:
                        print(f"  ⊙ 已存在并已关联")
                        stats['skipped'] += 1
                        continue
                    else:
                        # 关联到Gallery
                        gallery_image = GalleryImage(
                            gallery_id=gallery.id,
                            media_id=existing.id,
                            sort_order=gallery.image_count + 1,
                            is_visible=True
                        )
                        db.add(gallery_image)
                        gallery.image_count += 1
                        print(f"  + 关联到Gallery")
                        stats['imported'] += 1
                        stats['by_gallery'][gallery_slug] = stats['by_gallery'].get(gallery_slug, 0) + 1
                        continue

                # 创建MediaFile记录
                try:
                    # 获取图片信息
                    file_size = os.path.getsize(full_path)
                    width, height = get_image_dimensions(full_path)

                    # 为每个Gallery创建独立的目录
                    gallery_dir = STATIC_DIR / "uploads" / "gallery" / gallery_slug
                    os.makedirs(gallery_dir, exist_ok=True)

                    # 拷贝原图到static目录
                    import shutil
                    original_static_path = gallery_dir / filename
                    shutil.copy2(full_path, original_static_path)
                    print(f"  📁 拷贝原图到: {original_static_path.relative_to(STATIC_DIR)}")

                    # 生成缩略图路径
                    base_name = os.path.splitext(filename)[0]
                    thumb_dir = gallery_dir / "thumbnails"
                    os.makedirs(thumb_dir, exist_ok=True)
                    thumb_path_300 = thumb_dir / f"{base_name}_thumb.jpg"
                    thumb_path_800 = thumb_dir / f"{base_name}_medium.jpg"

                    # 原图路径（相对于static目录）
                    original_rel_path = f"/static/uploads/gallery/{gallery_slug}/{filename}"

                    # 生成缩略图
                    print(f"  ⚙ 生成缩略图...")
                    thumb_success = True
                    if not generate_thumbnail(full_path, thumb_path_300, THUMBNAIL_SIZES['thumbnail']):
                        thumb_success = False
                    if not generate_thumbnail(full_path, thumb_path_800, THUMBNAIL_SIZES['medium']):
                        thumb_success = False

                    if thumb_success:
                        print(f"  ✓ 缩略图生成成功")

                    # 创建MediaFile
                    media = MediaFile(
                        filename_original=filename,
                        mime_type='image/jpeg',
                        size_bytes=file_size,
                        width=width,
                        height=height,
                        path_original=original_rel_path,
                        path_thumb=f"/static/uploads/gallery/{gallery_slug}/thumbnails/{base_name}_thumb.jpg" if thumb_success else None,
                        path_medium=f"/static/uploads/gallery/{gallery_slug}/thumbnails/{base_name}_medium.jpg" if thumb_success else None,
                        title=os.path.splitext(filename)[0],
                        alt_text=f"{gallery.title} - {os.path.splitext(filename)[0]}",
                        tags=','.join(tags),
                        is_public=True,
                        file_type='image',
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.add(media)
                    db.flush()  # 获取media.id

                    # 创建GalleryImage关联
                    gallery_image = GalleryImage(
                        gallery_id=gallery.id,
                        media_id=media.id,
                        sort_order=gallery.image_count + 1,
                        is_visible=True,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.add(gallery_image)

                    # 更新Gallery计数
                    gallery.image_count += 1
                    gallery.updated_at = datetime.now()

                    # 如果Gallery没有封面，设置第一张为封面
                    if not gallery.cover_media_id:
                        gallery.cover_media_id = media.id

                    db.commit()

                    print(f"  ✓ 导入成功 (ID: {media.id})")
                    stats['imported'] += 1
                    stats['by_gallery'][gallery_slug] = stats['by_gallery'].get(gallery_slug, 0) + 1

                except Exception as e:
                    db.rollback()
                    print(f"  ✗ 导入失败: {e}")
                    stats['failed'] += 1

        # 打印统计报告
        print("\n" + "=" * 70)
        print("导入完成！")
        print("=" * 70)
        print(f"总文件数: {stats['total_files']}")
        print(f"成功导入: {stats['imported']}")
        print(f"跳过文件: {stats['skipped']}")
        print(f"失败文件: {stats['failed']}")
        print("\n按Gallery分类统计:")
        for gallery_slug, count in sorted(stats['by_gallery'].items()):
            gallery = galleries.get(gallery_slug)
            if gallery:
                print(f"  - {gallery.title} ({gallery_slug}): {count}张")
        print("=" * 70)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == '__main__':
    import_images()
