"""产品自定义字段模型"""

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class CustomFieldDef(BaseModel):
    """
    自定义字段定义模型

    定义产品可以有哪些额外的属性字段
    """

    __tablename__ = "custom_field_def"

    module_type = Column(
        Enum("PRODUCT", "POST", "CUSTOM", name="custom_field_module_type"),
        default="PRODUCT",
        nullable=False,
        comment="模块类型",
    )
    column_id = Column(
        Integer,
        ForeignKey("site_column.id"),
        nullable=True,
        comment="关联栏目ID（NULL表示全局）",
    )
    field_key = Column(String(100), nullable=False, comment="字段键名")
    label = Column(String(100), nullable=False, comment="字段显示名")
    input_type = Column(
        Enum(
            "text",
            "textarea",
            "number",
            "select",
            "multiselect",
            "radio",
            "boolean",
            "image",
            "color",
            "date",
            "price",
            name="custom_field_input_type",
        ),
        nullable=False,
        comment="输入类型",
    )
    required = Column(Boolean, default=False, nullable=False, comment="是否必填")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    min_value = Column(Float, nullable=True, comment="数字下限")
    max_value = Column(Float, nullable=True, comment="数字上限")

    # 关系
    column = relationship("SiteColumn", backref="custom_field_defs")
    options = relationship(
        "CustomFieldOption", back_populates="field", cascade="all, delete-orphan"
    )


class CustomFieldOption(BaseModel):
    """
    自定义字段选项模型

    为下拉框、单选、多选等字段提供可选项
    """

    __tablename__ = "custom_field_option"

    field_id = Column(
        Integer, ForeignKey("custom_field_def.id"), nullable=False, comment="关联字段ID"
    )
    value = Column(String(100), nullable=False, comment="内部存储值")
    label = Column(String(100), nullable=False, comment="显示标签")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否有效")

    # 关系
    field = relationship("CustomFieldDef", back_populates="options")


class ProductCustomFieldValue(BaseModel):
    """
    产品自定义字段值模型

    存储产品在具体自定义字段上的取值
    """

    __tablename__ = "product_custom_field_value"

    product_id = Column(
        Integer, ForeignKey("product.id"), nullable=False, comment="产品ID"
    )
    field_id = Column(
        Integer, ForeignKey("custom_field_def.id"), nullable=False, comment="字段ID"
    )
    value_text = Column(Text, nullable=False, comment="字段值")

    # 关系
    product = relationship("Product", backref="custom_field_values")
    field = relationship("CustomFieldDef")
