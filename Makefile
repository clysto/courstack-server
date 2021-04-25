dev:
	uvicorn --reload app:app

lint:
	flake8
