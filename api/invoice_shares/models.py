import datetime
from enum import Enum
from decimal import Decimal
from uuid import UUID
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship, Numeric
from api.core.models import BaseModel as DBBaseModel
from api.user.models import UserRead

if TYPE_CHECKING:
    from api.user.models import User
    from api.invoices.models import Invoice, InvoiceRead


class InvoiceShareStatus(str, Enum):
    PENDING = "PENDING"
    WATING_CONFIRMATION = "WATING_CONFIRMATION"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


class InvoiceShare(DBBaseModel, table=True):
    __tablename__ = "invoice_shares"

    invoice_id: UUID = Field(foreign_key="invoices.id", index=True)
    debtor_id: UUID = Field(foreign_key="users.id", index=True)
    creditor_id: UUID = Field(foreign_key="users.id", index=True)
    amount: Decimal = Field(sa_type=Numeric(precision=10, scale=2), gt=0)
    status: InvoiceShareStatus = Field(default=InvoiceShareStatus.PENDING, index=True)

    invoice: "Invoice" = Relationship(back_populates="invoice_shares")
    debtor: "User" = Relationship(
        back_populates="invoice_shares",
        sa_relationship_kwargs={
            "foreign_keys": "[InvoiceShare.debtor_id]",
            "primaryjoin": "InvoiceShare.debtor_id == User.id",
        },
    )
    creditor: "User" = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[InvoiceShare.creditor_id]",
            "primaryjoin": "InvoiceShare.creditor_id == User.id",
        }
    )


class InvoiceShareBase(BaseModel):
    debtor_id: UUID
    creditor_id: UUID
    amount: Decimal
    status: InvoiceShareStatus = InvoiceShareStatus.PENDING


class InvoiceShareCreate(InvoiceShareBase):
    pass


class InvoiceShareRead(InvoiceShareBase):
    model_config = {"from_attributes": True}
    
    id: UUID
    invoice_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime


class InvoiceShareWithDebtor(InvoiceShareRead):
    model_config = {"from_attributes": True}
    
    debtor: UserRead


class InvoiceShareDetailed(InvoiceShareRead):
    invoice: "InvoiceRead"
