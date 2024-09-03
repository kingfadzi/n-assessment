import pandas as pd
from tabulate import tabulate

# Load the Excel file
df = pd.read_excel('path/to/your/file.xlsx')

# Convert to Markdown
markdown_table = tabulate(df, tablefmt="pipe", headers="keys", showindex="never")

# Write to a Markdown file
with open('output.md', 'w') as f:
    f.write(markdown_table)

print("Markdown table saved to output.md")
