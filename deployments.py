import pandas as pd

df = pd.read_csv('sample_data.csv')

# Total Number of Deployments
total_deployments = df['Number of Nolio Deployments'].sum()

# Average Number of Deployments per Application
average_deployments = df['Number of Nolio Deployments'].mean()

# Distribution of Applications by Architecture Model
architecture_distribution = df['Architecture Model'].value_counts()

# Count of Applications by Operational Status
operational_status_count = df['Operational Status'].value_counts()

# Average Availability Rating
average_availability_rating = df['Availability Rating'].mean()

# Distribution of Resilience Categories
resilience_distribution = df['Resilience Category'].value_counts()

# Service Classification Frequency
service_classification_frequency = df['Service Classification'].value_counts()

# Number of Applications per Developer/Team
applications_per_developer = df.groupby('Developed By').size()

# Average Time Between Updates
df['Created'] = pd.to_datetime(df['Created'])
df['Updated'] = pd.to_datetime(df['Updated'])
df['Time Between Updates'] = (df['Updated'] - df['Created']).dt.days
average_time_between_updates = df['Time Between Updates'].mean()

# Average Security Rating
average_security_rating = df['Security Rating'].mean()

# Percentage of Applications Meeting Compliance Deadlines
current_date = pd.Timestamp('today')  # Or any specific date you are assessing against
df['ACA Next Due Date'] = pd.to_datetime(df['ACA Next Due Date'])
compliance_meeting = (df['ACA Next Due Date'] > current_date).mean() * 100

# Print the summary statistics
print(f"Total Number of Deployments: {total_deployments}")
print(f"Average Number of Deployments per Application: {average_deployments:.2f}")
print("Distribution of Applications by Architecture Model:", architecture_distribution)
print("Count of Applications by Operational Status:", operational_status_count)
print(f"Average Availability Rating: {average_availability_rating:.2f}")
print("Distribution of Resilience Categories:", resilience_distribution)
print("Service Classification Frequency:", service_classification_frequency)
print("Number of Applications per Developer/Team:", applications_per_developer)
print(f"Average Time Between Updates: {average_time_between_updates:.2f} days")
print(f"Average Security Rating: {average_security_rating:.2f}")
print(f"Percentage of Applications Meeting Compliance Deadlines: {compliance_meeting:.2f}%")
