from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import String, Column, Integer, ForeignKey, CheckConstraint

from models.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )


class CartItemDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cart_id: str | None = None
    category_id: str | None = None
    subcategory_id: str | None = None
    quantity: int | None = None

    model_config = {
        "from_attributes": True
    }
