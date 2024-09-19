import pyodbc
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import argparse
import time

chunk_size = 50000  # Global variable for batch processing size

def create_pg_connection():
    """Creates and returns a connection engine to the PostgreSQL database."""
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    return engine

def drop_table_if_exists(engine, table_name):
    """Drops the table in PostgreSQL if it exists."""
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
            transaction.commit()  # Committing the transaction if successful
        except Exception as e:
            print(f"Failed to drop table {table_name}: {e}")
            transaction.rollback()  # Rolling back in case of error

def fetch_column_info(sql_conn, table_name):
    """Fetches column information to determine which are not VARBINARY."""
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    columns = [row[0] for row in sql_cursor.fetchall() if 'binary' not in row[1]]
    sql_cursor.close()
    return columns

def fetch_and_transfer_data(sql_conn, pg_engine, table_name, date_column, limit=None):
    # Fetch column information excluding VARBINARY types
    columns = fetch_column_info(sql_conn, table_name)
    if not columns:
        print("No suitable columns found for data transfer.")
        return

    sql_cursor = sql_conn.cursor()
    ninety_days_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    select_clause = f"SELECT TOP {limit} {', '.join(columns)}" if limit else f"SELECT {', '.join(columns)}"
    query = f"{select_clause} FROM {table_name} WHERE {date_column} >= ?"
    
    print(f"Executing SQL Server query: {query}")
    sql_cursor.execute(query, (ninety_days_ago,))

    try:
        # Fetch all at once if data size is manageable, otherwise use fetchmany in a loop
        rows = sql_cursor.fetchall()
        print(f"Fetched {len(rows)} rows")  # Debug: Check how many rows are fetched
        if rows:
            print(f"Sample data: {rows[0]}")  # Debug: Inspect the first row of fetched data
        df = pd.DataFrame(rows, columns=columns)
        df.to_sql(table_name, con=pg_engine, if_exists='append', index=False)
        print("Data transferred successfully to PostgreSQL.")
    except Exception as e:
        print(f"Failed to create DataFrame or transfer to PostgreSQL: {e}")
    finally:
        sql_cursor.close()



def main():
    parser = argparse.ArgumentParser(description='Fetch and transfer specified data excluding binary columns.')
    parser.add_argument('--host', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--table', required=True, help='Table name to query from.')
    parser.add_argument('--datecol', required=True, help='Date column to filter the data.')
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
