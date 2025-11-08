from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from injector import inject
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from api.core.repository import DatabaseEngineProvider
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

    def create_balance(
        self,
        user_id: UUID,
        initial_owed_to_user: Decimal = Decimal("0.00"),
        initial_user_owes: Decimal = Decimal("0.00"),
    ) -> Balance:
        """Create a new balance record for a user"""
        with Session(self.engine) as session:
            balance = Balance(
                user_id=user_id,
                owed_to_user=initial_owed_to_user,
                user_owes=initial_user_owes,
            )
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

    def add_to_owed_to_user(self, user_id: UUID, amount: Decimal) -> Balance:
        """Increase amount others owe to this user."""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            balance = session.exec(query).first()
            if balance is None:
                balance = Balance(user_id=user_id, owed_to_user=Decimal("0.00"), user_owes=Decimal("0.00"))
                session.add(balance)
                session.flush()
            balance.owed_to_user += amount
            session.add(balance)
            session.commit()
            session.refresh(balance)
            return balance

    def add_to_user_owes(self, user_id: UUID, amount: Decimal) -> Balance:
        """Increase amount this user owes to others."""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            balance = session.exec(query).first()
            if balance is None:
                balance = Balance(user_id=user_id, owed_to_user=Decimal("0.00"), user_owes=Decimal("0.00"))
                session.add(balance)
                session.flush()
            balance.user_owes += amount
            session.add(balance)
            session.commit()
            session.refresh(balance)
            return balance

    def subtract_from_owed_to_user(self, user_id: UUID, amount: Decimal) -> Balance:
        """Decrease amount others owe to this user."""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            balance = session.exec(query).first()
            if balance is None:
                balance = Balance(user_id=user_id, owed_to_user=Decimal("0.00"), user_owes=Decimal("0.00"))
                session.add(balance)
                session.flush()
            balance.owed_to_user -= amount
            # Ensure balance doesn't go negative (optional safety check)
            if balance.owed_to_user < Decimal("0.00"):
                raise ValueError("Owed to user cannot be negative")
            session.add(balance)
            session.commit()
            session.refresh(balance)
            return balance

    def subtract_from_user_owes(self, user_id: UUID, amount: Decimal) -> Balance:
        """Decrease amount this user owes to others."""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            balance = session.exec(query).first()
            if balance is None:
                balance = Balance(user_id=user_id, owed_to_user=Decimal("0.00"), user_owes=Decimal("0.00"))
                session.add(balance)
                session.flush()
            balance.user_owes -= amount
            # Ensure balance doesn't go negative (optional safety check)
            if balance.user_owes < Decimal("0.00"):
                raise ValueError("User owes cannot be negative")
            session.add(balance)
            session.commit()
            session.refresh(balance)
            return balance

    def set_balances(
        self, user_id: UUID, owed_to_user: Decimal, user_owes: Decimal
    ) -> Balance:
        """Set both balance sides for a user."""
        with Session(self.engine) as session:
            query = select(Balance).where(Balance.user_id == user_id)
            balance_obj = session.exec(query).first()
            if balance_obj is None:
                balance_obj = Balance(
                    user_id=user_id, owed_to_user=owed_to_user, user_owes=user_owes
                )
                session.add(balance_obj)
            else:
                balance_obj.owed_to_user = owed_to_user
                balance_obj.user_owes = user_owes
                session.add(balance_obj)
            session.commit()
            session.refresh(balance_obj)
            return balance_obj

    def batch_update_balances(
        self, 
        owed_to_user_updates: dict[UUID, Decimal],
        user_owes_updates: dict[UUID, Decimal]
    ) -> None:
        """Batch update multiple balances in a single transaction.
        
        Args:
            owed_to_user_updates: Dict mapping user_id -> amount to add to owed_to_user
            user_owes_updates: Dict mapping user_id -> amount to add to user_owes
        """
        with Session(self.engine) as session:
            # Get all unique user IDs that need updates
            all_user_ids = set(owed_to_user_updates.keys()) | set(user_owes_updates.keys())
            
            if not all_user_ids:
                return
            
            # Fetch all balances in one query
            query = select(Balance).where(Balance.user_id.in_(all_user_ids))
            existing_balances = {balance.user_id: balance for balance in session.exec(query)}
            
            # Update or create balances
            for user_id in all_user_ids:
                balance = existing_balances.get(user_id)

                if balance is None:
                    balance = Balance(
                        user_id=user_id,
                        owed_to_user=Decimal("0.00"),
                        user_owes=Decimal("0.00")
                    )
                    session.add(balance)
                
                # Update owed_to_user
                if user_id in owed_to_user_updates:
                    balance.owed_to_user += owed_to_user_updates[user_id]
                
                # Update user_owes
                if user_id in user_owes_updates:
                    balance.user_owes += user_owes_updates[user_id]
                
                session.add(balance)
            
            # Single commit for all updates
            session.commit()

