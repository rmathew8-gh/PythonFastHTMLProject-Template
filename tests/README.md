# API Tests for Agno-2.Trials

This directory contains comprehensive tests for the FastAPI application.

## Test Structure

- `test_app.py` - Main test file containing all API endpoint tests
- `conftest.py` - Shared test fixtures and configuration
- `__init__.py` - Makes tests a Python package

## Test Categories

### 1. Root Endpoint Tests (`TestRootEndpoint`)
Tests for the main `/` endpoint:
- Status code verification (200 OK)
- Content type verification (HTML)
- Content verification (title, messages, styling)

### 2. API Behavior Tests (`TestAPIEndpoints`)
Tests for API behavior and edge cases:
- 404 responses for nonexistent endpoints
- 405 Method Not Allowed for unsupported HTTP methods

### 3. HTML Structure Tests (`TestHTMLStructure`)
Tests for HTML structure and content:
- Proper HTML structure (html, head, body elements)
- Presence of specific elements (h1, div, p)
- CSS class attributes

### 4. Response Headers Tests (`TestResponseHeaders`)
Tests for response headers:
- Content-Type header verification
- Character encoding verification

## Running Tests

### Using Make (Recommended)
```bash
make help              # Show all available commands
make test              # Run basic tests
make test-verbose      # Run tests with verbose output
make test-coverage     # Run tests with coverage report
make test-fast         # Run tests and stop on first failure
make test-failed       # Run only previously failed tests
make test-specific     # Run specific tests (use: make test-specific TEST="test_name")
make test-debug        # Run tests with debug output
make test-html         # Generate HTML coverage report
make test-install-deps # Install additional test dependencies
```

### Using pytest directly
```bash
uv run pytest                    # Run all tests
uv run pytest -v                 # Verbose output
uv run pytest tests/ -k "test_root"  # Run specific tests
uv run pytest --cov=app          # With coverage
```

### Using Make (recommended)
```bash
make test              # Run basic tests
make test-verbose      # Run tests with verbose output
make test-coverage     # Run tests with coverage report
make test-fast         # Run tests and stop on first failure
make test-failed       # Run only previously failed tests
make test-specific     # Run specific tests (use: make test-specific TEST="test_name")
make test-debug        # Run tests with debug output
make test-html         # Generate HTML coverage report
make test-install-deps # Install additional test dependencies
```

## Test Coverage

The test suite covers:
- ✅ HTTP status codes
- ✅ Response headers
- ✅ Content verification
- ✅ HTML structure validation
- ✅ Error handling (404, 405)
- ✅ HTTP method validation

## Adding New Tests

When adding new endpoints or features:

1. Add test methods to the appropriate test class
2. Use descriptive test method names starting with `test_`
3. Include docstrings explaining what each test verifies
4. Use the `client` fixture for making requests
5. Follow the existing test patterns and naming conventions

## Test Dependencies

- `pytest` - Test framework
- `httpx` - HTTP client for testing (required by FastAPI TestClient)
- `fastapi` - For TestClient functionality

## Notes

- Tests use FastAPI's `TestClient` for making requests
- The FastHTML library returns Python representations rather than HTML markup
- Tests are designed to work with the actual response format
