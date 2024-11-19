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
    
def get_date_time():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def get_information():
    values = []

    call_key = "Randomsomething"
    call_date_time = get_date_time()
    priority = ""
    call_number = input("Insert your phone number: ")

    district = input("Insert the district abbreviation: ")
    desription = input("Insert the name of the crime: ")
    incident_location = input("Insert the location where the crime occured: ")
    needs_sync = input("Press '1' if the data is updated in all devices: ")

    location = input("Insert the reporters localization: ")
    neighborhood = input("Insert the neighborhood of the incident: ")
    council_district = input("Insert the number of the council district: ")
    com_stat_areas = input("Insert a known neighborhoods near the incident (remember to use '/' to separate them): ")
    census_tracts = input("Insert the census tract: ")
    census_tracts = "Census Tract " + census_tracts
    zip_code = input("Insert the ZIP Code: ")
    esri_oid = input("Insert the Esri OID: ")

    police_post = input("Insert the number of the police post: ")
    sherrif_district = input("Insert the sherrif district: ")
    police_district = input("Insert the police district: ")

    fields = [call_key, call_date_time, priority, call_number, district, desription, incident_location, needs_sync, 
              location, neighborhood, council_district, com_stat_areas, census_tracts, zip_code, esri_oid, police_post, 
              sherrif_district, police_district]
    
    for element in fields:
        values.append(element)

    for _ in values:
        print(_)


def insert_to_db(information):

    # police_stations table

    # locations table
    
    # incidents table

    # calls table

    try:
        py = 1
    except Error as e:
        print(f"Error: {e}")
        #connection.rollback()




def main():
    connection = connect_to_db()
    while connection:
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
        elif choice == "2":
            print("Selected 2")
        elif choice == "3":
            print("Selected 3")
        elif choice == "0":
            print("Selected Exit")
            break
        else:
            print("Invalid option, please try again")

    # connection.close()


# main()

get_information()

''' Passing from a dictionary to a tuple THE INSERT VALUES MUST BE A TUPLE
data = {
    "columna1": "valor1",
    "columna2": "valor2",
    "columna3": "valor3"
}

insert_query = """
INSERT INTO tu_tabla (columna1, columna2, columna3)
VALUES (%s, %s, %s)
"""

# Convert dictionary values to a tuple
valores = tuple(data.values())

cursor.execute(insert_query, valores)
connection.commit()

'''
