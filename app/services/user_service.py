# -*- coding: utf-8 -*-
"""User Service - User and authentication management"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import User


class UserService:
    """Service class for managing users and authentication"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = True,
        role: Optional[str] = None,
    ) -> List[User]:
        """
        Get all users with optional filters

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            is_active: Filter by active status
            role: Filter by role

        Returns:
            List of User objects
        """
        query = self.db.query(User)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        if role:
            query = query.filter(User.role == role)

        return query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username

        Args:
            username: Username

        Returns:
            User object or None
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            email: Email address

        Returns:
            User object or None
        """
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_data: dict) -> User:
        """
        Create a new user

        Args:
            user_data: Dictionary containing user data

        Returns:
            Created User object
        """
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        """
        Update user

        Args:
            user_id: User ID
            user_data: Dictionary containing updated data

        Returns:
            Updated User object or None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            if hasattr(user, key) and key not in ["id", "created_at", "password_hash"]:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """
        Delete user

        Args:
            user_id: User ID

        Returns:
            True if deleted successfully, False otherwise
        """
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True

    def authenticate(self, username_or_email: str, password_hash: str) -> Optional[User]:
        """
        Authenticate user by username/email and password

        Args:
            username_or_email: Username or email
            password_hash: Hashed password

        Returns:
            User object if authenticated, None otherwise

        Note:
            This is a simplified version. In production, you should use
            proper password hashing libraries like bcrypt or passlib
        """
        user = self.get_by_username(username_or_email)
        if not user:
            user = self.get_by_email(username_or_email)

        if not user or not user.is_active:
            return None

        # In production, use proper password verification
        # Example: if not verify_password(password, user.password_hash):
        if user.password_hash != password_hash:
            # Increment failed login attempts
            user.failed_login_attempts += 1
            self.db.commit()
            return None

        # Reset failed login attempts on successful login
        user.failed_login_attempts = 0
        user.last_login_at = datetime.utcnow()
        user.login_count += 1
        self.db.commit()
        self.db.refresh(user)

        return user

    def register(self, user_data: dict) -> Optional[User]:
        """
        Register a new user

        Args:
            user_data: Dictionary containing user registration data

        Returns:
            Created User object or None if username/email exists
        """
        # Check if username or email already exists
        if self.get_by_username(user_data.get("username")):
            return None

        if self.get_by_email(user_data.get("email")):
            return None

        # Set default role if not provided
        if "role" not in user_data:
            user_data["role"] = "member"

        return self.create(user_data)

    def change_password(self, user_id: int, new_password_hash: str) -> Optional[User]:
        """
        Change user password

        Args:
            user_id: User ID
            new_password_hash: New hashed password

        Returns:
            Updated User object or None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.password_hash = new_password_hash
        self.db.commit()
        self.db.refresh(user)
        return user

    def verify_email(self, user_id: int) -> Optional[User]:
        """
        Verify user email

        Args:
            user_id: User ID

        Returns:
            Updated User object or None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_points(self, user_id: int, points_delta: int) -> Optional[User]:
        """
        Update user points

        Args:
            user_id: User ID
            points_delta: Points to add (positive) or subtract (negative)

        Returns:
            Updated User object or None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.points += points_delta
        if points_delta > 0:
            user.total_earned_points += points_delta

        self.db.commit()
        self.db.refresh(user)
        return user

    def upgrade_membership(
        self, user_id: int, membership_level: str, expires_at: Optional[datetime] = None
    ) -> Optional[User]:
        """
        Upgrade user membership level

        Args:
            user_id: User ID
            membership_level: New membership level
            expires_at: Membership expiration date

        Returns:
            Updated User object or None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.membership_level = membership_level
        user.membership_expires_at = expires_at
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_count(self, is_active: Optional[bool] = True, role: Optional[str] = None) -> int:
        """
        Get total count of users

        Args:
            is_active: Filter by active status
            role: Filter by role

        Returns:
            Count of users
        """
        query = self.db.query(User)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        if role:
            query = query.filter(User.role == role)

        return query.count()
