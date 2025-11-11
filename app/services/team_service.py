# -*- coding: utf-8 -*-
"""Team Service - Team member management"""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models import TeamMember
from app.utils.cache import cache_content


class TeamService:
    """Service class for managing team members"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = True,
        is_featured: Optional[bool] = None,
    ) -> List[TeamMember]:
        """
        Get all team members with optional filters

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            is_active: Filter by active status
            is_featured: Filter by featured status

        Returns:
            List of TeamMember objects
        """
        query = self.db.query(TeamMember).options(joinedload(TeamMember.photo))

        if is_active is not None:
            query = query.filter(TeamMember.is_active == is_active)

        if is_featured is not None:
            query = query.filter(TeamMember.is_featured == is_featured)

        return query.order_by(TeamMember.sort_order, TeamMember.id).offset(skip).limit(limit).all()

    def get_by_id(self, member_id: int) -> Optional[TeamMember]:
        """
        Get team member by ID

        Args:
            member_id: Team member ID

        Returns:
            TeamMember object or None
        """
        return (
            self.db.query(TeamMember)
            .options(joinedload(TeamMember.photo))
            .filter(TeamMember.id == member_id)
            .first()
        )

    def get_by_department(self, department: str, is_active: bool = True) -> List[TeamMember]:
        """
        Get team members by department

        Args:
            department: Department name
            is_active: Filter by active status

        Returns:
            List of TeamMember objects
        """
        query = (
            self.db.query(TeamMember)
            .options(joinedload(TeamMember.photo))
            .filter(TeamMember.department == department)
        )

        if is_active:
            query = query.filter(TeamMember.is_active == is_active)

        return query.order_by(TeamMember.sort_order).all()

    def get_featured_members(self, limit: int = 10) -> List[TeamMember]:
        """
        Get featured team members

        Args:
            limit: Maximum number of members to return

        Returns:
            List of featured TeamMember objects
        """
        return (
            self.db.query(TeamMember)
            .options(joinedload(TeamMember.photo))
            .filter(TeamMember.is_featured == True, TeamMember.is_active == True)
            .order_by(TeamMember.sort_order)
            .limit(limit)
            .all()
        )

    def create(self, member_data: dict) -> TeamMember:
        """
        Create a new team member

        Args:
            member_data: Dictionary containing team member data

        Returns:
            Created TeamMember object
        """
        member = TeamMember(**member_data)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def update(self, member_id: int, member_data: dict) -> Optional[TeamMember]:
        """
        Update team member

        Args:
            member_id: Team member ID
            member_data: Dictionary containing updated data

        Returns:
            Updated TeamMember object or None
        """
        member = self.get_by_id(member_id)
        if not member:
            return None

        for key, value in member_data.items():
            if hasattr(member, key):
                setattr(member, key, value)

        self.db.commit()
        self.db.refresh(member)
        return member

    def delete(self, member_id: int) -> bool:
        """
        Delete team member

        Args:
            member_id: Team member ID

        Returns:
            True if deleted successfully, False otherwise
        """
        member = self.get_by_id(member_id)
        if not member:
            return False

        self.db.delete(member)
        self.db.commit()
        return True

    def get_count(self, is_active: Optional[bool] = True) -> int:
        """
        Get total count of team members

        Args:
            is_active: Filter by active status

        Returns:
            Count of team members
        """
        query = self.db.query(TeamMember)

        if is_active is not None:
            query = query.filter(TeamMember.is_active == is_active)

        return query.count()
