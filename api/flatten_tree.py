import json
import pandas as pd

# Configuration
json_filename = 'data/large_tree_dataset.json'  # Input JSON file
output_csv_filename = 'tree_structure.csv'  # Output CSV file

def flatten_tree(node, level=0, path=None):
    """Recursively flatten the tree structure into rows."""
    if path is None:
        path = []

    # Ensure node is a dictionary
    if isinstance(node, dict):
        if 'name' in node:
            # Extend the path with the current node's name
            new_path = path + [node['name']]
            print(f"Processing Node: {node['name']}, Path: {new_path}")

            # If the node has child nodes, recursively process them
            if 'nodes' in node and isinstance(node['nodes'], list) and node['nodes']:
                rows = []
                for child in node['nodes']:
                    rows.extend(flatten_tree(child, level + 1, new_path))
                return rows
            else:
                # If the node is a leaf, return the path as a row
                return [new_path]
        else:
            print(f"Warning: Node missing 'name' key: {node}")
            return [path]
    else:
        print(f"Warning: Unexpected node structure: {node}")
        return []

def tree_to_spreadsheet(data):
    """Convert tree data to a spreadsheet format."""
    rows = []
    for node in data:
        print(f"Root Node: {node['name']}")
        rows.extend(flatten_tree(node))

    if not rows:
        print("Error: No rows generated, possibly due to unexpected data structure.")
        return pd.DataFrame()  # Return an empty DataFrame to avoid further errors

    # Determine the maximum number of levels in the data
    max_levels = max(len(row) for row in rows)

    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(rows, columns=[f'Level {i+1}' for i in range(max_levels)])

    return df

# Load the JSON data
with open(json_filename) as f:
    data = json.load(f)['list']  # Access the 'list' key directly

print(f"Loaded JSON Data: {data}")

# Convert the tree to a DataFrame
df = tree_to_spreadsheet(data)

if not df.empty:
    # Save the DataFrame to a CSV file
    df.to_csv(output_csv_filename, index=False)
    print(f"Dataset successfully dumped into '{output_csv_filename}'")
else:
    print("Failed to generate CSV. Please check the JSON structure.")
