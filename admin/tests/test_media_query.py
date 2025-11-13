"""
测试媒体查询功能

测试用例:
1. 获取媒体列表
2. 媒体列表分页
3. 按类型筛选
4. 按文件名搜索
5. 获取单个媒体详情
6. 获取不存在的媒体
"""
from io import BytesIO

import pytest
from PIL import Image


class TestMediaQuery:
    """测试媒体查询功能"""

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

    def test_get_media_list(self, client, db_session):
        """测试获取媒体列表"""
        # 创建多个测试媒体
        self.upload_test_media(client, "image1.jpg")
        self.upload_test_media(client, "image2.jpg")
        self.upload_test_media(client, "image3.jpg")

        # 获取媒体列表
        response = client.get("/admin/media")

        # 验证响应
        assert response.status_code == 200
        data = response.json()

        # 验证返回列表
        assert "items" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) >= 3

        # 验证分页信息
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert data["total"] >= 3

    def test_media_list_pagination(self, client, db_session):
        """测试媒体列表分页"""
        # 创建 25 个媒体
        for i in range(25):
            self.upload_test_media(client, f"image_{i}.jpg")

        # 获取第一页（20条）
        response1 = client.get("/admin/media?page=1&per_page=20")
        assert response1.status_code == 200
        data1 = response1.json()

        # 验证返回 20 条
        assert len(data1["items"]) == 20
        assert data1["page"] == 1
        assert data1["per_page"] == 20
        assert data1["total"] >= 25

        # 获取第二页（5条）
        response2 = client.get("/admin/media?page=2&per_page=20")
        assert response2.status_code == 200
        data2 = response2.json()

        # 验证返回 5 条
        assert len(data2["items"]) >= 5
        assert data2["page"] == 2

    def test_filter_by_type(self, client, db_session):
        """测试按类型筛选"""
        # 创建不同类型的媒体
        self.upload_test_media(client, "image1.jpg", "image/jpeg")
        self.upload_test_media(client, "image2.png", "image/png")
        self.upload_test_media(client, "image3.gif", "image/gif")

        # 按类型筛选 JPEG
        response = client.get("/admin/media?mime_type=image/jpeg")

        # 验证响应
        assert response.status_code == 200
        data = response.json()

        # 验证只返回 JPEG 图片
        assert len(data["items"]) >= 1
        for item in data["items"]:
            assert item["mime_type"] == "image/jpeg"

    def test_search_by_filename(self, client, db_session):
        """测试按文件名搜索"""
        # 创建多个媒体
        self.upload_test_media(client, "logo_main.jpg")
        self.upload_test_media(client, "logo_secondary.jpg")
        self.upload_test_media(client, "banner.jpg")

        # 搜索包含 "logo" 的文件
        response = client.get("/admin/media?search=logo")

        # 验证响应
        assert response.status_code == 200
        data = response.json()

        # 验证只返回文件名包含 logo 的媒体
        assert len(data["items"]) >= 2
        for item in data["items"]:
            assert "logo" in item["filename_original"].lower()

    def test_get_single_media(self, client, db_session):
        """测试获取单个媒体详情"""
        # 创建媒体
        media = self.upload_test_media(client, "test_detail.jpg")

        # 获取媒体详情
        response = client.get(f"/admin/media/{media['id']}")

        # 验证响应
        assert response.status_code == 200
        data = response.json()

        # 验证返回完整信息
        assert data["id"] == media["id"]
        assert data["filename_original"] == "test_detail.jpg"
        assert "mime_type" in data
        assert "size_bytes" in data
        assert "width" in data
        assert "height" in data
        assert "path_original" in data
        assert "created_at" in data

    def test_get_nonexistent_media(self, client):
        """测试获取不存在的媒体返回 404"""
        # 获取不存在的媒体
        response = client.get("/admin/media/99999")

        # 验证返回 404
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
