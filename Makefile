.PHONY: up down logs test shell migrate

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	docker compose run --rm test

shell:
	docker compose exec web bash

migrate:
	docker compose exec web python manage.py migrate
