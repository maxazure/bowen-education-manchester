# -*- coding: utf-8 -*-
"""Video Service - Video gallery management"""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models import Video, VideoCategory, VideoPlaylist


class VideoService:
    """Service class for managing videos"""

    def __init__(self, db: Session):
        self.db = db

    # Video management
    def get_all_videos(
        self,
        skip: int = 0,
        limit: int = 100,
        status: str = "published",
        is_public: bool = True,
        category_id: Optional[int] = None,
        is_featured: Optional[bool] = None,
    ) -> List[Video]:
        """Get all videos with optional filters"""
        query = (
            self.db.query(Video)
            .options(
                joinedload(Video.category),
                joinedload(Video.video_media),
                joinedload(Video.thumbnail_media),
            )
            .filter(Video.status == status)
        )

        if is_public:
            query = query.filter(Video.is_public == is_public)

        if category_id:
            query = query.filter(Video.category_id == category_id)

        if is_featured is not None:
            query = query.filter(Video.is_featured == is_featured)

        return query.order_by(Video.sort_order.desc(), Video.id.desc()).offset(skip).limit(limit).all()

    def get_video_by_id(self, video_id: int) -> Optional[Video]:
        """Get video by ID"""
        return (
            self.db.query(Video)
            .options(
                joinedload(Video.category),
                joinedload(Video.video_media),
                joinedload(Video.thumbnail_media),
            )
            .filter(Video.id == video_id)
            .first()
        )

    def get_video_by_slug(self, slug: str, status: str = "published") -> Optional[Video]:
        """Get video by slug"""
        return (
            self.db.query(Video)
            .options(
                joinedload(Video.category),
                joinedload(Video.video_media),
                joinedload(Video.thumbnail_media),
            )
            .filter(Video.slug == slug, Video.status == status)
            .first()
        )

    def get_featured_videos(self, limit: int = 6, status: str = "published") -> List[Video]:
        """Get featured videos"""
        return (
            self.db.query(Video)
            .options(joinedload(Video.thumbnail_media))
            .filter(Video.is_featured == True, Video.status == status, Video.is_public == True)
            .order_by(Video.sort_order.desc())
            .limit(limit)
            .all()
        )

    def create_video(self, video_data: dict) -> Video:
        """Create a new video"""
        video = Video(**video_data)
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video

    def update_video(self, video_id: int, video_data: dict) -> Optional[Video]:
        """Update video"""
        video = self.get_video_by_id(video_id)
        if not video:
            return None

        for key, value in video_data.items():
            if hasattr(video, key) and key not in ["id", "created_at"]:
                setattr(video, key, value)

        self.db.commit()
        self.db.refresh(video)
        return video

    def delete_video(self, video_id: int) -> bool:
        """Delete video"""
        video = self.get_video_by_id(video_id)
        if not video:
            return False

        self.db.delete(video)
        self.db.commit()
        return True

    def increment_view_count(self, video_id: int) -> Optional[Video]:
        """Increment video view count"""
        video = self.get_video_by_id(video_id)
        if not video:
            return None

        video.view_count += 1
        self.db.commit()
        self.db.refresh(video)
        return video

    def increment_like_count(self, video_id: int) -> Optional[Video]:
        """Increment video like count"""
        video = self.get_video_by_id(video_id)
        if not video:
            return None

        video.like_count += 1
        self.db.commit()
        self.db.refresh(video)
        return video

    # Category management
    def get_categories(self, visible_only: bool = True) -> List[VideoCategory]:
        """Get video categories"""
        query = self.db.query(VideoCategory)

        if visible_only:
            query = query.filter(VideoCategory.is_visible == visible_only)

        return query.order_by(VideoCategory.sort_order).all()

    def get_category_by_id(self, category_id: int) -> Optional[VideoCategory]:
        """Get video category by ID"""
        return self.db.query(VideoCategory).filter(VideoCategory.id == category_id).first()

    def create_category(self, category_data: dict) -> VideoCategory:
        """Create a new video category"""
        category = VideoCategory(**category_data)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category_id: int, category_data: dict) -> Optional[VideoCategory]:
        """Update video category"""
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
        """Delete video category"""
        category = self.get_category_by_id(category_id)
        if not category:
            return False

        self.db.delete(category)
        self.db.commit()
        return True

    # Playlist management
    def get_all_playlists(self, is_public: bool = True) -> List[VideoPlaylist]:
        """Get all video playlists"""
        query = self.db.query(VideoPlaylist).options(joinedload(VideoPlaylist.cover_media))

        if is_public:
            query = query.filter(VideoPlaylist.is_public == is_public)

        return query.order_by(VideoPlaylist.sort_order.desc()).all()

    def get_playlist_by_id(self, playlist_id: int) -> Optional[VideoPlaylist]:
        """Get playlist by ID"""
        return (
            self.db.query(VideoPlaylist)
            .options(joinedload(VideoPlaylist.cover_media), joinedload(VideoPlaylist.videos))
            .filter(VideoPlaylist.id == playlist_id)
            .first()
        )

    def create_playlist(self, playlist_data: dict) -> VideoPlaylist:
        """Create a new video playlist"""
        playlist = VideoPlaylist(**playlist_data)
        self.db.add(playlist)
        self.db.commit()
        self.db.refresh(playlist)
        return playlist

    def update_playlist(self, playlist_id: int, playlist_data: dict) -> Optional[VideoPlaylist]:
        """Update video playlist"""
        playlist = self.get_playlist_by_id(playlist_id)
        if not playlist:
            return None

        for key, value in playlist_data.items():
            if hasattr(playlist, key) and key not in ["id", "created_at"]:
                setattr(playlist, key, value)

        self.db.commit()
        self.db.refresh(playlist)
        return playlist

    def delete_playlist(self, playlist_id: int) -> bool:
        """Delete video playlist"""
        playlist = self.get_playlist_by_id(playlist_id)
        if not playlist:
            return False

        self.db.delete(playlist)
        self.db.commit()
        return True

    def get_video_count(
        self, status: str = "published", is_public: bool = True, category_id: Optional[int] = None
    ) -> int:
        """Get total count of videos"""
        query = self.db.query(Video).filter(Video.status == status)

        if is_public:
            query = query.filter(Video.is_public == is_public)

        if category_id:
            query = query.filter(Video.category_id == category_id)

        return query.count()
