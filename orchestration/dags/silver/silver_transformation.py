"""
Silver Layer DAG - Data Transformation
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
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
}


def transform_staging_orders():
    """Transform orders from staging to trusted"""
    print("Transforming orders to silver...")
    pass


def transform_staging_deliveries():
    """Transform deliveries from staging to trusted"""
    print("Transforming deliveries to silver...")
    pass


def validate_silver():
    """Validate silver layer data quality"""
    print("Validating silver data quality...")
    pass


with DAG(
    "silver_transformation",
    default_args=default_args,
    description="Transform and clean data in silver layer",
    schedule_interval="0 * * * *",
    catchup=False,
    tags=["silver", "transformation"],
) as dag:
    start = BashOperator(
        task_id="start",
        bash_command="echo 'Starting silver transformation'",
    )

    orders = PythonOperator(
        task_id="transform_orders",
        python_callable=transform_staging_orders,
    )

    deliveries = PythonOperator(
        task_id="transform_deliveries",
        python_callable=transform_staging_deliveries,
    )

    validate = PythonOperator(
        task_id="validate_silver",
        python_callable=validate_silver,
    )

    start >> [orders, deliveries] >> validate
