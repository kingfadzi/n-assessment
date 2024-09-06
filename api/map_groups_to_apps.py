import requests
import pandas as pd
import xml.etree.ElementTree as ET
import logging
import re

# Set up console logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

input_csv_file = 'names.csv'
output_csv_file = 'group_apps.csv'
cacert_path = '/path/to/cacert.pem'
api_base_url = 'https://api.example.com/group/{group_name}/applications'

# Function to clean and extract XML content by removing unwanted characters
def clean_xml_response(response_text):
    cleaned_xml = re.sub(r'[^\x00-\x7F]+', '', response_text)  # Remove non-ASCII characters
    cleaned_xml = cleaned_xml.strip()  # Remove leading and trailing whitespace/newlines
    return cleaned_xml

# Function to extract application names from the XML
def extract_app_names(xml_content):
    try:
        root = ET.fromstring(xml_content)

        # Debug: Print the root XML element to inspect the structure
        logging.debug(f"Root element: {ET.tostring(root, encoding='unicode')}")

        # Find all <application> elements in the entire XML document
        applications = root.findall(".//application")

        # Debug: Print all application elements found
        logging.debug(f"Found application elements: {applications}")

        # Extract the 'name' attribute from each <application> element
        app_names = [app.get('name') for app in applications if app.get('name')]

        # Debug: Print the application names found
        logging.debug(f"Extracted application names: {app_names}")

        return app_names
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

        # Clean the response and print for debugging
        cleaned_response = clean_xml_response(response.text)
        print(f"Cleaned Response for group {group_name}:\n{cleaned_response}\n")

        if response.status_code == 200:
            app_names = extract_app_names(cleaned_response)
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
