"""
Integration tests for the FastHTML application.

These tests verify the complete end-to-end functionality of the application,
including HTTP requests, HTML rendering, static file serving, and system behavior.
"""

import time
from pathlib import Path

import pytest

# Import shared test utilities
from tests.conftest import (
    assert_content_type_html,
    assert_css_styling_present,
    assert_dependencies_available,
    assert_favicon_present,
    assert_html_structure,
    assert_main_content_present,
    assert_no_python_representation,
    assert_static_files_exist,
)


class TestEndToEndIntegration:
    """End-to-end integration tests for the complete application"""

    def test_server_responds_to_root(self, client):
        """Test that the server responds to root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert_content_type_html(response)

    def test_complete_html_document_rendering(self, root_soup):
        """Test that the complete HTML document is properly rendered"""
        # Verify document structure
        assert_html_structure(root_soup)

        # Verify content
        title = root_soup.find("title")
        assert title is not None
        assert title.text == "Agno-2.Trials - Hello World"

        h1 = root_soup.find("h1")
        assert h1 is not None
        assert h1.text == "Hello from Agno-2.Trials!"

    def test_static_file_serving(self, client):
        """Test that static files are properly served"""
        # Test favicon
        response = client.get("/static/favicon.svg")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/svg+xml"

        # Verify favicon content is SVG
        assert response.text.startswith("<svg") or response.text.startswith("<?xml")

    def test_css_styling_integration(self, root_soup):
        """Test that CSS styling is properly integrated"""
        assert_css_styling_present(root_soup)

    def test_favicon_integration(self, root_soup):
        """Test that favicon is properly linked in HTML"""
        assert_favicon_present(root_soup)

    def test_content_accessibility(self, root_soup):
        """Test that all content is accessible and properly structured"""
        assert_main_content_present(root_soup)

    def test_error_handling(self, client):
        """Test error handling for non-existent endpoints"""
        # Test 404 for non-existent endpoint
        response = client.get("/nonexistent")
        assert response.status_code == 404

        # Test 405 for wrong HTTP method
        response = client.post("/")
        assert response.status_code == 405

    def test_html_quality_and_standards(self, root_response):
        """Test HTML quality and adherence to standards"""
        html_content = root_response.text

        # Test proper HTML structure
        assert html_content.startswith("<!doctype html>")
        assert "<html>" in html_content
        assert "<head>" in html_content
        assert "<body>" in html_content

        # Test that Python representation is NOT present
        assert_no_python_representation(html_content)

    def test_responsive_design_elements(self, root_soup):
        """Test responsive design elements in the CSS"""
        style = root_soup.find("style")
        css_content = style.string

        # Test responsive design properties
        responsive_properties = ["max-width: 800px", "margin: 0 auto", "padding: 2rem"]

        for property_name in responsive_properties:
            assert property_name in css_content

    def test_performance_basic(self, client):
        """Test basic performance characteristics"""
        # Test response time
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()

        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second
        assert response.status_code == 200

    def test_multiple_requests(self, client):
        """Test that the server can handle multiple requests"""
        # Make multiple requests
        for _ in range(5):
            response = client.get("/")
            assert response.status_code == 200
            assert_content_type_html(response)


class TestApplicationBehavior:
    """Tests for specific application behavior and edge cases"""

    def test_content_type_headers(self, client):
        """Test that content type headers are properly set"""
        response = client.get("/")
        assert_content_type_html(response)

    def test_favicon_file_exists(self):
        """Test that the favicon file actually exists"""
        assert_static_files_exist()

    def test_static_directory_structure(self):
        """Test that static directory structure is correct"""
        assert_static_files_exist()

    def test_application_structure(self):
        """Test that the application has the correct file structure"""
        app_file = Path(__file__).parent.parent / "src" / "web" / "app.py"
        assert app_file.exists()
        assert app_file.is_file()

    def test_dependencies_available(self):
        """Test that all required dependencies are available"""
        assert_dependencies_available()


class TestHTMLSemantics:
    """Tests for HTML semantic correctness"""

    def test_semantic_structure(self, root_soup):
        """Test that HTML has proper semantic structure"""
        # Test document structure
        html = root_soup.find("html")
        head = root_soup.find("head")
        body = root_soup.find("body")

        assert html is not None
        assert head is not None
        assert body is not None

        # Test that head contains appropriate elements
        assert head.find("title") is not None
        assert head.find("link", rel="icon") is not None
        assert head.find("style") is not None

    def test_heading_hierarchy(self, root_soup):
        """Test that heading hierarchy is correct"""
        # Test that there's exactly one h1 element
        h1_elements = root_soup.find_all("h1")
        assert len(h1_elements) == 1

        # Test that h1 contains the expected text
        assert h1_elements[0].text == "Hello from Agno-2.Trials!"

    def test_container_semantics(self, root_soup):
        """Test that container elements have proper semantics"""
        # Test container div
        container = root_soup.find("div", class_="container")
        assert container is not None

        # Test that container contains paragraphs
        paragraphs = container.find_all("p")
        assert len(paragraphs) >= 1


class TestFastHTMLIntegration:
    """Tests specifically for FastHTML integration features"""

    def test_fasthtml_to_xml_rendering(self, root_response):
        """Test that FastHTML components are properly rendered to XML"""
        html_content = root_response.text

        # Test that FastHTML components are rendered as proper HTML
        assert "<!doctype html>" in html_content
        assert "<html>" in html_content
        assert "<head>" in html_content
        assert "<body>" in html_content
        assert "<h1>" in html_content
        assert '<div class="container">' in html_content
        assert "<p>" in html_content

        # Test that Python representation is NOT present
        assert_no_python_representation(html_content)

    def test_fasthtml_component_structure(self, root_soup):
        """Test that FastHTML components maintain proper structure"""
        # Test that all expected FastHTML components are present
        assert root_soup.find("title") is not None
        assert root_soup.find("link", rel="icon") is not None
        assert root_soup.find("style") is not None
        assert root_soup.find("h1") is not None
        assert root_soup.find("div", class_="container") is not None
        assert len(root_soup.find_all("p")) >= 2

    def test_fasthtml_styling_integration(self, root_soup):
        """Test that FastHTML styling is properly integrated"""
        assert_css_styling_present(root_soup)


class TestSystemIntegration:
    """Tests for system-level integration and behavior"""

    def test_concurrent_requests(self, client):
        """Test that the application can handle concurrent requests"""
        import queue
        import threading

        results = queue.Queue()

        def make_request():
            response = client.get("/")
            results.put((response.status_code, response.headers.get("content-type")))

        # Create multiple threads
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        while not results.empty():
            status_code, content_type = results.get()
            assert status_code == 200
            assert "text/html" in content_type

    def test_memory_usage_stability(self, client):
        """Test that memory usage remains stable across multiple requests"""
        try:
            import os

            import psutil

            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss

            # Make multiple requests
            for _ in range(10):
                response = client.get("/")
                assert response.status_code == 200

            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory

            # Memory increase should be reasonable (less than 10MB)
            assert memory_increase < 10 * 1024 * 1024
        except ImportError:
            # Skip this test if psutil is not available
            pytest.skip("psutil not available for memory usage testing")

    def test_error_recovery(self, client):
        """Test that the application recovers gracefully from errors"""
        # Make a request that should fail
        response = client.get("/nonexistent")
        assert response.status_code == 404

        # Immediately make a valid request
        response = client.get("/")
        assert response.status_code == 200
        assert_content_type_html(response)

    def test_static_file_error_handling(self, client):
        """Test error handling for non-existent static files"""
        # Test non-existent static file
        response = client.get("/static/nonexistent.svg")
        assert response.status_code == 404


class TestAccessibilityIntegration:
    """Tests for accessibility features and standards"""

    def test_basic_accessibility_structure(self, root_soup):
        """Test basic accessibility features"""
        # Test heading hierarchy
        h1 = root_soup.find("h1")
        assert h1 is not None

        # Test semantic structure
        assert root_soup.find("head") is not None
        assert root_soup.find("body") is not None

    def test_content_readability(self, root_soup):
        """Test that content is readable and well-structured"""
        # Test that main content is present
        assert_main_content_present(root_soup)

        # Test that text content is accessible
        h1 = root_soup.find("h1")
        assert h1.text.strip() != ""

        paragraphs = root_soup.find_all("p")
        for p in paragraphs:
            assert p.text.strip() != ""


if __name__ == "__main__":
    pytest.main([__file__])
