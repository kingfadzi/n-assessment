import lxml.etree as ET
import pandas as pd

file_path = 'nes_summary.xml'
output_markdown_file = 'nes_summary.md'  # Output Markdown file
tree = ET.parse(file_path)

def count_nes_by_region_and_city_with_xpath(tree):
    results = []

    entries = tree.xpath('//Entry')

    for entry in entries:
        entry_id = entry.get('id')

        region_city_pairs = entry.xpath('.//region/@env | .//city/@inst')

        for region_env in set(region_city_pairs[::2]):
            cities = entry.xpath(f'.//region[@env="{region_env}"]/city')

            for city in cities:
                city_inst = city.get('inst')
                nes_count = len(city.xpath('./nes'))

                results.append({
                    'Environment': entry_id,
                    'Region': region_env,
                    'City': city_inst,
                    'NES Count': nes_count
                })

    return results

nes_counts = count_nes_by_region_and_city_with_xpath(tree)

df = pd.DataFrame(nes_counts)

with open(output_markdown_file, 'w') as md_file:
    md_file.write(df.to_markdown(index=False))

print("\nFinal NES Count by Region and City:")
print(df)
