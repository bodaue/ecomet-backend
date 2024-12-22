import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.routes import top100, activity
from src.core.di.main import container_factory
from src.core.settings import create_settings


def setup_routers(app: FastAPI) -> None:
    app.include_router(top100.router)
    app.include_router(activity.router)


def setup_di_container(app: FastAPI) -> None:
    container = container_factory()
    setup_dishka(container, app)


def create_application() -> FastAPI:
    settings = create_settings()
    app = FastAPI(
        title=settings.project.title,
        debug=settings.project.debug,
        root_path="/api",
    )

    setup_di_container(app)
    setup_routers(app)
    return app


if __name__ == "__main__":
    uvicorn.run("src.main:create_application", factory=True, reload=True)
