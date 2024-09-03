import pandas as pd
import json

# Path to the JSON file
json_file_path = 'large_tree_dataset.json'  # Replace with your actual file path

# Configuration for column names (set as variables)
column1_name = 'Root'
column2_name = 'Branch'
column3_name = 'Leaf'
column4_name = 'Subleaf'
# Add more column names as needed

# Store the column names in a list
custom_column_names = [column1_name, column2_name, column3_name, column4_name]

# Load the JSON data from the file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Recursive function to flatten the hierarchy
def flatten_hierarchy(node, path=None, result=None):
    if result is None:
        result = []
    if path is None:
        path = []

    # Append the current node's name to the path
    new_path = path + [node['name']]

    # If there are no more children, add the path to the result
    if not node.get('nodes'):
        result.append(new_path)
    else:
        # Recursively process child nodes
        for child in node['nodes']:
            flatten_hierarchy(child, new_path, result)

    return result

# Flatten the hierarchy for each item in the list
all_paths = []
for item in data['list']:
    all_paths.extend(flatten_hierarchy(item))

# Create a DataFrame, automatically adjusting for the variable depth
df = pd.DataFrame(all_paths)

# Determine the maximum depth of the hierarchy
max_depth = df.shape[1]

# Ensure the custom column names list is as long as the maximum depth
if len(custom_column_names) < max_depth:
    custom_column_names.extend([f'Level_{i+1}_Name' for i in range(len(custom_column_names), max_depth)])

# Rename the columns using the custom names
df.columns = custom_column_names[:max_depth]

# Skip the first column 'Root'
df_reduced = df.iloc[:, 1:]  # Exclude the first column

# Update column names to skip 'Root'
reduced_column_names = custom_column_names[1:max_depth]  # Exclude the first column name
df_reduced.columns = reduced_column_names

# Save the reduced DataFrame to a CSV file
output_csv_path = 'output_hierarchy_custom_columns.csv'  # Replace with desired output path
df_reduced.to_csv(output_csv_path, index=False)

# Save the reduced DataFrame to a Markdown file
output_md_path = 'output_hierarchy_custom_columns.md'  # Replace with desired output path
with open(output_md_path, 'w') as f:
    f.write(df_reduced.to_markdown(index=False))

# Display the reduced DataFrame
df_reduced
