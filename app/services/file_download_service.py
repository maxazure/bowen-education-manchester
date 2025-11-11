# -*- coding: utf-8 -*-
"""File Download Service - Downloadable files management"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models import FileDownload, FileCategory, FileDownloadLog


class FileDownloadService:
    """Service class for managing downloadable files"""

    def __init__(self, db: Session):
        self.db = db

    # File management
    def get_all_files(
        self,
        skip: int = 0,
        limit: int = 100,
        status: str = "published",
        category_id: Optional[int] = None,
        is_featured: Optional[bool] = None,
        access_level: Optional[str] = None,
    ) -> List[FileDownload]:
        """Get all downloadable files with optional filters"""
        query = (
            self.db.query(FileDownload)
            .options(
                joinedload(FileDownload.category),
                joinedload(FileDownload.file_media),
                joinedload(FileDownload.thumbnail_media),
            )
            .filter(FileDownload.status == status)
        )

        if category_id:
            query = query.filter(FileDownload.category_id == category_id)

        if is_featured is not None:
            query = query.filter(FileDownload.is_featured == is_featured)

        if access_level:
            query = query.filter(FileDownload.access_level == access_level)

        return query.order_by(FileDownload.sort_order.desc(), FileDownload.id.desc()).offset(skip).limit(limit).all()

    def get_file_by_id(self, file_id: int) -> Optional[FileDownload]:
        """Get file by ID"""
        return (
            self.db.query(FileDownload)
            .options(
                joinedload(FileDownload.category),
                joinedload(FileDownload.file_media),
                joinedload(FileDownload.thumbnail_media),
            )
            .filter(FileDownload.id == file_id)
            .first()
        )

    def get_file_by_slug(self, slug: str, status: str = "published") -> Optional[FileDownload]:
        """Get file by slug"""
        return (
            self.db.query(FileDownload)
            .options(
                joinedload(FileDownload.category),
                joinedload(FileDownload.file_media),
                joinedload(FileDownload.thumbnail_media),
            )
            .filter(FileDownload.slug == slug, FileDownload.status == status)
            .first()
        )

    def get_featured_files(self, limit: int = 6, status: str = "published") -> List[FileDownload]:
        """Get featured files"""
        return (
            self.db.query(FileDownload)
            .options(joinedload(FileDownload.thumbnail_media))
            .filter(FileDownload.is_featured == True, FileDownload.status == status, FileDownload.is_active == True)
            .order_by(FileDownload.sort_order.desc())
            .limit(limit)
            .all()
        )

    def create_file(self, file_data: dict) -> FileDownload:
        """Create a new downloadable file"""
        file = FileDownload(**file_data)
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def update_file(self, file_id: int, file_data: dict) -> Optional[FileDownload]:
        """Update file"""
        file = self.get_file_by_id(file_id)
        if not file:
            return None

        for key, value in file_data.items():
            if hasattr(file, key) and key not in ["id", "created_at"]:
                setattr(file, key, value)

        self.db.commit()
        self.db.refresh(file)
        return file

    def delete_file(self, file_id: int) -> bool:
        """Delete file"""
        file = self.get_file_by_id(file_id)
        if not file:
            return False

        self.db.delete(file)
        self.db.commit()
        return True

    def increment_view_count(self, file_id: int) -> Optional[FileDownload]:
        """Increment file view count"""
        file = self.get_file_by_id(file_id)
        if not file:
            return None

        file.view_count += 1
        self.db.commit()
        self.db.refresh(file)
        return file

    def increment_download_count(self, file_id: int) -> Optional[FileDownload]:
        """Increment file download count"""
        file = self.get_file_by_id(file_id)
        if not file:
            return None

        file.download_count += 1
        file.last_downloaded_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(file)
        return file

    # Category management
    def get_categories(self, visible_only: bool = True) -> List[FileCategory]:
        """Get file categories"""
        query = self.db.query(FileCategory)

        if visible_only:
            query = query.filter(FileCategory.is_visible == visible_only)

        return query.order_by(FileCategory.sort_order).all()

    def get_category_by_id(self, category_id: int) -> Optional[FileCategory]:
        """Get file category by ID"""
        return self.db.query(FileCategory).filter(FileCategory.id == category_id).first()

    def create_category(self, category_data: dict) -> FileCategory:
        """Create a new file category"""
        category = FileCategory(**category_data)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category_id: int, category_data: dict) -> Optional[FileCategory]:
        """Update file category"""
        category = self.get_category_by_id(category_id)
        if not category:
            return None

        for key, value in category_data.items():
            if hasattr(category, key) and key not in ["id", "created_at"]:
                setattr(category, key, value)

        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        """Delete file category"""
        category = self.get_category_by_id(category_id)
        if not category:
            return False

        self.db.delete(category)
        self.db.commit()
        return True

    # Download log management
    def log_download(self, log_data: dict) -> FileDownloadLog:
        """Log a file download"""
        log = FileDownloadLog(**log_data)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        # Increment download count
        if log.download_status == "success":
            self.increment_download_count(log.file_id)

        return log

    def get_download_logs(
        self, file_id: Optional[int] = None, user_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[FileDownloadLog]:
        """Get download logs"""
        query = self.db.query(FileDownloadLog).options(
            joinedload(FileDownloadLog.file), joinedload(FileDownloadLog.user)
        )

        if file_id:
            query = query.filter(FileDownloadLog.file_id == file_id)

        if user_id:
            query = query.filter(FileDownloadLog.user_id == user_id)

        return query.order_by(FileDownloadLog.created_at.desc()).offset(skip).limit(limit).all()

    def get_file_count(
        self,
        status: str = "published",
        category_id: Optional[int] = None,
        access_level: Optional[str] = None,
    ) -> int:
        """Get total count of files"""
        query = self.db.query(FileDownload).filter(FileDownload.status == status)

        if category_id:
            query = query.filter(FileDownload.category_id == category_id)

        if access_level:
            query = query.filter(FileDownload.access_level == access_level)

        return query.count()
