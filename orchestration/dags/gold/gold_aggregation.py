"""
Gold Layer DAG - Data Aggregation
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
    "retry_delay": timedelta(minutes=15),
}


def aggregate_orders():
    """Aggregate orders metrics to gold layer"""
    print("Aggregating orders metrics...")
    pass


def run_dbt_gold():
    """Run dbt models for gold layer"""
    print("Running dbt gold models...")
    pass


def validate_gold():
    """Validate gold layer data quality"""
    print("Validating gold data quality...")
    pass


with DAG(
    "gold_aggregation",
    default_args=default_args,
    description="Aggregate and create metrics in gold layer",
    schedule_interval="0 */6 * * *",
    catchup=False,
    tags=["gold", "aggregation"],
) as dag:
    start = BashOperator(
        task_id="start",
        bash_command="echo 'Starting gold aggregation'",
    )

    aggregate = PythonOperator(
        task_id="aggregate_metrics",
        python_callable=aggregate_orders,
    )

    dbt = PythonOperator(
        task_id="run_dbt_models",
        python_callable=run_dbt_gold,
    )

    validate = PythonOperator(
        task_id="validate_gold",
        python_callable=validate_gold,
    )

    start >> aggregate >> dbt >> validate
