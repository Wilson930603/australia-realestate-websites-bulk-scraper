import pandas as pd
from database import Database


db = Database()
df = pd.read_excel('Suburbs_in_Australia.xlsx', sheet_name='Sheet1')
df['Search String'] = df['Suburb Name'] + ', ' + df['State Abbreviation'] + ', real estate agent'

for i, row in df.iterrows():
    data = {
        'search_text': row['Search String'],
        'suburb': row['Suburb Name'],
        'state': row['State Abbreviation']
    }
    print(data)
    db.insert_suburb(data)
