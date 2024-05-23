from logging import getLogger

from google.cloud import logging
from veritasai.config import location

if location.is_production:
    client = logging.Client()
    client.setup_logging()

get_logger = getLogger

__all__ = ["get_logger"]
