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

def migrate_table(sql_server_conn, pg_engine, table_name):
    # Convert table name to lower case to avoid case sensitivity issues
    table_name = table_name.lower()
    print(f"Starting migration for table: {table_name}")

    # Querying data from SQL Server
    sql_query = f"SELECT * FROM {table_name}"
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
    args = parser.parse_args()

    # Connect to databases
    sql_server_conn = connect_sql_server(args.host, args.port, args.instance, args.db)
    pg_engine = connect_postgres()

    # Process each table
    for table in args.tables:
        migrate_table(sql_server_conn, pg_engine, table.lower())

    # Close the SQL Server connection
    sql_server_conn.close()

if __name__ == "__main__":
    main()
