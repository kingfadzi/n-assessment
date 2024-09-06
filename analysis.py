import pandas as pd

# Load the CSV dataset
df = pd.read_csv('servers.csv')

# Function to save data to a markdown file
def save_to_markdown(data, file_name, header):
    with open(file_name, 'a') as f:
        f.write(f"## {header}\n")
        f.write(data.to_markdown())
        f.write("\n\n")

# Summary statistics for categorical columns
categorical_summary = df.describe(include=['object', 'bool'])
print("\nSummary statistics for categorical columns:")
print(categorical_summary)

# Distribution of operating systems
os_distribution = df['osType'].value_counts()
print("\nOperating System Distribution:")
print(os_distribution)

# Reachability distribution
reachability_distribution = df['reachable'].value_counts()
print("\nReachability Distribution:")
print(reachability_distribution)

# Server state distribution
state_distribution = df['state'].value_counts()
print("\nServer State Distribution:")
print(state_distribution)

# Server group distribution
group_distribution = df['serverGroups'].value_counts()
print("\nServer Group Distribution:")
print(group_distribution)

# Frequency of combinations of 'osType' and 'state'
os_state_combination = df.groupby(['osType', 'state']).size().reset_index(name='count')
print("\nFrequency of OS type and state combinations:")
print(os_state_combination)

# Cross-tabulation of 'osType' and 'reachable'
crosstab = pd.crosstab(df['osType'], df['reachable'])
print("\nCross-tabulation of OS type and reachability:")
print(crosstab)

# Writing results to a Markdown file
markdown_file = 'analysis_results.md'
open(markdown_file, 'w').close()  # Clear previous contents
save_to_markdown(df.head(), markdown_file, "First few rows of the dataset")
save_to_markdown(categorical_summary, markdown_file, "Summary statistics for categorical columns")
save_to_markdown(os_distribution, markdown_file, "Operating System Distribution")
save_to_markdown(reachability_distribution, markdown_file, "Reachability Distribution")
save_to_markdown(state_distribution, markdown_file, "Server State Distribution")
save_to_markdown(group_distribution, markdown_file, "Server Group Distribution")
save_to_markdown(os_state_combination, markdown_file, "Frequency of OS type and state combinations")
save_to_markdown(crosstab, markdown_file, "Cross-tabulation of OS type and reachability")
