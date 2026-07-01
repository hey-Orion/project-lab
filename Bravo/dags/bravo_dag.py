from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator 

from src.tasks import run_extraction, run_validation 

default_args = {
    "owner": "Bravo",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="007",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["bro"],
) as dag:

    task_1 = PythonOperator(
        task_id="one",
        python_callable=run_extraction,
        provide_context=True,
    )

    task_2 = PythonOperator(
        task_id="two",
        python_callable=run_validation, 
        provide_context=True,
    )

    task_1 >> task_2