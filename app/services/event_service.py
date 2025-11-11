# -*- coding: utf-8 -*-
"""Event Service - Event and registration management"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models import Event, EventRegistration


class EventService:
    """Service class for managing events and registrations"""

    def __init__(self, db: Session):
        self.db = db

    # Event management
    def get_all_events(
        self,
        skip: int = 0,
        limit: int = 100,
        status: str = "published",
        event_type: Optional[str] = None,
        is_featured: Optional[bool] = None,
    ) -> List[Event]:
        """Get all events with optional filters"""
        query = (
            self.db.query(Event)
            .options(joinedload(Event.cover_media))
            .filter(Event.status == status)
        )

        if event_type:
            query = query.filter(Event.event_type == event_type)

        if is_featured is not None:
            query = query.filter(Event.is_featured == is_featured)

        return query.order_by(Event.start_datetime.desc()).offset(skip).limit(limit).all()

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        return (
            self.db.query(Event)
            .options(joinedload(Event.cover_media), joinedload(Event.registrations))
            .filter(Event.id == event_id)
            .first()
        )

    def get_event_by_slug(self, slug: str, status: str = "published") -> Optional[Event]:
        """Get event by slug"""
        return (
            self.db.query(Event)
            .options(joinedload(Event.cover_media))
            .filter(Event.slug == slug, Event.status == status)
            .first()
        )

    def get_upcoming_events(self, limit: int = 10, status: str = "published") -> List[Event]:
        """Get upcoming events"""
        now = datetime.utcnow()
        return (
            self.db.query(Event)
            .options(joinedload(Event.cover_media))
            .filter(Event.status == status, Event.start_datetime >= now)
            .order_by(Event.start_datetime.asc())
            .limit(limit)
            .all()
        )

    def create_event(self, event_data: dict) -> Event:
        """Create a new event"""
        event = Event(**event_data)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def update_event(self, event_id: int, event_data: dict) -> Optional[Event]:
        """Update event"""
        event = self.get_event_by_id(event_id)
        if not event:
            return None

        for key, value in event_data.items():
            if hasattr(event, key) and key not in ["id", "created_at"]:
                setattr(event, key, value)

        self.db.commit()
        self.db.refresh(event)
        return event

    def delete_event(self, event_id: int) -> bool:
        """Delete event"""
        event = self.get_event_by_id(event_id)
        if not event:
            return False

        self.db.delete(event)
        self.db.commit()
        return True

    # Registration management
    def get_all_registrations(
        self,
        skip: int = 0,
        limit: int = 100,
        event_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> List[EventRegistration]:
        """Get all event registrations"""
        query = self.db.query(EventRegistration).options(
            joinedload(EventRegistration.event), joinedload(EventRegistration.user)
        )

        if event_id:
            query = query.filter(EventRegistration.event_id == event_id)

        if status:
            query = query.filter(EventRegistration.status == status)

        return query.order_by(EventRegistration.created_at.desc()).offset(skip).limit(limit).all()

    def get_registration_by_id(self, registration_id: int) -> Optional[EventRegistration]:
        """Get registration by ID"""
        return (
            self.db.query(EventRegistration)
            .options(joinedload(EventRegistration.event), joinedload(EventRegistration.user))
            .filter(EventRegistration.id == registration_id)
            .first()
        )

    def get_registration_by_number(self, registration_number: str) -> Optional[EventRegistration]:
        """Get registration by registration number"""
        return (
            self.db.query(EventRegistration)
            .options(joinedload(EventRegistration.event))
            .filter(EventRegistration.registration_number == registration_number)
            .first()
        )

    def create_registration(self, registration_data: dict) -> Optional[EventRegistration]:
        """Create a new event registration"""
        # Check if event has available capacity
        event_id = registration_data.get("event_id")
        event = self.get_event_by_id(event_id)

        if not event:
            return None

        # Check capacity
        if event.max_attendees and event.current_attendees >= event.max_attendees:
            if event.allow_waitlist:
                registration_data["status"] = "waitlist"
                event.waitlist_count += 1
            else:
                return None
        else:
            event.current_attendees += 1

        registration = EventRegistration(**registration_data)
        self.db.add(registration)
        self.db.commit()
        self.db.refresh(registration)
        return registration

    def update_registration(
        self, registration_id: int, registration_data: dict
    ) -> Optional[EventRegistration]:
        """Update event registration"""
        registration = self.get_registration_by_id(registration_id)
        if not registration:
            return None

        for key, value in registration_data.items():
            if hasattr(registration, key) and key not in ["id", "registration_number", "created_at"]:
                setattr(registration, key, value)

        self.db.commit()
        self.db.refresh(registration)
        return registration

    def update_registration_status(
        self, registration_id: int, status: str
    ) -> Optional[EventRegistration]:
        """Update registration status"""
        registration = self.get_registration_by_id(registration_id)
        if not registration:
            return None

        registration.status = status

        now = datetime.utcnow()
        if status == "confirmed":
            registration.confirmed_at = now
        elif status == "cancelled":
            registration.cancelled_at = now

        self.db.commit()
        self.db.refresh(registration)
        return registration

    def check_in_registration(self, registration_id: int) -> Optional[EventRegistration]:
        """Check in a registration"""
        registration = self.get_registration_by_id(registration_id)
        if not registration:
            return None

        registration.is_checked_in = True
        registration.checked_in_at = datetime.utcnow()
        registration.status = "attended"

        self.db.commit()
        self.db.refresh(registration)
        return registration

    def cancel_registration(
        self, registration_id: int, cancel_reason: Optional[str] = None
    ) -> Optional[EventRegistration]:
        """Cancel a registration"""
        registration = self.get_registration_by_id(registration_id)
        if not registration:
            return None

        registration.status = "cancelled"
        registration.cancelled_at = datetime.utcnow()
        if cancel_reason:
            registration.cancel_reason = cancel_reason

        # Update event attendee count
        event = registration.event
        if registration.status == "confirmed" and event.current_attendees > 0:
            event.current_attendees -= 1

        self.db.commit()
        self.db.refresh(registration)
        return registration

    def delete_registration(self, registration_id: int) -> bool:
        """Delete event registration"""
        registration = self.get_registration_by_id(registration_id)
        if not registration:
            return False

        self.db.delete(registration)
        self.db.commit()
        return True

    def get_event_count(self, status: str = "published", event_type: Optional[str] = None) -> int:
        """Get total count of events"""
        query = self.db.query(Event).filter(Event.status == status)

        if event_type:
            query = query.filter(Event.event_type == event_type)

        return query.count()

    def get_registration_count(self, event_id: Optional[int] = None, status: Optional[str] = None) -> int:
        """Get total count of registrations"""
        query = self.db.query(EventRegistration)

        if event_id:
            query = query.filter(EventRegistration.event_id == event_id)

        if status:
            query = query.filter(EventRegistration.status == status)

        return query.count()
