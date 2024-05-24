from logging import basicConfig, getLogger

from google.cloud import logging
from veritasai.config import location

if location.is_production:
    client = logging.Client()
    client.setup_logging()
elif location.is_development:
    basicConfig(level="INFO")

get_logger = getLogger

__all__ = ["get_logger"]
