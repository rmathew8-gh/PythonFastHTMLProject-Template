.PHONY: help install dev run lint test test-verbose test-coverage test-watch test-fast test-failed test-specific test-debug test-html test-install-deps test-integration test-unit test-all clean

help:
	@echo "install dev run lint test test-all test-unit test-integration test-coverage clean"

install:
	uv run pip install -e ".[dev]"
	# uv sync

dev:
	uv run uvicorn web.app:app --reload --host 127.0.0.1 --port 8001

run:
	uv run uvicorn web.app:app --host 127.0.0.1 --port 8001

lint:
	uv run ruff check --unsafe-fixes --fix .

test:
	uv run pytest

test-all:
	uv run pytest tests/

test-unit:
	uv run pytest tests/test_app.py

test-integration:
	uv run pytest tests/test_integration.py

test-verbose:
	uv run pytest -v

test-coverage:
	uv run pytest --cov=agno_trials --cov-report=term-missing

test-watch:
	uv run pytest-watch

test-fast:
	uv run pytest -x

test-failed:
	uv run pytest --lf

test-specific:
	uv run pytest -k $(TEST)

test-debug:
	uv run pytest -s -vv

test-html:
	uv run pytest --cov=agno_trials --cov-report=html:htmlcov

test-install-deps:
	uv add --dev pytest-cov pytest-watch

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov
	find . -name __pycache__ -type d -delete
