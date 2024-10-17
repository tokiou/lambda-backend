from fastapi import FastAPI
from routers import ai_router


def include_router(app):
    app.include_router(ai_router.ai_router)


def init_app():
    app = FastAPI()
    include_router(app)
    return app


app = init_app()
