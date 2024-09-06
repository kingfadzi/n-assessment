import json
import pandas as pd


json_file_path = 'data.json'  # Replace with your JSON file path

with open(json_file_path, 'r') as f:
    data = json.load(f)

if 'list' in data:
    names = [item['name'] for item in data['list'] if 'name' in item]
else:
    raise ValueError("The JSON structure doesn't contain a 'list' field.")

df = pd.DataFrame(names, columns=['name'])

csv_file_path = 'names.csv'  # Replace with your desired CSV file path
df.to_csv(csv_file_path, index=False)

print(f"Names successfully written to {csv_file_path}")
