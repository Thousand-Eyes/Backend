.PHONY: install run build clean test help

help:
	@echo "Available commands:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make run         - Run the application with uvicorn"
	@echo "  make build       - Build the Docker image"
	@echo "  make clean       - Remove cache and build files"
	@echo "  make test        - Run tests with pytest"

install:
	pip install -r requirements.txt

run:
	uvicorn src.oaa.main:app --reload

build:
	docker build -t coding-butler-backend:latest .

clean:
	find . -type f -name "*.pyc" | xargs rm -f
	find . -type d -name "__pycache__" | xargs rm -rf
	rm -rf .venv

test:
	pytest