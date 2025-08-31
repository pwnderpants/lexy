.PHONY: help install install-dev test test-cov lint format type-check clean build upload-test upload docs serve-docs all

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# Installation targets
install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt
	pip install -e .

# Testing targets
test: ## Run tests
	pytest

test-cov: ## Run tests with coverage report
	pytest --cov=lexy --cov-report=html --cov-report=term

# Code quality targets
lint: ## Run linting (flake8)
	flake8 lexy tests

format: ## Format code with black and isort
	black lexy tests
	isort lexy tests

format-check: ## Check code formatting without making changes
	black --check lexy tests
	isort --check-only lexy tests

type-check: ## Run type checking with mypy
	mypy lexy

# Quality check combination
check: format-check lint type-check ## Run all code quality checks

# Cleanup targets
clean: ## Clean up build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build targets
build: clean ## Build distribution packages
	python -m build

# Upload targets (use with caution)
upload-test: build ## Upload to test PyPI
	twine upload --repository testpypi dist/*

upload: build ## Upload to PyPI
	twine upload dist/*

# Documentation targets
docs: ## Build documentation
	cd docs && make html

serve-docs: docs ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

# Development workflow
all: install-dev check test ## Install dev dependencies, run checks and tests

# Development server (if applicable)
dev: ## Run in development mode
	python -m lexy