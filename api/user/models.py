

from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from api.utils.py_object_id import PyObjectId


class UserBase(BaseModel):
    telegram_user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None


# Database Model
class User(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "exclude_none": True,
    }

# API Models

class UserRead(UserBase):
    id: str

    @classmethod
    def from_db_model(cls, user: User) -> "UserRead":
        return cls(
            id=str(user.id),
            telegram_user_id=user.telegram_user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url
        )

class UserCreate(UserBase):
    pass