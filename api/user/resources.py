from typing import List
from fastapi import APIRouter, Depends
from fastapi_injector import Injected
from api.user.models import User, UserRead, UserCreate
from api.user.service import UserService
from api.core.dependencies import get_current_user


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/")
async def register_user(
    user: UserCreate, user_service: UserService = Injected(UserService)
):
    user = user_service.create_user(user)
    return UserRead(**user.model_dump())


@user_router.get("/", response_model=List[UserRead])
async def get_users(
    user_service: UserService = Injected(UserService),
    _: User = Depends(get_current_user),
):
    users = user_service.get_all_users()
    return [UserRead(**user.model_dump()) for user in users]


@user_router.get("/me", response_model=UserRead)
async def get_current_user_route(current_user: User = Depends(get_current_user)):
    return UserRead(**current_user.model_dump())


@user_router.get("/{id}", response_model=UserRead)
async def get_user(
    id: str,
    user_service: UserService = Injected(UserService),
):
    user = user_service.get_user_by_telegram_id(int(id))
    return UserRead(**user.model_dump())
