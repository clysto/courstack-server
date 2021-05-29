dev:
	uvicorn --reload app:app

start:
	gunicorn -w 16 -k uvicorn.workers.UvicornWorker app:app

format:
	black . && isort .

lint:
	flake8

revision:
	alembic revision --autogenerate

migrate:
	alembic upgrade head
