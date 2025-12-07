from datetime import datetime
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import String, Integer, Column, ForeignKey, BigInteger, DateTime, func, CheckConstraint, Enum

from enums.cryptocurrency import Cryptocurrency
from models.base import Base


class Deposit(Base):
    __tablename__ = 'deposits'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    network = Column(Enum(Cryptocurrency), nullable=False)
    amount = Column(BigInteger, nullable=False)
    deposit_datetime = Column(DateTime, default=func.now())

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )


class DepositDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str | None = None
    network: Cryptocurrency | None = None
    amount: int | None = None
    deposit_datetime: datetime | None = None

    model_config = {
        "from_attributes": True
    }
