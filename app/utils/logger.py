# -*- coding: utf-8 -*-
"""日志配置模块

提供应用日志记录功能，支持文件和控制台输出
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(app_name: str = "docms", log_level: str = "INFO") -> logging.Logger:
    """
    配置应用日志系统

    Args:
        app_name: 应用名称，用于日志文件命名
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        配置好的 Logger 实例

    Example:
        >>> logger = setup_logging("docms", "DEBUG")
        >>> logger.info("Application started")
    """

    # 创建 logs 目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 配置日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 文件处理器 (轮转日志，最大10MB，保留5个备份)
    file_handler = RotatingFileHandler(
        log_dir / f"{app_name}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 清除现有处理器（避免重复）
    root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # 配置应用日志记录器
    app_logger = logging.getLogger(app_name)
    app_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 禁用第三方库的详细日志
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return app_logger
