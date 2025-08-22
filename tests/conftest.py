import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    """Fixture that provides a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def app_instance():
    """Fixture that provides the FastAPI application instance"""
    return app
