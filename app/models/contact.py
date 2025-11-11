"""留言/询价模型"""

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ContactMessage(BaseModel):
    """
    留言/询价模型

    访客通过前台表单提交的留言和询价信息
    """

    __tablename__ = "contact_message"

    name = Column(String(100), nullable=False, comment="访客姓名")
    contact_info = Column(String(200), nullable=False, comment="联系方式")
    message_text = Column(Text, nullable=False, comment="留言内容")
    product_id = Column(
        Integer, ForeignKey("product.id"), nullable=True, comment="关联产品ID"
    )
    source_page_url = Column(String(500), nullable=True, comment="来源页面URL")
    status = Column(
        Enum("unread", "handled", name="contact_message_status"),
        default="unread",
        nullable=False,
        comment="处理状态",
    )
    handled_at = Column(DateTime, nullable=True, comment="处理时间")

    # 关系
    product = relationship("Product", backref="inquiries")
