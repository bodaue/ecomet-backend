import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.core.di.main import container_factory


def setup_routers(app: FastAPI) -> None:
    pass


def setup_di_container(app: FastAPI) -> None:
    container = container_factory()
    setup_dishka(container, app)


def create_application() -> FastAPI:
    app = FastAPI(
        title="Ecomet",
        debug=True,
        root_path="/api",
    )

    setup_di_container(app)
    setup_routers(app)
    return app


if __name__ == "__main__":
    uvicorn.run("src.main:create_application", factory=True, reload=True)
