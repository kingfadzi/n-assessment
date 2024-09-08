import urllib.parse

def encode_url(driver, server, port, database, username, password, encrypt, timeout):
    # Construct the human-readable ODBC connection string
    human_readable_url = (
        f"Driver={{{driver}}};"           # Driver enclosed in curly braces
        f"Server=tcp:{server},{port};"     # Server in tcp format with port
        f"Database={database};"            # Database name
        f"Uid={username};"                 # Username
        f"Pwd={password};"                 # Password
        f"Encrypt={encrypt};"              # Encrypt flag
        f"Connection Timeout={timeout}"    # Connection Timeout
    )

    # URL encode the constructed connection string
    encoded_url = urllib.parse.quote(human_readable_url)

    # Return the full SQLAlchemy connection string format
    return f"mssql+pyodbc:///?odbc_connect={encoded_url}"

# Example usage with dynamic parameters:
driver = "ODBC Driver 17 for SQL Server"
server = "<my_server>"  # Replace with actual server
port = 1433
database = "my_database"
username = "my_user_name"
password = "my_password"
encrypt = "yes"
timeout = 30

# Encode the URL
encoded_string = encode_url(driver, server, port, database, username, password, encrypt, timeout)

# Print the encoded URL
print("Encoded URL: ", encoded_string)
