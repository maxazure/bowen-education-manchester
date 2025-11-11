# -*- coding: utf-8 -*-
"""应用配置管理

支持从 YAML 文件加载配置
"""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent.parent


class SiteConfig(BaseModel):
    """站点配置"""

    # 基本信息
    site_name: str = "Docms Site"
    site_description: str = "A website powered by Docms"
    site_url: str = "http://localhost:8000"

    # 路径配置
    base_dir: Path = Field(default_factory=lambda: Path.cwd())
    template_dir: Path = Field(default_factory=lambda: Path.cwd() / "templates")
    static_dir: Path = Field(default_factory=lambda: Path.cwd() / "templates" / "static")
    media_dir: Path = Field(default_factory=lambda: Path.cwd() / "upload")

    # 数据库配置
    database_url: str = "sqlite:///./instance/database.db"

    # 主题配置
    theme: str = "default"
    available_themes: list[str] = ["default"]

    # 日志配置
    log_level: str = "INFO"

    # 缓存配置
    enable_cache: bool = True
    cache_ttl: int = 300  # 5 分钟

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "SiteConfig":
        """从 YAML 文件加载配置"""
        import yaml

        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 转换路径字符串为 Path 对象
        if "base_dir" in data:
            data["base_dir"] = Path(data["base_dir"])
        if "template_dir" in data:
            data["template_dir"] = Path(data["template_dir"])
        if "static_dir" in data:
            data["static_dir"] = Path(data["static_dir"])
        if "media_dir" in data:
            data["media_dir"] = Path(data["media_dir"])

        return cls(**data)

    def save_yaml(self, yaml_path: Path):
        """保存配置到 YAML 文件"""
        import yaml

        data = self.model_dump()
        # 转换 Path 对象为字符串
        for key in ["base_dir", "template_dir", "static_dir", "media_dir"]:
            if key in data:
                data[key] = str(data[key])

        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)


# 兼容环境变量配置（保持向后兼容）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./instance/database.db")
APP_NAME = os.getenv("APP_NAME", "Docms CMS")
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
SITE_NAME = os.getenv("SITE_NAME", "Bowen-Education-Manchester")
SITE_TITLE = os.getenv("SITE_TITLE", "Bowen-Education-Manchester")
SITE_DESCRIPTION = os.getenv("SITE_DESCRIPTION", "A professional website for Bowen-Education-Manchester")
ACTIVE_THEME = os.getenv("ACTIVE_THEME", "default")

# 静态文件路径
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = TEMPLATE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "upload"

# 确保上传目录存在
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 保持 MEDIA_DIR 作为别名，便于兼容性
MEDIA_DIR = UPLOAD_DIR


class Settings:
    """应用设置类"""

    def __init__(self):
        self.database_url = DATABASE_URL
        self.app_name = APP_NAME
        self.debug = DEBUG
        self.site_name = SITE_NAME
        self.site_title = SITE_TITLE
        self.site_description = SITE_DESCRIPTION
        self.static_dir = STATIC_DIR
        self.media_dir = MEDIA_DIR
        self.template_dir = TEMPLATE_DIR

    def get_site_settings(self) -> dict[str, Any]:
        """获取站点设置字典"""
        return {
            "site_name": self.site_name,
            "site_title": self.site_title,
            "site_description": self.site_description,
        }


# 创建全局设置实例
settings = Settings()
