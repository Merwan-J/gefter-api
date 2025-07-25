import datetime
from enum import Enum
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, Relationship
from api.core.models import BaseModel as DBBaseModel
from api.invoice_shares.models import InvoiceShare, InvoiceShareCreate, InvoiceShareRead


class InvoiceType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    GROUP = "GROUP"


class InvoiceStatus(str, Enum):
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    SETTLED = "SETTLED"


class Invoice(DBBaseModel, table=True):
    __tablename__ = "invoices"

    creator_id: UUID
    amount: Decimal = Field(sa_type=Decimal(10, 2), gt=0)
    title: str = Field(max_length=30)
    description: Optional[str] = Field(max_length=255)
    type: InvoiceType
    status: InvoiceStatus = Field(default=InvoiceStatus.PENDING)

    invoice_shares: List[InvoiceShare] = Relationship(back_populates="invoice")


class InvoiceBase(BaseModel):
    creator_id: UUID
    amount: Decimal
    title: str
    description: Optional[str] = None
    type: InvoiceType
    status: InvoiceStatus = InvoiceStatus.PENDING


class InvoiceCreate(InvoiceBase):
    invoice_shares: List[InvoiceShareCreate] = Field(min_items=1)


class InvoiceRead(InvoiceBase):
    id: UUID
    invoice_shares: List[InvoiceShareRead] = Field(min_items=1)
    created_at: datetime.datetime
    updated_at: datetime.datetime
