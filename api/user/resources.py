from fastapi import APIRouter, Depends, Request
from api.user.models import User, UserRead, UserCreate
from api.user.service import UserService
from api.utils.dependencies import get_current_user, get_user_service


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/")
async def register_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)


@user_router.get("/me", response_model=UserRead)
async def get_current_user_route(
    current_user: User = Depends(get_current_user)
):
    return UserRead.from_db_model(current_user)

@user_router.get("/{id}", response_model=UserRead)
async def get_user(
    id: str,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user_by_telegram_id(int(id))
    return UserRead.from_db_model(user)
