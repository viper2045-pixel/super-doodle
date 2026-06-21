"""Logging configuration"""

import logging
import sys
from pathlib import Path
from utils.config import Config

# Create logs directory
log_dir = Path("./logs")
log_dir.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Get configured logger.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(Config.LOG_LEVEL)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(f"./logs/{Config.LOG_FILE}")
    file_handler.setLevel(Config.LOG_LEVEL)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
