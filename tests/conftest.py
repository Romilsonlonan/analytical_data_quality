from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest


@pytest.fixture(scope="session")
def project_root():
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def dbt_project():
    return os.getenv("DBT_TARGET", "dev")


@pytest.fixture(scope="session")
def database_url():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "admin")
    password = os.getenv("POSTGRES_PASSWORD", "admin123")
    db = os.getenv("POSTGRES_DB", "industrial_logistics")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


@pytest.fixture(scope="session")
def minio_config():
    return {
        "endpoint": os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        "access_key": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        "secret_key": os.getenv("MINIO_SECRET_KEY", "minioadmin123"),
        "bucket_bronze": "bronze",
        "bucket_silver": "silver",
        "bucket_gold": "gold",
    }


@pytest.fixture
def sample_orders_data():
    return [
        {
            "order_id": "ORD-001",
            "customer_id": "CUST-001",
            "order_date": "2024-01-15",
            "status": "delivered",
            "total_amount": 1500.00,
        },
        {
            "order_id": "ORD-002",
            "customer_id": "CUST-002",
            "order_date": "2024-01-16",
            "status": "shipped",
            "total_amount": 2300.50,
        },
    ]


@pytest.fixture
def sample_deliveries_data():
    return [
        {
            "delivery_id": "DEL-001",
            "order_id": "ORD-001",
            "carrier_id": "CAR-001",
            "delivery_date": "2024-01-18",
            "status": "delivered",
        },
        {
            "delivery_id": "DEL-002",
            "order_id": "ORD-002",
            "carrier_id": "CAR-001",
            "delivery_date": "2024-01-19",
            "status": "in_transit",
        },
    ]


@pytest.fixture
def sample_inventory_data():
    return [
        {
            "sku": "SKU-001",
            "product_name": "Produto A",
            "category": "Eletrônicos",
            "quantity_on_hand": 100,
            "warehouse_id": "WH-001",
        },
        {
            "sku": "SKU-002",
            "product_name": "Produto B",
            "category": "Móveis",
            "quantity_on_hand": 50,
            "warehouse_id": "WH-001",
        },
    ]


@pytest.fixture
def great_expectations_context(project_root):
    ge_path = project_root / "tests" / "data_quality" / "great_expectations"
    if ge_path.exists():
        try:
            if TYPE_CHECKING:
                pass
            else:
                import great_expectations as ge
                return ge.get_context(context_root_dir=str(ge_path))
        except ImportError:
            pass
    return None