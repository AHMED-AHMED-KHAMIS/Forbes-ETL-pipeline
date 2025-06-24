import pandas as pd

def extract():
    input_path = "/opt/airflow/data/input.csv"
    df = pd.read_csv(input_path)
    return df
