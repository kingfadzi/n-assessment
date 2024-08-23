import pandas as pd

# Load data from CSV
df = pd.read_csv('deployments.csv')

# 1. Calculate the total number of unique applications per LOB
total_apps_per_lob = df.groupby('LOB')['AppName'].nunique().reset_index(name='Total Apps')

# 2. Calculate the number of applications in Prod, UAT, and Dev environments per LOB
env_counts = df.groupby(['LOB', 'Environment'])['AppName'].nunique().unstack(fill_value=0).reset_index()
env_counts.columns.name = None  # Remove the name from columns for easier access
env_counts = env_counts.rename(columns={'Prod': 'Prod Apps', 'UAT': 'UAT Apps', 'Dev': 'Dev Apps'})

# 3. Identify the most critical application in Prod for each LOB and its details
prod_critical = df[df['Environment'] == 'Prod'].sort_values(['Criticality', 'Strategy'], ascending=[True, True])
most_critical_prod = prod_critical.groupby('LOB').first().reset_index()

# 4. Merge the results into a single DataFrame
result = pd.merge(total_apps_per_lob, env_counts, on='LOB')
result = pd.merge(result, most_critical_prod[['LOB', 'AppName', 'Criticality', 'Strategy', 'OfferingStatus']], on='LOB')
result = result.rename(columns={
    'AppName': 'Most Critical Prod App',
    'Strategy': 'Strategy',
    'Criticality': 'Criticality',
    'OfferingStatus': 'OfferingStatus'
})

# 5. Display the final result
print(result)
