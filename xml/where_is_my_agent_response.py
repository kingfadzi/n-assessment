import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML file
tree = ET.parse('where_is_my_agent_response.xml')  # Replace 'input.xml' with your XML file name
root = tree.getroot()

# Initialize a list to store the flattened data
flattened_data = []

# Loop through each Entry
for entry in root.findall('.//Entry'):
    entry_id = entry.get('id')

    # Loop through each category in the Entry
    for category in entry.findall('.//category'):
        category_name = category.get('name')

        # Loop through each region in the category
        for region in category.findall('.//region'):
            region_env = region.get('env')

            # Loop through each city in the region
            for city in region.findall('.//city'):
                city_inst = city.get('inst')

                # Loop through each nag in the city
                for nag in city.findall('.//nag'):
                    name = nag.get('name')
                    dc = nag.get('dc')
                    port = nag.get('port')
                    reachable = nag.get('reachable')
                    nodeid = nag.get('nodeid')
                    version = nag.get('version')

                    # Append the flattened record to the list
                    flattened_data.append({
                        'EntryID': entry_id,
                        'CategoryName': category_name,
                        'RegionEnv': region_env,
                        'CityInst': city_inst,
                        'Name': name,
                        'DC': dc,
                        'Port': port,
                        'Reachable': reachable,
                        'NodeID': nodeid,
                        'Version': version
                    })

# Convert the flattened data into a DataFrame
df = pd.DataFrame(flattened_data)

# Save to CSV
df.to_csv('where_is_my_agent_response.csv', index=False)  # Replace 'output.csv' with your desired output file name

# Display the DataFrame to ensure correct output
print(df)
