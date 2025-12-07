from datetime import datetime, timezone, timedelta
from decimal import Decimal
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import BigInteger, Column, DateTime, Enum, Boolean, String, Integer, Numeric

from enums.coupon_type import CouponType
from models.base import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(12), unique=True, nullable=False, index=True)
    type = Column(Enum(CouponType), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    create_datetime = Column(DateTime(timezone=True), nullable=False)
    expire_datetime = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    usage_limit = Column(Integer, default=1)
    usage_count = Column(Integer, default=0)


class CouponDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str | None = None
    type: CouponType | None = None
    value: Decimal | None = None
    create_datetime: datetime = datetime.now(tz=timezone.utc)
    expire_datetime: datetime = datetime.now(tz=timezone.utc) + timedelta(days=30)
    is_active: bool = True
    usage_limit: int = 1
    usage_count: int = 0

    model_config = {
        "from_attributes": True
    }
