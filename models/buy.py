from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import String, Column, Integer, Numeric, DateTime, Boolean, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship

from enums.language import Language
from models.base import Base


class Buy(Base):
    __tablename__ = 'buys'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    buyer = relationship('User', backref='buys')

    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(36, 12), nullable=False)

    buy_datetime = Column(DateTime, default=func.now())
    is_refunded = Column(Boolean, default=False)
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=True)

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('total_price > 0', name='check_total_price_positive'),
    )


class BuyDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    buyer_id: str | None = None
    quantity: int | None = None
    total_price: Decimal | None = None
    buy_datetime: datetime | None = None
    is_refunded: bool | None = None
    coupon_id: str | None = None

    model_config = {
        "from_attributes": True
    }


class RefundDTO(BaseModel):
    telegram_username: str | None = None
    telegram_id: int | None = None
    subcategory_name: str | None = None
    total_price: Decimal | None = None
    quantity: int | None = None
    buy_id: str | None = None
    language: Language
