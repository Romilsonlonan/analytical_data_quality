# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-01-15

### Added

- Arquitetura Medallion completa (Bronze/Silver/Gold)
- Pipeline dbt com modelos staging, trusted, refined
- Docker Compose com PostgreSQL, MinIO, Airflow, Prometheus, Grafana
- Configurações de ambiente (dev, staging, prod)
- Policies de governança (acesso, classificação, retenção)
- SLAs definidos para pipelines e serviços
- Runbooks de incidente e reprocessamento
- Pre-commit hooks configurados
- Great Expectations para qualidade de dados
- Terraform para infraestrutura AWS
- ADR documents para decisões arquiteturais
- Documentação em Obsidian
- API FastAPI base

### Fixed

- Configurações de ambiente ajustadas
- Scripts de setup e migração criados

### Dependencies

- PostgreSQL 15
- MinIO latest
- Apache Airflow 2.8.1
- dbt latest
- Great Expectations 0.18+
- Python 3.12