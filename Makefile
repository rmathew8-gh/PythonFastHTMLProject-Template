.PHONY: help install dev run lint test test-verbose test-coverage test-watch test-fast test-failed test-specific test-debug test-html test-install-deps clean

help:
	@echo "Available commands:"
	@echo "  install          - Install dependencies"
	@echo "  dev              - Run development server with auto-reload"
	@echo "  run              - Run production server"
	@echo "  lint             - Run linting with ruff"
	@echo "  test             - Run basic tests"
	@echo "  test-verbose     - Run tests with verbose output"
	@echo "  test-coverage    - Run tests with coverage report"
	@echo "  test-watch       - Run tests in watch mode"
	@echo "  test-fast        - Run tests and stop on first failure"
	@echo "  test-failed      - Run only previously failed tests"
	@echo "  test-specific    - Run specific tests (use: make test-specific TEST=\"test_name\")"
	@echo "  test-debug       - Run tests with debug output"
	@echo "  test-html        - Generate HTML coverage report"
	@echo "  test-install-deps- Install additional test dependencies"
	@echo "  clean            - Clean up cache and build files"

install:
	uv run pip install -e ".[dev]"
	# uv sync

dev:
	uv run uvicorn app:app --reload --host 127.0.0.1 --port 8001

run:
	uv run uvicorn app:app --host 127.0.0.1 --port 8001

lint:
	uv run ruff check --fix .

test:
	uv run pytest

test-verbose:
	uv run pytest -v

test-coverage:
	uv run pytest --cov=app --cov-report=term-missing --cov-report=html:htmlcov

test-watch:
	uv run pytest-watch -- -v

test-fast:
	uv run pytest -x --tb=short

test-failed:
	uv run pytest --lf

test-specific:
	uv run pytest -k $(TEST)

test-debug:
	uv run pytest -s -vv --tb=long

test-html:
	uv run pytest --cov=app --cov-report=html:htmlcov
	@echo "Coverage report generated in htmlcov/index.html"

test-install-deps:
	uv add --dev pytest-cov pytest-watch

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
