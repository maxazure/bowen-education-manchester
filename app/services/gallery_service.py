"""Gallery Service - 相册服务"""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models.gallery import Gallery, GalleryImage


class GalleryService:
    """相册服务类"""

    def __init__(self, db: Session):
        self.db = db

    def get_gallery_by_slug(self, slug: str) -> Optional[Gallery]:
        """
        根据slug获取相册

        Args:
            slug: 相册slug

        Returns:
            Gallery对象或None
        """
        return (
            self.db.query(Gallery)
            .filter(Gallery.slug == slug, Gallery.is_public == True)
            .first()
        )

    def get_gallery_images(self, gallery_id: int, visible_only: bool = True) -> List[GalleryImage]:
        """
        获取相册中的所有图片

        Args:
            gallery_id: 相册ID
            visible_only: 是否只返回可见的图片

        Returns:
            GalleryImage对象列表
        """
        query = (
            self.db.query(GalleryImage)
            .filter(GalleryImage.gallery_id == gallery_id)
            .options(joinedload(GalleryImage.media))
        )

        if visible_only:
            query = query.filter(GalleryImage.is_visible == True)

        return query.order_by(GalleryImage.sort_order, GalleryImage.id).all()

    def get_all_galleries(
        self,
        category: Optional[str] = None,
        featured_only: bool = False,
        public_only: bool = True,
        limit: Optional[int] = None,
    ) -> List[Gallery]:
        """
        获取所有相册列表

        Args:
            category: 分类筛选
            featured_only: 是否只返回推荐相册
            public_only: 是否只返回公开相册
            limit: 返回数量限制

        Returns:
            Gallery对象列表
        """
        query = self.db.query(Gallery)

        if category:
            query = query.filter(Gallery.category == category)

        if featured_only:
            query = query.filter(Gallery.is_featured == True)

        if public_only:
            query = query.filter(Gallery.is_public == True)

        query = query.order_by(Gallery.sort_order, Gallery.id.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def increment_view_count(self, gallery_id: int):
        """
        增加相册浏览次数

        Args:
            gallery_id: 相册ID
        """
        gallery = self.db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery:
            gallery.view_count += 1
            self.db.commit()

    def increment_image_download_count(self, image_id: int):
        """
        增加图片下载次数

        Args:
            image_id: 图片ID
        """
        image = self.db.query(GalleryImage).filter(GalleryImage.id == image_id).first()
        if image:
            image.download_count += 1
            self.db.commit()
