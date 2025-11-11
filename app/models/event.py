"""活动报名模块 - Event Registration Module"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import BaseModel


class Event(BaseModel):
    """
    活动模型

    用于发布活动、会议、培训、研讨会等
    """

    __tablename__ = "event"

    # 基本信息
    title = Column(String(200), nullable=False, comment="活动标题")
    slug = Column(String(200), nullable=False, comment="活动Slug")
    description = Column(Text, nullable=False, comment="活动描述")
    summary = Column(Text, nullable=True, comment="活动简介")

    # 活动类型
    event_type = Column(
        Enum(
            "conference",
            "workshop",
            "seminar",
            "training",
            "webinar",
            "social",
            "other",
            name="event_type",
        ),
        default="other",
        nullable=False,
        comment="活动类型",
    )

    # 时间信息
    start_datetime = Column(DateTime, nullable=False, comment="开始时间")
    end_datetime = Column(DateTime, nullable=False, comment="结束时间")
    timezone = Column(
        String(50), nullable=True, default="Pacific/Auckland", comment="时区"
    )
    registration_deadline = Column(DateTime, nullable=True, comment="报名截止时间")

    # 地点信息
    location_type = Column(
        Enum("physical", "online", "hybrid", name="event_location_type"),
        default="physical",
        nullable=False,
        comment="活动形式",
    )
    venue_name = Column(String(200), nullable=True, comment="场地名称")
    venue_address = Column(String(500), nullable=True, comment="场地地址")
    venue_city = Column(String(100), nullable=True, comment="城市")
    venue_postal_code = Column(String(20), nullable=True, comment="邮编")
    online_meeting_url = Column(String(500), nullable=True, comment="在线会议链接")
    online_meeting_password = Column(String(100), nullable=True, comment="会议密码")

    # 容量管理
    max_attendees = Column(Integer, nullable=True, comment="最大参会人数")
    current_attendees = Column(Integer, default=0, nullable=False, comment="当前报名人数")
    allow_waitlist = Column(
        Boolean, default=False, nullable=False, comment="是否允许候补"
    )
    waitlist_count = Column(Integer, default=0, nullable=False, comment="候补人数")

    # 票务信息
    is_free = Column(Boolean, default=True, nullable=False, comment="是否免费")
    ticket_price = Column(Float, nullable=True, comment="票价")
    early_bird_price = Column(Float, nullable=True, comment="早鸟价")
    early_bird_deadline = Column(DateTime, nullable=True, comment="早鸟截止时间")

    # 图片
    cover_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="封面图ID"
    )

    # 活动状态
    status = Column(
        Enum("draft", "published", "cancelled", "completed", name="event_status"),
        default="draft",
        nullable=False,
        comment="活动状态",
    )
    is_featured = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    is_public = Column(
        Boolean, default=True, nullable=False, comment="是否公开(私人活动需邀请)"
    )

    # 主办方信息
    organizer_name = Column(String(200), nullable=True, comment="主办方名称")
    organizer_email = Column(String(100), nullable=True, comment="主办方邮箱")
    organizer_phone = Column(String(50), nullable=True, comment="主办方电话")
    contact_person = Column(String(100), nullable=True, comment="联系人")

    # 议程与资料
    agenda = Column(Text, nullable=True, comment="活动议程(JSON或HTML格式)")
    speakers = Column(Text, nullable=True, comment="演讲嘉宾(JSON格式)")
    materials_url = Column(String(500), nullable=True, comment="活动资料链接")

    # SEO
    seo_title = Column(String(200), nullable=True, comment="SEO标题")
    seo_description = Column(Text, nullable=True, comment="SEO描述")

    # 其他
    tags = Column(String(255), nullable=True, comment="标签(逗号分隔)")
    notes = Column(Text, nullable=True, comment="内部备注")

    # 关系
    cover_media = relationship("MediaFile", foreign_keys=[cover_media_id])
    registrations = relationship(
        "EventRegistration", back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Event {self.title}>"


class EventRegistration(BaseModel):
    """
    活动报名记录模型

    管理参会者报名信息
    """

    __tablename__ = "event_registration"

    # 关联信息
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False, comment="活动ID")
    user_id = Column(
        Integer, ForeignKey("user.id"), nullable=True, comment="关联用户ID(可选)"
    )

    # 报名编号
    registration_number = Column(
        String(50), unique=True, nullable=False, comment="报名编号(唯一标识)"
    )

    # 参会者信息
    attendee_name = Column(String(100), nullable=False, comment="参会者姓名")
    attendee_email = Column(String(100), nullable=False, comment="参会者邮箱")
    attendee_phone = Column(String(50), nullable=True, comment="参会者电话")
    company = Column(String(200), nullable=True, comment="所属公司/机构")
    job_title = Column(String(100), nullable=True, comment="职位")

    # 报名状态
    status = Column(
        Enum(
            "pending",
            "confirmed",
            "waitlist",
            "cancelled",
            "attended",
            "no_show",
            name="registration_status",
        ),
        default="pending",
        nullable=False,
        comment="报名状态",
    )

    # 票务类型
    ticket_type = Column(
        Enum("regular", "early_bird", "vip", "free", name="ticket_type"),
        default="regular",
        nullable=False,
        comment="票务类型",
    )

    # 支付信息
    ticket_price = Column(Float, default=0.0, nullable=False, comment="票价")
    payment_status = Column(
        Enum("unpaid", "paid", "refunded", name="event_payment_status"),
        default="unpaid",
        nullable=False,
        comment="支付状态",
    )
    payment_method = Column(String(50), nullable=True, comment="支付方式")
    payment_transaction_id = Column(String(100), nullable=True, comment="支付交易ID")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")

    # 时间节点
    registered_at = Column(DateTime, nullable=True, comment="报名时间")
    confirmed_at = Column(DateTime, nullable=True, comment="确认时间")
    checked_in_at = Column(DateTime, nullable=True, comment="签到时间")
    cancelled_at = Column(DateTime, nullable=True, comment="取消时间")

    # 签到信息
    check_in_code = Column(String(100), nullable=True, comment="签到码(二维码)")
    is_checked_in = Column(Boolean, default=False, nullable=False, comment="是否已签到")
    check_in_method = Column(
        String(50), nullable=True, comment="签到方式(qr_code/manual等)"
    )

    # 额外信息
    dietary_requirements = Column(Text, nullable=True, comment="饮食要求")
    special_needs = Column(Text, nullable=True, comment="特殊需求")
    how_heard = Column(String(100), nullable=True, comment="如何得知活动")
    custom_fields = Column(Text, nullable=True, comment="自定义字段(JSON格式)")

    # 其他
    notes = Column(Text, nullable=True, comment="备注")
    admin_notes = Column(Text, nullable=True, comment="管理员备注")
    cancel_reason = Column(Text, nullable=True, comment="取消原因")

    # 通知记录
    confirmation_email_sent = Column(
        Boolean, default=False, nullable=False, comment="是否已发送确认邮件"
    )
    reminder_email_sent = Column(
        Boolean, default=False, nullable=False, comment="是否已发送提醒邮件"
    )

    # 关系
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", backref="event_registrations")

    def __repr__(self):
        return f"<EventRegistration {self.registration_number} for {self.attendee_name}>"


class EventTicketType(BaseModel):
    """
    活动票务类型模型

    管理活动的不同票务类型(可选,用于复杂票务管理)
    """

    __tablename__ = "event_ticket_type"

    # 关联信息
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False, comment="活动ID")

    # 票务信息
    name = Column(String(100), nullable=False, comment="票务名称")
    description = Column(Text, nullable=True, comment="票务描述")
    price = Column(Float, nullable=False, comment="价格")

    # 库存管理
    quantity = Column(Integer, nullable=True, comment="数量(null表示不限)")
    sold_count = Column(Integer, default=0, nullable=False, comment="已售数量")

    # 销售时间
    sale_start_time = Column(DateTime, nullable=True, comment="开售时间")
    sale_end_time = Column(DateTime, nullable=True, comment="停售时间")

    # 显示控制
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")

    # 其他
    notes = Column(Text, nullable=True, comment="备注")

    # 关系
    event = relationship("Event", backref="ticket_types")

    def __repr__(self):
        return f"<EventTicketType {self.name} - ${self.price}>"
