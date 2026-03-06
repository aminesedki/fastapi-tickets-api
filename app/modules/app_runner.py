import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.api.base import api_router
from app.core.logging_config import setup_logging
from app.core.settings import settings
from app.utils.db import init_db

setup_logging()


logger = logging.getLogger(__name__)


class AppRun:
    APP_TITLE: str = f"{settings.APP_TITLE} ({settings.ENV.upper()})"
    APP_DESC: str = f"Environment: {settings.ENV.upper()} | API version: {settings.API_VERSION}"
    def __init__(self) -> None:

        self.app = FastAPI(
            title=self.APP_TITLE,
            description=self.APP_DESC,
            lifespan=self.lifespan,
        )
        self._config_app()

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Starting app - init DB")
        await init_db()
        logger.info("DB initialized")
        yield
        logger.info("Shutting down app")

    def _add_middlewares(self) -> None:
        # DEV-friendly CORS (no credentials with "*")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _set_routes(self) -> None:
        self.app.include_router(api_router)

        @self.app.get("/", response_class=HTMLResponse)
        async def index():
            env = settings.ENV.upper()
            return f"""
            <html>
              <head><title>{settings.APP_TITLE} - {env}</title></head>
                    <body>
                        <h1>{settings.APP_TITLE}</h1>
                        <p><b>ENV:</b> {env}</p>
                        <p><b>API Version:</b> {settings.API_VERSION}</p>
                        <p><a href="/docs">Swagger</a></p>
                    </body>
            </html>
            """

    def _config_app(self) -> None:
        self._add_middlewares()
        self._set_routes()
