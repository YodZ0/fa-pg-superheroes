.PHONY: build up down logs test

# ========== Dev ==========
revision:
	alembic revision --autogenerate -m $(NAME)

migrate:
	alembic upgrade head

rollback:
	alembic downgrade $(NUM)


# ========== Prod ==========
build:
	docker compose -f docker-compose.yml up -d --build

down:
	docker compose -f docker-compose.yml down

logs:
	docker compose -f docker-compose.yml logs -f app


# ========== Test ==========
test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker compose -f docker-compose.test.yml down --remove-orphans
