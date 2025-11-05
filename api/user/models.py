from typing_extensions import List
import uuid
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
from sqlmodel import Field, Relationship
from api.core.models import BaseModel as DBBaseModel


if TYPE_CHECKING:
    from api.invoices.models import Invoice
    from api.invoice_shares.models import InvoiceShare


class User(DBBaseModel, table=True):
    __tablename__ = "users"

    telegram_user_id: int = Field(unique=True)
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None

    invoices: List["Invoice"] = Relationship(back_populates="creator")
    invoice_shares: List["InvoiceShare"] = Relationship(
        back_populates="debtor",
        sa_relationship_kwargs={
            "foreign_keys": "[InvoiceShare.debtor_id]",
            "primaryjoin": "User.id == InvoiceShare.debtor_id"
        }
    )


class UserBase(BaseModel):
    telegram_user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None


class UserRead(UserBase):
    model_config = {"from_attributes": True}
    
    id: uuid.UUID


class UserCreate(UserBase):
    pass
