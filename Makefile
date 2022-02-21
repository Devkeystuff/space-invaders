setup:
	@echo "Installing dependencies"
	pip install black
	python -m venv venv

format:
	@echo "Formatting app"
	black ./app
	
	@echo "Formatting api"
	black ./api

dev:
	docker-compose up