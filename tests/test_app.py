"""
Unit tests for the FastHTML application.

These tests focus on individual components, endpoints, and edge cases
using shared test utilities from conftest.py.
"""

import pytest
from bs4 import BeautifulSoup

# Import shared test utilities
from tests.conftest import (
    assert_html_structure,
    assert_content_type_html,
    assert_favicon_present,
    assert_css_styling_present,
    assert_main_content_present,
    assert_no_python_representation
)


class TestRootEndpoint:
    """Unit tests for the root endpoint ('/')"""

    def test_root_endpoint_returns_200(self, client):
        """Test that the root endpoint returns a 200 status code"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_html(self, client):
        """Test that the root endpoint returns HTML content"""
        response = client.get("/")
        assert_content_type_html(response)

    def test_root_endpoint_contains_title(self, root_response):
        """Test that the HTML response contains the expected title"""
        assert "Agno-2.Trials - Hello World" in root_response.text

    def test_root_endpoint_contains_hello_message(self, root_response):
        """Test that the HTML response contains the hello message"""
        assert "Hello from Agno-2.Trials!" in root_response.text

    def test_root_endpoint_contains_welcome_message(self, root_response):
        """Test that the HTML response contains the welcome message"""
        assert "Welcome to your basic FastHTML application." in root_response.text

    def test_root_endpoint_contains_styling(self, root_response):
        """Test that the HTML response contains CSS styling"""
        html_content = root_response.text
        assert "font-family" in html_content
        assert "color: #2563eb" in html_content
        assert "background: #f9fafb" in html_content


class TestAPIEndpoints:
    """Unit tests for API behavior and edge cases"""

    def test_nonexistent_endpoint_returns_404(self, client):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_root_endpoint_with_post_method_returns_405(self, client):
        """Test that POST method on root endpoint returns 405 Method Not Allowed"""
        response = client.post("/")
        assert response.status_code == 405

    def test_root_endpoint_with_put_method_returns_405(self, client):
        """Test that PUT method on root endpoint returns 405 Method Not Allowed"""
        response = client.put("/")
        assert response.status_code == 405

    def test_root_endpoint_with_delete_method_returns_405(self, client):
        """Test that DELETE method on root endpoint returns 405 Method Not Allowed"""
        response = client.delete("/")
        assert response.status_code == 405


class TestHTMLStructure:
    """Unit tests for HTML structure and content"""

    def test_html_has_proper_structure(self, root_soup):
        """Test that the HTML has proper structure with head and body"""
        assert_html_structure(root_soup)

    def test_html_contains_h1_element(self, root_soup):
        """Test that the HTML contains an H1 element"""
        h1 = root_soup.find('h1')
        assert h1 is not None
        assert h1.text == "Hello from Agno-2.Trials!"

    def test_html_contains_container_div(self, root_soup):
        """Test that the HTML contains a container div with proper class"""
        container = root_soup.find('div', class_='container')
        assert container is not None

    def test_html_contains_paragraph_elements(self, root_soup):
        """Test that the HTML contains paragraph elements"""
        paragraphs = root_soup.find_all('p')
        assert len(paragraphs) >= 2
        assert any("Welcome to your basic FastHTML application." in p.text for p in paragraphs)
        assert any("This is a minimal starting point for your project." in p.text for p in paragraphs)

    def test_html_contains_title_tag(self, root_soup):
        """Test that the HTML contains a proper title tag"""
        title = root_soup.find('title')
        assert title is not None
        assert title.text == "Agno-2.Trials - Hello World"

    def test_html_contains_favicon_link(self, root_soup):
        """Test that the HTML contains the favicon link"""
        assert_favicon_present(root_soup)

    def test_html_contains_style_tag(self, root_soup):
        """Test that the HTML contains CSS styling"""
        assert_css_styling_present(root_soup)


class TestResponseHeaders:
    """Unit tests for response headers"""

    def test_response_has_correct_content_type(self, client):
        """Test that the response has the correct content type header"""
        response = client.get("/")
        assert_content_type_html(response)

    def test_response_has_charset_utf8(self, client):
        """Test that the response specifies UTF-8 charset"""
        response = client.get("/")
        assert "charset=utf-8" in response.headers["content-type"]


class TestFastHTMLComponents:
    """Unit tests for FastHTML component rendering"""

    def test_fasthtml_to_html_rendering(self, root_response):
        """Test that FastHTML components are properly rendered to HTML"""
        html_content = root_response.text
        
        # Test that FastHTML components are rendered as proper HTML
        assert '<!doctype html>' in html_content
        assert '<html>' in html_content
        assert '<head>' in html_content
        assert '<body>' in html_content
        assert '<h1>' in html_content
        assert '<div class="container">' in html_content
        assert '<p>' in html_content
        
        # Test that Python representation is NOT present
        assert_no_python_representation(html_content)

    def test_fasthtml_component_structure(self, root_soup):
        """Test that FastHTML components maintain proper structure"""
        # Test that all expected FastHTML components are present
        assert root_soup.find('title') is not None
        assert root_soup.find('link', rel='icon') is not None
        assert root_soup.find('style') is not None
        assert root_soup.find('h1') is not None
        assert root_soup.find('div', class_='container') is not None
        assert len(root_soup.find_all('p')) >= 2

    def test_fasthtml_styling_integration(self, root_soup):
        """Test that FastHTML styling is properly integrated"""
        assert_css_styling_present(root_soup)


class TestCSSStyling:
    """Unit tests for CSS styling components"""

    def test_css_contains_font_family(self, root_soup):
        """Test that CSS contains font-family property"""
        style = root_soup.find('style')
        assert 'font-family: -apple-system' in style.string

    def test_css_contains_layout_properties(self, root_soup):
        """Test that CSS contains layout properties"""
        style = root_soup.find('style')
        css_content = style.string
        assert 'max-width: 800px' in css_content
        assert 'margin: 0 auto' in css_content
        assert 'padding: 2rem' in css_content

    def test_css_contains_color_properties(self, root_soup):
        """Test that CSS contains color properties"""
        style = root_soup.find('style')
        css_content = style.string
        assert 'color: #2563eb' in css_content
        assert 'background: #f9fafb' in css_content

    def test_css_contains_border_properties(self, root_soup):
        """Test that CSS contains border properties"""
        style = root_soup.find('style')
        css_content = style.string
        assert 'border-radius: 8px' in css_content


class TestContentValidation:
    """Unit tests for content validation"""

    def test_main_content_present(self, root_soup):
        """Test that main content elements are present and correct"""
        assert_main_content_present(root_soup)

    def test_heading_text_content(self, root_soup):
        """Test that heading contains expected text"""
        h1 = root_soup.find('h1')
        assert h1.text == "Hello from Agno-2.Trials!"

    def test_paragraph_text_content(self, root_soup):
        """Test that paragraphs contain expected text"""
        paragraphs = root_soup.find_all('p')
        expected_texts = [
            "Welcome to your basic FastHTML application.",
            "This is a minimal starting point for your project."
        ]
        
        actual_texts = [p.text for p in paragraphs]
        for expected in expected_texts:
            assert expected in actual_texts


if __name__ == "__main__":
    pytest.main([__file__])
