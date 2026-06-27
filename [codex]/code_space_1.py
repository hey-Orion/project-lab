from datetime import datetime, timedelta
from aiflow import DAG
from aiflow.operators.python import PythonOperator

from Bravo.src.main import run_extraction, run_validation 

default_args = { what is args and why is the block used in dag 
    "owner": "Bravo",
    "depends_on_past": False,
    "retries": 1, 
    "retry_delay": timedelta(minutes=2), what is timedelta 
}


with DAG(
    dag_id="test_AA",
    default_args=default_args, what is default_args and what is this line doing 
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False, this is to run the todays contaner right not the old once
    tags=["dataops"], what is tags and what is it doing 
) as dag:


task_1 = PythonOperator(
    task_id="fetcher",
    python_callable=run_extraction,
)

task_2 = PythonOperator(
    task_id="cleaner",
    python_callable=run_validation, what is python_callable and what is it doing 
)

task_1 >> task_2 