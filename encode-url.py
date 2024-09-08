from sqlalchemy import create_engine

connection_string = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server_name_or_ip,1433;"
    "DATABASE=your_database_name;"
    "UID=your_username;"
    "PWD=your_password;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=30;"
)

engine = create_engine(connection_string)

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")
