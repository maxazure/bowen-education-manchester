# -*- coding: utf-8 -*-
"""Services Module"""

from app.services import (
    event_service,
    faq_service,
    gallery_service,
    post_service,
    product_service,
    site_service,
    team_service,
)

# Also export classes where they exist
from app.services.event_service import EventService
from app.services.faq_service import FAQService
from app.services.team_service import TeamService

__all__ = [
    "event_service",
    "faq_service",
    "gallery_service",
    "post_service",
    "product_service",
    "site_service",
    "team_service",
    "EventService",
    "FAQService",
    "TeamService",
]
