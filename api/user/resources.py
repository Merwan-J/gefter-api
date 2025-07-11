from fastapi import APIRouter, Depends
from api.user.models import User
from api.user.service import UserService
from api.utils.dependencies import get_user_service


user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/")
async def register_user(user: User, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)


@user_router.get("/{id}")
async def get_user_by_telegram_id(id: str, user_service: UserService = Depends(get_user_service)): 
    return user_service.get_user_by_telegram_id(id)

