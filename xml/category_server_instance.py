import lxml.etree as ET
import pandas as pd

file_path = 'category_server_instance.xml'
tree = ET.parse(file_path)

def count_apps_by_mgmnt_group(tree):
    data = []
    mgmnt_groups = tree.xpath('//MgmntGroup')

    for mgmnt_group in mgmnt_groups:
        group_name = mgmnt_group.get('name')
        app_count = len(mgmnt_group.xpath('.//Application'))
        data.append({'MgmntGroup': group_name, 'ApplicationCount': app_count})

    return data

app_counts = count_apps_by_mgmnt_group(tree)

df = pd.DataFrame(app_counts)

print(df)
