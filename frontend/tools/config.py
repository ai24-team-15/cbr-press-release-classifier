import logging
import os
from typing import Optional


# Настройка логгера с указанным уровнем логирования
def configure_logging(level: Optional[int] = logging.INFO) -> None:
    """
    Настраивает логирование для приложения.

    :param level: Уровень логирования (по умолчанию logging.INFO).
    """
    logging.basicConfig(
        filename="logs/app.log",  # Файл для сохранения логов
        encoding="utf-8",         # Кодировка файла логов
        format="%(asctime)s %(levelname)-8s %(message)s",  # Формат сообщения
        datefmt="%Y-%m-%d %H:%M:%S",                      # Формат даты и времени
        level=level,                                      # Уровень логирования
    )


# Создаем директорию для логов, если она отсутствует
os.makedirs("logs", exist_ok=True)
