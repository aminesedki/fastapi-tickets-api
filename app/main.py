import uvicorn

from app.modules.app_runner import AppRun, settings

appRunInstance = AppRun()

app = appRunInstance.app


if __name__ == "__main__":
    uvicorn.run("main:app", port=settings.APP_PORT, host=settings.APP_HOST)
