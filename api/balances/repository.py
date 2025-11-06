from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from injector import inject
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from api.core.repository import DatabaseEngineProvider
from api.core.exceptions import NotFoundError
from api.balances.models import Balance


@inject
@dataclass
class BalanceRepository:
    engine_provider: DatabaseEngineProvider

    def __post_init__(self):
        self.engine: Engine = self.engine_provider.get_engine()

    def get_balance_by_user_id(self, user_id: UUID) -> Balance | None:
        """Get balance for a user, returns None if not found"""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            return session.exec(query).first()

    def create_balance(self, user_id: UUID, initial_balance: Decimal = Decimal("0.00")) -> Balance:
        """Create a new balance record for a user"""
        with Session(self.engine) as session:
            balance = Balance(user_id=user_id, balance=initial_balance)
            session.add(balance)
            session.commit()
            session.refresh(balance)
            return balance

    def get_or_create_balance(self, user_id: UUID) -> Balance:
        """Get balance for a user, create if it doesn't exist"""
        balance = self.get_balance_by_user_id(user_id)
        if balance is None:
            balance = self.create_balance(user_id)
        return balance

    def update_balance(self, user_id: UUID, amount: Decimal) -> Balance:
        """Add amount to user's balance (can be negative to subtract)"""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            balance = session.exec(query).first()
            
            if balance is None:
                balance = Balance(user_id=user_id, balance=Decimal("0.00"))
                session.add(balance)
                session.flush()
            
            balance.balance += amount
            session.add(balance)
            session.commit()
            session.refresh(balance)
            return balance

    def set_balance(self, user_id: UUID, balance: Decimal) -> Balance:
        """Set user's balance to a specific value"""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            balance_obj = session.exec(query).first()
            
            if balance_obj is None:
                balance_obj = Balance(user_id=user_id, balance=balance)
                session.add(balance_obj)
            else:
                balance_obj.balance = balance
                session.add(balance_obj)
            
            session.commit()
            session.refresh(balance_obj)
            return balance_obj

