import json
import random

# Configuration
levels = 4  # Number of levels in the tree
nodes_per_level = [30, 20, 50, 20]  # Number of nodes at each level (starting from level 1)
child_probability = [0.1, 0.1, 0.5, 0.3]  # Probability of each node having children at each level

def generate_tree(levels, nodes_per_level, child_probability):
    def create_node(level, node_id):
        """Create a single node in the tree."""
        node = {
            "name": f"Node L{level} N{node_id}",
            "description": f"A node at level {level}",
            "type": "branch" if level < levels else "leaf",
            "id": f"{level}-{node_id}",
            "children": []
        }
        return node

    def add_children(node, level):
        """Recursively add children to a node."""
        if level >= levels:
            return
        for i in range(1, nodes_per_level[level-1] + 1):
            if random.random() <= child_probability[level-1]:
                child_node = create_node(level + 1, i)
                add_children(child_node, level + 1)
                node["children"].append(child_node)

    # Start with the root node
    root = create_node(1, 1)
    add_children(root, 1)

    return root

# Generate the tree
large_tree = generate_tree(levels, nodes_per_level, child_probability)

# Save the tree to a JSON file
file_path = "data/large_tree_dataset.json"
with open(file_path, "w") as f:
    json.dump([large_tree], f, indent=4)

print(f"Dataset saved to {file_path}")
