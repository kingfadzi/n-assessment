import pandas as pd

# Load the CSV dataset
df = pd.read_csv('servers.csv')

# Function to save data to a markdown file without row indices
def save_to_markdown(data, file_name, header):
    with open(file_name, 'a') as f:
        f.write(f"## {header}\n")
        f.write(data.to_markdown(index=False))  # Set index=False to remove row numbers
        f.write("\n\n")

# Summary statistics for categorical columns
categorical_summary = df.describe(include=['object', 'bool'])
print("\nSummary statistics for categorical columns:")
print(categorical_summary)

# Distribution of operating systems
os_distribution = df['osType'].value_counts().reset_index(name='count').rename(columns={'index': 'osType'}).sort_values(by='count', ascending=False)
print("\nOperating System Distribution:")
print(os_distribution)

# Reachability distribution
reachability_distribution = df['reachable'].value_counts().reset_index(name='count').rename(columns={'index': 'reachable'}).sort_values(by='count', ascending=False)
print("\nReachability Distribution:")
print(reachability_distribution)

# Server group distribution with osType and reachability
group_os_reach_distribution = df.groupby(['serverGroups', 'osType', 'reachable']).size().reset_index(name='count')
group_os_reach_distribution = group_os_reach_distribution.sort_values(by='count', ascending=False)
print("\nServer Group Distribution with OS Type and Reachability:")
print(group_os_reach_distribution)

# Cross-tabulation of 'osType' and 'reachable'
crosstab = pd.crosstab(df['osType'], df['reachable']).reset_index()
print("\nCross-tabulation of OS type and reachability:")
print(crosstab)

# Writing results to a Markdown file
markdown_file = 'analysis_results.md'
open(markdown_file, 'w').close()  # Clear previous contents
save_to_markdown(categorical_summary, markdown_file, "Summary statistics for categorical columns")
save_to_markdown(os_distribution, markdown_file, "Operating System Distribution")
save_to_markdown(reachability_distribution, markdown_file, "Reachability Distribution")
save_to_markdown(group_os_reach_distribution, markdown_file, "Server Group Distribution with OS Type and Reachability")
save_to_markdown(crosstab, markdown_file, "Cross-tabulation of OS type and reachability")
