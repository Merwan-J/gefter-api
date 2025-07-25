from dataclasses import dataclass
from typing import List, Type, TypeVar
from uuid import UUID
from injector import inject, singleton
from sqlalchemy import Engine
from sqlmodel import Session, create_engine, delete, func, select
from api.core.models import BaseModel as DBBaseModel
from config import Config


@inject
@singleton
class DatabaseEngineProvider:
    def __init__(self, config: Config):
        self.engine = create_engine(
            url=str(config.db_url),
            echo=False,
            pool_pre_ping=True,
            pool_size=50,
            max_overflow=10,
        )

    def get_engine(self) -> Engine:
        return self.engine


ModelType = TypeVar(name="ModelType", bound=DBBaseModel)


@inject
@singleton
@dataclass
class PostgresRepositoryDelegate:
    def __init__(self, engine_provider: DatabaseEngineProvider):
        self.engine = engine_provider.get_engine()

    def exists(self, model: Type[ModelType], id: UUID) -> bool:
        with Session(self.engine) as session:
            query = select(model).where(model.id == id)
            result = session.exec(query).first()
            return result is not None

    def find_by_id(self, model: Type[ModelType], id: UUID) -> ModelType | None:
        with Session(self.engine) as session:
            query = select(model).where(model.id == id)
            result = session.exec(query).one()
            return result

    def find_all(self, model: Type[ModelType]) -> List[ModelType]:
        with Session(self.engine) as session:
            query = select(model)
            result = session.exec(query)
            return list(result)

    def count(self, model: Type[ModelType]) -> int:
        with Session(self.engine) as session:
            query = select(func.count()).select_from(model)
            result = session.exec(query).one()
            return result

    def save(self, item: ModelType):
        with Session(self.engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

    def save_all(self, items: List[ModelType]):
        with Session(self.engine) as session:
            session.add_all(items)
            session.commit()
            session.refresh_all()

    def delete(self, model: Type[ModelType], id: UUID) -> bool:
        with Session(self.engine) as session:
            query = delete(model).where(model.id == id)
            session.exec(query)
            return True

    def delete_many(self, model: Type[ModelType], ids: List[UUID]) -> bool:
        with Session(self.engine) as session:
            query = delete(model).where(model.id.in_(ids))
            session.exec(query)
            session.commit()
            return True

    def close(self):
        self.engine.dispose()
