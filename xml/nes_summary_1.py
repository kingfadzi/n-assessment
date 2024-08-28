import lxml.etree as ET
import pandas as pd

file_path = 'nes_summary.xml'
output_markdown_file = 'nes_summary.md'  # Output Markdown file
tree = ET.parse(file_path)

def count_nes_by_region_and_city(tree):
    cities = tree.xpath('//Entry//region/city')

    results = [
        {
            'Environment': city.xpath('ancestor::Entry/@id')[0],
            'Region': city.xpath('ancestor::region/@env')[0],
            'City': city.get('inst'),
            'NES Count': len(city.xpath('./nes'))
        }
        for city in cities
    ]

    return results

nes_counts = count_nes_by_region_and_city(tree)

df = pd.DataFrame(nes_counts)

with open(output_markdown_file, 'w') as md_file:
    md_file.write(df.to_markdown(index=False))

print("\nFinal NES Count by Region and City:")
print(df)
