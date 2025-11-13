"""
测试相册图片排序功能

测试用例:
1. test_drag_sort - 拖拽排序
2. test_batch_update_order - 批量更新排序
"""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.gallery import Gallery, GalleryImage
from app.models.media import MediaFile


def test_drag_sort(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_files: list[MediaFile],
) -> None:
    """
    测试拖拽排序功能

    验证:
    - 拖拽排序成功
    - 排序序号正确更新
    - 其他图片顺序自动调整
    """
    # 先创建 3 张图片
    images = []
    for i, media in enumerate(test_media_files[:3]):
        image = GalleryImage(
            gallery_id=test_gallery.id,
            media_id=media.id,
            title=f"图片 {i+1}",
            sort_order=i,
        )
        db_session.add(image)
        images.append(image)
    db_session.commit()

    # 刷新获取 ID
    for img in images:
        db_session.refresh(img)

    # 模拟拖拽：将第 1 张图片（索引0）拖到第 3 张位置（索引2）
    # 原顺序: [img0, img1, img2]
    # 新顺序: [img1, img2, img0]
    sort_data = {
        "image_id": images[0].id,
        "new_position": 2,
    }

    response = client.post(
        f"/admin/galleries/{test_gallery.id}/images/drag-sort",
        json=sort_data,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True

    # 验证排序
    sorted_images = (
        db_session.query(GalleryImage)
        .filter_by(gallery_id=test_gallery.id)
        .order_by(GalleryImage.sort_order)
        .all()
    )

    assert len(sorted_images) == 3
    assert sorted_images[0].id == images[1].id  # img1 现在是第一个
    assert sorted_images[0].sort_order == 0
    assert sorted_images[1].id == images[2].id  # img2 现在是第二个
    assert sorted_images[1].sort_order == 1
    assert sorted_images[2].id == images[0].id  # img0 现在是第三个
    assert sorted_images[2].sort_order == 2


def test_batch_update_order(
    client: TestClient,
    db_session: Session,
    test_gallery: Gallery,
    test_media_files: list[MediaFile],
) -> None:
    """
    测试批量更新排序

    验证:
    - 批量更新排序成功
    - 所有图片的排序序号正确更新
    """
    # 先创建 4 张图片
    images = []
    for i, media in enumerate(test_media_files[:4]):
        image = GalleryImage(
            gallery_id=test_gallery.id,
            media_id=media.id,
            title=f"图片 {i+1}",
            sort_order=i,
        )
        db_session.add(image)
        images.append(image)
    db_session.commit()

    # 刷新获取 ID
    for img in images:
        db_session.refresh(img)

    # 批量更新排序：完全打乱顺序
    # 原顺序: [0, 1, 2, 3]
    # 新顺序: [2, 0, 3, 1]
    new_order = [
        {"id": images[2].id, "sort_order": 0},
        {"id": images[0].id, "sort_order": 1},
        {"id": images[3].id, "sort_order": 2},
        {"id": images[1].id, "sort_order": 3},
    ]

    response = client.post(
        f"/admin/galleries/{test_gallery.id}/images/reorder",
        json={"order": new_order},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["updated_count"] == 4

    # 验证排序
    sorted_images = (
        db_session.query(GalleryImage)
        .filter_by(gallery_id=test_gallery.id)
        .order_by(GalleryImage.sort_order)
        .all()
    )

    assert len(sorted_images) == 4
    assert sorted_images[0].id == images[2].id
    assert sorted_images[0].sort_order == 0
    assert sorted_images[1].id == images[0].id
    assert sorted_images[1].sort_order == 1
    assert sorted_images[2].id == images[3].id
    assert sorted_images[2].sort_order == 2
    assert sorted_images[3].id == images[1].id
    assert sorted_images[3].sort_order == 3
