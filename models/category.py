from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import String, Integer, Column, String

from models.base import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True, index=True)
    media_id = Column(String, nullable=False)


class CategoryDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str | None = None
    media_id: str | None = None

    model_config = {
        "from_attributes": True
    }
