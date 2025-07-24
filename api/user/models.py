import uuid
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field
from api.core.models import BaseModel as DBBaseModel


class User(DBBaseModel, table=True):
    __tablename__ = "users"

    telegram_user_id: int = Field(unique=True)
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None


class UserBase(BaseModel):
    telegram_user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None


class UserRead(UserBase):
    id: uuid.UUID


class UserCreate(UserBase):
    pass
