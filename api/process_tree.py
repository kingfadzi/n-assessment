import json
import os

# Define paths for the files
project_dir = '.'  # Set your project directory here, assuming current directory
data_dir = os.path.join(project_dir, 'data')
json_file = os.path.join(data_dir, 'data.json')
input_json_file = os.path.join(project_dir, 'processes_tree.json')  # Input file

# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

# Step 1: Load your processes_tree JSON data from disk
with open(input_json_file, 'r') as f:
    processes_tree_data = json.load(f)

# Function to transform the data
def transform_node(node):
    return {
        "name": node["name"],
        "description": node.get("description", ""),
        "type": node["type"],
        "id": node["id"],
        "children": [transform_node(child) for child in node.get("nodes", [])]
    }

def transform_data(data):
    return [transform_node(node) for node in data["list"]]

# Transform the processes_tree data
transformed_data = transform_data(processes_tree_data)

# Step 2: Write the transformed data to data.json
with open(json_file, 'w') as outfile:
    json.dump(transformed_data, outfile, indent=4)

print(f'Transformed data written to {json_file}.')
