"""
测试相册图片元数据管理

测试用例:
1. test_set_image_title - 设置图片标题
2. test_set_image_caption - 设置图片说明
3. test_toggle_visibility - 切换显示/隐藏
4. test_set_cover_image - 设置封面图
"""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.gallery import Gallery, GalleryImage
from app.models.media import MediaFile


def test_set_image_title(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_file: MediaFile,
) -> None:
    """
    测试设置图片标题

    验证:
    - 设置标题成功
    - 标题正确保存到数据库
    """
    # 创建一张图片
    image = GalleryImage(
        gallery_id=test_gallery.id,
        media_id=test_media_file.id,
        title="原始标题",
        sort_order=0,
    )
    db_session.add(image)
    db_session.commit()
    db_session.refresh(image)

    # 更新标题
    update_data = {"title": "精彩瞬间 - 决赛现场"}

    response = client.patch(
        f"/admin/galleries/{test_gallery.id}/images/{image.id}",
        json=update_data,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]

    # 验证数据库
    db_session.refresh(image)
    assert image.title == update_data["title"]


def test_set_image_caption(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_file: MediaFile,
) -> None:
    """
    测试设置图片说明

    验证:
    - 设置说明成功
    - 说明正确保存到数据库
    - 可以同时更新多个字段（title、caption、alt_text）
    """
    # 创建一张图片
    image = GalleryImage(
        gallery_id=test_gallery.id,
        media_id=test_media_file.id,
        title="比赛图片",
        sort_order=0,
    )
    db_session.add(image)
    db_session.commit()
    db_session.refresh(image)

    # 更新说明和 alt_text
    update_data = {
        "caption": "2024年春季羽毛球比赛决赛现场，选手正在进行激烈对决",
        "alt_text": "羽毛球比赛决赛现场照片",
    }

    response = client.patch(
        f"/admin/galleries/{test_gallery.id}/images/{image.id}",
        json=update_data,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["caption"] == update_data["caption"]
    assert data["alt_text"] == update_data["alt_text"]

    # 验证数据库
    db_session.refresh(image)
    assert image.caption == update_data["caption"]
    assert image.alt_text == update_data["alt_text"]


def test_toggle_visibility(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_file: MediaFile,
) -> None:
    """
    测试切换图片显示/隐藏

    验证:
    - 切换显示状态成功
    - 状态正确保存到数据库
    - 可以多次切换
    """
    # 创建一张图片（默认可见）
    image = GalleryImage(
        gallery_id=test_gallery.id,
        media_id=test_media_file.id,
        title="测试图片",
        is_visible=True,
        sort_order=0,
    )
    db_session.add(image)
    db_session.commit()
    db_session.refresh(image)

    # 第一次切换：隐藏
    response = client.post(
        f"/admin/galleries/{test_gallery.id}/images/{image.id}/toggle-visibility",
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_visible"] is False

    # 验证数据库
    db_session.refresh(image)
    assert image.is_visible is False

    # 第二次切换：显示
    response = client.post(
        f"/admin/galleries/{test_gallery.id}/images/{image.id}/toggle-visibility",
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_visible"] is True

    # 验证数据库
    db_session.refresh(image)
    assert image.is_visible is True


def test_set_cover_image(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_files: list[MediaFile],
) -> None:
    """
    测试设置相册封面图

    验证:
    - 设置封面图成功
    - 封面图 ID 正确更新
    - 可以更换封面图
    """
    # 添加 2 张图片
    image1 = GalleryImage(
        gallery_id=test_gallery.id,
        media_id=test_media_files[0].id,
        title="图片1",
        sort_order=0,
    )
    image2 = GalleryImage(
        gallery_id=test_gallery.id,
        media_id=test_media_files[1].id,
        title="图片2",
        sort_order=1,
    )
    db_session.add_all([image1, image2])
    db_session.commit()
    db_session.refresh(image1)
    db_session.refresh(image2)

    # 设置第一张图片为封面
    response = client.post(
        f"/admin/galleries/{test_gallery.id}/set-cover",
        json={"media_id": test_media_files[0].id},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["cover_media_id"] == test_media_files[0].id

    # 验证数据库
    db_session.refresh(test_gallery)
    assert test_gallery.cover_media_id == test_media_files[0].id

    # 更换封面图为第二张
    response = client.post(
        f"/admin/galleries/{test_gallery.id}/set-cover",
        json={"media_id": test_media_files[1].id},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["cover_media_id"] == test_media_files[1].id

    # 验证数据库
    db_session.refresh(test_gallery)
    assert test_gallery.cover_media_id == test_media_files[1].id
