"""Hero幻灯片模型"""

from sqlalchemy import Boolean, Column, Integer, String, Text

from app.models.base import BaseModel


class HeroSlide(BaseModel):
    """Hero幻灯片模型"""

    __tablename__ = "hero_slides"

    # 基本信息
    title = Column(String(200), nullable=False, comment="标题")
    title_en = Column(String(200), comment="英文标题")
    subtitle = Column(String(300), comment="副标题")
    subtitle_en = Column(String(300), comment="英文副标题")
    description = Column(Text, comment="描述")
    description_en = Column(Text, comment="英文描述")

    # 图片和徽章
    background_image = Column(
        String(500), nullable=False, comment="背景图片路径"
    )
    badge_text = Column(String(100), comment="徽章文字")
    badge_text_en = Column(String(100), comment="英文徽章文字")

    # 按钮配置
    button_text = Column(String(100), comment="按钮文字")
    button_text_en = Column(String(100), comment="英文按钮文字")
    button_url = Column(String(500), comment="按钮链接")
    button_style = Column(
        String(50), default="btn-primary", comment="按钮样式"
    )

    # 第二个按钮（可选）
    button2_text = Column(String(100), comment="第二个按钮文字")
    button2_text_en = Column(String(100), comment="第二个按钮英文文字")
    button2_url = Column(String(500), comment="第二个按钮链接")
    button2_style = Column(
        String(50), default="btn-outline-light", comment="第二个按钮样式"
    )

    # 排序和状态
    sort_order = Column(Integer, default=0, comment="排序顺序（数字越小越靠前）")
    is_active = Column(Boolean, default=True, comment="是否启用")

    def __repr__(self):
        return f"<HeroSlide {self.id}: {self.title}>"
