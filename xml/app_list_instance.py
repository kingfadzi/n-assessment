import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML file
tree = ET.parse('app_list_instance.xml')  # Replace 'input.xml' with your actual XML file
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
        sn_id = application.get('sn_id')

        # Append the flattened record to the list
        flattened_data.append({
            'EntryID': entry_id,
            'ApplicationName': application_name,
            'NolioAppID': nolio_app_id,
            'SNID': sn_id
        })

# Convert the flattened data into a DataFrame
df = pd.DataFrame(flattened_data)

# Save to CSV
df.to_csv('app_list_instance.csv', index=False)  # Replace 'output.csv' with your desired output file name

# Display the DataFrame to ensure correct output
print(df)
