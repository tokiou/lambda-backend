from fastapi import FastAPI
from routers import ai_router, users_router, content_router, team_router
from logs.handle_logger import logger


def include_router(app) -> None:
    app.include_router(ai_router.ai_router)
    app.include_router(users_router.user_router)
    app.include_router(content_router.content_router)
    app.include_router(team_router.team_router)


def init_app() -> FastAPI:
    app = FastAPI()
    include_router(app)
    return app


logger.info('Initializing app...')
app = init_app()