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
            password="root",
            database="911_emergency_calls",
            port=3307 #UniServerZ port
        )

        if connection.is_connected():
            print("Connected to MySQL database via UniServerZ")
            return connection

    except Error as e:
        print(f"ERROR: {e}")
        return None


def insert_data():
    call_key = entry_call_key.get()
    record_ID = entry_record_ID.get()
    call_date_time = entry_call_date_time.get()
    priority = entry_priority.get()
    call_number = entry_call_number.get()
    '''
    district = entry_district.get()
    description = entry_description.get()
    incident_location = entry_incident_location.get()
    needs_sync = entry_needs_sync()
    location_record_ID = entry_location_record_ID.get()
    location = entry_location.get()
    council_district = entry_council_district.get()
    community_statistical_areas = entry_community_statistical_areas.get()
    census_tracts = entry_census_tracts.get()
    zip_code = entry_zip_code.get()
    esri_oid = entry_esri_oid.get()
    neighborhood = entry_neighborhood.get()
    police_station_ID = entry_police_station_ID.get()
    police_post = entry_police_post.get()
    sheriff_district = entry_sheriff_district.get()
    police_district = entry_police_district.get()
    

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO "

        except Error as e:
            print(f"Error: {e}")
            return None

'''

'''
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
'''

# Initialize Custom TKinter app
app = ctk.CTk()
# app._set_appearance_mode("dark")
app.title("911 Emergency Calls")
app.geometry("750x450")

dropdown = ctk.CTkComboBox(app, values=["Insert", "Update", "Delete"], width=200)
dropdown.grid(row=0, column=0, padx=10, pady=10)

label_call_key = ctk.CTkLabel(app, text="callKey:")
label_call_key.grid(row=1, column=0, padx=10, pady=5)
entry_call_key = ctk.CTkEntry(app, width=200)
entry_call_key.grid(row=1, column=1, padx=10, pady=5)

label_record_ID = ctk.CTkLabel(app, text="Record ID:")
label_record_ID.grid(row=1, column=0, padx=10, pady=5)
entry_record_ID = ctk.CTkEntry(app, width=200)
entry_record_ID.grid(row=1, column=1, padx=10, pady=5)

label_call_date_time = ctk.CTkLabel(app, text="Call Date Time:")
label_call_date_time.grid(row=1, column=0, padx=10, pady=5)
entry_call_date_time = ctk.CTkEntry(app, width=200)
entry_call_date_time.grid(row=1, column=1, padx=10, pady=5)

label_priority = ctk.CTkLabel(app, text="Priority:")
label_priority.grid(row=1, column=0, padx=10, pady=5)
entry_priority = ctk.CTkEntry(app, width=200)
entry_priority.grid(row=1, column=1, padx=10, pady=5)

label_call_number = ctk.CTkLabel(app, text="Call Number:")
label_call_number.grid(row=1, column=0, padx=10, pady=5)
entry_call_number = ctk.CTkEntry(app, width=200)
entry_call_number.grid(row=1, column=1, padx=10, pady=5)

app.mainloop()
