import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint ('/')"""

    def test_root_endpoint_returns_200(self):
        """Test that the root endpoint returns a 200 status code"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_html(self):
        """Test that the root endpoint returns HTML content"""
        response = client.get("/")
        assert response.headers["content-type"] == "text/html; charset=utf-8"

    def test_root_endpoint_contains_title(self):
        """Test that the HTML response contains the expected title"""
        response = client.get("/")
        html_content = response.text
        assert "Agno-2.Trials - Hello World" in html_content

    def test_root_endpoint_contains_hello_message(self):
        """Test that the HTML response contains the hello message"""
        response = client.get("/")
        html_content = response.text
        assert "Hello from Agno-2.Trials!" in html_content

    def test_root_endpoint_contains_welcome_message(self):
        """Test that the HTML response contains the welcome message"""
        response = client.get("/")
        html_content = response.text
        assert "Welcome to your basic FastHTML application." in html_content

    def test_root_endpoint_contains_styling(self):
        """Test that the HTML response contains CSS styling"""
        response = client.get("/")
        html_content = response.text
        assert "font-family" in html_content
        assert "color: #2563eb" in html_content
        assert "background: #f9fafb" in html_content


class TestAPIEndpoints:
    """Test cases for API behavior and edge cases"""

    def test_nonexistent_endpoint_returns_404(self):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_root_endpoint_with_post_method_returns_405(self):
        """Test that POST method on root endpoint returns 405 Method Not Allowed"""
        response = client.post("/")
        assert response.status_code == 405

    def test_root_endpoint_with_put_method_returns_405(self):
        """Test that PUT method on root endpoint returns 405 Method Not Allowed"""
        response = client.put("/")
        assert response.status_code == 405

    def test_root_endpoint_with_delete_method_returns_405(self):
        """Test that DELETE method on root endpoint returns 405 Method Not Allowed"""
        response = client.delete("/")
        assert response.status_code == 405


class TestHTMLStructure:
    """Test cases for HTML structure and content"""

    def test_html_has_proper_structure(self):
        """Test that the HTML has proper structure with head and body"""
        response = client.get("/")
        html_content = response.text
        assert "html(" in html_content
        assert "head(" in html_content
        assert "body(" in html_content

    def test_html_contains_h1_element(self):
        """Test that the HTML contains an H1 element"""
        response = client.get("/")
        html_content = response.text
        assert "h1(" in html_content

    def test_html_contains_container_div(self):
        """Test that the HTML contains a container div with proper class"""
        response = client.get("/")
        html_content = response.text
        assert "'class': 'container'" in html_content

    def test_html_contains_paragraph_elements(self):
        """Test that the HTML contains paragraph elements"""
        response = client.get("/")
        html_content = response.text
        assert "p(" in html_content


class TestResponseHeaders:
    """Test cases for response headers"""

    def test_response_has_correct_content_type(self):
        """Test that the response has the correct content type header"""
        response = client.get("/")
        assert "content-type" in response.headers
        assert "text/html" in response.headers["content-type"]

    def test_response_has_charset_utf8(self):
        """Test that the response specifies UTF-8 charset"""
        response = client.get("/")
        assert "charset=utf-8" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__])
