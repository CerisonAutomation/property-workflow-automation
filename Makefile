.PHONY: install dev test lint

install:
	pip install -r requirements.txt

dev:
	uvicorn app:app --reload --port 8001

test:
	pytest tests/ -v

lint:
	ruff check .
