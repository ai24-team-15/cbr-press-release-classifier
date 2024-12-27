import logging
import os


# Настройка логгера
def configure_logging(level=logging.INFO):
    logging.basicConfig(
        filename="logs/app.log",
        encoding='utf-8',
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )


# Создаем директорию для логов, если её нет
os.makedirs("logs", exist_ok=True)
    