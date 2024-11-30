DIRECTORIES = app/

# Setup
install:
	@poetry install

# Build Dockerfile
build:
	docker build -t producer .

# Format & Lint Code via Ruff
format:
	@poetry run ruff check --select I --fix
	@poetry run ruff format

lint:
	@poetry run ruff check --fix

# Run MyPy
type-check:
	@poetry run mypy ./app/

# Run Django server
run:
	@poetry run python manage.py runserver 0.0.0.0:9001

# System commands for Makefile
MAKEFLAGS += --no-print-directory

# System Makefile commands
.PHONY: install format lint type-check run-server