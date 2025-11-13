"""
测试媒体上传功能

测试用例:
1. 上传 JPG 图片
2. 上传 PNG 图片
3. 上传 GIF 图片
4. 上传 WebP 图片
5. 上传不支持的格式
6. 上传超大文件
7. 缩略图生成
8. 文件名清洗
9. 重复文件名处理
"""
import os
from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image


class TestMediaUpload:
    """测试媒体上传功能"""

    def create_test_image(self, format: str = "JPEG", size: tuple = (800, 600), file_size_mb: float = None) -> BytesIO:
        """
        创建测试图片

        Args:
            format: 图片格式 (JPEG, PNG, GIF, WEBP)
            size: 图片尺寸 (width, height)
            file_size_mb: 目标文件大小（MB），如果指定则创建接近该大小的图片

        Returns:
            BytesIO: 图片字节流
        """
        img = Image.new("RGB", size, color="red")
        img_io = BytesIO()

        if file_size_mb:
            # 创建指定大小的图片
            quality = 95
            while True:
                img_io = BytesIO()
                img.save(img_io, format=format, quality=quality)
                current_size_mb = img_io.tell() / (1024 * 1024)

                if current_size_mb >= file_size_mb * 0.9:  # 允许 10% 误差
                    break

                # 如果太小，增加图片尺寸
                if current_size_mb < file_size_mb * 0.5:
                    size = (int(size[0] * 1.5), int(size[1] * 1.5))
                    img = Image.new("RGB", size, color="red")
        else:
            img.save(img_io, format=format, quality=90)

        img_io.seek(0)
        return img_io

    def test_upload_jpg_image(self, client, db_session):
        """测试上传 JPG 图片成功"""
        # 创建测试图片
        img_io = self.create_test_image(format="JPEG")

        # 上传图片
        response = client.post(
            "/admin/media/upload",
            files={"file": ("test_image.jpg", img_io, "image/jpeg")},
        )

        # 验证响应
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["filename_original"] == "test_image.jpg"
        assert data["mime_type"] == "image/jpeg"
        assert data["width"] == 800
        assert data["height"] == 600

        # 验证文件保存到磁盘
        file_path = data["path_original"]
        assert Path(file_path).exists()

        # 验证数据库记录
        from app.models.media import MediaFile
        media = db_session.query(MediaFile).filter_by(id=data["id"]).first()
        assert media is not None
        assert media.filename_original == "test_image.jpg"

    def test_upload_png_image(self, client, db_session):
        """测试上传 PNG 图片成功"""
        # 创建测试图片
        img_io = self.create_test_image(format="PNG")

        # 上传图片
        response = client.post(
            "/admin/media/upload",
            files={"file": ("test_image.png", img_io, "image/png")},
        )

        # 验证响应
        assert response.status_code == 201
        data = response.json()
        assert data["filename_original"] == "test_image.png"
        assert data["mime_type"] == "image/png"

        # 验证文件保存到磁盘
        file_path = data["path_original"]
        assert Path(file_path).exists()

    def test_upload_gif_image(self, client, db_session):
        """测试上传 GIF 图片成功"""
        # 创建测试图片
        img_io = self.create_test_image(format="GIF")

        # 上传图片
        response = client.post(
            "/admin/media/upload",
            files={"file": ("test_image.gif", img_io, "image/gif")},
        )

        # 验证响应
        assert response.status_code == 201
        data = response.json()
        assert data["filename_original"] == "test_image.gif"
        assert data["mime_type"] == "image/gif"

        # 验证文件保存到磁盘
        file_path = data["path_original"]
        assert Path(file_path).exists()

    def test_upload_webp_image(self, client, db_session):
        """测试上传 WebP 图片成功"""
        # 创建测试图片
        img_io = self.create_test_image(format="WEBP")

        # 上传图片
        response = client.post(
            "/admin/media/upload",
            files={"file": ("test_image.webp", img_io, "image/webp")},
        )

        # 验证响应
        assert response.status_code == 201
        data = response.json()
        assert data["filename_original"] == "test_image.webp"
        assert data["mime_type"] == "image/webp"

        # 验证文件保存到磁盘
        file_path = data["path_original"]
        assert Path(file_path).exists()

    def test_upload_unsupported_format(self, client):
        """测试上传不支持格式失败"""
        # 创建不支持的文件
        file_io = BytesIO(b"fake executable content")

        # 上传文件
        response = client.post(
            "/admin/media/upload",
            files={"file": ("malware.exe", file_io, "application/x-msdownload")},
        )

        # 验证响应
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "不支持" in data["detail"] or "unsupported" in data["detail"].lower()

    def test_upload_oversized_file(self, client):
        """测试上传超大文件失败 (>5MB)"""
        # 创建 6MB 的测试数据（不使用真实图片，太慢）
        large_data = b"x" * (6 * 1024 * 1024)  # 6MB
        img_io = BytesIO(large_data)

        # 上传图片
        response = client.post(
            "/admin/media/upload",
            files={"file": ("large_image.jpg", img_io, "image/jpeg")},
        )

        # 验证响应
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "大小" in data["detail"] or "size" in data["detail"].lower()

    def test_thumbnail_generation(self, client, db_session):
        """测试生成缩略图"""
        # 创建测试图片
        img_io = self.create_test_image(format="JPEG", size=(1920, 1080))

        # 上传图片
        response = client.post(
            "/admin/media/upload",
            files={"file": ("test_large.jpg", img_io, "image/jpeg")},
        )

        # 验证响应
        assert response.status_code == 201
        data = response.json()

        # 验证 thumbnail_url 不为空
        assert "path_thumb" in data
        assert data["path_thumb"] is not None

        # 验证缩略图文件存在
        thumb_path = data["path_thumb"]
        assert Path(thumb_path).exists()

        # 验证缩略图尺寸正确 (300x300 或保持比例)
        from PIL import Image
        with Image.open(thumb_path) as thumb_img:
            width, height = thumb_img.size
            assert width <= 300
            assert height <= 300

    def test_filename_sanitization(self, client, db_session):
        """测试文件名清洗（移除特殊字符）"""
        # 创建测试图片
        img_io = self.create_test_image(format="JPEG")

        # 上传文件名包含特殊字符的图片
        dangerous_filename = "../../../etc/passwd.jpg"

        response = client.post(
            "/admin/media/upload",
            files={"file": (dangerous_filename, img_io, "image/jpeg")},
        )

        # 验证响应
        assert response.status_code == 201
        data = response.json()

        # 验证保存的文件名安全（不包含路径遍历字符）
        saved_filename = data["filename_original"]
        assert "../" not in saved_filename
        assert ".." not in saved_filename

        # 验证没有路径遍历风险
        file_path = data["path_original"]
        assert "../" not in file_path
        assert "etc/passwd" not in file_path

    def test_duplicate_filename_handling(self, client, db_session):
        """测试重复文件名处理"""
        # 创建测试图片
        img_io1 = self.create_test_image(format="JPEG")
        img_io2 = self.create_test_image(format="JPEG")

        # 上传第一个文件
        response1 = client.post(
            "/admin/media/upload",
            files={"file": ("duplicate.jpg", img_io1, "image/jpeg")},
        )
        assert response1.status_code == 201
        data1 = response1.json()

        # 上传同名文件
        response2 = client.post(
            "/admin/media/upload",
            files={"file": ("duplicate.jpg", img_io2, "image/jpeg")},
        )
        assert response2.status_code == 201
        data2 = response2.json()

        # 验证第二次文件名不同（自动添加后缀）
        assert data1["path_original"] != data2["path_original"]

        # 验证两个文件都保存成功
        assert Path(data1["path_original"]).exists()
        assert Path(data2["path_original"]).exists()
