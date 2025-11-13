"""
媒体文件服务层

提供文件上传、处理、管理的核心功能
"""

import mimetypes
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from fastapi import UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from app.models.media import MediaFile, MediaFolder


class MediaService:
    """媒体文件服务"""

    # 文件大小限制（字节）
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

    # 支持的文件类型
    SUPPORTED_IMAGE_TYPES = {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "image/svg+xml",
    }
    SUPPORTED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/ogg"}
    SUPPORTED_DOCUMENT_TYPES = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    }

    # 缩略图尺寸
    THUMB_SIZE = (300, 300)
    MEDIUM_SIZE = (800, 800)

    # 上传目录
    UPLOAD_DIR = Path("uploads/media")

    def __init__(self, db: Session):
        self.db = db
        # 确保上传目录存在
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def validate_file(
        self, file: UploadFile
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        验证文件类型和大小

        Args:
            file: 上传的文件

        Returns:
            (是否有效, 错误信息, 文件类型)
        """
        # 获取 MIME 类型
        mime_type = file.content_type

        # 确定文件类型
        if mime_type in self.SUPPORTED_IMAGE_TYPES:
            file_type = "image"
            max_size = self.MAX_IMAGE_SIZE
        elif mime_type in self.SUPPORTED_VIDEO_TYPES:
            file_type = "video"
            max_size = self.MAX_VIDEO_SIZE
        elif mime_type in self.SUPPORTED_DOCUMENT_TYPES:
            file_type = "document"
            max_size = self.MAX_DOCUMENT_SIZE
        else:
            return False, f"不支持的文件类型: {mime_type}", None

        # 检查文件大小
        file.file.seek(0, 2)  # 移动到文件末尾
        file_size = file.file.tell()
        file.file.seek(0)  # 重置到文件开头

        if file_size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            return False, f"文件过大，最大允许 {max_size_mb:.1f}MB", None

        if file_size == 0:
            return False, "文件为空", None

        return True, None, file_type

    def generate_filename(self, original_filename: str) -> str:
        """
        生成唯一的文件名

        Args:
            original_filename: 原始文件名

        Returns:
            新的文件名（带扩展名）
        """
        # 获取文件扩展名
        ext = Path(original_filename).suffix.lower()
        # 生成唯一文件名
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return unique_name

    def get_file_path(self, filename: str, subfolder: str = "") -> Path:
        """
        获取文件的完整路径

        Args:
            filename: 文件名
            subfolder: 子文件夹（如 'images', 'videos'）

        Returns:
            完整文件路径
        """
        # 按日期组织文件
        date_folder = datetime.now().strftime("%Y/%m")

        if subfolder:
            full_path = self.UPLOAD_DIR / subfolder / date_folder
        else:
            full_path = self.UPLOAD_DIR / date_folder

        full_path.mkdir(parents=True, exist_ok=True)
        return full_path / filename

    async def upload_file(
        self, file: UploadFile, folder_id: Optional[int] = None, uploaded_by: Optional[str] = None
    ) -> Tuple[Optional[MediaFile], Optional[str]]:
        """
        上传文件并生成缩略图

        Args:
            file: 上传的文件
            folder_id: 文件夹 ID
            uploaded_by: 上传者

        Returns:
            (MediaFile 对象, 错误信息)
        """
        # 验证文件
        is_valid, error_msg, file_type = self.validate_file(file)
        if not is_valid:
            return None, error_msg

        # 生成文件名
        unique_filename = self.generate_filename(file.filename)

        # 确定子文件夹
        subfolder = file_type + "s"  # images, videos, documents

        # 获取文件路径
        file_path = self.get_file_path(unique_filename, subfolder)

        try:
            # 保存原始文件
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            # 获取文件大小
            file_size = len(content)

            # 创建 MediaFile 对象
            media_file = MediaFile(
                filename_original=file.filename,
                mime_type=file.content_type,
                size_bytes=file_size,
                path_original=str(file_path),
                file_type=file_type,
                folder_id=folder_id,
                uploaded_by=uploaded_by,
            )

            # 如果是图片，生成缩略图并获取尺寸
            if file_type == "image":
                thumb_path, medium_path, width, height = self.generate_thumbnails(file_path)
                media_file.path_thumb = str(thumb_path) if thumb_path else None
                media_file.path_medium = str(medium_path) if medium_path else None
                media_file.width = width
                media_file.height = height

            # 保存到数据库
            self.db.add(media_file)
            self.db.commit()
            self.db.refresh(media_file)

            return media_file, None

        except Exception as e:
            # 如果出错，删除已上传的文件
            if file_path.exists():
                file_path.unlink()
            return None, f"上传失败: {str(e)}"

    def generate_thumbnails(
        self, image_path: Path
    ) -> Tuple[Optional[Path], Optional[Path], Optional[int], Optional[int]]:
        """
        生成缩略图和中等尺寸图

        Args:
            image_path: 原图路径

        Returns:
            (缩略图路径, 中等尺寸图路径, 宽度, 高度)
        """
        try:
            with Image.open(image_path) as img:
                # 获取原始尺寸
                width, height = img.size

                # 生成缩略图
                thumb_path = image_path.parent / f"thumb_{image_path.name}"
                img_thumb = img.copy()
                img_thumb.thumbnail(self.THUMB_SIZE, Image.Resampling.LANCZOS)
                img_thumb.save(thumb_path, optimize=True, quality=85)

                # 生成中等尺寸图
                medium_path = image_path.parent / f"medium_{image_path.name}"
                img_medium = img.copy()
                img_medium.thumbnail(self.MEDIUM_SIZE, Image.Resampling.LANCZOS)
                img_medium.save(medium_path, optimize=True, quality=90)

                return thumb_path, medium_path, width, height

        except Exception as e:
            print(f"生成缩略图失败: {e}")
            return None, None, None, None

    def crop_image(
        self, media_id: int, x: int, y: int, width: int, height: int
    ) -> Tuple[bool, Optional[str]]:
        """
        裁剪图片

        Args:
            media_id: 媒体文件 ID
            x: 裁剪起始 X 坐标
            y: 裁剪起始 Y 坐标
            width: 裁剪宽度
            height: 裁剪高度

        Returns:
            (是否成功, 错误信息)
        """
        media_file = self.db.query(MediaFile).filter(MediaFile.id == media_id).first()
        if not media_file or not media_file.is_image:
            return False, "文件不存在或不是图片"

        try:
            image_path = Path(media_file.path_original)
            with Image.open(image_path) as img:
                # 裁剪图片
                cropped = img.crop((x, y, x + width, y + height))

                # 生成新文件名
                cropped_filename = f"cropped_{uuid.uuid4().hex}{image_path.suffix}"
                cropped_path = image_path.parent / cropped_filename

                # 保存裁剪后的图片
                cropped.save(cropped_path, quality=95)

                # 更新数据库
                media_file.path_original = str(cropped_path)
                media_file.width = width
                media_file.height = height

                # 重新生成缩略图
                thumb_path, medium_path, _, _ = self.generate_thumbnails(cropped_path)
                media_file.path_thumb = str(thumb_path) if thumb_path else None
                media_file.path_medium = str(medium_path) if medium_path else None

                self.db.commit()

                # 删除旧文件
                if image_path.exists() and image_path != cropped_path:
                    image_path.unlink()

                return True, None

        except Exception as e:
            return False, f"裁剪失败: {str(e)}"

    def resize_image(
        self, media_id: int, width: int, height: int
    ) -> Tuple[bool, Optional[str]]:
        """
        缩放图片

        Args:
            media_id: 媒体文件 ID
            width: 目标宽度
            height: 目标高度

        Returns:
            (是否成功, 错误信息)
        """
        media_file = self.db.query(MediaFile).filter(MediaFile.id == media_id).first()
        if not media_file or not media_file.is_image:
            return False, "文件不存在或不是图片"

        try:
            image_path = Path(media_file.path_original)
            with Image.open(image_path) as img:
                # 缩放图片
                resized = img.resize((width, height), Image.Resampling.LANCZOS)

                # 生成新文件名
                resized_filename = f"resized_{uuid.uuid4().hex}{image_path.suffix}"
                resized_path = image_path.parent / resized_filename

                # 保存缩放后的图片
                resized.save(resized_path, quality=95)

                # 更新数据库
                media_file.path_original = str(resized_path)
                media_file.width = width
                media_file.height = height

                # 重新生成缩略图
                thumb_path, medium_path, _, _ = self.generate_thumbnails(resized_path)
                media_file.path_thumb = str(thumb_path) if thumb_path else None
                media_file.path_medium = str(medium_path) if medium_path else None

                self.db.commit()

                # 删除旧文件
                if image_path.exists() and image_path != resized_path:
                    image_path.unlink()

                return True, None

        except Exception as e:
            return False, f"缩放失败: {str(e)}"

    def compress_image(
        self, media_id: int, quality: int = 85
    ) -> Tuple[bool, Optional[str]]:
        """
        压缩图片

        Args:
            media_id: 媒体文件 ID
            quality: 压缩质量 (1-100)

        Returns:
            (是否成功, 错误信息)
        """
        media_file = self.db.query(MediaFile).filter(MediaFile.id == media_id).first()
        if not media_file or not media_file.is_image:
            return False, "文件不存在或不是图片"

        try:
            image_path = Path(media_file.path_original)
            with Image.open(image_path) as img:
                # 压缩并覆盖原文件
                img.save(image_path, optimize=True, quality=quality)

                # 更新文件大小
                media_file.size_bytes = image_path.stat().st_size

                # 重新生成缩略图
                thumb_path, medium_path, _, _ = self.generate_thumbnails(image_path)
                media_file.path_thumb = str(thumb_path) if thumb_path else None
                media_file.path_medium = str(medium_path) if medium_path else None

                self.db.commit()

                return True, None

        except Exception as e:
            return False, f"压缩失败: {str(e)}"

    def delete_file(self, media_id: int) -> Tuple[bool, Optional[str]]:
        """
        删除文件

        Args:
            media_id: 媒体文件 ID

        Returns:
            (是否成功, 错误信息)
        """
        media_file = self.db.query(MediaFile).filter(MediaFile.id == media_id).first()
        if not media_file:
            return False, "文件不存在"

        try:
            # 删除物理文件
            file_paths = [media_file.path_original]
            if media_file.path_thumb:
                file_paths.append(media_file.path_thumb)
            if media_file.path_medium:
                file_paths.append(media_file.path_medium)

            for path_str in file_paths:
                path = Path(path_str)
                if path.exists():
                    path.unlink()

            # 删除数据库记录
            self.db.delete(media_file)
            self.db.commit()

            return True, None

        except Exception as e:
            return False, f"删除失败: {str(e)}"

    def get_folder_tree(self) -> list:
        """
        获取文件夹树形结构

        Returns:
            文件夹列表（树形）
        """
        folders = self.db.query(MediaFolder).order_by(MediaFolder.sort_order).all()

        # 构建树形结构
        folder_dict = {f.id: f for f in folders}
        tree = []

        for folder in folders:
            if folder.parent_id is None:
                tree.append(folder)

        return tree
