from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api.core.injector import create_injector
from fastapi_injector import attach_injector
from api.user.resources import user_router


def create_app():
    app = FastAPI()

    injector = create_injector()

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    app.include_router(user_router)

    # origins = [
    #     config.web_url
    # ]

    attach_injector(app, injector)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    return app
