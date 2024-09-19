import decimal
from sqlalchemy import create_engine, text
import pyodbc
import pandas as pd
from datetime import datetime, timedelta
import argparse
import sys

chunk_size = 50000  # Adjust based on your environment and data size

def create_pg_connection():
    """Creates and returns a connection engine to the PostgreSQL database."""
    try:
        engine = create_engine(
            'postgresql://postgres:postgres@localhost:5432/postgres',
            echo=True  # Enable SQL logging for debugging
        )
        return engine
    except Exception as e:
        print(f"Error creating PostgreSQL engine: {e}")
        sys.exit(1)

def fetch_column_info(sql_conn, table_name):
    """Retrieves column names excluding VARBINARY types."""
    try:
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table_name}'
        """)
        columns = [row[0] for row in sql_cursor.fetchall() if 'binary' not in row[1].lower()]
        sql_cursor.close()
        return columns
    except Exception as e:
        print(f"Error fetching column info from SQL Server: {e}")
        sys.exit(1)

def drop_table_if_exists(engine, table_name):
    """Drops the table in PostgreSQL if it exists."""
    try:
        with engine.connect() as connection:
            connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}";'))
            print(f"Table '{table_name}' dropped successfully in PostgreSQL.")
    except Exception as e:
        print(f"Failed to drop table '{table_name}': {e}")

def fetch_and_transfer_data(sql_conn, pg_engine, table_name, date_column, limit=None):
    """Fetches data from SQL Server and transfers it to PostgreSQL."""
    columns = fetch_column_info(sql_conn, table_name)
    if not columns:
        print("No suitable columns found for data transfer.")
        return

    # Drop the PostgreSQL table if it exists
    drop_table_if_exists(pg_engine, table_name)

    sql_cursor = sql_conn.cursor()
    ninety_days_ago = datetime.now() - timedelta(days=90)
    select_columns = ', '.join(f'"{col}"' for col in columns)
    select_clause = f"SELECT TOP {limit} {select_columns}" if limit else f"SELECT {select_columns}"
    query = f"{select_clause} FROM [{table_name}] WHERE [{date_column}] >= ?"

    print(f"Executing SQL Server query: {query}")
    sql_cursor.execute(query, (ninety_days_ago,))
    print("SQL Server query executed successfully.")

    # Start PostgreSQL transaction
    with pg_engine.begin() as conn:
        try:
            while True:
                rows = sql_cursor.fetchmany(chunk_size)
                if not rows:
                    break

                # Convert Decimal types to float
                converted_rows = [
                    [float(item) if isinstance(item, decimal.Decimal) else item for item in row]
                    for row in rows
                ]

                df = pd.DataFrame(converted_rows, columns=columns)
                if not df.empty:
                    print(f"Inserting {len(df)} rows into PostgreSQL table '{table_name}'...")
                    df.to_sql(table_name, con=conn, if_exists='append', index=False)
                    print(f"Inserted {len(df)} rows.")
                else:
                    print("No data to write to the database.")

        except Exception as e:
            print(f"Error during data transfer: {e}")
            sys.exit(1)

    print(f"Data transfer to PostgreSQL table '{table_name}' completed successfully.")
    sql_cursor.close()

def main():
    """Main function to parse arguments and initiate data transfer."""
    parser = argparse.ArgumentParser(description='Fetch and transfer data excluding binary columns.')
    parser.add_argument('--host', required=True, help='SQL Server host')
    parser.add_argument('--instance', required=True, help='SQL Server instance name')
    parser.add_argument('--port', required=True, help='SQL Server port')
    parser.add_argument('--db', required=True, help='SQL Server database name')
    parser.add_argument('--table', required=True, help='Table name to fetch data from')
    parser.add_argument('--datecol', required=True, help='Date column to filter records from the last 90 days')
    parser.add_argument('--limit', type=int, help='Optional: Limit the number of records to fetch')
    args = parser.parse_args()

    # Build SQL Server connection string
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={args.host}\\{args.instance},{args.port};'
        f'DATABASE={args.db};'
        f'Trusted_Connection=yes;'
    )

    # Establish connections
    try:
        sql_connection = pyodbc.connect(conn_str)
        print("Connected to SQL Server successfully.")
    except Exception as e:
        print(f"Error connecting to SQL Server: {e}")
        sys.exit(1)

    pg_engine = create_pg_connection()
    print("Connected to PostgreSQL successfully.")

    # Perform data transfer
    fetch_and_transfer_data(sql_connection, pg_engine, args.table, args.datecol, args.limit)

    # Close connections
    sql_connection.close()
    pg_engine.dispose()

if __name__ == "__main__":
    main()
