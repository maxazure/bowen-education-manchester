"""在线预约模块 - Booking & Appointment Module"""

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
    Time,
)
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class BookingService(BaseModel):
    """
    预约服务类型模型

    定义可预约的服务项目
    """

    __tablename__ = "booking_service"

    # 基本信息
    name = Column(String(200), nullable=False, comment="服务名称")
    slug = Column(String(200), nullable=False, comment="服务Slug")
    description = Column(Text, nullable=True, comment="服务描述")

    # 服务设置
    duration_minutes = Column(Integer, nullable=False, comment="服务时长(分钟)")
    price = Column(Float, nullable=True, comment="服务价格")
    buffer_time_minutes = Column(
        Integer, default=0, nullable=False, comment="缓冲时间(分钟,两次预约间隔)"
    )

    # 容量设置
    max_capacity = Column(
        Integer, default=1, nullable=False, comment="最大容量(同时服务人数)"
    )
    allow_waitlist = Column(
        Boolean, default=False, nullable=False, comment="是否允许候补名单"
    )

    # 预约限制
    min_advance_hours = Column(
        Integer, default=24, nullable=False, comment="最少提前预约小时数"
    )
    max_advance_days = Column(
        Integer, default=30, nullable=False, comment="最多提前预约天数"
    )
    allow_cancel_hours = Column(
        Integer, default=24, nullable=False, comment="允许取消的最少提前小时数"
    )

    # 工作时间
    working_days = Column(
        String(100), nullable=True, comment="工作日(如:1,2,3,4,5表示周一到周五)"
    )
    working_start_time = Column(Time, nullable=True, comment="工作开始时间")
    working_end_time = Column(Time, nullable=True, comment="工作结束时间")

    # 显示控制
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")

    # 其他
    notes = Column(Text, nullable=True, comment="备注")

    def __repr__(self):
        return f"<BookingService {self.name}>"


class Booking(BaseModel):
    """
    预约记录模型

    管理客户预约记录
    """

    __tablename__ = "booking"

    # 关联信息
    user_id = Column(
        Integer, ForeignKey("user.id"), nullable=True, comment="关联用户ID(可选)"
    )
    service_id = Column(
        Integer, ForeignKey("booking_service.id"), nullable=False, comment="预约服务ID"
    )
    staff_id = Column(
        Integer, ForeignKey("team_member.id"), nullable=True, comment="指定服务人员ID"
    )

    # 预约编号
    booking_number = Column(
        String(50), unique=True, nullable=False, comment="预约编号(唯一标识)"
    )

    # 预约时间
    booking_date = Column(DateTime, nullable=False, comment="预约日期时间")
    duration_minutes = Column(Integer, nullable=False, comment="预约时长(分钟)")
    end_datetime = Column(DateTime, nullable=True, comment="预约结束时间")

    # 客户信息
    customer_name = Column(String(100), nullable=False, comment="客户姓名")
    customer_email = Column(String(100), nullable=False, comment="客户邮箱")
    customer_phone = Column(String(50), nullable=False, comment="客户电话")

    # 预约状态
    status = Column(
        Enum(
            "pending",
            "confirmed",
            "cancelled",
            "completed",
            "no_show",
            "waitlist",
            name="booking_status",
        ),
        default="pending",
        nullable=False,
        comment="预约状态",
    )
    confirmation_method = Column(
        Enum("auto", "manual", name="confirmation_method"),
        default="auto",
        nullable=False,
        comment="确认方式",
    )

    # 支付信息
    price = Column(Float, nullable=True, comment="预约价格")
    payment_status = Column(
        Enum("unpaid", "paid", "refunded", name="booking_payment_status"),
        default="unpaid",
        nullable=False,
        comment="支付状态",
    )
    payment_method = Column(String(50), nullable=True, comment="支付方式")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")

    # 时间节点
    confirmed_at = Column(DateTime, nullable=True, comment="确认时间")
    cancelled_at = Column(DateTime, nullable=True, comment="取消时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")

    # 提醒记录
    reminder_sent_at = Column(DateTime, nullable=True, comment="提醒发送时间")
    reminder_count = Column(Integer, default=0, nullable=False, comment="已发送提醒次数")

    # 其他
    customer_notes = Column(Text, nullable=True, comment="客户备注")
    admin_notes = Column(Text, nullable=True, comment="管理员备注")
    cancel_reason = Column(Text, nullable=True, comment="取消原因")
    source = Column(
        String(50), nullable=True, comment="预约来源(web/phone/app等)"
    )

    # 关系
    user = relationship("User", backref="bookings")
    service = relationship("BookingService", backref="bookings")
    staff = relationship("TeamMember", backref="bookings")

    def __repr__(self):
        return f"<Booking {self.booking_number} ({self.status})>"


class BookingTimeSlot(BaseModel):
    """
    预约时间槽模型

    管理可预约的时间段,包括特殊时段设置
    """

    __tablename__ = "booking_time_slot"

    # 关联信息
    service_id = Column(
        Integer, ForeignKey("booking_service.id"), nullable=False, comment="服务ID"
    )
    staff_id = Column(
        Integer, ForeignKey("team_member.id"), nullable=True, comment="服务人员ID"
    )

    # 时间设置
    date = Column(DateTime, nullable=False, comment="日期")
    start_time = Column(Time, nullable=False, comment="开始时间")
    end_time = Column(Time, nullable=False, comment="结束时间")

    # 可用性
    is_available = Column(
        Boolean, default=True, nullable=False, comment="是否可预约"
    )
    available_slots = Column(
        Integer, default=1, nullable=False, comment="可用名额"
    )
    booked_slots = Column(Integer, default=0, nullable=False, comment="已预约名额")

    # 特殊设置
    is_special = Column(
        Boolean, default=False, nullable=False, comment="是否为特殊时段"
    )
    special_price = Column(Float, nullable=True, comment="特殊价格")

    # 其他
    notes = Column(Text, nullable=True, comment="备注")

    # 关系
    service = relationship("BookingService")
    staff = relationship("TeamMember")

    def __repr__(self):
        return f"<BookingTimeSlot {self.date} {self.start_time}-{self.end_time}>"
