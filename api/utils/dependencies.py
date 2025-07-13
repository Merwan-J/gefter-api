from fastapi import HTTPException, Request, Depends
from pymongo.database import Database
from api.user.models import User
from api.user.service import UserService
from init_data_py import InitData
from config import get_config

def get_database(request: Request) -> Database:
    return request.app.database

def get_user_service(db: Database = Depends(get_database)) -> UserService:
    return UserService(db)


def get_current_user(request: Request) -> User:
    config = get_config()
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[-1]
    
    init_data = InitData.parse(token)
    if not init_data.validate(bot_token=config.bot_token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_service = UserService(request.app.database)
    user = user_service.get_user_by_telegram_id(init_data.user.id)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return user
