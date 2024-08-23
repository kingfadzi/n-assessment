import pandas as pd
from tabulate import tabulate  # Explicit import of tabulate

# Load data from CSV
df = pd.read_csv('sample_data.csv')

# Strip any whitespace from column names
df.columns = df.columns.str.strip()

# Print columns to check
print("Columns in the DataFrame:", df.columns.tolist())

# Configuration for column names (adjust based on the output of print above)
column_config = {
    'app_name': 'AppName',      # Ensure this matches exactly
    'lob': 'LOB',               # Ensure this matches exactly
    'environment': 'Environment',  # Ensure this matches exactly
    'criticality': 'Criticality',  # Ensure this matches exactly
    'strategy': 'Strategy',        # Ensure this matches exactly
    'offering_status': 'OfferingStatus',  # Ensure this matches exactly
    'deployments': 'Deployments'  # Ensure this matches exactly
}

# Verify that the key columns exist in the DataFrame
for key, col_name in column_config.items():
    if col_name not in df.columns:
        print(f"Error: Column '{col_name}' for key '{key}' not found in DataFrame.")
        # Handle the missing column appropriately (e.g., raise an error, provide a default value, etc.)

# 1. Calculate the total number of unique applications per LOB
try:
    total_apps_per_lob = df.groupby(column_config['lob'])[column_config['app_name']].nunique().reset_index(name='Total Apps')
    print("Total Apps per LOB calculated successfully.")
except KeyError as e:
    print(f"KeyError during grouping by '{column_config['lob']}':", e)

# 2. Calculate the number of applications in Prod, UAT, and Dev environments per LOB
try:
    env_counts = df.groupby([column_config['lob'], column_config['environment']])[column_config['app_name']].nunique().unstack(fill_value=0).reset_index()
    env_counts.columns.name = None  # Remove the name from columns for easier access
    env_counts = env_counts.rename(columns={'Prod': 'Prod Apps', 'UAT': 'UAT Apps', 'Dev': 'Dev Apps'})
    print("Environment counts calculated successfully.")
except KeyError as e:
    print(f"KeyError during grouping by '{column_config['lob']}' and '{column_config['environment']}':", e)

# 3. Identify the most critical application in Prod for each LOB and its details
try:
    prod_critical = df[df[column_config['environment']] == 'Prod'].sort_values(
        [column_config['criticality'], column_config['strategy']], ascending=[True, True])
    most_critical_prod = prod_critical.groupby(column_config['lob']).first().reset_index()
    print("Most critical Prod app identified successfully.")
except KeyError as e:
    print(f"KeyError during sorting or grouping:", e)

# 4. Merge the results into a single DataFrame
try:
    result = pd.merge(total_apps_per_lob, env_counts, on=column_config['lob'])
    result = pd.merge(result, most_critical_prod[
        [column_config['lob'], column_config['app_name'], column_config['deployments'], column_config['criticality'], column_config['strategy'], column_config['offering_status']]
    ], on=column_config['lob'])
    print("Results merged successfully.")
except KeyError as e:
    print(f"KeyError during merging:", e)

result = result.rename(columns={
    column_config['app_name']: 'Most Critical Prod App',
    column_config['deployments']: 'Deployments',
    column_config['strategy']: 'Strategy',
    column_config['criticality']: 'Criticality',
    column_config['offering_status']: 'OfferingStatus'
})

# Debugging step: Print the columns of the result DataFrame
print("Columns in result DataFrame:", result.columns.tolist())

# 5. Reorder the columns to make 'Deployments' the second column
try:
    result = result[['LOB', 'Deployments', 'Total Apps', 'Prod Apps', 'UAT Apps', 'Dev Apps', 'Most Critical Prod App', 'Strategy', 'Criticality', 'OfferingStatus']]
except KeyError as e:
    print("Error reordering columns:", e)
    print("Available columns:", result.columns.tolist())
    # Handle the missing columns appropriately

# 6. Write the result to a Markdown file
with open('result_summary.md', 'w') as f:
    f.write(tabulate(result, headers='keys', tablefmt='pipe', showindex=False))

print("Results written to 'result_summary.md'")
