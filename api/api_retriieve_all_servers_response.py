import json
import pandas as pd

with open('data.json', 'r') as f:
    data = json.load(f)

df = pd.json_normalize(data['list'])

df['serverGroups'] = df['serverGroups'].apply(lambda x: ','.join(x))
df.rename(columns={'serverGroups': 'serverGroup'}, inplace=True)

df.to_csv('flattened_data.csv', index=False)

print(df)
