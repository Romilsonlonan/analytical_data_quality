#!/bin/bash
set -e

echo "=== Industrial Logistics Platform - Setup ==="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Project directory: $PROJECT_DIR"

echo ""
echo "Checking Python version..."
python3 --version

echo ""
echo "Installing dependencies..."
poetry install --no-interaction --no-root


echo ""
echo "Setting up dbt..."
if [ -f "$PROJECT_DIR/dbt/profiles.yml.example" ]; then
    if [ ! -f "$HOME/.dbt/profiles.yml" ]; then
        mkdir -p "$HOME/.dbt"
        cp "$PROJECT_DIR/dbt/profiles.yml.example" "$HOME/.dbt/profiles.yml"
        echo "Created dbt profiles.yml from template"
    fi
fi

echo ""
echo "Installing dbt dependencies..."
cd "$PROJECT_DIR/dbt"
dbt deps || echo "dbt not installed, skipping..."

cd "$PROJECT_DIR"

echo ""
echo "Creating log directories..."
mkdir -p logs

echo ""
echo "Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Run 'make dev' to start the development environment"