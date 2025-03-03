import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Settings(BaseSettings):
    models_path: str = os.getenv("MODELS_PATH", default="ml_models")
    data_path: str = os.getenv("DATA_PATH", default="data")
    logs_path: str = os.getenv("LOGS_PATH", default="logs")
    random_state: int = os.getenv("RANDOM_STATE", default="42")
    threads_count: int = os.getenv("THREADS_COUNT", default="5")


settings = Settings()

if not os.path.exists(settings.models_path):
    os.makedirs(settings.models_path)
if not os.path.exists(settings.data_path):
    os.makedirs(settings.data_path)
if not os.path.exists(settings.logs_path):
    os.makedirs(settings.logs_path)
