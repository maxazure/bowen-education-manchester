"""
测试媒体更新功能

测试用例:
1. 更新媒体标题
2. 更新 Alt 文本
3. 更新说明
4. 更新所有元数据
"""
from io import BytesIO

import pytest
from PIL import Image


class TestMediaUpdate:
    """测试媒体更新功能"""

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

    def test_update_media_title(self, client, db_session):
        """测试更新媒体标题"""
        # 创建媒体
        media = self.upload_test_media(client, "test.jpg")

        # 更新标题
        response = client.put(
            f"/admin/media/{media['id']}",
            json={"title": "New Title"},
        )

        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"

        # 验证数据库更新
        from app.models.media import MediaFile
        updated_media = db_session.query(MediaFile).filter_by(id=media["id"]).first()
        assert updated_media.title == "New Title"

    def test_update_media_alt_text(self, client, db_session):
        """测试更新 Alt 文本"""
        # 创建媒体
        media = self.upload_test_media(client, "test.jpg")

        # 更新 Alt 文本
        response = client.put(
            f"/admin/media/{media['id']}",
            json={"alt_text": "Alt text for SEO"},
        )

        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["alt_text"] == "Alt text for SEO"

        # 验证数据库更新
        from app.models.media import MediaFile
        updated_media = db_session.query(MediaFile).filter_by(id=media["id"]).first()
        assert updated_media.alt_text == "Alt text for SEO"

    def test_update_media_caption(self, client, db_session):
        """测试更新说明"""
        # 创建媒体
        media = self.upload_test_media(client, "test.jpg")

        # 更新说明
        response = client.put(
            f"/admin/media/{media['id']}",
            json={"caption": "This is a caption"},
        )

        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["caption"] == "This is a caption"

        # 验证数据库更新
        from app.models.media import MediaFile
        updated_media = db_session.query(MediaFile).filter_by(id=media["id"]).first()
        assert updated_media.caption == "This is a caption"

    def test_update_all_metadata(self, client, db_session):
        """测试更新所有元数据"""
        # 创建媒体
        media = self.upload_test_media(client, "test.jpg")

        # 更新所有元数据
        response = client.put(
            f"/admin/media/{media['id']}",
            json={
                "title": "Complete Title",
                "alt_text": "Complete Alt Text",
                "caption": "Complete Caption",
            },
        )

        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Complete Title"
        assert data["alt_text"] == "Complete Alt Text"
        assert data["caption"] == "Complete Caption"

        # 验证数据库更新
        from app.models.media import MediaFile
        updated_media = db_session.query(MediaFile).filter_by(id=media["id"]).first()
        assert updated_media.title == "Complete Title"
        assert updated_media.alt_text == "Complete Alt Text"
        assert updated_media.caption == "Complete Caption"
