import uuid
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Enum

from enums.keyboard_button import KeyboardButton
from models.base import Base


class ButtonMedia(Base):
    __tablename__ = "buttons_media"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    media_id = Column(String, nullable=False)
    button = Column(Enum(KeyboardButton), unique=True)


class ButtonMediaDTO(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    media_id: str | None = None
    button: KeyboardButton | None = None
