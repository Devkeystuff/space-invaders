setup:
	@echo "Installing dependencies"
	pip install black

format:
	@echo "Formatting app"
	black ./app
	
	@echo "Formatting api"
	black ./api

dev:
	docker-compose up