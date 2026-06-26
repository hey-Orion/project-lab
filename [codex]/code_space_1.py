from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "dataops_bravo",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="bravo_v1",
    default_args=default_args,
    desc="airflow dag v1",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    def run_ingestion():
        print("step 1 ")
    
    def run_validation():
        print("step 2")

    one_task = PythonOperator(
        task_id="bravo_pull",
        python_callable=run_ingestion,
    )

    two_task = PythonOperator(
        task_id="bravo_clean",
        python_callable=run_validation,
    )

    one_task >> two_task