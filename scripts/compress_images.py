#!/usr/bin/env python3
"""
图片压缩和分类脚本
将"网站文案和照片"目录下的所有图片压缩并分类到upload文件夹
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif

# 注册HEIF插件
pillow_heif.register_heif_opener()

# 配置参数
SOURCE_DIR = "网站文案和照片"
OUTPUT_DIR = "upload"
MAX_SIZE = 1920  # 最大边长（像素）
QUALITY = 85  # JPEG质量（1-100）
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.heic', '.gif', '.bmp', '.webp'}

# 中文文件夹到英文的映射
FOLDER_MAPPING = {
    'Chess Club': 'chess-club',
    'parktastic活动': 'parktastic-activities',
    '中国新年 2025': 'chinese-new-year-2025',
    '政府项目 假期营': 'government-haf-camp',
    '活动 圣诞音乐会': 'christmas-concert',
    '活动 米德尔顿夏令营': 'middleton-summer-camp',
    '中文学校网站': 'chinese-school',
    '网站照片分享': 'website-photos',
    # 子目录映射
    '1中文学校 关于我们': 'about-us',
    '2中文课程设置': 'curriculum',
    '3中英文兴趣班': 'interest-classes',
    '4学期日期': 'term-dates',
    '5报名与试听': 'registration',
    '6 PTA': 'pta',
    '圣诞音乐会': 'christmas-concert',
    '米德尔顿夏令营': 'middleton-summer-camp',
    '政府camp': 'government-camp',
    'camp精选图片': 'camp-highlights',
    'psd': 'psd',  # PSD文件不处理
}


def get_english_path(chinese_path):
    """将中文路径转换为英文路径"""
    parts = Path(chinese_path).parts
    english_parts = []

    for part in parts:
        if part in FOLDER_MAPPING:
            english_parts.append(FOLDER_MAPPING[part])
        else:
            # 如果没有映射，使用原名称（已经是英文的情况）
            english_parts.append(part)

    return os.path.join(*english_parts) if english_parts else ''


def compress_image(input_path, output_path, max_size=MAX_SIZE, quality=QUALITY):
    """
    压缩图片
    - 转换HEIC为JPG
    - 调整尺寸（保持比例）
    - 压缩质量
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 转换RGBA为RGB（PNG透明背景处理）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # 获取原始尺寸
            width, height = img.size

            # 计算新尺寸（保持比例，最大边不超过max_size）
            if width > max_size or height > max_size:
                ratio = min(max_size / width, max_size / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 创建输出目录
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 保存为JPG
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

            return True, f"成功: {os.path.basename(input_path)} -> {os.path.basename(output_path)}"

    except Exception as e:
        return False, f"失败: {os.path.basename(input_path)} - {str(e)}"


def process_images():
    """处理所有图片"""
    # 统计信息
    total_files = 0
    processed_files = 0
    skipped_files = 0
    failed_files = 0
    total_size_before = 0
    total_size_after = 0

    print(f"开始处理图片...")
    print(f"源目录: {SOURCE_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"最大尺寸: {MAX_SIZE}px")
    print(f"JPEG质量: {QUALITY}")
    print("-" * 60)

    # 遍历所有文件
    for root, dirs, files in os.walk(SOURCE_DIR):
        for filename in files:
            # 检查文件扩展名
            ext = os.path.splitext(filename)[1].lower()
            if ext not in SUPPORTED_FORMATS:
                continue

            total_files += 1
            input_path = os.path.join(root, filename)

            # 跳过PSD目录
            if 'psd' in root.lower():
                skipped_files += 1
                continue

            # 获取相对路径
            rel_path = os.path.relpath(root, SOURCE_DIR)

            # 转换为英文路径
            english_path = get_english_path(rel_path)

            # 构建输出路径（转换为.jpg）
            output_filename = os.path.splitext(filename)[0] + '.jpg'
            output_path = os.path.join(OUTPUT_DIR, english_path, output_filename)

            # 检查文件是否已存在
            if os.path.exists(output_path):
                skipped_files += 1
                print(f"跳过（已存在）: {filename}")
                continue

            # 获取原始文件大小
            file_size_before = os.path.getsize(input_path)
            total_size_before += file_size_before

            # 压缩图片
            success, message = compress_image(input_path, output_path)

            if success:
                processed_files += 1
                file_size_after = os.path.getsize(output_path)
                total_size_after += file_size_after
                compression_ratio = (1 - file_size_after / file_size_before) * 100
                print(f"✓ {message} ({file_size_before/1024:.1f}KB -> {file_size_after/1024:.1f}KB, 压缩 {compression_ratio:.1f}%)")
            else:
                failed_files += 1
                print(f"✗ {message}")

    # 输出统计信息
    print("-" * 60)
    print(f"处理完成！")
    print(f"总文件数: {total_files}")
    print(f"成功处理: {processed_files}")
    print(f"跳过文件: {skipped_files}")
    print(f"失败文件: {failed_files}")
    print(f"总大小（压缩前）: {total_size_before / (1024*1024):.2f} MB")
    print(f"总大小（压缩后）: {total_size_after / (1024*1024):.2f} MB")
    if total_size_before > 0:
        total_compression = (1 - total_size_after / total_size_before) * 100
        print(f"总压缩率: {total_compression:.1f}%")


if __name__ == '__main__':
    try:
        process_images()
    except KeyboardInterrupt:
        print("\n\n用户中断处理")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
