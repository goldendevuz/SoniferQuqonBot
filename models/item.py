from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, backref

from models.base import Base


# Item is a unique good which can only be sold once
class Item(Base):
    __tablename__ = 'items'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id", ondelete="CASCADE"), nullable=False)

    private_data = Column(String, nullable=False)
    price = Column(Numeric(36, 12), nullable=False)

    is_sold = Column(Boolean, nullable=False, default=False)
    is_new = Column(Boolean, nullable=False, default=True)
    description = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )


class ItemDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category_id: str | None = None
    category_name: str | None = None
    subcategory_id: str | None = None
    subcategory_name: str | None = None
    private_data: str | None = None
    price: Decimal | None = None
    is_sold: bool | None = None
    is_new: bool | None = None
    description: str | None = None

    model_config = {
        "from_attributes": True
    }
