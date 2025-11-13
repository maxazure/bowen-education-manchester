"""
站点设置测试 - 保存功能

测试站点设置的各种保存操作，包括基本信息、联系方式、社交媒体、高级设置和 Key-Value 存储机制
"""

import pytest
from sqlalchemy.orm import Session

from app.models.site import SiteSetting
from app.services.site_settings_service import (get_setting,
                                                get_settings_group,
                                                update_setting,
                                                update_settings)


def test_save_basic_info(db_session: Session):
    """测试保存基本信息（站点名称、标语等）"""
    # 准备测试数据
    basic_settings = {
        "site_name": "博文教育",
        "site_tagline": "专业的羽毛球培训",
        "site_description": "提供优质的羽毛球教学服务",
        "logo_id": "123",
        "favicon_id": "456",
    }

    # 批量更新设置
    update_settings(db_session, basic_settings)

    # 验证数据已正确保存
    assert get_setting(db_session, "site_name") == "博文教育"
    assert get_setting(db_session, "site_tagline") == "专业的羽毛球培训"
    assert get_setting(db_session, "site_description") == "提供优质的羽毛球教学服务"
    assert get_setting(db_session, "logo_id") == "123"
    assert get_setting(db_session, "favicon_id") == "456"

    # 验证数据库中的记录数
    count = db_session.query(SiteSetting).count()
    assert count == 5


def test_save_contact(db_session: Session):
    """测试保存联系方式"""
    # 准备测试数据
    contact_settings = {
        "contact_phone": "0161-123-4567",
        "contact_email": "info@bowen-education.com",
        "contact_address": "Manchester, UK",
        "contact_hours": "周一至周五 9:00-18:00",
    }

    # 批量更新设置
    update_settings(db_session, contact_settings)

    # 验证数据已正确保存
    assert get_setting(db_session, "contact_phone") == "0161-123-4567"
    assert get_setting(db_session, "contact_email") == "info@bowen-education.com"
    assert get_setting(db_session, "contact_address") == "Manchester, UK"
    assert get_setting(db_session, "contact_hours") == "周一至周五 9:00-18:00"

    # 验证数据库中的记录数
    count = db_session.query(SiteSetting).count()
    assert count == 4


def test_save_social_media(db_session: Session):
    """测试保存社交媒体链接"""
    # 准备测试数据
    social_settings = {
        "social_wechat": "https://example.com/wechat-qr.jpg",
        "social_weibo": "https://weibo.com/bowen",
        "social_facebook": "https://facebook.com/bowen",
        "social_twitter": "https://twitter.com/bowen",
        "social_linkedin": "https://linkedin.com/company/bowen",
    }

    # 批量更新设置
    update_settings(db_session, social_settings)

    # 验证数据已正确保存
    assert (
        get_setting(db_session, "social_wechat") == "https://example.com/wechat-qr.jpg"
    )
    assert get_setting(db_session, "social_weibo") == "https://weibo.com/bowen"
    assert get_setting(db_session, "social_facebook") == "https://facebook.com/bowen"
    assert get_setting(db_session, "social_twitter") == "https://twitter.com/bowen"
    assert (
        get_setting(db_session, "social_linkedin")
        == "https://linkedin.com/company/bowen"
    )

    # 验证数据库中的记录数
    count = db_session.query(SiteSetting).count()
    assert count == 5


def test_save_advanced(db_session: Session):
    """测试保存高级设置"""
    # 准备测试数据
    advanced_settings = {
        "seo_keywords": "羽毛球, 培训, 曼彻斯特",
        "seo_description": "曼彻斯特最专业的羽毛球培训机构",
        "analytics_code": "UA-123456-1",
        "tracking_code": "<script>console.log('tracking');</script>",
    }

    # 批量更新设置
    update_settings(db_session, advanced_settings)

    # 验证数据已正确保存
    assert get_setting(db_session, "seo_keywords") == "羽毛球, 培训, 曼彻斯特"
    assert (
        get_setting(db_session, "seo_description") == "曼彻斯特最专业的羽毛球培训机构"
    )
    assert get_setting(db_session, "analytics_code") == "UA-123456-1"
    assert (
        get_setting(db_session, "tracking_code")
        == "<script>console.log('tracking');</script>"
    )

    # 验证数据库中的记录数
    count = db_session.query(SiteSetting).count()
    assert count == 4


def test_key_value_storage(db_session: Session):
    """测试 Key-Value 存储机制"""
    # 测试创建新设置项
    update_setting(db_session, "test_key", "test_value")
    assert get_setting(db_session, "test_key") == "test_value"

    # 测试更新现有设置项
    update_setting(db_session, "test_key", "updated_value")
    assert get_setting(db_session, "test_key") == "updated_value"

    # 验证数据库中只有一条记录（更新而不是插入）
    count = (
        db_session.query(SiteSetting)
        .filter(SiteSetting.setting_key == "test_key")
        .count()
    )
    assert count == 1

    # 测试批量操作
    bulk_settings = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }
    update_settings(db_session, bulk_settings)

    assert get_setting(db_session, "key1") == "value1"
    assert get_setting(db_session, "key2") == "value2"
    assert get_setting(db_session, "key3") == "value3"

    # 验证总记录数
    total_count = db_session.query(SiteSetting).count()
    assert total_count == 4  # test_key + key1 + key2 + key3
