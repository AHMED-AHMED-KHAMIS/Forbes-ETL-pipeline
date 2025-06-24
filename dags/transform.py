import pandas as pd

def transform(df):
    # 1. Drop unwanted columns
    df = df.drop(columns=['num', 'industry', 'daily_income', 'name_cleaned', 'countries'])

    # 2. Rename columns
    df = df.rename(columns={
        'time': 'year',
        'annual_income': 'net_worth_usd',
        'main_industry': 'industry',
        'wealth_source_details': 'source_of_wealth',
        'permanent_country': 'country'
    })

    
    # 3. Sort by year ASC then net_worth_usd DESC
    df = df.sort_values(by=['year', 'net_worth_usd'], ascending=[True, False])

    # 4. Drop duplicates: keep only one record per person per year based on name and year
    df = df.drop_duplicates(subset=['name', 'year'], keep='first')
    

    # 5. Create rank per year (like SQL RANK PARTITION BY year ORDER BY net_worth_usd DESC)
    df['rank'] = df.groupby('year')['net_worth_usd'].rank(method='first', ascending=False).astype(int)

    # 6. Create global index column starting from 1
    df.insert(0, 'index', range(1, len(df) + 1))

    # 7. Reorder columns: index, rank, next 5 cols, then net_worth_usd, then rest
    cols = df.columns.tolist()
    fixed_order = ['index', 'rank'] + cols[1:7] + ['net_worth_usd'] + [col for col in cols if col not in ['index', 'rank'] + cols[1:7] + ['net_worth_usd']]
    df = df[fixed_order]

    # 8. Split country column by '-' into country and state/city
    country_split = df['country'].str.split('-', n=1, expand=True)
    df['country'] = country_split[0].str.strip()
    df['state/city'] = country_split[1].str.strip() if country_split.shape[1] > 1 else ''

    # 9. Fill missing values in 'state' with values from 'state/city'
    df['state'] = df['state'].fillna(df['state/city'])
    df['state'] = df['state'].replace('', pd.NA)
    df['state'] = df['state'].fillna(df['state/city'])

    # 10. Drop state/city column
    df = df.drop(columns=['state/city'])

    # 11. Fill all remaining missing values with 'N/A'
    df = df.fillna('N/A')

    # 12. Replace 'M;F' with 'M' in gender column
    df['gender'] = df['gender'].replace('M;F', 'M')

    # 13. Fix specific people ages
    fixed_ages = {
        'Anne Cox Chambers': 100,
        'Walter Haefner': 101,
        'Kirk Kerkorian': 98,
        'David Rockefeller, Sr.': 101,
        'Aloysio de Andrade Faria': 99,
        'Liliane Bettencourt': 94,
        'Henry Hillman': 98,
        'Kwee Liong Phing': 67,
        'Kenneth C Rowe': 76,
        'Muktar Widjaja': 40,
        'Saleh Al Rajhi': 88,
        'Walter Shorenstein': 95,
        'John Kluge': 95
    }
    df['age'] = df.apply(lambda row: fixed_ages[row['name']] if row['name'] in fixed_ages else row['age'], axis=1)

    # 14. Replace ; and , in source_of_wealth with -
    df['source_of_wealth'] = df['source_of_wealth'].str.replace(r'[;,]', ' - ', regex=True)

    # 15. Drop headquarters column
    df = df.drop(columns=['headquarters'])

    # 16. Clean state column: replace ';' with '-'
    df['state'] = df['state'].str.replace(';', '-', regex=False)

    return df
