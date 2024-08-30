import json
import pandas as pd

# Configuration
json_filename = 'data/large_tree_dataset.json'  # Input JSON file
output_csv_filename = 'tree_structure.csv'  # Output CSV file

def flatten_tree(node, level=0, path=None):
    """Recursively flatten the tree structure into rows."""
    if path is None:
        path = []

    # Extend the path with the current node's name
    new_path = path + [node['name']]

    # If the node has children, recursively process them
    if 'children' in node and node['children']:
        rows = []
        for child in node['children']:
            rows.extend(flatten_tree(child, level + 1, new_path))
        return rows
    else:
        # If the node is a leaf, return the path as a row
        return [new_path]

def tree_to_spreadsheet(data):
    """Convert tree data to a spreadsheet format."""
    rows = []
    for node in data:
        rows.extend(flatten_tree(node))

    # Determine the maximum number of levels in the data
    max_levels = max(len(row) for row in rows)

    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(rows, columns=[f'Level {i+1}' for i in range(max_levels)])

    return df

# Load the JSON data
with open(json_filename) as f:
    data = json.load(f)

# Convert the tree to a DataFrame
df = tree_to_spreadsheet(data)

# Save the DataFrame to a CSV file
df.to_csv(output_csv_filename, index=False)

print(f"Dataset successfully dumped into '{output_csv_filename}'")
