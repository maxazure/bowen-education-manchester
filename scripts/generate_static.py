#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态页面生成命令行工具

用法:
    python scripts/generate_static.py              # 生成所有页面到 public/ 目录
    python scripts/generate_static.py -o dist      # 指定输出目录
    python scripts/generate_static.py --verbose    # 显示详细日志
"""

import argparse
import logging
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import SessionLocal
from app.services.static_generator import StaticPageGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="生成静态 HTML 页面",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                              # 生成所有页面
  %(prog)s -o dist                      # 输出到 dist 目录
  %(prog)s --verbose                    # 显示详细日志
  %(prog)s -o public --base-url https://example.com
        """,
    )

    parser.add_argument(
        "-o",
        "--output",
        default="public",
        help="输出目录路径 (默认: public)",
    )

    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="网站基础 URL (默认: http://localhost:8000)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="显示详细日志",
    )

    args = parser.parse_args()

    # 设置日志级别
    if args.verbose:
        logging.getLogger("docms").setLevel(logging.DEBUG)
        logging.getLogger("app.services.static_generator").setLevel(logging.DEBUG)

    logger.info("=" * 60)
    logger.info("静态页面生成工具")
    logger.info("=" * 60)
    logger.info(f"输出目录: {args.output}")
    logger.info(f"基础 URL: {args.base_url}")
    logger.info("-" * 60)

    # 创建数据库会话
    db = SessionLocal()

    try:
        # 创建生成器
        generator = StaticPageGenerator(
            db=db,
            output_dir=args.output,
            base_url=args.base_url,
        )

        # 开始生成
        logger.info("开始生成静态页面...")
        log = generator.generate_all()

        # 复制静态资源文件
        logger.info("-" * 60)
        logger.info("复制静态资源文件...")
        import shutil
        static_source = project_root / "templates" / "static"
        static_dest = Path(args.output) / "static"

        # 删除旧的静态文件（如果存在）
        if static_dest.exists():
            shutil.rmtree(static_dest)

        # 复制静态文件
        shutil.copytree(static_source, static_dest)
        logger.info(f"✓ 静态资源已复制到: {static_dest}")

        # 显示结果
        logger.info("-" * 60)
        logger.info("生成完成!")
        logger.info(f"总计: {log.total_pages} 页")
        logger.info(f"成功: {log.successful_pages} 页")
        logger.info(f"失败: {log.failed_pages} 页")

        if log.failed_pages > 0:
            logger.warning(f"状态: {log.status}")
            logger.warning("部分页面生成失败,请查看日志了解详情")
        else:
            logger.info(f"状态: {log.status}")

        duration = (log.end_time - log.start_time).total_seconds()
        logger.info(f"耗时: {duration:.2f} 秒")

        logger.info("=" * 60)

        # 返回退出码
        sys.exit(0 if log.failed_pages == 0 else 1)

    except KeyboardInterrupt:
        logger.warning("\n用户中断生成")
        sys.exit(130)
    except Exception as e:
        logger.error(f"生成失败: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
