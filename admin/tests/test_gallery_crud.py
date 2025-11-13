"""
测试相册 CRUD 功能

测试用例:
1. test_create_gallery - 创建相册
2. test_batch_add_images - 批量添加图片
3. test_update_gallery - 更新相册
4. test_delete_gallery - 删除相册
"""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.gallery import Gallery, GalleryImage
from app.models.media import MediaFile


def test_create_gallery(
    client: TestClient,
    db_session: Session,
    test_media_file: MediaFile,
) -> None:
    """
    测试创建相册

    验证:
    - 创建成功返回 200
    - 相册数据正确保存到数据库
    - slug 自动生成
    """
    gallery_data = {
        "title": "羽毛球比赛精彩瞬间",
        "description": "2024年春季羽毛球比赛精彩照片集锦",
        "category": "赛事活动",
        "tags": "羽毛球,比赛,2024",
        "cover_media_id": test_media_file.id,
        "display_mode": "grid",
        "is_featured": True,
        "is_public": True,
        "allow_download": False,
    }

    response = client.post(
        "/admin/galleries",
        json=gallery_data,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == gallery_data["title"]
    assert data["slug"] is not None
    assert data["category"] == gallery_data["category"]
    assert data["is_featured"] is True

    # 验证数据库
    gallery = db_session.query(Gallery).filter_by(id=data["id"]).first()
    assert gallery is not None
    assert gallery.title == gallery_data["title"]
    assert gallery.cover_media_id == test_media_file.id


def test_batch_add_images(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_files: list[MediaFile],
) -> None:
    """
    测试批量添加图片到相册

    验证:
    - 批量添加成功
    - 图片关联到相册
    - 排序序号自动设置
    """
    # 准备批量图片数据
    images_data = [
        {
            "media_id": media.id,
            "title": f"图片 {i+1}",
            "caption": f"这是第 {i+1} 张图片",
            "sort_order": i,
        }
        for i, media in enumerate(test_media_files[:3])
    ]

    response = client.post(
        f"/admin/galleries/{test_gallery.id}/images/batch",
        json={"images": images_data},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["added_count"] == 3

    # 验证数据库
    images = (
        db_session.query(GalleryImage)
        .filter_by(gallery_id=test_gallery.id)
        .order_by(GalleryImage.sort_order)
        .all()
    )
    assert len(images) == 3
    assert images[0].title == "图片 1"
    assert images[1].sort_order == 1


def test_update_gallery(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_file: MediaFile,
) -> None:
    """
    测试更新相册

    验证:
    - 更新成功返回 200
    - 相册信息正确更新
    - 可以更换封面图
    """
    update_data = {
        "title": "羽毛球比赛精彩瞬间（更新版）",
        "description": "更新后的描述",
        "category": "培训活动",
        "cover_media_id": test_media_file.id,
        "is_featured": False,
    }

    response = client.put(
        f"/admin/galleries/{test_gallery.id}",
        json=update_data,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["category"] == update_data["category"]
    assert data["is_featured"] is False

    # 验证数据库
    db_session.refresh(test_gallery)
    assert test_gallery.title == update_data["title"]
    assert test_gallery.cover_media_id == test_media_file.id


def test_delete_gallery(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_file: MediaFile,
) -> None:
    """
    测试删除相册

    验证:
    - 删除成功返回 200
    - 相册从数据库移除
    - 关联的图片记录也被删除（级联删除）
    """
    gallery_id = test_gallery.id

    # 先添加一些图片
    gallery_image = GalleryImage(
        gallery_id=gallery_id,
        media_id=test_media_file.id,
        title="测试图片",
        sort_order=0,
    )
    db_session.add(gallery_image)
    db_session.commit()

    # 删除相册
    response = client.delete(
        f"/admin/galleries/{gallery_id}",
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True

    # 验证数据库
    gallery = db_session.query(Gallery).filter_by(id=gallery_id).first()
    assert gallery is None

    # 验证关联图片也被删除
    images = db_session.query(GalleryImage).filter_by(gallery_id=gallery_id).all()
    assert len(images) == 0
