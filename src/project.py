'''
DEFINITION OF THE PROGRAM
'''


import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
from datetime import datetime

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="911_emergency_calls",
            port=3307 #phpmyadmin port
        )

        if connection.is_connected():
            print("Connected to MySQL database via UniServerZ")
            return connection

    except Error as e:
        print(f"ERROR: {e}")
        return None

connection = connect_to_db()
if connection:
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        for table in cursor.fetchall():
            print(table)
    except Error as e:
        print(f"Query Error: {e}")
    finally:
        cursor.close()
        connection.close()
else:
    print("Failed to connect to the database.")
