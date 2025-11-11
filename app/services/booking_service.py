# -*- coding: utf-8 -*-
"""Booking Service - Appointment and booking management"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models import Booking, BookingService as BookingServiceModel, BookingTimeSlot


class BookingService:
    """Service class for managing bookings and appointments"""

    def __init__(self, db: Session):
        self.db = db

    def get_all_bookings(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        service_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> List[Booking]:
        """
        Get all bookings with optional filters

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            service_id: Filter by service ID
            user_id: Filter by user ID

        Returns:
            List of Booking objects
        """
        query = self.db.query(Booking).options(
            joinedload(Booking.service), joinedload(Booking.staff), joinedload(Booking.user)
        )

        if status:
            query = query.filter(Booking.status == status)

        if service_id:
            query = query.filter(Booking.service_id == service_id)

        if user_id:
            query = query.filter(Booking.user_id == user_id)

        return query.order_by(Booking.booking_date.desc()).offset(skip).limit(limit).all()

    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        """
        Get booking by ID

        Args:
            booking_id: Booking ID

        Returns:
            Booking object or None
        """
        return (
            self.db.query(Booking)
            .options(joinedload(Booking.service), joinedload(Booking.staff), joinedload(Booking.user))
            .filter(Booking.id == booking_id)
            .first()
        )

    def get_booking_by_number(self, booking_number: str) -> Optional[Booking]:
        """
        Get booking by booking number

        Args:
            booking_number: Booking number

        Returns:
            Booking object or None
        """
        return (
            self.db.query(Booking)
            .options(joinedload(Booking.service), joinedload(Booking.staff))
            .filter(Booking.booking_number == booking_number)
            .first()
        )

    def create_booking(self, booking_data: dict) -> Booking:
        """
        Create a new booking

        Args:
            booking_data: Dictionary containing booking data

        Returns:
            Created Booking object
        """
        booking = Booking(**booking_data)
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update_booking(self, booking_id: int, booking_data: dict) -> Optional[Booking]:
        """
        Update booking

        Args:
            booking_id: Booking ID
            booking_data: Dictionary containing updated data

        Returns:
            Updated Booking object or None
        """
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return None

        for key, value in booking_data.items():
            if hasattr(booking, key) and key not in ["id", "booking_number", "created_at"]:
                setattr(booking, key, value)

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update_booking_status(self, booking_id: int, status: str) -> Optional[Booking]:
        """
        Update booking status

        Args:
            booking_id: Booking ID
            status: New status

        Returns:
            Updated Booking object or None
        """
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return None

        booking.status = status

        # Update timestamps based on status
        now = datetime.utcnow()
        if status == "confirmed":
            booking.confirmed_at = now
        elif status == "cancelled":
            booking.cancelled_at = now
        elif status == "completed":
            booking.completed_at = now

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def cancel_booking(self, booking_id: int, cancel_reason: Optional[str] = None) -> Optional[Booking]:
        """
        Cancel a booking

        Args:
            booking_id: Booking ID
            cancel_reason: Reason for cancellation

        Returns:
            Updated Booking object or None
        """
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return None

        booking.status = "cancelled"
        booking.cancelled_at = datetime.utcnow()
        if cancel_reason:
            booking.cancel_reason = cancel_reason

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def delete_booking(self, booking_id: int) -> bool:
        """
        Delete booking

        Args:
            booking_id: Booking ID

        Returns:
            True if deleted successfully, False otherwise
        """
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return False

        self.db.delete(booking)
        self.db.commit()
        return True

    # Service management methods
    def get_all_services(self, is_active: bool = True) -> List[BookingServiceModel]:
        """
        Get all booking services

        Args:
            is_active: Filter by active status

        Returns:
            List of BookingService objects
        """
        query = self.db.query(BookingServiceModel)

        if is_active:
            query = query.filter(BookingServiceModel.is_active == is_active)

        return query.order_by(BookingServiceModel.sort_order).all()

    def get_service_by_id(self, service_id: int) -> Optional[BookingServiceModel]:
        """
        Get booking service by ID

        Args:
            service_id: Service ID

        Returns:
            BookingService object or None
        """
        return self.db.query(BookingServiceModel).filter(BookingServiceModel.id == service_id).first()

    def create_service(self, service_data: dict) -> BookingServiceModel:
        """
        Create a new booking service

        Args:
            service_data: Dictionary containing service data

        Returns:
            Created BookingService object
        """
        service = BookingServiceModel(**service_data)
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return service

    def update_service(self, service_id: int, service_data: dict) -> Optional[BookingServiceModel]:
        """
        Update booking service

        Args:
            service_id: Service ID
            service_data: Dictionary containing updated data

        Returns:
            Updated BookingService object or None
        """
        service = self.get_service_by_id(service_id)
        if not service:
            return None

        for key, value in service_data.items():
            if hasattr(service, key):
                setattr(service, key, value)

        self.db.commit()
        self.db.refresh(service)
        return service

    def delete_service(self, service_id: int) -> bool:
        """
        Delete booking service

        Args:
            service_id: Service ID

        Returns:
            True if deleted successfully, False otherwise
        """
        service = self.get_service_by_id(service_id)
        if not service:
            return False

        self.db.delete(service)
        self.db.commit()
        return True

    def get_available_slots(
        self, service_id: int, start_date: datetime, end_date: datetime
    ) -> List[BookingTimeSlot]:
        """
        Get available time slots for a service

        Args:
            service_id: Service ID
            start_date: Start date
            end_date: End date

        Returns:
            List of available BookingTimeSlot objects
        """
        return (
            self.db.query(BookingTimeSlot)
            .filter(
                BookingTimeSlot.service_id == service_id,
                BookingTimeSlot.date >= start_date,
                BookingTimeSlot.date <= end_date,
                BookingTimeSlot.is_available == True,
                BookingTimeSlot.booked_slots < BookingTimeSlot.available_slots,
            )
            .order_by(BookingTimeSlot.date, BookingTimeSlot.start_time)
            .all()
        )

    def get_booking_count(
        self, status: Optional[str] = None, service_id: Optional[int] = None, user_id: Optional[int] = None
    ) -> int:
        """
        Get total count of bookings

        Args:
            status: Filter by status
            service_id: Filter by service ID
            user_id: Filter by user ID

        Returns:
            Count of bookings
        """
        query = self.db.query(Booking)

        if status:
            query = query.filter(Booking.status == status)

        if service_id:
            query = query.filter(Booking.service_id == service_id)

        if user_id:
            query = query.filter(Booking.user_id == user_id)

        return query.count()
