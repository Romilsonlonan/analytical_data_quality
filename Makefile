.PHONY: help install setup up down logs test lint format clean dbt-run dbt-test quality-check jenkins-start jenkins-logs jenkins-stop

help:
	@echo "Industrial Logistics Platform - Make Commands"
	@echo ""
	@echo "Setup & Development:"
	@echo "  make install      - Install dependencies"
	@echo "  make setup        - Initial project setup"
	@echo "  make dev          - Start development environment"
	@echo ""
	@echo "Docker:"
	@echo "  make up           - Start all services"
	@echo "  make down         - Stop all services"
	@echo "  make logs         - View logs"
	@echo "  make restart      - Restart services"
	@echo ""
	@echo "Jenkins:"
	@echo "  make jenkins-start   - Start Jenkins"
	@echo "  make jenkins-logs    - View Jenkins logs"
	@echo "  make jenkins-stop    - Stop Jenkins"
	@echo ""
	@echo "Database:"
	@echo "  make migrate      - Run migrations"
	@echo "  make seed         - Seed data"
	@echo ""
	@echo "dbt:"
	@echo "  make dbt-deps     - Install dbt dependencies"
	@echo "  make dbt-run      - Run dbt models"
	@echo "  make dbt-test     - Run dbt tests"
	@echo ""
	@echo "Quality:"
	@echo "  make quality      - Run data quality checks"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make test         - Run tests"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Clean temporary files"

install:
	poetry install

setup:
	bash scripts/setup.sh

dev:
	docker-compose up -d

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

migrate:
	bash scripts/run_migrations.sh

seed:
	bash scripts/seed_data.sh

dbt-deps:
	cd dbt && dbt deps

dbt-run:
	cd dbt && dbt run

dbt-test:
	cd dbt && dbt test

dbt-docs:
	cd dbt && dbt docs generate && dbt docs serve

quality:
	python -m pytest tests/data_quality -v

lint:
	ruff check src/ tests/

format:
	black src/ tests/

test:
	python -m pytest tests/ -v --cov=src

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage

# Jenkins
jenkins-start:
	docker-compose up -d jenkins
	@echo "Jenkins starting at http://localhost:8081"

jenkins-logs:
	docker-compose logs -f jenkins

jenkins-stop:
	docker-compose stop jenkins

jenkins-password:
	@docker exec ilp-jenkins cat /var/jenkins_home/secrets/initialAdminPassword

.DEFAULT_GOAL := help