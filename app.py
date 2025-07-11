

from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from api.user.resources import user_router

config = dotenv_values(".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_url = config["DB_URL"]
    app.mongodb_client = MongoClient(db_url)
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    yield
    app.mongodb_client.close()


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(user_router) 

    @app.get("/health")
    async def health():
        return {"status": "ok"}
    return app


