#!/usr/bin/env python3
"""
博文教育集团网站 - Hero 背景图片生成脚本
使用 Image Generator Service 生成高质量的栏目背景图片
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 添加客户端路径到 sys.path
CLIENT_PATH = Path("/Users/maxazure/projects/image-generator-service")
sys.path.insert(0, str(CLIENT_PATH))

try:
    from client import ImageGeneratorClient, Quality, UsageCategory, TaskCreateRequest, OutputFormat
    import sqlite3
except ImportError as e:
    print(f"错误: 无法导入必要的模块 - {e}")
    print("请确保:")
    print("1. Image Generator Service 客户端存在于: /Users/maxazure/projects/image-generator-service/client/")
    print("2. 已安装必要依赖: pip install requests")
    sys.exit(1)

# 项目配置
PROJECT_DIR = Path("/Users/maxazure/projects/bowen-education-manchester")
IMAGE_DIR = PROJECT_DIR / "templates" / "static" / "images"
DATABASE_PATH = PROJECT_DIR / "instance" / "database.db"

# 服务配置
SERVICE_URL = "http://localhost:10033"

# 栏目配置
COLUMNS = [
    {
        "id": 3,
        "name": "中文学校",
        "slug": "school",
        "prompt": "Modern Chinese language classroom with students studying, warm lighting, traditional Chinese calligraphy decorations on walls, professional education environment, blue and white color scheme, bright and welcoming atmosphere, wide angle view suitable for hero banner, 16:9 aspect ratio",
    },
    {
        "id": 5,
        "name": "国际象棋俱乐部",
        "slug": "chess",
        "prompt": "Professional chess club interior with chess boards and pieces, students concentrating on chess games, modern education facility, blue color theme, bright natural lighting, inspiring learning atmosphere, wide composition for web banner, 16:9 aspect ratio",
    },
    {
        "id": 12,
        "name": "羽毛球俱乐部",
        "slug": "badminton",
        "prompt": "Indoor badminton court with players in action, professional sports facility, bright lighting, dynamic movement, blue and white color scheme, energetic atmosphere, wide angle suitable for hero background, 16:9 aspect ratio",
    },
    {
        "id": 4,
        "name": "补习中心",
        "slug": "tuition",
        "prompt": "Modern tutoring center with students and teachers, bright study environment, educational materials and books, professional and focused atmosphere, blue color theme, inspiring learning space, wide composition for website header, 16:9 aspect ratio",
    },
    {
        "id": 6,
        "name": "政府项目",
        "slug": "programmes",
        "prompt": "Community service and government partnership activities, diverse people collaborating, modern meeting room or community center, professional and trustworthy atmosphere, blue color scheme, bright and positive lighting, wide angle for hero banner, 16:9 aspect ratio",
    },
    {
        "id": 7,
        "name": "博文活动",
        "slug": "events",
        "prompt": "Cultural event celebration with Chinese elements, people enjoying activities, colorful and vibrant atmosphere, modern venue, blue accent colors, dynamic and festive mood, wide composition for website banner, 16:9 aspect ratio",
    },
    {
        "id": 11,
        "name": "联系我们",
        "slug": "contact",
        "prompt": "Modern office reception area, friendly and welcoming atmosphere, professional communication space, blue color theme, bright natural lighting, clean and organized environment, wide angle suitable for hero background, 16:9 aspect ratio",
    },
    {
        "id": 2,
        "name": "关于博文",
        "slug": "about",
        "prompt": "Professional education institution building exterior or modern interior, established and trustworthy atmosphere, blue corporate color scheme, bright daylight, impressive and welcoming composition, wide angle for website header, 16:9 aspect ratio",
    },
]


class HeroImageGenerator:
    """Hero 背景图片生成器"""

    def __init__(self):
        self.client = ImageGeneratorClient(base_url=SERVICE_URL)
        self.results = {
            "success": [],
            "failed": [],
            "total_cost": 0.0,
            "total_time": 0.0,
        }

    def generate_image(
        self, column: Dict, timeout: int = 120
    ) -> Optional[Dict[str, any]]:
        """
        为指定栏目生成图片

        Args:
            column: 栏目配置
            timeout: 超时时间（秒）

        Returns:
            生成结果字典或 None
        """
        print(f"\n{'='*80}")
        print(f"正在生成: {column['name']} ({column['slug']})")
        print(f"{'='*80}")

        start_time = time.time()

        try:
            # 创建任务请求
            request = TaskCreateRequest(
                prompt=column["prompt"],
                width=1920,
                height=1088,
                quality=Quality.HIGH_COMMERCIAL,
                usage_category=UsageCategory.HERO_BG,
                output_format=OutputFormat.JPG,
            )

            # 生成图片并获取路径
            image_path = self.client.generate_image(
                request=request,
                timeout=timeout,
            )

            generation_time = time.time() - start_time

            # 读取图片数据
            with open(image_path, "rb") as f:
                image_data = f.read()

            # 保存图片到项目目录
            filename = f"hero-{column['slug']}.jpg"
            file_path = IMAGE_DIR / filename
            relative_path = f"/static/images/{filename}"

            with open(file_path, "wb") as f:
                f.write(image_data)

            # 记录成功
            result_info = {
                "column_id": column["id"],
                "column_name": column["name"],
                "slug": column["slug"],
                "file_path": str(file_path),
                "relative_path": relative_path,
                "file_size": len(image_data),
                "generation_time": generation_time,
                "cost": 0.06,
                "source_path": image_path,
            }

            self.results["success"].append(result_info)
            self.results["total_cost"] += 0.06
            self.results["total_time"] += generation_time

            print(f"✓ 成功生成!")
            print(f"  - 源文件: {image_path}")
            print(f"  - 目标路径: {file_path}")
            print(f"  - 文件大小: {len(image_data) / 1024:.2f} KB")
            print(f"  - 生成耗时: {generation_time:.2f} 秒")
            print(f"  - 成本: ¥0.06")

            return result_info

        except Exception as e:
            generation_time = time.time() - start_time
            error_info = {
                "column_id": column["id"],
                "column_name": column["name"],
                "slug": column["slug"],
                "error": str(e),
                "generation_time": generation_time,
            }

            self.results["failed"].append(error_info)
            self.results["total_time"] += generation_time

            print(f"✗ 生成失败!")
            print(f"  - 错误: {e}")
            print(f"  - 耗时: {generation_time:.2f} 秒")

            return None

    def update_database(self):
        """更新数据库，关联生成的图片"""
        print(f"\n{'='*80}")
        print("更新数据库...")
        print(f"{'='*80}")

        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            for result in self.results["success"]:
                # 1. 插入媒体文件记录
                cursor.execute(
                    """
                    INSERT INTO media_file (
                        filename_original, mime_type, size_bytes,
                        width, height, path_original,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        f"hero-{result['slug']}.jpg",
                        "image/jpeg",
                        result["file_size"],
                        1920,
                        1088,
                        result["relative_path"],
                        datetime.now().isoformat(),
                        datetime.now().isoformat(),
                    ),
                )

                media_id = cursor.lastrowid

                # 2. 更新栏目的 hero_media_id
                cursor.execute(
                    """
                    UPDATE site_column
                    SET hero_media_id = ?,
                        updated_at = ?
                    WHERE id = ?
                """,
                    (media_id, datetime.now().isoformat(), result["column_id"]),
                )

                result["media_id"] = media_id

                print(f"✓ {result['column_name']}: media_id={media_id}")

            conn.commit()
            conn.close()

            print(f"\n数据库更新完成! 共更新 {len(self.results['success'])} 条记录")

        except Exception as e:
            print(f"✗ 数据库更新失败: {e}")
            if conn:
                conn.close()

    def verify_images(self):
        """验证生成的图片"""
        print(f"\n{'='*80}")
        print("验证图片...")
        print(f"{'='*80}")

        try:
            from PIL import Image

            for result in self.results["success"]:
                img = Image.open(result["file_path"])
                width, height = img.size

                print(f"\n{result['column_name']}:")
                print(f"  - 文件: {Path(result['file_path']).name}")
                print(f"  - 尺寸: {width} x {height}")
                print(f"  - 格式: {img.format}")
                print(f"  - 模式: {img.mode}")

                # 检查尺寸
                if width == 1920 and height == 1088:
                    print(f"  ✓ 尺寸正确")
                else:
                    print(f"  ✗ 尺寸不正确 (期望: 1920x1088)")

            print("\n验证完成!")

        except ImportError:
            print(
                "⚠ PIL/Pillow 未安装，跳过图片验证（pip install Pillow 安装后可验证）"
            )
        except Exception as e:
            print(f"✗ 验证失败: {e}")

    def print_report(self):
        """打印生成报告"""
        print(f"\n\n{'='*80}")
        print("生成报告")
        print(f"{'='*80}\n")

        print(f"总计栏目: {len(COLUMNS)}")
        print(f"成功生成: {len(self.results['success'])} 张")
        print(f"生成失败: {len(self.results['failed'])} 张")
        print(f"总耗时: {self.results['total_time']:.2f} 秒")
        print(f"总成本: ¥{self.results['total_cost']:.2f}")

        if self.results["success"]:
            print(f"\n成功生成的图片:")
            for i, result in enumerate(self.results["success"], 1):
                print(
                    f"  {i}. {result['column_name']} - {Path(result['file_path']).name}"
                )

        if self.results["failed"]:
            print(f"\n失败的图片:")
            for i, result in enumerate(self.results["failed"], 1):
                print(f"  {i}. {result['column_name']} - {result['error']}")

        print(f"\n{'='*80}\n")

    def run(self):
        """执行生成任务"""
        print("博文教育集团 - Hero 背景图片生成工具")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"图片保存目录: {IMAGE_DIR}")
        print(f"数据库: {DATABASE_PATH}")
        print(f"服务地址: {SERVICE_URL}")

        # 检查服务状态
        try:
            stats = self.client.get_queue_stats()
            print(f"\n✓ 图片生成服务运行正常")
            print(f"  - 队列任务数: {stats.total_count}")
            print(f"  - 进行中: {stats.processing_count}")
        except Exception as e:
            print(f"\n⚠ 无法连接到图片生成服务: {e}")
            print(f"将继续尝试生成图片...")

        # 确保图片目录存在
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)

        # 生成图片
        for column in COLUMNS:
            self.generate_image(column)

            # 添加延迟，避免并发限制
            if column != COLUMNS[-1]:  # 不是最后一个
                print("\n等待 5 秒...")
                time.sleep(5)

        # 更新数据库
        if self.results["success"]:
            self.update_database()

        # 验证图片
        if self.results["success"]:
            self.verify_images()

        # 打印报告
        self.print_report()


if __name__ == "__main__":
    generator = HeroImageGenerator()
    generator.run()
