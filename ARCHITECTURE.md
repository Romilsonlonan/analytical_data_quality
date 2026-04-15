# Industrial Logistics Platform - Arquitetura

## Visão Geral

Plataforma de dados para gestão logística industrial utilizando arquitetura Medallion (Bronze/Silver/Gold) com Domain-Driven Design (DDD).

## Stack Tecnológico

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| Database | PostgreSQL | 15 |
| Object Storage | MinIO | Latest |
| Orchestration | Apache Airflow | 2.8.1 |
| Transformação | dbt | Latest |
| Qualidade | Great Expectations | 0.18+ |
| Observabilidade | Prometheus + Grafana | Latest |
| IaC | Terraform | 1.0+ |
| Containers | Docker Compose | 3.8 |

## Arquitetura de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Lake (MinIO)                        │
├─────────────┬─────────────────┬─────────────────────────────────┤
│   Bronze    │     Silver      │              Gold               │
│  (Raw Data) │ (Cleaned Data)  │     (Business Metrics)         │
│   Parquet   │    Parquet      │          Parquet               │
└─────────────┴─────────────────┴─────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Warehouse (PostgreSQL)                  │
├─────────────┬─────────────────┬─────────────────────────────────┤
│   staging   │     trusted     │             refined             │
│  (dbt)      │     (dbt)       │            (dbt)               │
└─────────────┴─────────────────┴─────────────────────────────────┘
```

## Estrutura de Diretórios

```
.
├── config/              # Configurações por ambiente
│   ├── environments/   # dev, staging, prod
│   └── logging.yml     # Configuração de logs
├── data/               # Data Lake (Bronze/Silver/Gold)
├── dbt/                # Modelos dbt
├── governance/         # Contratos, lineage, políticas, SLA
├── infra/              # Infraestrutura (Docker, Terraform)
├── observability/       # Monitoramento
├── orchestration/      # Airflow DAGs
├── scripts/            # Scripts utilitários
├── services/           # Microsserviços
├── src/                # Código Python (DDD)
└── tests/              # Testes
```

## Configuração de Ambientes

### Desenvolvimento
- Database local (PostgreSQL)
- MinIO local
- Airflow integrado
- Qualidade de dados ativada
- Logs em modo DEBUG

### Staging
- Banco compartilhado
- MinIO cloud
- Airflow remoto
- Logging INFO
- SLAs definidos

### Produção
- RDS PostgreSQL
- S3/GCS
- CeleryExecutor (Airflow)
- Logging WARNING
- Alta disponibilidade

## Fluxo de Dados

1. **Ingestão**: Fontes → Bronze (Raw)
2. **Transformação Bronze→Silver**: Limpeza, padronização
3. **Transformação Silver→Gold**: Agregações, métricas
4. **Exposição**: dbt models → DW → API/BI

## Governança

- **Contratos**: Schemas definidos em `governance/contracts/`
- **Lineage**: Rastreabilidade em `governance/lineage/`
- **Políticas**: Access control, classificação, retenção
- **SLA**: Definições em `governance/sla/`

## Observabilidade

- **Métricas**: Prometheus (prometheus.yml)
- **Dashboards**: Grafana + Superset
- **Logs**: Centralizados via logging.yml
- **Alertas**: Regras em `observability/alerts/`

## Qualidade de Dados

- Great Expectations para validação
- Scripts em `tests/data_quality/`
- checkpoints: bronze_quality, silver_quality, gold_quality

## Comandos Úteis

```bash
make dev          # Iniciar ambiente desenvolvimento
make dbt-run      # Executar modelos dbt
make quality      # Verificar qualidade de dados
make test         # Executar testes
```