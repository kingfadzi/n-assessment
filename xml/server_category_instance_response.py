import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML file
tree = ET.parse('server_category_instance_response.xml')  # Replace 'input.xml' with your actual XML file
root = tree.getroot()

# Initialize a list to store the flattened data
flattened_data = []

# Loop through each Entry
for entry in root.findall('.//Entry'):
    entry_id = entry.get('id')

    # Loop through each MgmtGroup in the Entry
    for mgmt_group in entry.findall('.//MgmtGroup'):
        mgmt_group_name = mgmt_group.get('name')

        # Loop through each Business in the MgmtGroup
        for business in mgmt_group.findall('.//Business'):
            business_name = business.get('name')

            # Loop through each Area in the Business
            for area in business.findall('.//Area'):
                area_name = area.get('name')

                # Loop through each Application in the Area
                for application in area.findall('.//Application'):
                    application_name = application.get('name')

                    # Loop through each AppId in the Application
                    for appid in application.findall('.//AppId'):
                        appid_name = appid.get('name')

                        # Loop through each server in the AppId
                        for server in appid.findall('.//server'):
                            server_name = server.get('name')
                            nodeid = server.get('nodeid')

                            # Append the flattened record to the list
                            flattened_data.append({
                                'EntryID': entry_id,
                                'MgmtGroup': mgmt_group_name,
                                'Business': business_name,
                                'Area': area_name,
                                'Application': application_name,
                                'AppId': appid_name,
                                'ServerName': server_name,
                                'NodeID': nodeid
                            })

# Convert the flattened data into a DataFrame
df = pd.DataFrame(flattened_data)

# Save to CSV
df.to_csv('server_category_instance_response.csv', index=False)  # Replace 'output.csv' with your desired output file name

# Display the DataFrame to ensure correct output
print(df)
