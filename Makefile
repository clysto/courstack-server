dev:
	uvicorn --reload app:app

start:
	uvicorn --no-access-log app:app

format:
	black . && isort .

lint:
	flake8

revision:
	alembic revision --autogenerate

migrate:
	alembic upgrade head
