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

    def add_to_owed_to_user(self, user_id: UUID, amount: Decimal) -> Balance:
        """Increase amount others owe to this user."""
        try:
            return self.balance_repository.add_to_owed_to_user(user_id, amount)
        except BaseAPIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Unable to update owed_to_user: {str(e)}")

    def add_to_user_owes(self, user_id: UUID, amount: Decimal) -> Balance:
        """Increase amount this user owes to others."""
        try:
            return self.balance_repository.add_to_user_owes(user_id, amount)
        except BaseAPIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Unable to update user_owes: {str(e)}")

    def subtract_from_owed_to_user(self, user_id: UUID, amount: Decimal) -> Balance:
        """Decrease amount others owe to this user."""
        try:
            return self.balance_repository.subtract_from_owed_to_user(user_id, amount)
        except BaseAPIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Unable to update owed_to_user: {str(e)}")

    def subtract_from_user_owes(self, user_id: UUID, amount: Decimal) -> Balance:
        """Decrease amount this user owes to others."""
        try:
            return self.balance_repository.subtract_from_user_owes(user_id, amount)
        except BaseAPIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Unable to update user_owes: {str(e)}")

    def batch_update_balances(
        self,
        owed_to_user_updates: dict[UUID, Decimal],
        user_owes_updates: dict[UUID, Decimal]
    ) -> None:
        """Batch update multiple balances in a single transaction."""
        try:
            self.balance_repository.batch_update_balances(
                owed_to_user_updates, user_owes_updates
            )
        except BaseAPIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Unable to batch update balances: {str(e)}")

