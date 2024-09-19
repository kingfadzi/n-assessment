import pyodbc
from datetime import datetime, timedelta
import argparse

def fetch_data(connection, table_name, date_column, limit=None, sort_column=None, sort_direction='asc'):
    cursor = connection.cursor()
    
    # Calculate the date 90 days ago from today
    ninety_days_ago = datetime.now() - timedelta(days=90)
    ninety_days_ago_formatted = ninety_days_ago.strftime('%Y-%m-%d')
    
    # Build SQL Query to fetch the data
    select_clause = "SELECT TOP {} *".format(limit) if limit else "SELECT *"
    query = f"""
    {select_clause}
    FROM {table_name}
    WHERE {date_column} >= ?
    """
    if sort_column:
        query += f" ORDER BY {sort_column} {sort_direction}"
    
    print(f"Executing query: {query}")
    cursor.execute(query, (ninety_days_ago_formatted,))
    
    # Fetch and print the data
    while True:
        rows = cursor.fetchmany(5000)  # Adjust the batch size based on your needs
        if not rows:
            break
        for row in rows:
            print(row)

    cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Fetch data from the last 90 days from SQL Server.')
    parser.add_argument('--host', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--tables', nargs='+', required=True)
    parser.add_argument('--datecol', required=True, help='Date column to filter the data.')
    parser.add_argument('--limit', type=int, help='Optional: Limit the number of records to fetch')
    parser.add_argument('--sort_column', help='Optional: Column to sort by')
    parser.add_argument('--sort_direction', default='asc', choices=['asc', 'desc'], help='Optional: Sort direction (asc or desc)')
    args = parser.parse_args()

    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={args.host}\\{args.instance},{args.port};DATABASE={args.db};Trusted_Connection=yes;'
    connection = pyodbc.connect(conn_str)
    
    # Process each table
    for table in args.tables:
        print(f"Fetching data from table: {table}")
        fetch_data(connection, table, args.datecol, args.limit, args.sort_column, args.sort_direction)

    connection.close()

if __name__ == "__main__":
    main()
