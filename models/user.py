from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import BigInteger, Column, Integer, DateTime, String, Boolean, Numeric, func, CheckConstraint, Enum

from enums.language import Language
from models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    telegram_username = Column(String(255), unique=True, index=True, nullable=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)

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
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    telegram_username: str | None = None
    telegram_id: int | None = None
    top_up_amount: Decimal | None = None
    consume_records: Decimal | None = None
    registered_at: datetime | None = None
    can_receive_messages: bool | None = None
    language: Language = Language.EN

    model_config = {
        "from_attributes": True
    }
