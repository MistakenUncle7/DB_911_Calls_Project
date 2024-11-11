import customtkinter as ctk
# import mysql.connector

# Initialize customTkinter
root = ctk.CTk()
root.set_appearance_mode("dark")
root.geometry("750x450")
root.title("911 Calls DataBase")

title_label = ctk.CTkLabel(root, text="Searc Bar", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack()

root.mainloop()