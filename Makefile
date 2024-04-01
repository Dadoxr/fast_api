up:
	docker compose -f docker-compose-local.yml up -d
upb:
	docker compose -f docker-compose-local.yml up -d --build
down:
	docker compose -f docker-compose-local.yml down --remove-orphans

init:
	alembic init migrations

revision:
	alembic revision --autogenerate -m "comment"

upgrade:
	alembic upgrade heads

run:
	uvicorn main:app --reload