import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def get_logger(
    name:str = "querywave",
    level: int = logging.INFO,
    ):
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        return logger
    
    logger.propagate = False
    
    ##log formatting
    
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    ##file handling(with rotation)
    
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024, ##5MB
        backupCount=5,
        encoding="utf-8",
    )
    
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

