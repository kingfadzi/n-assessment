import pyodbc
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import pandas as pd
import argparse

# Global variable for batch processing size
chunk_size = 50000

def create_pg_connection():
    # PostgreSQL connection using SQLAlchemy for handling larger datasets efficiently
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    return engine

def drop_table_if_exists(engine, table_name):
    with engine.begin() as connection:  # Ensures transactional integrity
        connection.execute(f"DROP TABLE IF EXISTS {table_name};")

def fetch_and_transfer_data(sql_conn, pg_engine, table_name, date_column, limit=None):
    sql_cursor = sql_conn.cursor()
    ninety_days_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    select_clause = f"SELECT TOP {limit} *" if limit else "SELECT *"
    query = f"{select_clause} FROM {table_name} WHERE {date_column} >= ?"
    
    print(f"Executing SQL Server query: {query}")
    sql_cursor.execute(query, (ninety_days_ago,))
    
    while True:
        rows = sql_cursor.fetchmany(chunk_size)
        if not rows:
            break
        df = pd.DataFrame(rows, columns=[desc[0] for desc in sql_cursor.description])
        df.to_sql(table_name, con=pg_engine, if_exists='append', index=False)

    sql_cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Fetch data from the last 90 days from SQL Server and transfer to PostgreSQL.')
    parser.add_argument('--host', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--table', required=True, help='Table name to query from.')
    parser.add_argument('--datecol', required=True, help='Date column to filter the data.')
    parser.add_argument('--limit', type=int, help='Optional: Limit the number of records to fetch')
    args = parser.parse_args()

    # SQL Server connection string
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={args.host}\\{args.instance},{args.port};DATABASE={args.db};Trusted_Connection=yes;'
    sql_connection = pyodbc.connect(conn_str)
    
    # PostgreSQL connection
    pg_engine = create_pg_connection()

    # Drop existing table and transfer new data
    drop_table_if_exists(pg_engine, args.table)
    fetch_and_transfer_data(sql_connection, pg_engine, args.table, args.datecol, args.limit)

    # Close connections
    sql_connection.close()
    pg_engine.dispose()

if __name__ == "__main__":
    main()
