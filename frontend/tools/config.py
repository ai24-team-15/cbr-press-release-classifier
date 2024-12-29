import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# определяем глобальную переменную API_URL
API_URL = os.getenv("API_URL")


# Настройка логгера с указанным уровнем логирования
def configure_logging(level: Optional[int] = logging.INFO) -> None:
    """
    Настраивает логирование для приложения.

    :param level: Уровень логирования (по умолчанию logging.INFO).
    """
    handler = RotatingFileHandler(
        filename="logs/cbr_ui.log",  # Файл для сохранения логов
        backupCount=5,               # Количество бэкапов
        maxBytes=10 * 1024 * 1024,   # Максимальный размер файла (10 МБ)
        encoding="utf-8",            # Кодировка файла логов
    )

    # Создаем formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(message)s",     # Формат сообщения
        datefmt="%Y-%m-%d %H:%M:%S",                       # Формат даты и времени
    )

    # Присваиваем formatter handler
    handler.setFormatter(formatter)

    # Создаем root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)


# Создаем директорию для логов, если она отсутствует
os.makedirs("logs", exist_ok=True)

# Настройка логирования
configure_logging()
log = logging.getLogger()
