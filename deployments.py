import pandas as pd
from tabulate import tabulate

df = pd.read_csv('sample_data.csv')
df.columns = df.columns.str.strip()

column_config = {
    'app_name': 'AppName',
    'lob': 'LOB',
    'environment': 'Environment',
    'criticality': 'Criticality',
    'strategy': 'Strategy',
    'offering_status': 'OfferingStatus',
    'deployments': 'Deployments'
}

total_apps_per_lob = df.groupby(column_config['lob'])[column_config['app_name']].nunique().reset_index(
    name='Total Apps')

env_counts = df.groupby([column_config['lob'], column_config['environment']])[
    column_config['app_name']].nunique().unstack(fill_value=0).reset_index()
env_counts.columns.name = None
env_counts = env_counts.rename(columns={'Prod': 'Prod Apps', 'UAT': 'UAT Apps', 'Dev': 'Dev Apps'})

prod_critical = df[df[column_config['environment']] == 'Prod'].sort_values(
    [column_config['criticality'], column_config['strategy']], ascending=[True, True])
most_critical_prod = prod_critical.groupby(column_config['lob']).first().reset_index()

result = pd.merge(total_apps_per_lob, env_counts, on=column_config['lob'])
result = pd.merge(result, most_critical_prod[
    [column_config['lob'], column_config['app_name'], column_config['deployments'], column_config['criticality'],
     column_config['strategy'], column_config['offering_status']]
], on=column_config['lob'])
result = result.rename(columns={
    column_config['app_name']: 'Most Critical Prod App',
    column_config['deployments']: 'Deployments',
    column_config['strategy']: 'Strategy',
    column_config['criticality']: 'Criticality',
    column_config['offering_status']: 'OfferingStatus'
})

result = result[
    [column_config['lob'], 'Deployments', 'Total Apps', 'Prod Apps', 'UAT Apps', 'Dev Apps', 'Most Critical Prod App',
     'Strategy', 'Criticality', 'OfferingStatus']]

with open('result_summary.md', 'w') as f:
    f.write(tabulate(result, headers='keys', tablefmt='pipe', showindex=False))

print("Results written to 'result_summary.md'")
