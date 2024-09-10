import pyodbc
import psycopg2
import pandas as pd
import argparse

PG_HOST = 'localhost'
PG_DATABASE = 'scratchcard'
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
    conn_str = f"host={PG_HOST} dbname={PG_DATABASE} user={PG_USER} password={PG_PASSWORD}"
    return psycopg2.connect(conn_str)

def migrate_table(sql_server_conn, pg_conn, table_name):
    print(f"Migrating table {table_name}...")
    sql_query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(sql_query, sql_server_conn)
    data.columns = [col.replace(' ', '_').lower() for col in data.columns]
    cursor = pg_conn.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join([f'{col} TEXT' for col in data.columns])}
    );
    """
    cursor.execute(create_table_query)
    data.to_sql(table_name, pg_conn, if_exists='replace', index=False)
    pg_conn.commit()
    cursor.close()
    print(f"Table {table_name} migrated successfully.")

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
    pg_conn = connect_postgres()
    for table in args.tables:
        migrate_table(sql_server_conn, pg_conn, table)
    sql_server_conn.close()
    pg_conn.close()

if __name__ == "__main__":
    main()
