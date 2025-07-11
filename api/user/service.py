from api.user.models import User
from typing import List
from pymongo.database import Database
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["users"]
        
    def create_user(self, user: User) -> User:
        self.collection.insert_one(user.model_dump())
        return user
    
    def get_user_by_id(self, id: str) -> User:
        user = self.collection.find_one({"id": id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)
    
    def get_user_by_telegram_id(self, id: str) -> User:
        user = self.collection.find_one({"user_id": id})
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
    
