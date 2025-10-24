# src/logger_config.py
"""
Logging configuration for the Binance Futures CLI Bot.
Creates both console and JSON log output to bot.log.
"""

import logging
import logging.handlers
import os
import json
from datetime import datetime

LOG_FILE = os.getenv("BOT_LOG", "bot.log")

class JsonFormatter(logging.Formatter):
    """Format log records as JSON lines."""
    def format(self, record):
        base = {
            "ts": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage()
        }
        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(base)

def get_logger(name=__name__):
    """Return a logger configured for both console and file output."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # File handler with JSON format
    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JsonFormatter())

    # Console handler with readable text
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
