from loguru import logger

logger.remove()
logger.add("shopping_list.log", rotation="10 MB", retention="2 weeks")
