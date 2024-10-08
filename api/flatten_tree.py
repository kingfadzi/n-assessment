import json
import pandas as pd

# Configuration
json_filename = 'processes_tree.json'  # Input JSON file
output_csv_filename = 'tree_structure_custom_columns.csv'  # Output CSV file

def flatten_tree(node, path=None):
    """Recursively flatten the tree structure into rows."""
    if path is None:
        path = []  # Start with an empty path

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
                    rows.extend(flatten_tree(child, new_path))
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
        root = node['name']  # Assume 'name' at the root level corresponds to 'Root'
        print(f"Root Node: {root}")
        # Process the tree starting with the root name as the first element in the path
        rows.extend(flatten_tree(node, [root]))

    if not rows:
        print("Error: No rows generated, possibly due to unexpected data structure.")
        return pd.DataFrame()  # Return an empty DataFrame to avoid further errors

    # Define base column names according to the specified structure
    base_columns = ['Root', 'Architecture', 'Phase', 'Process', 'Process Category', 'Action']

    # Determine the maximum number of levels in the data
    max_levels = max(len(row) for row in rows)

    # Generate extra "Action" columns if needed
    if max_levels > len(base_columns):
        extra_columns = ['Action'] * (max_levels - len(base_columns))
        columns = base_columns + extra_columns
    else:
        columns = base_columns[:max_levels]

    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(rows, columns=columns)

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
