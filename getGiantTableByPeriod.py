import pyodbc
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import argparse

chunk_size = 50000  # Global variable for batch processing size

def create_pg_connection():
    """ Creates a connection to the PostgreSQL database. """
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    return engine

def recreate_table(engine, table_name, columns):
    """ Drops the table if exists and recreates it with the specified columns in PostgreSQL. """
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
            # Assuming columns is a dictionary with column names and SQL types
            col_definitions = ', '.join([f"{name} {type}" for name, type in columns.items()])
            connection.execute(text(f"CREATE TABLE {table_name} ({col_definitions});"))
            transaction.commit()  # Committing the transaction if successful
        except Exception as e:
            print(f"Failed to recreate table {table_name}: {e}")
            transaction.rollback()  # Rolling back in case of error

def fetch_column_info(sql_conn, table_name):
    """ Retrieves column information to exclude VARBINARY types and for table creation. """
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    columns = {row[0]: row[1] for row in sql_cursor.fetchall() if 'binary' not in row[1].lower()}
    sql_cursor.close()
    return columns

def fetch_and_transfer_data(sql_conn, pg_engine, table_name, date_column, limit=None):
    columns = fetch_column_info(sql_conn, table_name)
    if not columns:
        print("No suitable columns found for data transfer.")
        return

    recreate_table(pg_engine, table_name, columns)  # Drop and recreate table

    sql_cursor = sql_conn.cursor()
    ninety_days_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    column_names = ', '.join(columns.keys())
    select_clause = f"SELECT TOP {limit} {column_names}" if limit else f"SELECT {column_names}"
    query = f"{select_clause} FROM {table_name} WHERE {date_column} >= ?"
    
    print(f"Executing SQL Server query: {query}")
    sql_cursor.execute(query, (ninety_days_ago,))

    rows = sql_cursor.fetchall()
    df = pd.DataFrame(rows, columns=columns.keys())
    df.to_sql(table_name, con=pg_engine, if_exists='append', index=False)

    sql_cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Fetch and transfer specified data after recreating the table.')
    parser.add_argument('--host', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--table', required=True)
    parser.add_argument('--datecol', required=True)
    parser.add_argument('--limit', type=int, help='Optional: Limit the number of records to fetch')
    args = parser.parse_args()

    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={args.host}\\{args.instance},{args.port};DATABASE={args.db};Trusted_Connection=yes;'
    sql_connection = pyodbc.connect(conn_str)
    pg_engine = create_pg_connection()

    fetch_and_transfer_data(sql_connection, pg_engine, args.table, args.datecol, args.limit)

    sql_connection.close()
    pg_engine.dispose()

if __name__ == "__main__":
    main()
