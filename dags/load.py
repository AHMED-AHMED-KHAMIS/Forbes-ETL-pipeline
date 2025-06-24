import os
import pandas as pd
from sqlalchemy import create_engine

def load(df):
    # Save CSV locally 
    output_path = "/opt/airflow/data/output.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved transformed CSV to {output_path}")

    # PostgreSQL connection string
    user = 'airflow'
    password = 'airflow'
    host = 'khamis-postgres'
    port = '5432'
    database = 'airflow'
    table_name = 'forbes_billionaires'

    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)

    # Load data into PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Loaded data into PostgreSQL table: {table_name}")
