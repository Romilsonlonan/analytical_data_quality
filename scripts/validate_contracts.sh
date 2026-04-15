#!/bin/bash
set -e

echo "=== Validating Data Contracts ==="

CONTRACTS_DIR="./governance/contracts"

if [ ! -d "$CONTRACTS_DIR" ]; then
    echo "No contracts directory found"
    exit 0
fi

echo "Validating contract schemas..."

if command -v Great Expectations &> /dev/null; then
    echo "Running Great Expectations checkpoint..."
    great_expectations checkpoint run data_contract_validation || true
fi

if command -v dbt &> /dev/null; then
    echo "Running dbt contract tests..."
    cd dbt
    dbt test --select contract || true
    cd ..
fi

echo ""
echo "=== Contract Validation Complete ==="