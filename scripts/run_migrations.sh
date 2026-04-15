#!/bin/bash
set -e

echo "=== Running Database Migrations ==="

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-industrial_logistics}"
DB_USER="${DB_USER:-admin}"
DB_PASSWORD="${DB_PASSWORD:-admin123}"

POSTGRES_URL="postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"

echo "Database: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"

if [ -f "./infra/postgres/init.sql" ]; then
    echo "Running init.sql..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f ./infra/postgres/init.sql
fi

echo ""
echo "Running dbt migrations..."
cd dbt
dbt run --target dev || true

echo ""
echo "=== Migrations Complete ==="