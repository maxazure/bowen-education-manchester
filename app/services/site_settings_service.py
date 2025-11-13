"""
站点设置服务

提供站点设置的 Key-Value 存储和读取功能，支持单个设置项和设置组的操作
"""

from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models.site import SiteSetting


def get_setting(db: Session, key: str, default: Any = None) -> Any:
    """
    获取单个设置项

    Args:
        db: 数据库会话
        key: 设置键
        default: 默认值（如果设置不存在则返回此值）

    Returns:
        设置值或默认值
    """
    setting = db.query(SiteSetting).filter(SiteSetting.setting_key == key).first()
    if setting:
        return setting.value_text
    return default


def get_settings_group(db: Session, prefix: str) -> Dict[str, Any]:
    """
    获取设置组（所有以指定前缀开头的设置）

    Args:
        db: 数据库会话
        prefix: 设置键前缀（如 'contact_' 获取所有联系方式设置）

    Returns:
        设置字典 {key: value}
    """
    settings = (
        db.query(SiteSetting).filter(SiteSetting.setting_key.like(f"{prefix}%")).all()
    )

    return {setting.setting_key: setting.value_text for setting in settings}


def update_setting(db: Session, key: str, value: Any) -> None:
    """
    更新单个设置项（如果不存在则创建）

    Args:
        db: 数据库会话
        key: 设置键
        value: 设置值
    """
    # 查找现有设置
    setting = db.query(SiteSetting).filter(SiteSetting.setting_key == key).first()

    if setting:
        # 更新现有设置
        setting.value_text = str(value)
    else:
        # 创建新设置
        new_setting = SiteSetting(
            setting_key=key, value_text=str(value), value_type="string"
        )
        db.add(new_setting)

    db.commit()


def update_settings(db: Session, settings: Dict[str, Any]) -> None:
    """
    批量更新设置项

    Args:
        db: 数据库会话
        settings: 设置字典 {key: value}
    """
    for key, value in settings.items():
        update_setting(db, key, value)


def get_all_settings(db: Session) -> Dict[str, Any]:
    """
    获取所有设置项

    Args:
        db: 数据库会话

    Returns:
        所有设置的字典 {key: value}
    """
    settings = db.query(SiteSetting).all()
    return {setting.setting_key: setting.value_text for setting in settings}


def delete_setting(db: Session, key: str) -> bool:
    """
    删除单个设置项

    Args:
        db: 数据库会话
        key: 设置键

    Returns:
        是否成功删除
    """
    setting = db.query(SiteSetting).filter(SiteSetting.setting_key == key).first()
    if setting:
        db.delete(setting)
        db.commit()
        return True
    return False
