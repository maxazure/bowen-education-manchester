"""
站点设置测试 - 读取功能

测试站点设置的读取操作，包括单个设置项、设置组和默认值
"""

import pytest
from sqlalchemy.orm import Session

from app.models.site import SiteSetting
from app.services.site_settings_service import (get_setting,
                                                get_settings_group,
                                                update_setting,
                                                update_settings)


def test_read_single_setting(db_session: Session):
    """测试读取单个设置项"""
    # 创建测试数据
    update_setting(db_session, "site_name", "博文教育")
    update_setting(db_session, "site_tagline", "专业的羽毛球培训")

    # 测试读取已存在的设置
    assert get_setting(db_session, "site_name") == "博文教育"
    assert get_setting(db_session, "site_tagline") == "专业的羽毛球培训"

    # 测试读取不存在的设置（应返回 None）
    assert get_setting(db_session, "nonexistent_key") is None

    # 测试读取不存在的设置（带默认值）
    assert (
        get_setting(db_session, "nonexistent_key", "default_value") == "default_value"
    )


def test_read_settings_group(db_session: Session):
    """测试读取设置组（如所有联系方式）"""
    # 创建多个相关设置
    contact_settings = {
        "contact_phone": "0161-123-4567",
        "contact_email": "info@bowen-education.com",
        "contact_address": "Manchester, UK",
        "contact_hours": "周一至周五 9:00-18:00",
    }
    update_settings(db_session, contact_settings)

    # 创建其他设置（不属于 contact 组）
    update_setting(db_session, "site_name", "博文教育")
    update_setting(db_session, "social_facebook", "https://facebook.com/bowen")

    # 测试读取 contact 组
    contact_group = get_settings_group(db_session, "contact_")
    assert len(contact_group) == 4
    assert contact_group["contact_phone"] == "0161-123-4567"
    assert contact_group["contact_email"] == "info@bowen-education.com"
    assert contact_group["contact_address"] == "Manchester, UK"
    assert contact_group["contact_hours"] == "周一至周五 9:00-18:00"

    # 验证不包含其他组的设置
    assert "site_name" not in contact_group
    assert "social_facebook" not in contact_group

    # 测试读取 social 组
    social_group = get_settings_group(db_session, "social_")
    assert len(social_group) == 1
    assert social_group["social_facebook"] == "https://facebook.com/bowen"

    # 测试读取不存在的组（应返回空字典）
    empty_group = get_settings_group(db_session, "nonexistent_")
    assert empty_group == {}


def test_default_values(db_session: Session):
    """测试默认值"""
    # 测试空数据库的情况
    assert db_session.query(SiteSetting).count() == 0

    # 测试读取不存在的设置，应返回 None
    assert get_setting(db_session, "site_name") is None

    # 测试读取不存在的设置，带默认值
    assert get_setting(db_session, "site_name", "默认站点名") == "默认站点名"
    assert get_setting(db_session, "site_tagline", "") == ""
    assert get_setting(db_session, "logo_id", "0") == "0"

    # 测试读取不存在的组，应返回空字典
    assert get_settings_group(db_session, "contact_") == {}

    # 创建一个设置项
    update_setting(db_session, "site_name", "博文教育")

    # 再次读取，应返回实际值而不是默认值
    assert get_setting(db_session, "site_name") == "博文教育"
    assert get_setting(db_session, "site_name", "默认站点名") == "博文教育"

    # 测试不存在的设置仍然返回默认值
    assert get_setting(db_session, "nonexistent", "default") == "default"
