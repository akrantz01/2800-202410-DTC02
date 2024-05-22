import os

from dotenv import dotenv_values

from . import location

env = dotenv_values(f".env.{location.name}")

if location.is_development:
    env.update(dotenv_values(".env"))

env.update(os.environ)

__all__ = ["env", "location"]
