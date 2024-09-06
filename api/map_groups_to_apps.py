import requests
import pandas as pd
import xml.etree.ElementTree as ET

input_csv_file = 'names.csv'
output_csv_file = 'group_apps.csv'
cacert_path = '/path/to/cacert.pem'
api_base_url = 'https://api.example.com/group/{group_name}/applications'

def extract_app_names(xml_content):
    root = ET.fromstring(xml_content)
    return [app.get('name') for app in root.findall('.//application') if app.get('name')]

group_df = pd.read_csv(input_csv_file)

results = []

for group_name in group_df['name']:
    url = api_base_url.format(group_name=group_name)
    response = requests.get(url, verify=cacert_path)

    if response.status_code == 200:
        app_names = extract_app_names(response.text)
        results.append({'groupName': group_name, 'applications': ', '.join(app_names)})
    else:
        print(f"Failed to fetch data for group: {group_name}")

pd.DataFrame(results).to_csv(output_csv_file, index=False)
print(f"Results written to {output_csv_file}")
