from dataclasses import dataclass
from typing import List
from uuid import UUID

from api.user.repository import UserRepository
from .models import User, UserCreate
from fastapi import HTTPException
from injector import inject
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


@inject
@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, user_create: UserCreate) -> User:
        try:
            user_exists = self.user_repository.user_by_telegram_id_exists(
                user_create.telegram_user_id
            )
            if user_exists:
                raise HTTPException(status_code=400, detail="User already exists")

            user = self.user_repository.save(User(**user_create.model_dump()))
            return user

        except HTTPException:
            raise
        except IntegrityError as e:
            logger.error(f"Database integrity error while creating user: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Could not create user due to database constraint violation",
            )

        except Exception as e:
            logger.error(f"Unexpected error while creating user: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

    def get_user_by_telegram_id(self, telegram_id: int) -> User:
        try:
            user = self.user_repository.find_user_by_telegram_id(telegram_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while fetching user by telegram ID: {str(e)}"
            )
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

    def get_user_by_id(self, user_id: UUID) -> User:
        try:
            user = self.user_repository.find_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching user by ID: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

    def get_user_by_username(self, username: str) -> User:
        try:
            user = self.user_repository.find_user_by_username(username)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching user by username: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

    def get_all_users(self) -> List[User]:
        try:
            return self.user_repository.find_all_users()
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching all users: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

    def delete_user(self, user_id: UUID) -> bool:
        try:
            is_deleted = self.user_repository.delete_user(user_id)
            if not is_deleted:
                logger.error(f"User doesn't exist: ID --{user_id}")
                raise HTTPException(
                    status_code=400, detail="User with given Id doesn't exist"
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while deleting user: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred")
