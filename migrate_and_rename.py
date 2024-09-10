import pyodbc
import pandas as pd
import argparse
from sqlalchemy import create_engine, text

PG_HOST = 'localhost'
PG_DATABASE = 'scratchpad'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'

def connect_sql_server(host, port, instance, database):
    print("Connecting to SQL Server...")
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={host}\\{instance},{port};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    connection = pyodbc.connect(conn_str)
    print("Connected to SQL Server.")
    return connection

def connect_postgres():
    print("Connecting to PostgreSQL...")
    engine_url = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}"
    engine = create_engine(engine_url)
    print("Connected to PostgreSQL.")
    return engine

def migrate_table(sql_server_conn, pg_engine, table_name):
    print(f"Starting migration for table {table_name}...")
    sql_query = f"SELECT * FROM {table_name}"
    print(f"Executing query on SQL Server: {sql_query}")
    data = pd.read_sql(sql_query, sql_server_conn)
    print(f"Query executed successfully. Retrieved {len(data)} rows.")

    print("Transforming column names...")
    data.columns = [col.replace(' ', '_').replace('(', '_').replace(')', '_').lower() for col in data.columns]
    print("Column names transformed.")

    with pg_engine.connect() as conn:
        print(f"Dropping table {table_name} if it exists...")
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
        print(f"Table {table_name} dropped.")

        print(f"Creating table {table_name}...")
        create_table_query = f"""
        CREATE TABLE {table_name} (
            {', '.join([f'{col} TEXT' for col in data.columns])}
        );
        """
        conn.execute(create_table_query)
        print(f"Table {table_name} created.")

        print(f"Inserting data into {table_name}...")
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data inserted into {table_name} successfully.")

    print(f"Migration completed for table {table_name}.")

def main():
    parser = argparse.ArgumentParser(description='Migrate tables from SQL Server to PostgreSQL.')
    parser.add_argument('--host', required=True, help='SQL Server host')
    parser.add_argument('--instance', required=True, help='SQL Server instance name')
    parser.add_argument('--port', required=True, help='SQL Server port')
    parser.add_argument('--db', required=True, help='SQL Server database name')
    parser.add_argument('--tables', nargs='+', required=True, help='List of tables to migrate')

    args = parser.parse_args()

    sql_server_conn = connect_sql_server(
        args.host,
        args.port,
        args.instance,
        args.db
    )

    pg_engine = connect_postgres()

    for table in args.tables:
        migrate_table(sql_server_conn, pg_engine, table)

    sql_server_conn.close()
    print("Closed SQL Server connection.")
    print("Migration process completed for all tables.")

if __name__ == "__main__":
    main()
