import datetime
import uuid
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now, nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.datetime.now},
    )
