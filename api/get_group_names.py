import json
import pandas as pd

json_file_path = 'data.json'

with open(json_file_path, 'r') as f:
    data = json.load(f)

if isinstance(data, list):
    names = [item['name'] for item in data if 'name' in item]
else:
    raise ValueError("The JSON format is not a list of dictionaries.")

df = pd.DataFrame(names, columns=['name'])

csv_file_path = 'names.csv'  # Replace with your desired CSV file path
df.to_csv(csv_file_path, index=False)

print(f"Names successfully written to {csv_file_path}")
