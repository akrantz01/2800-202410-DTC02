from pathlib import Path

from functions_framework import create_app
from veritasai.config import env


def find_project_root_directory() -> Path:
    """
    Find the directory containing the project root.
    """
    for directory in Path(__file__).parents:
        try:
            next(directory.glob("pyproject.toml"))
            return directory
        except StopIteration:
            continue

    raise FileNotFoundError("Could not find the project root directory")


FUNCTION = env.get("FUNCTION")
if FUNCTION is None or len(FUNCTION) == 0:
    raise ValueError("The FUNCTION environment variable must be set")

root = find_project_root_directory()
source = root / "bases" / "veritasai" / FUNCTION / "handler.py"

if not source.exists():
    raise FileNotFoundError(f"Could not find the function {FUNCTION} at {source}")

app = create_app(source=source, target="handler")
