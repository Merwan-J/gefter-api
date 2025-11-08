import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, Numeric
from api.core.models import BaseModel as DBBaseModel

# DB Model
class Balance(DBBaseModel, table=True):
    __tablename__ = "balances"

    user_id: UUID = Field(foreign_key="users.id", unique=True, index=True)
    owed_to_user: Decimal = Field(
        sa_type=Numeric[Decimal](precision=10, scale=2),
        default=Decimal("0.00")
    )
    user_owes: Decimal = Field(
        sa_type=Numeric[Decimal](precision=10, scale=2),
        default=Decimal("0.00")
    )


class BalanceBase(BaseModel):
    user_id: UUID
    owed_to_user: Decimal
    user_owes: Decimal

# DTOs below
class BalanceRead(BalanceBase):
    model_config = {"from_attributes": True}
    
    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime


class BalanceUpdate(BaseModel):
    owed_to_user: Decimal
    user_owes: Decimal

