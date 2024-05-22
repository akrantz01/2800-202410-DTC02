from typing import Generator

import pytest

from .config import ConfigPatch

__all__ = ["ConfigPatch"]


@pytest.fixture
def env_var() -> Generator[ConfigPatch, None, None]:
    """
    Patch environment variables for the duration of the test.
    """
    patcher = ConfigPatch()
    yield patcher
    patcher.undo()
