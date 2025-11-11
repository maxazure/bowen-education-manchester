# -*- coding: utf-8 -*-
"""
Pydantic schemas for all modules
Used for request validation and response serialization
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ==================== Team Module ====================
class TeamMemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    qualifications: Optional[str] = None
    specialties: Optional[str] = Field(None, max_length=500)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    linkedin: Optional[str] = Field(None, max_length=255)
    twitter: Optional[str] = Field(None, max_length=255)
    sort_order: int = 0
    is_featured: bool = False
    is_active: bool = True
    photo_media_id: Optional[int] = None


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    qualifications: Optional[str] = None
    specialties: Optional[str] = Field(None, max_length=500)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    linkedin: Optional[str] = Field(None, max_length=255)
    twitter: Optional[str] = Field(None, max_length=255)
    sort_order: Optional[int] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    photo_media_id: Optional[int] = None


class TeamMemberResponse(TeamMemberBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Portfolio Module ====================
class PortfolioBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=300)
    summary: Optional[str] = None
    background: Optional[str] = None
    challenge: Optional[str] = None
    solution: Optional[str] = None
    result: Optional[str] = None
    content_html: Optional[str] = None
    client_name: Optional[str] = Field(None, max_length=200)
    is_client_anonymous: bool = False
    project_date: Optional[date] = None
    project_duration: Optional[str] = Field(None, max_length=100)
    project_url: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=500)
    is_featured: bool = False
    sort_order: int = 0
    status: str = "draft"
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = None
    cover_media_id: Optional[int] = None
    client_logo_media_id: Optional[int] = None


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=300)
    summary: Optional[str] = None
    background: Optional[str] = None
    challenge: Optional[str] = None
    solution: Optional[str] = None
    result: Optional[str] = None
    content_html: Optional[str] = None
    client_name: Optional[str] = Field(None, max_length=200)
    is_client_anonymous: Optional[bool] = None
    project_date: Optional[date] = None
    project_duration: Optional[str] = Field(None, max_length=100)
    project_url: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=500)
    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = None
    cover_media_id: Optional[int] = None
    client_logo_media_id: Optional[int] = None


class PortfolioResponse(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== FAQ Module ====================
class FAQBase(BaseModel):
    category: Optional[str] = Field(None, max_length=100)
    question: str = Field(..., min_length=1, max_length=500)
    answer: str = Field(..., min_length=1)
    sort_order: int = 0
    is_visible: bool = True
    is_pinned: bool = False


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    category: Optional[str] = Field(None, max_length=100)
    question: Optional[str] = Field(None, min_length=1, max_length=500)
    answer: Optional[str] = Field(None, min_length=1)
    sort_order: Optional[int] = None
    is_visible: Optional[bool] = None
    is_pinned: Optional[bool] = None


class FAQResponse(FAQBase):
    id: int
    view_count: int
    helpful_count: int
    unhelpful_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Comment Module ====================
class CommentBase(BaseModel):
    commentable_type: str = Field(..., max_length=50)
    commentable_id: int
    author_name: str = Field(..., min_length=1, max_length=100)
    author_email: EmailStr
    author_website: Optional[str] = Field(None, max_length=255)
    content: str = Field(..., min_length=1)
    rating: Optional[int] = Field(None, ge=1, le=5)
    parent_id: Optional[int] = None
    user_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    rating: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
    is_featured: Optional[bool] = None
    admin_reply: Optional[str] = None


class CommentResponse(CommentBase):
    id: int
    status: str
    is_featured: bool
    admin_reply: Optional[str]
    replied_at: Optional[datetime]
    helpful_count: int
    report_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    reviewable_type: str = Field(..., max_length=50)
    reviewable_id: int
    reviewer_name: str = Field(..., min_length=1, max_length=100)
    reviewer_email: EmailStr
    title: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=1)
    overall_rating: int = Field(..., ge=1, le=5)
    quality_rating: Optional[int] = Field(None, ge=1, le=5)
    service_rating: Optional[int] = Field(None, ge=1, le=5)
    value_rating: Optional[int] = Field(None, ge=1, le=5)
    user_id: Optional[int] = None
    order_id: Optional[int] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    overall_rating: Optional[int] = Field(None, ge=1, le=5)
    quality_rating: Optional[int] = Field(None, ge=1, le=5)
    service_rating: Optional[int] = Field(None, ge=1, le=5)
    value_rating: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
    is_featured: Optional[bool] = None


class ReviewResponse(ReviewBase):
    id: int
    is_verified_purchase: bool
    status: str
    is_featured: bool
    helpful_count: int
    unhelpful_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== User Module ====================
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=50)


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    display_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    marketing_emails: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    membership_level: str
    points: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Newsletter Module ====================
class NewsletterSubscribeRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    subscription_source: Optional[str] = Field(None, max_length=100)
    group_tags: Optional[str] = Field(None, max_length=255)


class NewsletterSubscriberResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    status: str
    is_verified: bool
    subscribed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Cart Module ====================
class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)
    product_variant: Optional[str] = Field(None, max_length=255)
    product_sku: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    discount_amount: float
    total_price: float
    product_variant: Optional[str]
    product_sku: Optional[str]
    notes: Optional[str]
    added_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    id: int
    user_id: Optional[int]
    session_id: Optional[str]
    is_active: int
    subtotal: float
    estimated_tax: float
    estimated_shipping: float
    estimated_total: float
    coupon_code: Optional[str]
    discount_amount: float
    items: List[CartItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Order Module ====================
class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str = Field(..., max_length=200)
    product_sku: Optional[str] = Field(None, max_length=100)
    product_variant: Optional[str] = Field(None, max_length=255)
    quantity: int = Field(1, ge=1)
    unit_price: float
    subtotal: float
    discount_amount: float = 0.0
    total_price: float


class OrderCreate(BaseModel):
    order_number: str = Field(..., max_length=50)
    customer_email: EmailStr
    customer_phone: Optional[str] = Field(None, max_length=50)
    customer_name: str = Field(..., max_length=100)
    shipping_address_line1: str = Field(..., max_length=255)
    shipping_address_line2: Optional[str] = Field(None, max_length=255)
    shipping_city: str = Field(..., max_length=100)
    shipping_state: Optional[str] = Field(None, max_length=100)
    shipping_postal_code: str = Field(..., max_length=20)
    shipping_country: str = Field("New Zealand", max_length=100)
    subtotal: float
    shipping_fee: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    total_amount: float
    shipping_method: str = "standard"
    customer_notes: Optional[str] = None
    user_id: Optional[int] = None
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    shipping_carrier: Optional[str] = Field(None, max_length=100)
    tracking_number: Optional[str] = Field(None, max_length=100)
    tracking_url: Optional[str] = Field(None, max_length=255)
    admin_notes: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: Optional[int]
    status: str
    payment_status: str
    customer_email: str
    customer_phone: Optional[str]
    customer_name: str
    subtotal: float
    shipping_fee: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    paid_amount: float
    shipping_method: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Booking Module ====================
class BookingCreate(BaseModel):
    booking_number: str = Field(..., max_length=50)
    service_id: int
    booking_date: datetime
    duration_minutes: int
    customer_name: str = Field(..., max_length=100)
    customer_email: EmailStr
    customer_phone: str = Field(..., max_length=50)
    customer_notes: Optional[str] = None
    user_id: Optional[int] = None
    staff_id: Optional[int] = None
    price: Optional[float] = None


class BookingUpdate(BaseModel):
    booking_date: Optional[datetime] = None
    status: Optional[str] = None
    customer_notes: Optional[str] = None
    admin_notes: Optional[str] = None
    cancel_reason: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    booking_number: str
    service_id: int
    user_id: Optional[int]
    staff_id: Optional[int]
    booking_date: datetime
    duration_minutes: int
    customer_name: str
    customer_email: str
    customer_phone: str
    status: str
    price: Optional[float]
    payment_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Restaurant Module ====================
class MenuItemCreate(BaseModel):
    category_id: int
    name: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    is_available: bool = True
    sort_order: int = 0


class RestaurantOrderItemCreate(BaseModel):
    menu_item_id: int
    item_name: str = Field(..., max_length=200)
    quantity: int = Field(1, ge=1)
    unit_price: float
    subtotal: float
    customizations: Optional[str] = None
    special_instructions: Optional[str] = None


class RestaurantOrderCreate(BaseModel):
    order_number: str = Field(..., max_length=50)
    order_type: str
    customer_name: str = Field(..., max_length=100)
    customer_phone: str = Field(..., max_length=50)
    customer_email: Optional[EmailStr] = None
    subtotal: float
    delivery_fee: float = 0.0
    service_fee: float = 0.0
    tax_amount: float = 0.0
    total_amount: float
    customer_notes: Optional[str] = None
    user_id: Optional[int] = None
    items: List[RestaurantOrderItemCreate]


class RestaurantOrderResponse(BaseModel):
    id: int
    order_number: str
    order_type: str
    status: str
    payment_status: str
    customer_name: str
    customer_phone: str
    subtotal: float
    total_amount: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Event Module ====================
class EventCreate(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    description: str
    summary: Optional[str] = None
    event_type: str = "other"
    start_datetime: datetime
    end_datetime: datetime
    location_type: str = "physical"
    venue_name: Optional[str] = Field(None, max_length=200)
    venue_address: Optional[str] = Field(None, max_length=500)
    max_attendees: Optional[int] = None
    is_free: bool = True
    ticket_price: Optional[float] = None
    status: str = "draft"


class EventRegistrationCreate(BaseModel):
    registration_number: str = Field(..., max_length=50)
    event_id: int
    attendee_name: str = Field(..., max_length=100)
    attendee_email: EmailStr
    attendee_phone: Optional[str] = Field(None, max_length=50)
    company: Optional[str] = Field(None, max_length=200)
    job_title: Optional[str] = Field(None, max_length=100)
    ticket_type: str = "regular"
    ticket_price: float = 0.0
    user_id: Optional[int] = None


class EventResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    event_type: str
    start_datetime: datetime
    end_datetime: datetime
    location_type: str
    max_attendees: Optional[int]
    current_attendees: int
    is_free: bool
    ticket_price: Optional[float]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Gallery Module ====================
class GalleryCreate(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = Field(None, max_length=255)
    display_mode: str = "grid"
    is_featured: bool = False
    is_public: bool = True
    sort_order: int = 0


class GalleryImageCreate(BaseModel):
    gallery_id: int
    media_id: int
    title: Optional[str] = Field(None, max_length=200)
    caption: Optional[str] = None
    alt_text: Optional[str] = Field(None, max_length=255)
    tags: Optional[str] = Field(None, max_length=255)
    sort_order: int = 0
    is_visible: bool = True


class GalleryResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    category: Optional[str]
    display_mode: str
    is_featured: bool
    is_public: bool
    view_count: int
    image_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Video Module ====================
class VideoCreate(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    video_source: str = "upload"
    youtube_id: Optional[str] = Field(None, max_length=100)
    vimeo_id: Optional[str] = Field(None, max_length=100)
    external_url: Optional[str] = Field(None, max_length=500)
    duration_seconds: Optional[int] = None
    is_featured: bool = False
    is_public: bool = True
    status: str = "draft"
    sort_order: int = 0


class VideoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: Optional[bool] = None
    is_public: Optional[bool] = None
    status: Optional[str] = None
    sort_order: Optional[int] = None


class VideoResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    video_source: str
    duration_seconds: Optional[int]
    is_featured: bool
    is_public: bool
    status: str
    view_count: int
    like_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== File Download Module ====================
class FileDownloadCreate(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    file_media_id: int
    file_name: str = Field(..., max_length=255)
    file_extension: Optional[str] = Field(None, max_length=20)
    file_size_kb: Optional[int] = None
    file_type: str = "other"
    version: Optional[str] = Field(None, max_length=50)
    is_latest: bool = True
    access_level: str = "public"
    requires_login: bool = False
    is_featured: bool = False
    is_active: bool = True
    status: str = "draft"
    sort_order: int = 0


class FileDownloadUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    access_level: Optional[str] = None
    requires_login: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None
    sort_order: Optional[int] = None


class FileDownloadResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    file_name: str
    file_extension: Optional[str]
    file_size_kb: Optional[int]
    file_type: str
    version: Optional[str]
    is_latest: bool
    access_level: str
    requires_login: bool
    is_featured: bool
    is_active: bool
    status: str
    download_count: int
    view_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Post Module ====================
class PostCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    column_id: int
    sort_order: int = 0
    is_visible: bool = True


class PostCategoryCreate(PostCategoryBase):
    pass


class PostCategoryResponse(PostCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    summary: Optional[str] = None
    content_html: str
    column_id: int
    cover_media_id: Optional[int] = None
    is_recommended: bool = False
    is_approved: bool = True
    status: str = "draft"
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = None
    published_at: Optional[datetime] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    summary: Optional[str] = None
    content_html: Optional[str] = None
    column_id: Optional[int] = None
    cover_media_id: Optional[int] = None
    is_recommended: Optional[bool] = None
    is_approved: Optional[bool] = None
    status: Optional[str] = None
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = None
    published_at: Optional[datetime] = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Product Module ====================
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    summary: Optional[str] = None
    description_html: str
    column_id: int
    cover_media_id: Optional[int] = None
    price_text: Optional[str] = Field(None, max_length=100)
    availability_status: str = "in_stock"
    is_recommended: bool = False
    status: str = "draft"
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = None
    published_at: Optional[datetime] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    summary: Optional[str] = None
    description_html: Optional[str] = None
    column_id: Optional[int] = None
    cover_media_id: Optional[int] = None
    price_text: Optional[str] = Field(None, max_length=100)
    availability_status: Optional[str] = None
    is_recommended: Optional[bool] = None
    status: Optional[str] = None
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = None
    published_at: Optional[datetime] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
