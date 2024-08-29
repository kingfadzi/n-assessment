import lxml.etree as ET
import pandas as pd

file_path = 'category_server_instance.xml'
tree = ET.parse(file_path)
output_markdown_file = 'mgmnt_group_app_counts.md'  # The output Markdown file

def count_apps_by_mgmnt_group(tree):
    data = []

    mgmnt_groups = tree.xpath('//RESULT/Entry/RESULT/MgmntGroup')

    for mgmnt_group in mgmnt_groups:
        group_name = mgmnt_group.get('name')
        app_count = len(mgmnt_group.xpath('.//Business/Area/Application[not(AppId[starts-with(@name, "prod")])]'))
        data.append({'Mgmnt Group': group_name, 'ApplicationCount': app_count})

    return data

app_counts = count_apps_by_mgmnt_group(tree)

df = pd.DataFrame(app_counts)

df = df[df['ApplicationCount'] > 0]

df = df.sort_values(by='ApplicationCount', ascending=False)

df.to_markdown(output_markdown_file, index=False)

print(f"Markdown table written to: {output_markdown_file}")
