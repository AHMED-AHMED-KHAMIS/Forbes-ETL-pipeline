from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from extract import extract
from transform import transform
from load import load


def extract_task():
    df = extract()
    df.to_csv("/opt/airflow/data/extracted.csv", index=False)

def transform_task():
    df = pd.read_csv("/opt/airflow/data/extracted.csv")
    df = transform(df)
    df.to_csv("/opt/airflow/data/transformed.csv", index=False)

def load_task():
    df = pd.read_csv("/opt/airflow/data/transformed.csv")
    load(df)

default_args = {
    'owner': 'khamis',
    'start_date': datetime(2025, 6, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='etl_csv_pipeline',
    default_args=default_args,
    description='Three-step ETL pipeline using separate extract, transform, and load tasks',
    schedule_interval=None,
    catchup=False,
    tags=['etl', 'csv'],
) as dag:

    extract_op = PythonOperator(
        task_id='extract',
        python_callable=extract_task,
    )

    transform_op = PythonOperator(
        task_id='transform',
        python_callable=transform_task,
    )

    load_op = PythonOperator(
        task_id='load',
        python_callable=load_task,
    )

    extract_op >> transform_op >> load_op
