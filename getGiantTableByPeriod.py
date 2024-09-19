import decimal
from sqlalchemy import create_engine, text
import pyodbc
import pandas as pd
from datetime import datetime, timedelta
import argparse

chunk_size = 50000  # Adjust based on your environment and data size

def create_pg_connection():
    """ Creates a connection to the PostgreSQL database. """
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    return engine

def fetch_column_info(sql_conn, table_name):
    """ Retrieves column information excluding VARBINARY types. """
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    columns = [row[0] for row in sql_cursor.fetchall() if 'binary' not in row[1].lower()]
    sql_cursor.close()
    return columns

def fetch_and_transfer_data(sql_conn, pg_engine, table_name, date_column, limit=None):
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

    rows = sql_cursor.fetchall()
    converted_rows = [[float(item) if isinstance(item, decimal.Decimal) else item for item in row] for row in rows]

    df = pd.DataFrame(converted_rows, columns=columns)
    df.to_sql(table_name, con=pg_engine, if_exists='append', index=False)
    print(f"Data transferred successfully to PostgreSQL.")

    sql_cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Fetch and transfer data excluding binary columns.')
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
