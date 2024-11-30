# Variables for Docker Compose files
DEV_COMPOSE_FILE := docker-compose.dev.yml
PROD_COMPOSE_FILE := docker-compose.yml

# Default to development if not specified
COMPOSE_FILE ?= $(DEV_COMPOSE_FILE)

# Common Docker Compose commands
up:
	docker-compose -f $(COMPOSE_FILE) up --build -d

down:
	docker-compose -f $(COMPOSE_FILE) down

build:
	docker-compose -f $(COMPOSE_FILE) build

logs:
	docker-compose -f $(COMPOSE_FILE)  logs -f

.PHONY: up down build logs