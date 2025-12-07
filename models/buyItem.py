from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.base import Base


class BuyItem(Base):
    __tablename__ = "buyItem"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    buy_id = Column(Integer, ForeignKey("buys.id", ondelete="CASCADE"), nullable=False)
    buy = relationship("Buy", backref=backref("buys", cascade="all"), passive_deletes="all")
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    item = relationship("Item", backref=backref("items", cascade="all"), passive_deletes="all")


class BuyItemDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    buy_id: str | None = None
    item_id: str | None = None

    model_config = {
        "from_attributes": True
    }
