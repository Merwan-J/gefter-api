from typing import List
from .models import User, UserCreate
from fastapi import HTTPException
from pymongo.database import Database

class UserService:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["users"]
    
    def create_user(self, user_create: UserCreate) -> User:
        user = User(**user_create.model_dump())
        
        user_exists = self.collection.find_one(
            {"telegram_user_id": user.telegram_user_id}
        )
        if user_exists:
            raise HTTPException(status_code=400, detail="User already exists")
        
        user_dict = user.model_dump()
        self.collection.insert_one(user_dict)
        return user

    def get_user_by_telegram_id(self, id: int) -> User:
        user = self.collection.find_one({"telegram_user_id": id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(user)
    
    def get_user_by_id(self, id: str) -> User:
        user = self.collection.find_one({"id": id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)
    
    def get_user_by_username(self, username: str) -> User:
        user = self.collection.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)
    
    def get_all_users(self) -> List[User]:
        users = self.collection.find()
        return [User(**user) for user in users]
    
