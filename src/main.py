'''
DESCRIPTION OF THE PROGRAM
'''


import mysql.connector
import os
import time
import random
import string
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


def delete_from_db(connection):
    try:
        cursor = connection.cursor()
        connection.start_transaction()

        call_key = input("Enter the Call Key to delete: ")

        # Verify if the call_key exists
        check_call_query = """
        SELECT COUNT(*) FROM calls WHERE call_key = %s
        """
        cursor.execute(check_call_query, (call_key,))
        result = cursor.fetchone()

        if result[0] == 0:
            print(f"No record found with call_key: {call_key}")
            return

        call_query = """
        SELECT record_ID FROM calls WHERE call_key = %s
        """
        cursor.execute(call_query, (call_key,))
        record_ID = cursor.fetchone()

        if not record_ID:
            print(f"No record found for Call Key: {call_key}")
            return
        
        record_ID = record_ID[0]

        incident_query = """
        SELECT location_record_ID FROM incidents WHERE record_ID = %s
        """
        cursor.execute(incident_query, (record_ID,))
        location_record_ID = cursor.fetchone()

        if not location_record_ID:
            print(f"Not record found for record_ID: {record_ID}")
            return
        
        location_record_ID = location_record_ID[0]

        location_query = """
        SELECT police_station_ID FROM locations WHERE location_record_ID = %s
        """
        cursor.execute(location_query, (location_record_ID,))
        police_station_ID = cursor.fetchone()

        if not police_station_ID:
            print(f"No location found for location_record_ID: {location_record_ID}")
            return
        
        police_station_ID = police_station_ID[0]

        delete_police_station_querry = """
        DELETE FROM police_stations WHERE police_station_ID = %s
        """
        cursor.execute(delete_police_station_querry, (police_station_ID,))
        connection.commit()
        print(f"Record with call_key {call_key} and all related entries deleted successfully.")
        

    except Error as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

    finally:
        if cursor:
            cursor.close()

def generate_call_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def get_date_time():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def get_information():
    values = {}

    # calls table fields
    values["call_key"] = generate_call_key()
    values["call_date_time"] = get_date_time()
    emergency_levels = ["Non-Emergency", "Low", "Medium", "High", "Emergency", "Out of Service"]
    values["priority"] = select_from_enum(emergency_levels, "Select emergency level: ")
    values["call_number"] = input("Insert your phone number: ")

    # incidents table fields
    districts = ["WD", "NW", "SE", "NE", "SD", "CD", "TRU", "ED", "SW", "ND", "SS", "CW"]
    values["district"] = select_from_enum(districts, "Select the district abbreviation: ")
    values["description"] = input("Insert the name of the crime: ")
    values["incident_location"] = input("Insert the location where the crime occured: ")
    values["needs_sync"] = input_binary("Is the data updated in all devices?")

    # locations table fields
    values["location"] = input("Insert the reporters localization: ")
    values["neighborhood"] = input("Insert the neighborhood of the incident: ")
    coun_dist_num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
    values["council_district"] = select_from_enum(coun_dist_num, "Select the council district: ")
    values["com_stat_areas"] = input("Insert a known neighborhoods near the incident (remember to use '/' to separate them): ") # Upgrade this
    census_tracts = input("Insert the number of the census tract: ")
    values["census_tracts"] = f"Census Tract {census_tracts}"
    values["zip_code"] = input("Insert the ZIP Code: ")
    values["esri_oid"] = input("Insert the Esri OID: ")

    # police_stations table fields
    values["police_post"] = input("Insert the number of the police post: ")
    sheriff_districts = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]
    values["sheriff_district"] = select_from_enum(sheriff_districts, "Select the sheriff_district")
    police_districts = ["Central", "Eastern", "Northeaster", "Northern", "Northwestern", "Southeastern", "Southern", "Southwestern", "Western"]
    values["police_district"] = select_from_enum(police_districts, "Select the police district")

    return values


def input_binary(prompt):
    while True:
        try:
            choice = int(input(f"{prompt} (1 for Yes, 0 for No): "))
            if choice in [1, 0]:
                return choice
            print("Invalid input. Please enter 1 or 0")
        except ValueError:
            print("Invalid input. Please enter a number.")

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
        # connection.commit()
        police_station_ID = cursor.lastrowid
        print(f"Inserted into 'police_stations' with ID: {police_station_ID}")

        # Insert into locations table
        locations_query = """
        INSERT INTO locations (location, council_district, community_statistical_areas , census_tracts, zip_code, esri_oid, neighborhood, police_station_ID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        locations_data = (
            data["location"],
            data["council_district"],
            data["com_stat_areas"],
            data["census_tracts"],
            data["zip_code"],
            data["esri_oid"],
            data["neighborhood"],
            police_station_ID
        )
        cursor.execute(locations_query, locations_data)
        # connection.commit()
        location_record_ID = cursor.lastrowid
        print(f"Inserted into 'locations' with ID: {location_record_ID}")

        # Insert into incidents table
        incidents_query = """
        INSERT INTO incidents (district, description, incident_location, needs_sync, location_record_ID)
        VALUES (%s, %s, %s, %s, %s)
        """
        incidents_data = (
            data["district"],
            data["description"],
            data["incident_location"],
            data["needs_sync"],
            location_record_ID
        )
        cursor.execute(incidents_query, incidents_data)
        # connection.commit()
        record_ID = cursor.lastrowid
        print(f"Inserted into 'incidents' with ID: {record_ID}")

        # Insert into calls table
        calls_query = """
        INSERT INTO calls (call_key, call_date_time, priority, call_number, record_ID)
        VALUES (%s, %s, %s, %s, %s)
        """
        calls_data = (
            data["call_key"],
            data["call_date_time"],
            data["priority"],
            data["call_number"],
            record_ID
        )
        cursor.execute(calls_query, calls_data)
        connection.commit()
        print(f"Inserted into 'calls' with ID: {data['call_key']}")

        wait = input("Press enter to continue: ")


    except Error as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

    finally:
        if cursor:
            cursor.close()


def main():
    clear_screen(0)
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
            update_db(connection)
        elif choice == "3":
            print("Selected 3")
            delete_from_db(connection)
        elif choice == "0":
            print("Selected Exit")
            cursor.close()
            connection.close()
            break
        else:
            print("Invalid option, please try again")

    # connection.close()

def update_db(connection):

    '''try:
        cursor = connection.cursor()
        connection.start_transaction()

        call_key = input("Enter the Call Key to update: ")

        # Verify if the call_key exists
        check_call_query = """
        SELECT COUNT(*) FROM calls WHERE call_key = %s
        """
        cursor.execute(check_call_query, (call_key,))
        result = cursor.fetchone()

        if result[0] == 0:
            print(f"No record found with call_key: {call_key}")
            return

        call_query = """
        SELECT record_ID FROM calls WHERE call_key = %s
        """
        cursor.execute(call_query, (call_key,))
        record_ID = cursor.fetchone()

        if not record_ID:
            print(f"No record found for Call Key: {call_key}")
            return
        
        record_ID = record_ID[0]

        incident_query = """
        SELECT location_record_ID FROM incidents WHERE record_ID = %s
        """
        cursor.execute(incident_query, (record_ID,))
        location_record_ID = cursor.fetchone()

        if not location_record_ID:
            print(f"Not record found for record_ID: {record_ID}")
            return
        
        location_record_ID = location_record_ID[0]

        location_query = """
        SELECT police_station_ID FROM locations WHERE location_record_ID = %s
        """
        cursor.execute(location_query, (location_record_ID,))
        police_station_ID = cursor.fetchone()

        if not police_station_ID:
            print(f"No location found for location_record_ID: {location_record_ID}")
            return
        
        police_station_ID = police_station_ID[0]

        # User input
        # emergency_levels = ["Non-Emergency", "Low", "Medium", "High", "Emergency", "Out of Service", ""]
        # new_priority = select_from_enum(emergency_levels, "Select new priority (select 7 to skip): ")
        new_priority = input("Enter new priority (leave blank to skip): ")
        new_call_number = input("Enter new call number (leave blank to skip): ")
        new_incident_location = input("Enter new incident location (leave blank to skip): ")
        new_district = input("Enter new district (leave blank to skip): ")
        new_neighborhood = input("Enter new neighborhood of the incident (leave blank to skip): ")
        new_description = input("Enter new description (leave blank to skip): ")
        new_location = input("Enter new reporters location (leave blank to skip): ")
        new_needs_sync = input("Enter is the data updated on all devices (1 or 0) (leave blank to skip): ")
        new_council_district = input("Enter new council district (leave blank to skip): ")
        new_com_stat_areas = input("Enter new known neighborhoods near the incident (leave blank to skip): ")
        new_census_tracts = input("Enter new census tracts (leave blank to skip): ")
        new_zip_code = input("Enter new zip code (leave blank to skip): ")
        new_esri_oid = input("Enter new esri_oid (leave blank to skip): ")
        new_police_post = input("Enter new police post (leave blank to skip): ")
        new_sheriff_district = input("Enter new sheriff district (leave blank to skip): ")
        new_police_district = input("Enter new police district (leave blank to skip): ")

        # Update police_stations table
        if new_police_post:
            update_query = """
        UPDATE police_stations SET police_post = %s WHERE police_station_ID = %s
        """
            cursor.execute(update_query, (new_police_post, police_station_ID))
        
        if new_sheriff_district:
            update_query = """
        UPDATE police_stations SET sheriff_district = %s WHERE police_station_ID = %s
        """
            cursor.execute(update_query, (new_sheriff_district, police_station_ID))

        if new_police_post:
            update_query = """
        UPDATE police_stations SET police_district = %s WHERE police_station_ID = %s
        """
            cursor.execute(update_query, (new_police_district, police_station_ID))

        # Update locations table
        if new_location:
            update_query = """
        UPDATE locations SET location = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_location, location_record_ID))
        
        if new_council_district:
            update_query = """
        UPDATE locations SET council_district = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_council_district, location_record_ID))
        
        if new_com_stat_areas:
            update_query = """
        UPDATE locations SET community_statistical_areas = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_com_stat_areas, location_record_ID))

        if new_census_tracts:
            update_query = """
        UPDATE locations SET census_tracts = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_census_tracts, location_record_ID))

        if new_zip_code:
            update_query = """
        UPDATE locations SET zip_code = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_zip_code, location_record_ID))

        if new_esri_oid:
            update_query = """
        UPDATE locations SET esri_oid = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_esri_oid, location_record_ID))

        if new_neighborhood:
            update_query = """
        UPDATE locations SET neighborhood = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_neighborhood, location_record_ID))

        # Update incidents table
        if new_district:
            update_query = """
        UPDATE incidents SET district = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_district, record_ID))

        if new_description:
            update_query = """
        UPDATE incidents SET description = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_district, record_ID))
        
        if new_incident_location:
            update_query = """
        UPDATE incidents SET incident_location = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_incident_location, record_ID))
        
        if new_needs_sync:
            update_query = """
        UPDATE incidents SET needs_sync = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_needs_sync, record_ID))

        # Update calls table
        if new_priority:
            update_query = """
        UPDATE calls SET needs_sync = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_priority, record_ID))

        if new_call_number:
            update_query = """
        UPDATE calls SET call_number = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_call_number, record_ID))

        connection.commit()
        print(f"Record with call_key {call_key} updated successfully.")

        
    except Error as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

    finally:
        if cursor:
            cursor.close()'''
    try:
        cursor = connection.cursor()
        connection.start_transaction()

        call_key = input("Enter the Call Key to update: ")

        # Verify if the call_key exists
        check_call_query = """
        SELECT COUNT(*) FROM calls WHERE call_key = %s
        """
        cursor.execute(check_call_query, (call_key,))
        result = cursor.fetchone()

        if result[0] == 0:
            print(f"No record found with call_key: {call_key}")
            return

        call_query = """
        SELECT record_ID FROM calls WHERE call_key = %s
        """
        cursor.execute(call_query, (call_key,))
        record_ID = cursor.fetchone()

        if not record_ID:
            print(f"No record found for Call Key: {call_key}")
            return
        
        record_ID = record_ID[0]

        incident_query = """
        SELECT location_record_ID FROM incidents WHERE record_ID = %s
        """
        cursor.execute(incident_query, (record_ID,))
        location_record_ID = cursor.fetchone()

        if not location_record_ID:
            print(f"Not record found for record_ID: {record_ID}")
            return
        
        location_record_ID = location_record_ID[0]

        location_query = """
        SELECT police_station_ID FROM locations WHERE location_record_ID = %s
        """
        cursor.execute(location_query, (location_record_ID,))
        police_station_ID = cursor.fetchone()

        if not police_station_ID:
            print(f"No location found for location_record_ID: {location_record_ID}")
            return
        
        police_station_ID = police_station_ID[0]

        # User input
        emergency_levels = ["Non-Emergency", "Low", "Medium", "High", "Emergency", "Out of Service", ""]
        new_priority = select_from_enum(emergency_levels, "Select new priority (select 7 to skip): ")
        # new_priority = input("Enter new priority (leave blank to skip): ")
        new_call_number = input("Enter new call number (leave blank to skip): ")
        new_incident_location = input("Enter new incident location (leave blank to skip): ")
        districts = ["WD", "NW", "SE", "NE", "SD", "CD", "TRU", "ED", "SW", "ND", "SS", "CW", ""]
        new_district = select_from_enum(districts, "Select new district (select 13 to skip): ")
        # new_district = input("Enter new district (leave blank to skip): ")
        new_neighborhood = input("Enter new neighborhood of the incident (leave blank to skip): ")
        new_description = input("Enter new description (leave blank to skip): ")
        new_location = input("Enter new reporters location (leave blank to skip): ")
        new_needs_sync = input("Is the new data updated in all devices? (Select 1 for Yes and 0 for No): ")
        # new_needs_sync = input("Enter is the data updated on all devices (1 or 0) (leave blank to skip): ")
        coun_dist_num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", ""]
        new_council_district = select_from_enum(coun_dist_num, "Select new council district (select 16 to skip): ")
        # new_council_district = input("Enter new council district (leave blank to skip): ")
        new_com_stat_areas = input("Enter new known neighborhoods near the incident (leave blank to skip): ")
        new_census_tracts = input("Enter new census tracts (leave blank to skip): ")
        new_census_tracts = f"Census Tract {new_census_tracts}"
        if new_census_tracts == "Census Tract ":
            new_census_tracts = ""
        new_zip_code = input("Enter new zip code (leave blank to skip): ")
        new_esri_oid = input("Enter new esri_oid (leave blank to skip): ")
        new_police_post = input("Enter new police post (leave blank to skip): ")
        sheriff_district = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", ""]
        new_sheriff_district = select_from_enum(sheriff_district, "Select new sheriff district (select 11 to skip): ")
        # new_sheriff_district = input("Enter new sheriff district (leave blank to skip): ")
        police_district = ["Central", "Eastern", "Northeaster", "Northern", "Northwestern", "Southeastern", "Southern", "Southwestern", "Western", ""]
        new_police_district = select_from_enum(police_district, "Select new police district (select 10 to skip): ")
        # new_police_district = input("Enter new police district (leave blank to skip): ")

        # Update police_stations table
        if new_police_post:
            update_query = """
        UPDATE police_stations SET police_post = %s WHERE police_station_ID = %s
        """
            cursor.execute(update_query, (new_police_post, police_station_ID))
        
        if new_sheriff_district:
            update_query = """
        UPDATE police_stations SET sheriff_district = %s WHERE police_station_ID = %s
        """
            cursor.execute(update_query, (new_sheriff_district, police_station_ID))

        if new_police_post:
            update_query = """
        UPDATE police_stations SET police_district = %s WHERE police_station_ID = %s
        """
            cursor.execute(update_query, (new_police_post, police_station_ID))

        # Update locations table
        if new_location:
            update_query = """
        UPDATE locations SET location = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_location, location_record_ID))
        
        if new_council_district:
            update_query = """
        UPDATE locations SET council_district = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_council_district, location_record_ID))
        
        if new_com_stat_areas:
            update_query = """
        UPDATE locations SET community_statistical_areas = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_com_stat_areas, location_record_ID))

        if new_census_tracts:
            update_query = """
        UPDATE locations SET census_tracts = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_census_tracts, location_record_ID))

        if new_zip_code:
            update_query = """
        UPDATE locations SET zip_code = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_zip_code, location_record_ID))

        if new_esri_oid:
            update_query = """
        UPDATE locations SET esri_oid = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_esri_oid, location_record_ID))

        if new_neighborhood:
            update_query = """
        UPDATE locations SET neighborhood = %s WHERE location_record_ID = %s
        """
            cursor.execute(update_query, (new_neighborhood, location_record_ID))

        # Update incidents table
        if new_district:
            update_query = """
        UPDATE incidents SET district = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_district, record_ID))

        if new_description:
            update_query = """
        UPDATE incidents SET description = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_description, record_ID))
        
        if new_incident_location:
            update_query = """
        UPDATE incidents SET incident_location = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_incident_location, record_ID))
        
        if new_needs_sync:
            update_query = """
        UPDATE incidents SET needs_sync = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_needs_sync, record_ID))

        # Update calls table
        if new_priority:
            update_query = """
        UPDATE calls SET priority = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_priority, record_ID))

        if new_call_number:
            update_query = """
        UPDATE calls SET call_number = %s WHERE record_ID = %s
        """
            cursor.execute(update_query, (new_call_number, record_ID))

        connection.commit()
        print(f"Record with call_key {call_key} updated successfully.")

        
    except Error as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

    finally:
        if cursor:
            cursor.close()

def select_from_enum(options, prompt):
    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
