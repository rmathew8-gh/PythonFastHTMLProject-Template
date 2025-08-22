"""
Shared test configuration and utilities for the Agno-2.Trials test suite.

This module provides common fixtures, helper functions, and test utilities
that can be shared across all test files.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from web.app import app


@pytest.fixture
def client():
    """Provide a test client for all tests."""
    return TestClient(app)


@pytest.fixture
def root_response(client):
    """Provide the root endpoint response for tests that need it."""
    return client.get("/")


@pytest.fixture
def root_soup(root_response):
    """Provide a BeautifulSoup object of the root endpoint for HTML parsing tests."""
    return BeautifulSoup(root_response.text, "html.parser")


class TestHelpers:
    """Helper class containing common test utility methods."""

    @staticmethod
    def assert_html_structure(soup):
        """Assert that the HTML has proper basic structure."""
        assert soup.find("html") is not None
        assert soup.find("head") is not None
        assert soup.find("body") is not None

    @staticmethod
    def assert_content_type_html(response):
        """Assert that the response has correct HTML content type."""
        assert "content-type" in response.headers
        assert "text/html" in response.headers["content-type"]
        assert "charset=utf-8" in response.headers["content-type"]

    @staticmethod
    def assert_favicon_present(soup):
        """Assert that favicon is properly linked in HTML."""
        favicon = soup.find("link", rel="icon")
        assert favicon is not None
        assert favicon.get("href") == "/static/favicon.svg"
        assert favicon.get("type") == "image/svg+xml"
        assert favicon.get("sizes") == "any"

    @staticmethod
    def assert_css_styling_present(soup):
        """Assert that CSS styling is present and contains expected properties."""
        style = soup.find("style")
        assert style is not None

        css_content = style.string
        expected_properties = [
            "font-family: -apple-system",
            "max-width: 800px",
            "margin: 0 auto",
            "color: #2563eb",
            "background: #f9fafb",
        ]

        for property_name in expected_properties:
            assert property_name in css_content

    @staticmethod
    def assert_main_content_present(soup):
        """Assert that main content elements are present."""
        h1 = soup.find("h1")
        assert h1 is not None
        assert h1.text == "Hello from Agno-2.Trials!"

        container = soup.find("div", class_="container")
        assert container is not None

        paragraphs = container.find_all("p")
        assert len(paragraphs) == 2

        expected_texts = [
            "Welcome to your basic FastHTML application.",
            "This is a minimal starting point for your project.",
        ]

        actual_texts = [p.text for p in paragraphs]
        for expected in expected_texts:
            assert expected in actual_texts

    @staticmethod
    def assert_no_python_representation(html_content):
        """Assert that HTML doesn't contain Python representation artifacts."""
        python_artifacts = ["html(", "head(", "body(", "h1(", "div(", "p("]
        for artifact in python_artifacts:
            assert artifact not in html_content

    @staticmethod
    def assert_static_files_exist():
        """Assert that required static files exist."""
        static_dir = Path(__file__).parent.parent / "static"
        assert static_dir.exists()
        assert static_dir.is_dir()

        favicon_file = static_dir / "favicon.svg"
        assert favicon_file.exists()
        assert favicon_file.is_file()

    @staticmethod
    def assert_dependencies_available():
        """Assert that all required dependencies are available."""
        required_deps = ["fastapi", "uvicorn", "fasthtml", "httpx", "bs4"]
        for dep in required_deps:
            try:
                __import__(dep)
            except ImportError as e:
                pytest.fail(f"Required dependency '{dep}' not available: {e}")


# Make helpers available as module-level functions for convenience
assert_html_structure = TestHelpers.assert_html_structure
assert_content_type_html = TestHelpers.assert_content_type_html
assert_favicon_present = TestHelpers.assert_favicon_present
assert_css_styling_present = TestHelpers.assert_css_styling_present
assert_main_content_present = TestHelpers.assert_main_content_present
assert_no_python_representation = TestHelpers.assert_no_python_representation
assert_static_files_exist = TestHelpers.assert_static_files_exist
assert_dependencies_available = TestHelpers.assert_dependencies_available
