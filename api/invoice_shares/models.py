import datetime
from enum import Enum
from decimal import Decimal
from uuid import UUID
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship
from api.core.models import BaseModel as DBBaseModel

if TYPE_CHECKING:
    from api.invoices.models import Invoice, InvoiceRead

class InvoiceShareStatus(str, Enum):
    PENDING = "PENDING"
    WATING_CONFIRMATION = "WATING_CONFIRMATION"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"

class InvoiceShare(DBBaseModel, table=True):
    __tablename__ = "invoice_shares"

    invoice_id: UUID = Field(foreign_key="invoices.id")
    debtor_id: UUID = Field(foreign_key="users.id")
    creditor_id: UUID = Field(foreign_key="users.id")
    amount: Decimal = Field(sa_type=Decimal(10, 2), gt=0)
    status: InvoiceShareStatus = Field(default=InvoiceShareStatus.PENDING) 

    invoice: "Invoice" = Relationship(back_populates="invoice_shares")



class InvoiceShareBase(BaseModel):
    debtor_id: UUID
    creditor_id: UUID
    amount: Decimal
    status: InvoiceShareStatus = InvoiceShareStatus.PENDING


class InvoiceShareCreate(InvoiceShareBase):
    pass


class InvoiceShareRead(InvoiceShareBase):
    id: UUID
    invoice_id: UUID
    invoice: "InvoiceRead"
    created_at: datetime.datetime
    updated_at: datetime.datetime

    