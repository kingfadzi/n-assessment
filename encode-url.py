import urllib.parse

def generate_superset_connection_string(driver, server, port, database, encrypt, timeout):
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"Authentication=ActiveDirectoryIntegrated;" 
        f"Encrypt={encrypt};"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout={timeout};"
    )
    encoded_connection_string = urllib.parse.quote(connection_string)
    return f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}"

driver = "ODBC Driver 17 for SQL Server"
server = "your_server_name_or_ip"
port = 10501
database = "your_database_name"
encrypt = "yes"
timeout = 30

superset_connection_string = generate_superset_connection_string(driver, server, port, database, encrypt, timeout)

print(superset_connection_string)
