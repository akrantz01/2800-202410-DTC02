from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient
from functions_framework import create_app
from pytest import FixtureRequest, MonkeyPatch


@pytest.fixture(scope="session")
def project_root() -> Path:
    """
    Retrieve the root directory of the project.
    """
    for directory in Path(__file__).parents:
        try:
            next(directory.glob("pyproject.toml"))
            return directory
        except StopIteration:
            continue

    raise FileNotFoundError("Could not find the project root directory")


@pytest.fixture(scope="session")
def bases_dir(project_root: Path) -> Path:
    """
    Retrieve the directory containing the bases.
    """
    return project_root / "bases" / "veritasai"


@pytest.fixture(scope="session")
def components_dir(project_root: Path) -> Path:
    """
    Retrieve the directory containing the components.
    """
    return project_root / "components" / "veritasai"


@pytest.fixture
def function_source(request: FixtureRequest, bases_dir: Path) -> Path:
    """
    Get the source file for the function handler.

    The test must be annotated with the `@pytest.mark.function` marker.
    """
    marker = request.node.get_closest_marker("function")
    if not marker:
        raise ValueError("Test must be marked with `@pytest.mark.function`")

    return bases_dir / marker.args[0] / "handler.py"


@pytest.fixture
def app(function_source: Path) -> Flask:
    """
    Create a new function application instance.
    """
    instance = create_app(source=function_source, target="handler")
    instance.config.update({"TESTING": True})

    return instance


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    Retrieve the test client for the function handler.
    """
    return app.test_client()


@pytest.fixture(autouse=True)
def disable_dotenv(monkeypatch: MonkeyPatch):
    """
    Disable the loading of the .env file for all tests.
    """
    with monkeypatch.context() as m:
        m.setattr("dotenv.load_dotenv", lambda: None)

        yield


@pytest.fixture(autouse=True)
def disable_firebase_admin_sdk_initialization(monkeypatch: MonkeyPatch):
    """
    Disables the initialization process for the Firebase Admin SDK.

    This ensures that credentials are not required to run tests.
    """
    with monkeypatch.context() as m:
        m.setattr("firebase_admin.initialize_app", lambda *args, **kwargs: None)

        yield


@pytest.fixture(autouse=True)
def set_articles_bucket(monkeypatch: MonkeyPatch):
    """
    Set the ARTICLES_BUCKET environment variable to "test-bucket".
    """
    with monkeypatch.context() as m:
        m.setenv("ARTICLES_BUCKET", "test-bucket")

        yield
