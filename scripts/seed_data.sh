#!/bin/bash
set -e

echo "=== Seeding Data ==="

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-industrial_logistics}"
DB_USER="${DB_USER:-admin}"
DB_PASSWORD="${DB_PASSWORD:-admin123}"

echo "Seeding dbt seeds..."
cd dbt
dbt seed --target dev || true

echo ""
echo "=== Seed Complete ==="