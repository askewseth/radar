import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host = os.environ.get("mysql_host", "localhost"),
        user = os.environ.get("mysql_user"),
        password = os.environ.get("mysql_password")
    )

def query_test():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test")
    print(cursor.fetchall())

if __name__ == "__main__":
    query_test()