import pyodbc

def get_connection(database_name="CRM"):
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"  # Remplacez par le nom ou l'IP de votre serveur SQL
        f"DATABASE={database_name};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(connection_string)
