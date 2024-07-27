import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hackathon"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def get_cursor(connection):
    try:
        if connection is not None and connection.is_connected():
            cursor = connection.cursor()
            return cursor
    except Error as e:
        print(f"Error: {e}")
        return None
