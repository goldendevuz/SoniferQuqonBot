# cart is a container for unsold items to collect items from different (sub-)categories
# to be able to checkout this cart at once together with a shipment fee. Only the
# quantity, category, subcategory is stored because the unique item is not yet sold
#
# note that the item is NOT reserved or blocked so that the availability of the item
# needs to be checked again during checkout
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import String, Column, Integer, ForeignKey
from models.base import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class CartDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str | None = None

    model_config = {
        "from_attributes": True
    }
