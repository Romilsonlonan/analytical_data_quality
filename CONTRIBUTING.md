# Contributing Guide

## Como Contribuir

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Padrões de Código

### Python
- Use `black` para formatação (linha máx: 100)
- Use `ruff` para linting
- Use `mypy` para type checking
- Docstrings em formato Google

### SQL (dbt)
- Nome de modelos em snake_case
- Camadas: staging, trusted, refined
- Sempre adicione descrições
- Inclua testes

### Git
- Commits em português ou inglês
- Use Conventional Commits:
  - `feat: nova funcionalidade`
  - `fix: correção de bug`
  - `docs: documentação`
  - `refactor: refatoração`
  - `test: testes`

## Testing

```bash
# Execute testes
make test

# Execute lint
make lint

# Execute qualidade de dados
make quality
```

## Ambiente de Desenvolvimento

```bash
# Setup
make setup

# Iniciar serviços
make dev
```

## Commits Significativos

- Sempre inclua contexto
- Reference issues quando aplicável
- Explique o "porquê" para mudanças não óbvias