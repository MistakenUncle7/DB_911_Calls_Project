'''
DESCRIPTION OF THE PROGRAM
'''


import mysql.connector
import os
import time
from mysql.connector import Error
from datetime import datetime

def clear_screen(seconds):
    time.sleep(seconds)
    if os.name == 'nt':
        os.system('cls')

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
        print(f"Error: {e}")
        return None
    

def delete_from_db():
    print("NOT YET")

def get_date_time():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def get_information():
    values = {}

    # calls table fields
    values["call_key"] = "Randomsomething" # Need to create the way to generate a CALLKEY
    values["call_date_time"] = get_date_time()
    values["priority"] = "" # Need to make the user choose from the ENUM
    values["call_number"] = input("Insert your phone number: ")

    # incidents table fields
    values["district"] = input("Insert the district abbreviation: ") # See if you can do it an ENUM
    values["desription"] = input("Insert the name of the crime: ")
    values["incident_location"] = input("Insert the location where the crime occured: ")
    values["needs_sync"] = input("Press '1' if the data is updated in all devices: ") # Check how to make the user input 1 or 0

    # locations table fields
    values["location"] = input("Insert the reporters localization: ")
    values["neighborhood"] = input("Insert the neighborhood of the incident: ")
    values["council_district"] = input("Insert the number of the council district: ")
    values["com_stat_areas"] = input("Insert a known neighborhoods near the incident (remember to use '/' to separate them): ") # Upgrade this
    census_tracts = input("Insert the census tract: ")
    values["census_tracts"] = "Census Tract " + census_tracts
    values["zip_code"] = input("Insert the ZIP Code: ")
    values["esri_oid"] = input("Insert the Esri OID: ")

    # police_stations table fields
    values["police_post"] = input("Insert the number of the police post: ")
    values["sherrif_district"] = input("Insert the sherrif district: ")
    values["police_district"] = input("Insert the police district: ")

    return values


def insert_to_db(connection):
    try:
        cursor = connection.cursor()
        connection.start_transaction()

        data = get_information()

        # Insert into police_station table
        police_stations_query = """ 
        INSERT INTO police_stations (police_post, sheriff_district, police_district)
        VALUES (%s, %s, %s)
        """
        police_stations_data = (
            data["police_post"],
            data["sheriff_district"],
            data["police_district"]
        )
        cursor.execute(police_stations_query, police_stations_data)
        connection.commit()
        police_station_ID = cursor.lastrowid
        print(f"Inserted into 'police_stations' with ID: {police_station_ID}")

        # Insert into locations table
        locations_query = """
        INSERT INTO locations (location, council_district, community_statistical_areas ,census_tracts, zip_code, esri_oid, neighborhood)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        locations_data = (
            data["location"],
            data["council_district"],
            data["com_stat_areas"],
            data["census_tracts"],
            data["zip_code"],
            data["esri_oid"],
            data["neighborhood"]
        )
        cursor.execute(locations_query, locations_data)
        connection.commit()
        location_record_ID = cursor.lastrowid
        print(f"Inserted into 'locations' with ID: {location_record_ID}")

        # Insert into incidents table
        incidents_query = """
        INSERT INTO incidents (district, description, incident_location, needs_sync)
        VALUES (%s, %s, %s, %s)
        """
        incidents_data = (
            data["district"],
            data["description"],
            data["incident_location"],
            data["needs_sync"]
        )
        cursor.execute(incidents_query, incidents_data)
        connection.commit()
        record_ID = cursor.lastrowid
        print(f"Inserted into 'incidents' with ID: {record_ID}")

        # Insert into calls table
        calls_query = """
        INSERT INTO calls (call_key, call_date_time, priority, call_number)
        VALUES (%s, %s, %s, %s)
        """
        calls_data = (
            data["call_key"],
            data["call_date_time"],
            data["priority"],
            data["call_number"]
        )
        cursor.execute(calls_query, calls_data)
        connection.commit()
        record_ID = cursor.lastrowid
        print(f"Inserted into 'calls' with ID: {record_ID}")


    except Error as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

    finally:
        if cursor:
            cursor.close()


def main():
    connection = connect_to_db()
    while connection:
        cursor = connection.cursor()
        clear_screen(5)

        print("\n--- Menu ---")
        print("Selet the index of the operation you would like to realize")
        print("1. Insert")
        print("2. Update")
        print("3. Delete")
        print("0. Exit")

        choice = input("\nOption: ")

        if choice == "1":
            print("Selected 1")
            insert_to_db(connection)
        elif choice == "2":
            print("Selected 2")
        elif choice == "3":
            print("Selected 3")
        elif choice == "0":
            print("Selected Exit")
            cursor.close()
            connection.close()
            break
        else:
            print("Invalid option, please try again")

    # connection.close()

def update_db():
    print("NOT YET")

if __name__ == "__main__":
    main()
