"""
Bronze Layer DAG - Data Ingestion
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-engineer",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


def ingest_orders():
    """Ingest orders data to bronze layer"""
    print("Ingesting orders to bronze...")
    pass


def ingest_deliveries():
    """Ingest deliveries data to bronze layer"""
    print("Ingesting deliveries to bronze...")
    pass


def ingest_quali_vendas():
    """Ingest qualitative sales data to bronze layer"""
    import sys

    sys.path.insert(
        0, "/home/romilson/Projetos/Industrial-Logistic-Management/analytical_data_quality"
    )
    from src.pipelines.bronze.setor_vendas import quali_vendas

    result = quali_vendas.run_quali_vendas(source="excel", file_path="data/raw/quali_vendas.xlsx")
    print(f"Quali Vendas: {result}")
    return result


def validate_bronze():
    """Validate bronze layer data quality"""
    print("Validating bronze data quality...")
    pass


with DAG(
    "bronze_ingestion",
    default_args=default_args,
    description="Ingest raw data to bronze layer",
    schedule_interval="*/15 * * * *",
    catchup=False,
    tags=["bronze", "ingestion"],
) as dag:
    start = BashOperator(
        task_id="start",
        bash_command="echo 'Starting bronze ingestion'",
    )

    orders = PythonOperator(
        task_id="ingest_orders",
        python_callable=ingest_orders,
    )

    deliveries = PythonOperator(
        task_id="ingest_deliveries",
        python_callable=ingest_deliveries,
    )

    quali_vendas = PythonOperator(
        task_id="ingest_quali_vendas",
        python_callable=ingest_quali_vendas,
    )

    validate = PythonOperator(
        task_id="validate_bronze",
        python_callable=validate_bronze,
    )

    start >> [orders, deliveries, quali_vendas] >> validate
