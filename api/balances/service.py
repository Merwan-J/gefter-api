from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from injector import inject

from api.core.exceptions import BaseAPIException, InternalServerError
from api.balances.models import Balance
from api.balances.repository import BalanceRepository


@inject
@dataclass
class BalanceService:
    balance_repository: BalanceRepository

    def get_balance(self, user_id: UUID) -> Balance:
        """Get balance for a user, creates one if it doesn't exist"""
        try:
            return self.balance_repository.get_or_create_balance(user_id)
        except BaseAPIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Unable to fetch balance: {str(e)}")

    def update_balance(self, user_id: UUID, amount: Decimal) -> Balance:
        """Update user's balance by adding amount (can be negative)"""
        try:
            return self.balance_repository.update_balance(user_id, amount)
        except BaseAPIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Unable to update balance: {str(e)}")

    def add_to_balance(self, user_id: UUID, amount: Decimal) -> Balance:
        """Add amount to user's balance"""
        return self.update_balance(user_id, amount)

    def subtract_from_balance(self, user_id: UUID, amount: Decimal) -> Balance:
        """Subtract amount from user's balance"""
        return self.update_balance(user_id, -amount)

