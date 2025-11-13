"""
测试媒体删除功能

测试用例:
1. 删除未使用的媒体成功
2. 删除被引用的媒体失败
3. 删除时清理文件
4. 删除不存在的媒体
"""
from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image


class TestMediaDelete:
    """测试媒体删除功能"""

    def create_test_image(self, format: str = "JPEG", size: tuple = (800, 600)) -> BytesIO:
        """创建测试图片"""
        img = Image.new("RGB", size, color="red")
        img_io = BytesIO()
        img.save(img_io, format=format, quality=90)
        img_io.seek(0)
        return img_io

    def upload_test_media(self, client, filename: str, mime_type: str = "image/jpeg"):
        """上传测试媒体"""
        img_io = self.create_test_image()
        response = client.post(
            "/admin/media/upload",
            files={"file": (filename, img_io, mime_type)},
        )
        assert response.status_code == 201
        return response.json()

    def test_delete_unused_media(self, client, db_session):
        """测试删除未使用的媒体成功"""
        # 创建媒体（usage_count=0）
        media = self.upload_test_media(client, "test_delete.jpg")

        # 记录文件路径
        file_path = media["path_original"]
        thumb_path = media.get("path_thumb")

        # 验证文件存在
        assert Path(file_path).exists()

        # 删除媒体
        response = client.delete(f"/admin/media/{media['id']}")

        # 验证返回 204
        assert response.status_code == 204

        # 验证文件被删除
        assert not Path(file_path).exists()
        if thumb_path:
            assert not Path(thumb_path).exists()

        # 验证数据库记录被删除
        from app.models.media import MediaFile
        deleted_media = db_session.query(MediaFile).filter_by(id=media["id"]).first()
        assert deleted_media is None

    def test_delete_used_media_fails(self, client, db_session):
        """测试删除被引用的媒体失败"""
        # 创建媒体
        media = self.upload_test_media(client, "test_used.jpg")

        # 模拟媒体被使用（增加 usage_count）
        from app.models.media import MediaFile
        used_media = db_session.query(MediaFile).filter_by(id=media["id"]).first()
        used_media.usage_count = 5
        db_session.commit()

        # 记录文件路径
        file_path = media["path_original"]

        # 尝试删除媒体
        response = client.delete(f"/admin/media/{media['id']}")

        # 验证返回 400
        assert response.status_code == 400

        # 验证错误消息
        data = response.json()
        assert "detail" in data
        assert "使用" in data["detail"] or "use" in data["detail"].lower()

        # 验证文件未被删除
        assert Path(file_path).exists()

        # 验证数据库记录未被删除
        still_exists = db_session.query(MediaFile).filter_by(id=media["id"]).first()
        assert still_exists is not None

    def test_delete_with_file_cleanup(self, client, db_session):
        """测试删除时清理文件"""
        # 创建媒体
        media = self.upload_test_media(client, "test_cleanup.jpg")

        # 记录文件路径
        original_path = media["path_original"]
        thumb_path = media.get("path_thumb")

        # 验证原图和缩略图都存在
        assert Path(original_path).exists()
        if thumb_path:
            assert Path(thumb_path).exists()

        # 删除媒体
        response = client.delete(f"/admin/media/{media['id']}")

        # 验证返回 204
        assert response.status_code == 204

        # 验证原图和缩略图都被删除
        assert not Path(original_path).exists()
        if thumb_path:
            assert not Path(thumb_path).exists()

    def test_delete_nonexistent_media(self, client):
        """测试删除不存在的媒体"""
        # 删除不存在的媒体
        response = client.delete("/admin/media/99999")

        # 验证返回 404
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
