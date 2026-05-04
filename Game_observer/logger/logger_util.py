from loguru import logger

logger.add("game_log.txt", format="{time:YYYY-MM-DD HH:mm:ss} | {message}")

def log_event(event: str):
    logger.info(event)