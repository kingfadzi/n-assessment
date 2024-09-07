import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML file
tree = ET.parse('input.xml')  # Replace 'input.xml' with your actual XML file
root = tree.getroot()

# Initialize a list to store the flattened data
flattened_data = []

# Loop through each Entry
for entry in root.findall('.//Entry'):
    entry_id = entry.get('id')

    # Loop through each application in the Entry
    for application in entry.findall('.//application'):
        application_name = application.get('name')
        nolio_app_id = application.get('nolio_app_id')
        sn_ids = application.get('sn_id')

        # Split the sn_id values by semicolon, and create a row for each one
        for sn_id in sn_ids.split(';'):
            # Append the flattened record to the list
            flattened_data.append({
                'Environment': entry_id,
                'ApplicationName': application_name,
                'NolioAppID': nolio_app_id,
                'SNID': sn_id.strip()  # Ensure any leading/trailing whitespace is removed
            })

# Convert the flattened data into a DataFrame
df = pd.DataFrame(flattened_data)

# Save to CSV
df.to_csv('output.csv', index=False)  # Replace 'output.csv' with your desired output file name

# Display the DataFrame to ensure correct output
print(df)
