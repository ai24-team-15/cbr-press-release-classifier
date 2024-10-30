from loguru import logger


logger.add(
    "logs/log.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level="INFO",
)
