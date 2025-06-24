import sys
import os
import pandas as pd

# Add the dags folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dags')))

from transform import transform

def test_transform_removes_duplicates():
    sample_data = pd.DataFrame({
        'num': [1, 2],  
        'name': ['Bill Gates', 'Bill Gates'],
        'time': [2020, 2020],
        'annual_income': [100000, 100000],
        'main_industry': ['Tech', 'Tech'],
        'wealth_source_details': ['Microsoft', 'Microsoft'],
        'permanent_country': ['USA - Washington', 'USA - Washington'],
        'industry': ['Tech', 'Tech'],
        'daily_income': [12345, 12345],
        'name_cleaned': ['Bill Gates', 'Bill Gates'],
        'countries': ['USA', 'USA'],
        'state': ['', ''],
        'headquarters': ['Redmond', 'Redmond'],
        'gender': ['M', 'M'],
        'age': [65, 65]
    })

    transformed = transform(sample_data)
    unique_names = transformed.groupby(['name', 'year']).size().reset_index()
    
    # Ensure each name appears only once per year
    assert all(unique_names.groupby('year')['name'].count() == 1)
