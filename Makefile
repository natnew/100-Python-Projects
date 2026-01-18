.PHONY: install test lint format run clean

# Configuration
PYTHON := python
POETRY := poetry

install:
	$(POETRY) install

test:
	$(POETRY) run pytest

lint:
	$(POETRY) run ruff check .
	$(POETRY) run black --check .

format:
	$(POETRY) run black .
	$(POETRY) run ruff check --fix .

# Example: make run p=Tier-3-Evaluation-and-Safety/100-Final-Omnibus-Agent
run:
	$(POETRY) run python $(p)/src/main.py

clean:
	rm -rf .pytest_cache
	rm -rf dist
	find . -type d -name "__pycache__" -exec rm -rf {} +
