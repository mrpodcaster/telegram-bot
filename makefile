include .env

build:
	docker compose build web

dev: format lint build
	docker compose up --remove-orphans -d

lint:
	ruff check --fix ../telegram-bot

format:
	ruff format ../telegram-bot

makemigrations:
	poetry run python ./manage.py makemigrations

migrate: makemigrations
	python ./manage.py migrate

createsuperuser:
	poetry run python ./manage.py createsuperuser

