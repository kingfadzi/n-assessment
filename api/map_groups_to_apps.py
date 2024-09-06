import requests
import pandas as pd
import xml.etree.ElementTree as ET
import logging

# Set up console logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

input_csv_file = 'names.csv'
output_csv_file = 'group_apps.csv'
cacert_path = '/path/to/cacert.pem'
api_base_url = 'https://api.example.com/group/{group_name}/applications'

def extract_app_names(xml_content):
    try:
        root = ET.fromstring(xml_content)
        return [app.get('name') for app in root.findall('.//application') if app.get('name')]
    except ET.ParseError as e:
        logging.error(f"Failed to parse XML: {e}")
        return []

group_df = pd.read_csv(input_csv_file)
logging.info(f"Read {len(group_df)} group names from {input_csv_file}")

results = []

for group_name in group_df['name']:
    url = api_base_url.format(group_name=group_name)
    try:
        logging.info(f"Making API request for group: {group_name}")
        response = requests.get(url, verify=cacert_path)

        # Print the full response for debugging
        print(f"Response for group {group_name}:\n{response.text}\n")

        if response.status_code == 200:
            app_names = extract_app_names(response.text)
            if app_names:
                logging.info(f"Extracted {len(app_names)} apps for group: {group_name}")
            else:
                logging.warning(f"No apps found for group: {group_name}")
            results.append({'groupName': group_name, 'applications': ', '.join(app_names)})
        else:
            logging.error(f"Failed to fetch data for group: {group_name}, Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for group: {group_name}, Error: {e}")

if results:
    pd.DataFrame(results).to_csv(output_csv_file, index=False)
    logging.info(f"Results written to {output_csv_file}")
else:
    logging.warning("No results to write to CSV.")
