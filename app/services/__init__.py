# -*- coding: utf-8 -*-
"""Services Module"""

from app.services import (
    booking_service,
    event_service,
    faq_service,
    file_download_service,
    post_service,
    product_service,
    site_service,
    team_service,
    user_service,
    video_service,
)

# Also export classes where they exist
from app.services.booking_service import BookingService
from app.services.event_service import EventService
from app.services.faq_service import FAQService
from app.services.file_download_service import FileDownloadService
from app.services.team_service import TeamService
from app.services.user_service import UserService
from app.services.video_service import VideoService

__all__ = [
    "booking_service",
    "event_service",
    "faq_service",
    "file_download_service",
    "post_service",
    "product_service",
    "site_service",
    "team_service",
    "user_service",
    "video_service",
    "BookingService",
    "EventService",
    "FAQService",
    "FileDownloadService",
    "TeamService",
    "UserService",
    "VideoService",
]
