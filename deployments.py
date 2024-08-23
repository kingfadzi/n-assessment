import pandas as pd
from tabulate import tabulate  # Explicit import of tabulate

# Load data from CSV
df = pd.read_csv('sample_data.csv')

# Strip any whitespace from column names
df.columns = df.columns.str.strip()

# Configuration for column names
column_config = {
    'app_name': 'AppName',
    'lob': 'LOB',
    'environment': 'Environment',
    'criticality': 'Criticality',
    'strategy': 'Strategy',
    'offering_status': 'OfferingStatus',
    'deployments': 'Deployments'
}

# 1. Calculate the total number of unique applications per LOB
total_apps_per_lob = df.groupby(column_config['lob'])[column_config['app_name']].nunique().reset_index(name='Total Apps')

# 2. Calculate the number of applications in Prod, UAT, and Dev environments per LOB
env_counts = df.groupby([column_config['lob'], column_config['environment']])[column_config['app_name']].nunique().unstack(fill_value=0).reset_index()
env_counts.columns.name = None  # Remove the name from columns for easier access
env_counts = env_counts.rename(columns={'Prod': 'Prod Apps', 'UAT': 'UAT Apps', 'Dev': 'Dev Apps'})

# 3. Identify the most critical application in Prod for each LOB and its details
prod_critical = df[df[column_config['environment']] == 'Prod'].sort_values(
    [column_config['criticality'], column_config['strategy']], ascending=[True, True])
most_critical_prod = prod_critical.groupby(column_config['lob']).first().reset_index()

# 4. Merge the results into a single DataFrame
result = pd.merge(total_apps_per_lob, env_counts, on=column_config['lob'])
result = pd.merge(result, most_critical_prod[
    [column_config['lob'], column_config['app_name'], column_config['deployments'], column_config['criticality'], column_config['strategy'], column_config['offering_status']]
], on=column_config['lob'])

result = result.rename(columns={
    column_config['app_name']: 'Most Critical Prod App',
    column_config['deployments']: 'Deployments',
    column_config['strategy']: 'Strategy',
    column_config['criticality']: 'Criticality',
    column_config['offering_status']: 'OfferingStatus'
})

# 5. Reorder the columns to make 'Deployments' the second column
result = result[['LOB', 'Deployments', 'Total Apps', 'Prod Apps', 'UAT Apps', 'Dev Apps', 'Most Critical Prod App', 'Strategy', 'Criticality', 'OfferingStatus']]

# 6. Write the result to a Markdown file
with open('result_summary.md', 'w') as f:
    f.write(tabulate(result, headers='keys', tablefmt='pipe', showindex=False))

print("Results written to 'result_summary.md'")
