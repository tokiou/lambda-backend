from fastapi import FastAPI
from routers import ai_router
from logs.handle_logger import logger


def include_router(app):
    app.include_router(ai_router.ai_router)


def init_app():
    app = FastAPI()
    include_router(app)
    return app


logger.info('Initializing app...')
app = init_app()
