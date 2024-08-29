import lxml.etree as ET
import pandas as pd

file_path = 'app_list_instance.xml'
tree = ET.parse(file_path)

def extract_applications(tree):

    applications = tree.xpath('//Entry/RESULT/application')

    results = [
        {
            'Entry ID': app.xpath('ancestor::Entry/@id')[0],
            'Application Name': app.get('name'),
            'SN ID': app.get('sn_id')
        }
        for app in applications
    ]

    return results

app_data = extract_applications(tree)

df = pd.DataFrame(app_data)

output_markdown_file = 'app_list_instance.md'
with open(output_markdown_file, 'w') as md_file:
    md_file.write(df.to_markdown(index=False))

# Display the final DataFrame
print("\nApplication Summary by Entry:")
print(df)
