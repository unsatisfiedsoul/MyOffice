import os
import init
os.system("pip install tkinter")
os.system("pip install customtkinter")
os.system("pip install tkcalendar")
import init 
import customtkinter as ctk 
import mysql.connector as my

def log():
    inputUsername = usernameEntry.get()
    inputPassword = passwordEntry.get()

    mydb = my.connect(
        host = "127.0.0.1",
        user = "root",
        password = "766900",
        database = "my_app_db"
    )
    mycursor = mydb.cursor()
    query = "select password from users where username=%s"
    data = [inputUsername]
    mycursor.execute(query,data)
    results = mycursor.fetchall()
    for row in results:
        pwd=row[0]

    if (inputPassword == pwd):
        print("Welcome")
    mydb.close()
    root.destroy()
    import app

root = ctk.CTk()
root.title("My App")
root.geometry("500x400")
rootFrame = ctk.CTkFrame(root)
rootFrame.pack(expand="Yes")

usernameLabel = ctk.CTkLabel(rootFrame,text="Username:",font=("Helvatica",16))
usernameLabel.grid(row=0,column=0,padx=10,pady=20)
usernameEntry = ctk.CTkEntry(rootFrame,width=300,font=("Helvatica",16))
usernameEntry.grid(row=0,column=1,padx=10,pady=20)
passwordLabel = ctk.CTkLabel(rootFrame,text="Password:",font=("Helvatica",16))
passwordLabel.grid(row=1,column=0,padx=10,pady=20)
passwordEntry = ctk.CTkEntry(rootFrame,width=300,font=("Helvatica",16))
passwordEntry.grid(row=1,column=1,padx=10,pady=20)
loginButton = ctk.CTkButton(rootFrame,text="Login",command=log,font=("Helvatica",16))
loginButton.grid(row=2,columnspan=2,padx=10,pady=20)

root.mainloop()
