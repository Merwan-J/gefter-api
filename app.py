

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI
from pymongo import MongoClient
from api.user.resources import user_router
from config import get_config



@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    app.mongodb_client = MongoClient(config.db_url)
    app.database = app.mongodb_client[config.db_name]
    app.config = config
    print("Connected to the MongoDB database!")
    yield
    app.mongodb_client.close()


def create_app():
    app = FastAPI(lifespan=lifespan)

    @app.get("/health")
    async def health():
        return {"status": "ok"}
    
    app.include_router(user_router) 
    
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    return app


