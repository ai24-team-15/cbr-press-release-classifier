from contextlib import asynccontextmanager
import logging
import uvicorn
from fastapi import FastAPI
from router import router
from settings import settings
from utils import (
    load_data_from_file,
    load_models_from_file,
    save_data_to_file,
    save_models_to_file,
)


logging.basicConfig(
    handlers=[logging.handlers.RotatingFileHandler(f"{settings.logs_path}/cbr_service.log", maxBytes=1000000)],
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Выполнение до запуска и после завершения сервиса
    """
    logging.info("Запуск сервиса")
    application.data = load_data_from_file()
    application.ml_models = load_models_from_file()
    yield
    save_data_to_file(application.data)
    save_models_to_file(application.ml_models)
    logging.info("Остановка сервиса")


app = FastAPI(
    title="cbr_press_release_classifier",
    version="1.0.0",
    lifespan=lifespan,
)

app.ml_models = {}
app.data = []


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
