import lxml.etree as ET
from collections import defaultdict

# Load and parse the XML file
file_path = 'nes_summary.xml'  # Replace with your actual XML file path
tree = ET.parse(file_path)

def count_nes_by_region_and_city_with_xpath(tree):
    results = {}

    # Find all Entry elements
    entries = tree.xpath('//Entry')

    for entry in entries:
        entry_id = entry.get('id')  # This could represent environments like dev, prod, uat
        env_results = defaultdict(lambda: defaultdict(int))

        # Use XPath to find all regions and their cities within the current Entry
        regions = entry.xpath('.//region')

        for region in regions:
            region_env = region.get('env')

            # For each region, get all cities
            cities = region.xpath('./city')

            for city in cities:
                city_inst = city.get('inst')

                # Count the NES elements directly using XPath
                nes_count = len(city.xpath('./nes'))

                # Store the count in the results
                env_results[region_env][city_inst] += nes_count

        results[entry_id] = dict(env_results)

    return results

# Get the NES count by region and city using XPath
nes_counts = count_nes_by_region_and_city_with_xpath(tree)

# Print the results
for entry, regions in nes_counts.items():
    print(f"Environment: {entry}")
    for region, cities in regions.items():
        print(f"  Region: {region}")
        for city, count in cities.items():
            print(f"    City: {city}, NES Count: {count}")
