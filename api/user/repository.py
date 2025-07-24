from typing import List
from uuid import UUID
from injector import inject
from sqlmodel import Session, select
from api.core.repository import DatabaseEngineProvider
from .models import User


@inject
class UserRepository:
    def __init__(self, engine_provider: DatabaseEngineProvider):
        self.engine = engine_provider.get_engine()

    def user_by_telegram_id_exists(self, telegram_user_id: int) -> bool:
        with Session(self.engine) as session:
            query = select(User).where(User.telegram_user_id == telegram_user_id)
            result = session.exec(query).first()
            return result is not None

    def user_by_id_exists(self, id: UUID) -> bool:
        with Session(self.engine) as session:
            return session.get(User, id) is not None

    def save(self, user: User) -> User:
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def find_user_by_id(self, id: UUID) -> User:
        with Session(self.engine) as session:
            return session.get(User, id)

    def find_user_by_telegram_id(self, telegram_user_id: int) -> User:
        with Session(self.engine) as session:
            query = select(User).where(User.telegram_user_id == telegram_user_id)
            return session.exec(query).one()

    def find_user_by_username(self, username: str) -> User:
        with Session(self.engine) as session:
            query = select(User).where(User.username == username)
            return session.exec(query).first()

    def find_all_users(self) -> List[User]:
        with Session(self.engine) as session:
            query = select(User)
            result = session.exec(query)
            return list(result)

    def delete_user(self, id: UUID) -> bool:
        with Session(self.engine) as session:
            user = session.get(User, id)
            if not user:
                return False
            session.delete(user)
            session.commit()
            return True
