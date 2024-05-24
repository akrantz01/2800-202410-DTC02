"""
Metadata about where the application is running.
"""

from os import environ
from sys import modules

VALID_ENVIRONMENTS = {"development", "production", "test"}

if (app_env := environ.get("APP_ENV")) is not None:
    name = app_env.lower().strip()

    if name not in VALID_ENVIRONMENTS:
        raise ValueError(f"Invalid APP_ENV: {app_env}")

elif "pytest" in modules:
    name = "test"

elif "K_SERVICE" in environ and "K_REVISION" in environ:
    name = "production"

else:
    name = "development"


is_development = name == "development"
is_production = name == "production"
