#!/bin/bash
set -e

echo "Initializing MinIO buckets..."

MC_HOST_LOCAL="http://localhost:9000"

mc alias set local http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD || true

echo "Creating buckets..."
mc mb local/bronze --ignore-existing || true
mc mb local/silver --ignore-existing || true
mc mb local/gold --ignore-existing || true

echo "Setting bucket policies..."
mc anonymous set download local/bronze
mc anonymous set download local/silver
mc anonymous set download local/gold

echo "Enabling versioning..."
mc version enable local/bronze
mc version enable local/silver
mc version enable local/gold

echo "MinIO initialization complete!"
mc ls local