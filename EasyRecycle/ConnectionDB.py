import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="060605",
        database="EasyRecycle"
    )
    return connection
