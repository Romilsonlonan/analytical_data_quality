from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import Any, List

class IndustrialLogisticsPostgresHook(PostgresHook):
    """
    Custom Hook for Industrial Logistics Platform.
    Wraps the standard PostgresHook with project-specific defaults.
    """
    
    def __init__(self, postgres_conn_id: str = "postgres_default", *args, **kwargs):
        super().__init__(postgres_conn_id=postgres_conn_id, *args, **kwargs)

    def get_staging_data(self, table_name: str) -> List[Any]:
        """
        Helper method to fetch data from the staging schema.
        """
        sql = f"SELECT * FROM staging.{table_name}"
        return self.get_records(sql)

    def log_data_quality(self, dataset: str, check: str, status: str, message: str):
        """
        Helper to log data quality results into the governance schema.
        """
        sql = """
            INSERT INTO governance.data_quality_log (dataset_name, check_name, status, message)
            VALUES (%s, %s, %s, %s)
        """
        self.run(sql, parameters=(dataset, check, status, message))
