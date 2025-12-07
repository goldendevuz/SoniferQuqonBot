from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import Column, Integer, DateTime, String, Boolean, Numeric, func, CheckConstraint, Enum

from enums.language import Language
from models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_username = Column(String, unique=True, index=True)
    telegram_id = Column(Integer, nullable=False, unique=True, index=True)

    top_up_amount = Column(Numeric(36, 12), default=0)
    consume_records = Column(Numeric(36, 12), default=0)

    registered_at = Column(DateTime, default=func.now())
    can_receive_messages = Column(Boolean, default=True)
    language = Column(Enum(Language), default=Language.EN)

    __table_args__ = (
        CheckConstraint('top_up_amount >= 0', name='check_top_up_amount_positive'),
        CheckConstraint('consume_records >= 0', name='check_consume_records_positive'),
    )


class UserDTO(BaseModel):
    id: int | None = None
    telegram_username: str | None = None
    telegram_id: int | None = None
    top_up_amount: Decimal | None = None
    consume_records: Decimal | None = None
    registered_at: datetime | None = None
    can_receive_messages: bool | None = None
    language: Language = Language.EN
