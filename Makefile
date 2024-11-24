# Makefile
.PHONY: build up down logs test clean

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose run user-service pytest
	docker-compose run recipe-service pytest
	docker-compose run ingredient-service pytest
	docker-compose run rating-service pytest
	docker-compose run mealplan-service pytest

clean:
	docker-compose down -v
	docker system prune -f