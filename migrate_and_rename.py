import pyodbc
import pandas as pd
import argparse
from sqlalchemy import create_engine, text

# Define PostgreSQL connection details explicitly
PG_HOST = 'localhost'
PG_DATABASE = 'scratchpad'  # Updated to 'scratchpad' as per your correction
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'

def connect_sql_server(host, port, instance, database):
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={host}\\{instance},{port};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

def connect_postgres():
    engine_url = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}"
    return create_engine(engine_url)

def migrate_table(sql_server_conn, pg_engine, table_name):
    print(f"Starting migration for table {table_name}...")
    sql_query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(sql_query, sql_server_conn)

    data.columns = [col.replace(' ', '_').replace('(', '_').replace(')', '_').lower() for col in data.columns]

    with pg_engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS public.{table_name};"))
        data.to_sql(table_name, con=conn, schema='public', if_exists='replace', index=False)

    print(f"Table {table_name} migrated successfully.")

def main():
    parser = argparse.ArgumentParser(description='Migrate tables from SQL Server to PostgreSQL.')
    parser.add_argument('--host', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--tables', nargs='+', required=True)

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

if __name__ == "__main__":
    main()
