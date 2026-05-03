.PHONY: install dev lint format typecheck test security docker-build

PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	pre-commit install

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app

test:
	pytest --cov=app --cov-report=term-missing --cov-report=xml

security:
	bandit -r app -c bandit.yaml
	pip-audit -r requirements.txt -r requirements-dev.txt

docker-build:
	docker build -t collabsta-backend:test .
