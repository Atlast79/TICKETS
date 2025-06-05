"""Ticket support application package."""

import logging

from . import config

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

__version__ = "0.2.1"
