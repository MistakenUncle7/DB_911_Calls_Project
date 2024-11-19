import customtkinter as ctk

# title_label = ctk.CTkLabel(root, text="Searc Bar", font=ctk.CTkFont(size=30, weight="bold"))
# title_label.pack()

import customtkinter as ctk
import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="911_emergency_calls"  # Replace with your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to handle insert query
def insert_data():
    name = entry_name.get()
    age = entry_age.get()

    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO your_table_name (name, age) VALUES (%s, %s)"
        cursor.execute(query, (name, age))
        connection.commit()
        cursor.close()
        connection.close()
        print("Data inserted successfully")
    else:
        print("Connection failed.")

# Function to handle update query
def update_data():
    id = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()

    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "UPDATE your_table_name SET name = %s, age = %s WHERE id = %s"
        cursor.execute(query, (name, age, id))
        connection.commit()
        cursor.close()
        connection.close()
        print("Data updated successfully")
    else:
        print("Connection failed.")

# Function to handle delete query
def delete_data():
    id = entry_id.get()

    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = "DELETE FROM your_table_name WHERE id = %s"
        cursor.execute(query, (id,))
        connection.commit()
        cursor.close()
        connection.close()
        print("Data deleted successfully")
    else:
        print("Connection failed.")

# Create the main window
root = ctk.CTk()

# Dropdown for Structural Queries
dropdown = ctk.CTkComboBox(root, values=["Insert", "Update", "Delete"], width=200)
dropdown.grid(row=0, column=0, padx=10, pady=10)

# Entry fields for form (Insert and Update)
label_name = ctk.CTkLabel(root, text="Name:")
label_name.grid(row=1, column=0, padx=10, pady=5)
entry_name = ctk.CTkEntry(root, width=200)
entry_name.grid(row=1, column=1, padx=10, pady=5)

label_age = ctk.CTkLabel(root, text="Age:")
label_age.grid(row=2, column=0, padx=10, pady=5)
entry_age = ctk.CTkEntry(root, width=200)
entry_age.grid(row=2, column=1, padx=10, pady=5)

# Additional entry for Update and Delete
label_id = ctk.CTkLabel(root, text="ID:")
label_id.grid(row=0, column=1, padx=10, pady=5)
entry_id = ctk.CTkEntry(root, width=200)
entry_id.grid(row=0, column=2, padx=10, pady=5)

# Buttons for actions
def handle_query():
    query_type = dropdown.get()

    if query_type == "Insert":
        insert_data()
    elif query_type == "Update":
        update_data()
    elif query_type == "Delete":
        delete_data()

button_execute = ctk.CTkButton(root, text="Execute Query", command=handle_query)
button_execute.grid(row=3, column=0, columnspan=3, pady=10)

# Run the GUI
root.mainloop()

