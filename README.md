# Industrial Logistics Platform

Plataforma de dados para gestão logística industrial com arquitetura Medallion (Bronze/Silver/Gold) e Domain-Driven Design (DDD).

## Stack Tecnológico

| Componente | Tecnologia |
|------------|------------|
| Database | PostgreSQL 15 |
| Object Storage | MinIO |
| Orchestration | Apache Airflow 2.8.1 |
| Transformação | dbt |
| Qualidade | Great Expectations |
| Observabilidade | Prometheus + Grafana |
| IaC | Terraform |

## Quick Start

```bash
# 1. Clone o projeto
git clone <repo>
cd analytical_data_quality

# 2. Configure o ambiente
cp .env.example .env
make setup

# 3. Inicie os serviços
make dev

# 4. Acesse
# - Airflow: http://localhost:8080 (admin/admin123)
# - Grafana: http://localhost:3000 (admin/admin123)
# - MinIO: http://localhost:9001 (minioadmin/minioadmin123)
```

## Estrutura do Projeto

```
├── config/          # Configurações por ambiente
├── data/            # Data Lake (bronze/silver/gold)
├── dbt/             # Modelos dbt
├── docs/            # Documentação
├── governance/      # Políticas, SLAs, contratos
├── infra/          # Docker, Terraform
├── observability/  # Monitoramento
├── orchestration/  # Airflow DAGs
├── scripts/        # Scripts utilitários
├── src/            # Código Python (DDD)
└── tests/          # Testes
```

## Comandos

| Comando | Descrição |
|---------|-----------|
| `make dev` | Iniciar ambiente desenvolvimento |
| `make dbt-run` | Executar modelos dbt |
| `make quality` | Verificar qualidade de dados |
| `make test` | Executar testes |
| `make lint` | Verificar código |

## Arquitetura de Dados

```
Fontes → Bronze (Raw) → Silver (Trusted) → Gold (Refined) → Consumidores
```

## Documentação

- [Arquitetura](docs/architecture/overview.md)
- [ADR](docs/adr/)
- [Runbooks](docs/runbooks/)
- [Obsidian](docs/obsidian/)

## Licença

MIT