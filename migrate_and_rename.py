import pyodbc
import pandas as pd
import argparse
from sqlalchemy import create_engine, text

def connect_sql_server(host, port, instance, database):
    # Setup the SQL Server connection
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host}\\{instance},{port};DATABASE={database};Trusted_Connection=yes;'
    return pyodbc.connect(conn_str)

def connect_postgres():
    # Setup the PostgreSQL connection
    engine_url = f"postgresql://postgres:postgres@localhost/scratchpad"
    return create_engine(engine_url)

def migrate_table(sql_server_conn, pg_engine, table_name, limit=None, sort_column=None, sort_direction='asc'):
    # Convert table name to lower case to avoid case sensitivity issues
    table_name = table_name.lower()
    print(f"Starting migration for table: {table_name}")

    # Building the SQL query with optional sorting and limit
    sql_query = f"SELECT * FROM {table_name}"
    if sort_column:
        sql_query += f" ORDER BY {sort_column} {sort_direction}"
    if limit:
        sql_query += f" LIMIT {limit}"
    data = pd.read_sql(sql_query, sql_server_conn)

    if data.empty:
        print(f"No data found in {table_name}. Skipping.")
        return

    # Ensuring column names are in lower case
    data.columns = [col.lower().replace(' ', '_').replace('(', '_').replace(')', '_') for col in data.columns]

    with pg_engine.connect() as conn:
        # Dropping the table if exists in PostgreSQL
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
        print(f"Dropped table {table_name} if it existed.")

        # Creating the table and inserting data
        data.to_sql(table_name, con=conn, index=False, if_exists='replace')
        print(f"Data inserted into table {table_name}.")

def main():
    parser = argparse.ArgumentParser(description='Migrate tables from SQL Server to PostgreSQL.')
    parser.add_argument('--host', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--tables', nargs='+', required=True)
    parser.add_argument('--limit', type=int, help='Limit the number of records to fetch')
    parser.add_argument('--sort_column', help='Column to sort by')
    parser.add_argument('--sort_direction', default='asc', choices=['asc', 'desc'], help='Sort direction (asc or desc)')
    args = parser.parse_args()

    # Connect to databases
    sql_server_conn = connect_sql_server(args.host, args.port, args.instance, args.db)
    pg_engine = connect_postgres()

    # Process each table
    for table in args.tables:
        migrate_table(sql_server_conn, pg_engine, table.lower(), args.limit, args.sort_column, args.sort_direction)

    # Close the SQL Server connection
    sql_server_conn.close()

if __name__ == "__main__":
    main()
