import pandas as pd
from transform import transform

def test_transform_removes_duplicates():
    sample_data = pd.DataFrame({
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
    assert transformed['name'].nunique() == 1
