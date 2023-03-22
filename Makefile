#!/usr/bin/env bash
# Tab sign surrounded by two dots: .	.

THIS_FILE := $(lastword $(MAKEFILE_LIST))
# ID=$$(docker ps -f name=momenty-uwsgi-momenty-org |tail -1 |colrm 12)
.PHONY: help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


build: ## Билд парсера
	docker compose -f docker-compose.yml build
start-dev: ## Запуск сервиса
	docker compose -f docker-compose.yml up --force-recreate --remove-orphans

makemigrations:
	docker compose exec web python manage.py makemigrations
migrate:
	docker compose exec web python manage.py migrate
createsuperuser:
	docker compose exec web python manage.py createsuperuser

restart:
	docker compose -f docker-compose.yml restart
stop:
	docker compose -f docker-compose.yml down
ps-docker: ## docker ps в нормальном виде
	docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}\t{{.Ports}}"
docs: ## Генерация документации
