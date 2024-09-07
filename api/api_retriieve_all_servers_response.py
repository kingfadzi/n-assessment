import json
import pandas as pd

# Load JSON from a file
with open('data.json', 'r') as f:
    data = json.load(f)

# Flatten the JSON data
df = pd.json_normalize(data['list'])

# Explode 'serverGroups' into rows
df = df.explode('serverGroups')

# Rename the 'serverGroups' column to 'serverGroup'
df.rename(columns={'serverGroups': 'serverGroup'}, inplace=True)

# Save to CSV
df.to_csv('flattened_data.csv', index=False)

print(df)
