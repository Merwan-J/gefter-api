from fastapi import Request, Depends
from pymongo.database import Database
from api.user.service import UserService

def get_database(request: Request) -> Database:
    return request.app.database

def get_user_service(db: Database = Depends(get_database)) -> UserService:
    return UserService(db)
