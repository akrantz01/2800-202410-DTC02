import os

from dotenv import dotenv_values
from google import auth

from . import location

env = dotenv_values(f".env.{location.name}")

if location.is_development:
    env.update(dotenv_values(".env"))

env.update(os.environ)

project_id = env.get("GOOGLE_CLOUD_PROJECT")
if project_id is None:
    _, project_id = auth.default()

__all__ = ["env", "location"]
