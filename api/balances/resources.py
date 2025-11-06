from fastapi import APIRouter, Depends
from fastapi_injector import Injected
from api.core.dependencies import get_current_user
from api.balances.models import BalanceRead
from api.balances.service import BalanceService
from api.user.models import User


balance_router = APIRouter(prefix="/balances", tags=["balances"])


@balance_router.get("/me", response_model=BalanceRead)
async def get_my_balance(
    balance_service: BalanceService = Injected(BalanceService),
    current_user: User = Depends(get_current_user),
):
    """Get current user's balance"""
    balance = balance_service.get_balance(current_user.id)
    return BalanceRead.model_validate(balance)


@balance_router.get("/{user_id}", response_model=BalanceRead)
async def get_user_balance(
    user_id: str,
    balance_service: BalanceService = Injected(BalanceService),
    _: User = Depends(get_current_user),
):
    """Get balance for a specific user (by UUID)"""
    from uuid import UUID
    balance = balance_service.get_balance(UUID(user_id))
    return BalanceRead.model_validate(balance)

