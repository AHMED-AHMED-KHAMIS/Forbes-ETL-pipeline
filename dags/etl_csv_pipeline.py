from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from extract import extract
from transform import transform
from load import load

default_args = {
    'owner': 'khamis',
    'start_date': datetime(2025, 6, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def extract_transform_load():
    df = extract()
    df = transform(df)
    load(df)

with DAG(
    dag_id='etl_csv_pipeline',
    default_args=default_args,
    description='Simple ETL pipeline for CSV using pandas',
    schedule_interval=None,
    catchup=False,
    tags=['etl', 'csv'],
) as dag:

    run_etl = PythonOperator(
        task_id='extract_transform_load',
        python_callable=extract_transform_load,
    )
