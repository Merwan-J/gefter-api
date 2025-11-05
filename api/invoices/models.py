import datetime
from enum import Enum
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, Relationship, Numeric
from api.core.models import BaseModel as DBBaseModel
from api.invoice_shares.models import (
    InvoiceShare,
    InvoiceShareCreate,
    InvoiceShareRead,
    InvoiceShareWithDebtor,
)
from api.user.models import User, UserRead


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

    creator_id: UUID = Field(foreign_key="users.id", index=True)
    amount: Decimal = Field(sa_type=Numeric(precision=10, scale=2), gt=0)
    title: str = Field(max_length=30)
    description: Optional[str] = Field(max_length=255)
    type: InvoiceType
    status: InvoiceStatus = Field(default=InvoiceStatus.PENDING, index=True)

    invoice_shares: List[InvoiceShare] = Relationship(back_populates="invoice")
    creator: "User" = Relationship(back_populates="invoices")


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
    model_config = {"from_attributes": True}
    
    id: UUID
    invoice_shares: List[InvoiceShareRead] = Field(min_items=1)
    created_at: datetime.datetime
    updated_at: datetime.datetime


class InvoiceActivityRead(BaseModel):
    id: UUID
    creditor_id: UUID
    amount: Decimal
    title: str
    description: Optional[str]
    type: InvoiceType
    status: InvoiceStatus
    created_at: datetime.datetime
    is_creditor: bool
    participants: List[UserRead] = []


class InvoiceDetailRead(InvoiceRead):
    model_config = {"from_attributes": True}
    
    creator: UserRead
    invoice_shares: List[InvoiceShareWithDebtor]
