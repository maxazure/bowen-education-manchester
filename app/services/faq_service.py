# -*- coding: utf-8 -*-
"""FAQ Service - Frequently Asked Questions management"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import FAQ, FAQCategory


class FAQService:
    """Service class for managing FAQs"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_visible: Optional[bool] = True,
        category: Optional[str] = None,
    ) -> List[FAQ]:
        """
        Get all FAQs with optional filters

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            is_visible: Filter by visible status
            category: Filter by category

        Returns:
            List of FAQ objects
        """
        query = self.db.query(FAQ)

        if is_visible is not None:
            query = query.filter(FAQ.is_visible == is_visible)

        if category:
            query = query.filter(FAQ.category == category)

        return query.order_by(FAQ.is_pinned.desc(), FAQ.sort_order, FAQ.id).offset(skip).limit(limit).all()

    def get_by_id(self, faq_id: int) -> Optional[FAQ]:
        """
        Get FAQ by ID

        Args:
            faq_id: FAQ ID

        Returns:
            FAQ object or None
        """
        return self.db.query(FAQ).filter(FAQ.id == faq_id).first()

    def get_by_category(self, category: str, is_visible: bool = True) -> List[FAQ]:
        """
        Get FAQs by category

        Args:
            category: Category name
            is_visible: Filter by visible status

        Returns:
            List of FAQ objects
        """
        query = self.db.query(FAQ).filter(FAQ.category == category)

        if is_visible:
            query = query.filter(FAQ.is_visible == is_visible)

        return query.order_by(FAQ.is_pinned.desc(), FAQ.sort_order).all()

    def get_pinned(self, limit: int = 5, is_visible: bool = True) -> List[FAQ]:
        """
        Get pinned FAQs

        Args:
            limit: Maximum number of FAQs to return
            is_visible: Filter by visible status

        Returns:
            List of pinned FAQ objects
        """
        query = self.db.query(FAQ).filter(FAQ.is_pinned == True)

        if is_visible:
            query = query.filter(FAQ.is_visible == is_visible)

        return query.order_by(FAQ.sort_order).limit(limit).all()

    def get_categories(self, visible_only: bool = True) -> List[FAQCategory]:
        """
        Get FAQ categories

        Args:
            visible_only: Only return visible categories

        Returns:
            List of FAQCategory objects
        """
        query = self.db.query(FAQCategory)

        if visible_only:
            query = query.filter(FAQCategory.is_visible == True)

        return query.order_by(FAQCategory.sort_order).all()

    def create(self, faq_data: dict) -> FAQ:
        """
        Create a new FAQ

        Args:
            faq_data: Dictionary containing FAQ data

        Returns:
            Created FAQ object
        """
        faq = FAQ(**faq_data)
        self.db.add(faq)
        self.db.commit()
        self.db.refresh(faq)
        return faq

    def update(self, faq_id: int, faq_data: dict) -> Optional[FAQ]:
        """
        Update FAQ

        Args:
            faq_id: FAQ ID
            faq_data: Dictionary containing updated data

        Returns:
            Updated FAQ object or None
        """
        faq = self.get_by_id(faq_id)
        if not faq:
            return None

        for key, value in faq_data.items():
            if hasattr(faq, key):
                setattr(faq, key, value)

        self.db.commit()
        self.db.refresh(faq)
        return faq

    def delete(self, faq_id: int) -> bool:
        """
        Delete FAQ

        Args:
            faq_id: FAQ ID

        Returns:
            True if deleted successfully, False otherwise
        """
        faq = self.get_by_id(faq_id)
        if not faq:
            return False

        self.db.delete(faq)
        self.db.commit()
        return True

    def increment_view_count(self, faq_id: int) -> Optional[FAQ]:
        """
        Increment view count for FAQ

        Args:
            faq_id: FAQ ID

        Returns:
            Updated FAQ object or None
        """
        faq = self.get_by_id(faq_id)
        if not faq:
            return None

        faq.view_count += 1
        self.db.commit()
        self.db.refresh(faq)
        return faq

    def mark_helpful(self, faq_id: int, is_helpful: bool = True) -> Optional[FAQ]:
        """
        Mark FAQ as helpful or not helpful

        Args:
            faq_id: FAQ ID
            is_helpful: True for helpful, False for not helpful

        Returns:
            Updated FAQ object or None
        """
        faq = self.get_by_id(faq_id)
        if not faq:
            return None

        if is_helpful:
            faq.helpful_count += 1
        else:
            faq.unhelpful_count += 1

        self.db.commit()
        self.db.refresh(faq)
        return faq

    def get_count(self, is_visible: Optional[bool] = True, category: Optional[str] = None) -> int:
        """
        Get total count of FAQs

        Args:
            is_visible: Filter by visible status
            category: Filter by category

        Returns:
            Count of FAQs
        """
        query = self.db.query(FAQ)

        if is_visible is not None:
            query = query.filter(FAQ.is_visible == is_visible)

        if category:
            query = query.filter(FAQ.category == category)

        return query.count()
