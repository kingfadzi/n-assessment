import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from sklearn.cluster import KMeans

# Load the CSV dataset
df = pd.read_csv('servers.csv')

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(df.head())

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

# Select only numeric columns for correlation matrix
numeric_df = df.select_dtypes(include='number')

# Correlation matrix for numerical columns
correlation_matrix = numeric_df.corr()
print("\nCorrelation matrix:")
print(correlation_matrix)

# Visualize the correlation matrix
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Additional analysis continues below...


# Mean server counts per group and state
group_state_mean = df.groupby(['serverGroups', 'state']).agg({'id': 'count'}).reset_index()
print("\nMean server counts per group and state:")
print(group_state_mean)

# Calculate quantiles (e.g., 25th, 50th, 75th percentiles)
if 'numeric_column' in df.columns:
    quantiles = df['numeric_column'].quantile([0.25, 0.5, 0.75])
    print("\nQuantiles of numeric_column:")
    print(quantiles)

# Standard deviation and variance of numerical columns
if 'numeric_column' in df.columns:
    std_dev = df['numeric_column'].std()
    variance = df['numeric_column'].var()
    print(f"\nStandard Deviation: {std_dev}, Variance: {variance}")

# Z-score calculation
if 'numeric_column' in df.columns:
    df['z_score'] = stats.zscore(df['numeric_column'])
    print("\nZ-scores for numeric_column:")
    print(df[['numeric_column', 'z_score']])

# Outlier detection using IQR
if 'numeric_column' in df.columns:
    Q1 = df['numeric_column'].quantile(0.25)
    Q3 = df['numeric_column'].quantile(0.75)
    IQR = Q3 - Q1

    outliers = df[(df['numeric_column'] < (Q1 - 1.5 * IQR)) | (df['numeric_column'] > (Q3 + 1.5 * IQR))]
    print("\nOutliers detected in numeric_column:")
    print(outliers)

# T-test comparing 'numeric_column' across two different 'state' categories
if 'numeric_column' in df.columns and 'state' in df.columns:
    group1 = df[df['state'] == 'Active']['numeric_column']
    group2 = df[df['state'] == 'Inactive']['numeric_column']

    t_stat, p_value = stats.ttest_ind(group1, group2)
    print(f"\nT-test comparing 'Active' and 'Inactive' states:\nT-statistic: {t_stat}, P-value: {p_value}")

# Chi-square test on the cross-tabulation of 'osType' and 'reachable'
chi2, p, dof, expected = stats.chi2_contingency(crosstab)
print(f"\nChi-square test on OS type and reachability:\nChi2: {chi2}, P-value: {p}")

# Simple linear regression example
if 'numeric_column1' in df.columns and 'numeric_column2' in df.columns:
    X = df[['numeric_column1', 'numeric_column2']]
    y = df['numeric_column']  # Assuming 'numeric_column' is your dependent variable

    X = sm.add_constant(X)  # Add an intercept
    model = sm.OLS(y, X).fit()

    print("\nSimple linear regression summary:")
    print(model.summary())

# KMeans clustering (if applicable)
if 'numeric_column1' in df.columns and 'numeric_column2' in df.columns:
    kmeans = KMeans(n_clusters=3)
    df['cluster'] = kmeans.fit_predict(df[['numeric_column1', 'numeric_column2']])

    print("\nCluster assignments using KMeans:")
    print(df['cluster'].value_counts())

# Visualizations
# OS Distribution
plt.figure(figsize=(10, 6))
sns.countplot(y='osType', data=df)
plt.title('Operating System Distribution')
plt.show()

# Reachability Distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='reachable', data=df)
plt.title('Server Reachability')
plt.show()

# Server State Distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='state', data=df)
plt.title('Server State Distribution')
plt.show()
