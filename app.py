import tkinter as tk
from tkinter import ttk, END
import customtkinter as ctk
import mysql.connector as my
from tkcalendar import Calendar,DateEntry
import os

os.system("sudo systemctl start mariadb")

#Constant Portion:
USER = "root"
PASSWORD = "766900"

FONT = ("Arial",20,"bold")

#Function Portion:
def info():
    id = idcsDataEntry.get()

    idShowEntry.delete(0,END)
    idcsShowEntry.delete(0,END)
    nameShowEntry.delete(0,END)
    joinShowEntry.delete(0,END)
    sectionShowEntry.delete(0,END)

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    query = "select * from operator_data where dcs_id = %s"
    values = [id]
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    for i in data:
        print(i)
    idShowEntry.insert(0,i[0])
    idcsShowEntry.insert(0,i[1])
    nameShowEntry.insert(0,i[2])
    joinShowEntry.insert(0,i[3])
    sectionShowEntry.insert(0,i[4])

    mydb.close()
    idcsDataEntry.delete(0,END)

    #lists = []

def delete():
    id = idcsDataEntry.get()
    mydb = my.connect(
            host = "127.0.0.1",
            user = USER,
            password = PASSWORD,
            database = "my_app_db"
            )
    query = "delete from operator_data where dcs_id = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    idcsDataEntry.delete(0,END)


def insert():
    id = idcsInsertEntry.get()
    name = nameInsertEntry.get()
    join = joinInsertDateEntry.get_date()
    section = sectionInsertOption.get()

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    values = (id,name,join,section)
    query = "insert into operator_data(dcs_id,name,join_date,section) values(%s,%s,'%s',%s)"
    try:
        mycursor.execute(query,values)
        mydb.commit()
    except:
        try:

            query = "create table operator_data(id int not null auto_increment,dcs_id varchar(10) not null,name varchar(100) not null,join_date date not null,section varchar(50) not null, primary key(id))"
            mycursor.execute(query)
            mydb.commit()
        except:
            print("Table already existed")
        query = "insert into operator_data(dcs_id,name,join_date,section) values(%s,%s,%s,%s)"
        mycursor.execute(query,values)
        mydb.commit()
    mydb.close()
    idcsInsertEntry.delete(0,END)
    nameInsertEntry.delete(0,END)
    
def section_info():

    id = sectionDataOption.get()
    
    top = tk.Toplevel(root)
    #top.geometry("600x600")
    top.title("Section Data")

    showFrame = ctk.CTkFrame(top)
    showFrame.pack(expand="yes")
    #showTextbox = ctk.CTkTextbox(showFrame,wrap="none",width=600)
    #showTextbox.grid(row=0,column=0)
    #showTextbox.insert(1.0,i)
    showTable = ttk.Treeview(showFrame,column=("id","dcs_id","name","join_date","section"))
    showTable.heading("id",text="ID")
    showTable.heading("dcs_id",text="DCS ID")
    showTable.heading("name",text="Name")
    showTable.heading("join_date",text="Join Date")
    showTable.heading("section",text="Section")
    showTable["show"]="headings"
    showTable.grid(row=1,column=0)
    
    mydb = my.connect(
            host = "127.0.0.1",
            user = USER,
            password = PASSWORD,
            database = "my_app_db"
            )
    query = "select * from operator_data where section = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    info = mycursor.fetchall()
    """for i in info:

        print(i)
        showTextbox.insert(END,"".join(str(i))+"\n")"""
    for i in info:
        showTable.insert("",END,values=i)
    mydb.close()

def update():

    id = idcsInsertEntry.get()
    name = nameInsertEntry.get()
    join = joinInsertDateEntry.get_date()
    section = sectionInsertOption.get()

    print(type(join))

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    values = (name,join,section,id)
    query = "update  operator_data set name=%s,join_date=%s,section=%s where dcs_id=%s"

    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    idcsInsertEntry.delete(0,END)
    nameInsertEntry.delete(0,END)


#Design Portion:
root = ctk.CTk()
root.title("My App")
root.geometry("800x600")
rootFrame = ctk.CTkFrame(root)
rootFrame.pack(expand="Yes")

#Data Frame Section:
firstFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
firstFrame.grid(row=0,column=0,padx=10,pady=10)

operatorDataFrame = ctk.CTkFrame(firstFrame,width=200,height=200)
operatorDataFrame.grid(row=0,column=0,padx=10,pady=10)

idcsDataLabel = ctk.CTkLabel(operatorDataFrame,text="DCS ID:",font=FONT)
idcsDataLabel.grid(row=0,column=0)
idcsDataEntry = ctk.CTkEntry(operatorDataFrame,width=200,placeholder_text="DCS0000",font=FONT)
idcsDataEntry.grid(row=0,column=1)
enterDataButton = ctk.CTkButton(operatorDataFrame,text="Show",command=info,width=10)
enterDataButton.grid(row=1,column=0)
deleteDataButton = ctk.CTkButton(operatorDataFrame,text="Delete",command=delete,width=10)
deleteDataButton.grid(row=1,column=1)


sectionDataLabel = ctk.CTkLabel(operatorDataFrame,text="Select Section:",font=FONT)
sectionDataLabel.grid(row=4,column=0)
sectionDataOption = ctk.CTkOptionMenu(operatorDataFrame,values = ["Hydrated Lime","Lime Kiln","Pmcc","Store","Boiler","Power House","Utility","Crane","Mechanic","Workshop","Feeding"])
sectionDataOption.grid(row=4,column=1)
enterDataButton = ctk.CTkButton(operatorDataFrame,text="Show Section",command=section_info,width=10)
enterDataButton.grid(row=5,columnspan=2)


#Insert Frame Section:
secondFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
secondFrame.grid(row=1,column=0,padx=10,pady=10)

operatorInsertFrame = ctk.CTkFrame(secondFrame,width=200,height=200)
operatorInsertFrame.grid(row=0,column=0,padx=10,pady=20)
idcsInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="DCS ID: ",font=FONT)
idcsInsertLabel.grid(row=0,column=0)
idcsInsertEntry = ctk.CTkEntry(operatorInsertFrame,width=200,placeholder_text="DCS0000",font=FONT)
idcsInsertEntry.grid(row=0,column=1)
nameInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="Name: ",font=FONT)
nameInsertLabel.grid(row=1,column=0)
nameInsertEntry = ctk.CTkEntry(operatorInsertFrame,width=200,placeholder_text="Firstname Lastname",font=FONT)
nameInsertEntry.grid(row=1,column=1)
joinInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="Join Date: ",font=FONT)
joinInsertLabel.grid(row=2,column=0)
joinInsertDateEntry = DateEntry(operatorInsertFrame,width=20,date_pattern='YYYY-mm-dd', background="darkblue", foreground="white", borderwidth=2)
joinInsertDateEntry.grid(row=2,column=1)
#joinInsertCalendar = Calendar(operatorInsertFrame,width=20)
#joinInsertCalendar.grid(row=3,columnspan=2)
sectionInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="Section: ",font=FONT)
sectionInsertLabel.grid(row=4,column=0)
sectionInsertOption = ctk.CTkOptionMenu(operatorInsertFrame,values=["Hydrated Lime","Power House","Utility","Lime Kiln","Boiler","Crane","Mechanic","Workshop","Store","Pmcc","Feeding"],)
sectionInsertOption.grid(row=4,column=1)
enterInsertButton = ctk.CTkButton(operatorInsertFrame,text="Insert",command=insert,width=10)
enterInsertButton.grid(row=5,column=0)
updateInsertButton = ctk.CTkButton(operatorInsertFrame,text="Update",command=update,width=10)
updateInsertButton.grid(row=5,column=1)

#Show Frame Section:
thirdFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
thirdFrame.grid(row=2,column=0,padx=10,pady=10)

operatorShowFrame = ctk.CTkFrame(thirdFrame,width=200,height=300)
operatorShowFrame.grid(row=0,column=0,padx=10,pady=10)

idShowLabel = ctk.CTkLabel(operatorShowFrame,text="ID:",font=FONT)
idShowLabel.grid(row=0,column=0)
idShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
idShowEntry.grid(row=0,column=1)
idcsShowLabel = ctk.CTkLabel(operatorShowFrame,text="DCS_ID:",font=FONT)
idcsShowLabel.grid(row=1,column=0)
idcsShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
idcsShowEntry.grid(row=1,column=1)
nameShowLabel = ctk.CTkLabel(operatorShowFrame,text="NAME:",font=FONT)
nameShowLabel.grid(row=2,column=0)
nameShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
nameShowEntry.grid(row=2,column=1)
joinShowLabel = ctk.CTkLabel(operatorShowFrame,text="JOIN DATE:",font=FONT)
joinShowLabel.grid(row=3,column=0)
joinShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
joinShowEntry.grid(row=3,column=1)
sectionShowLabel = ctk.CTkLabel(operatorShowFrame,text="SECTION:",font=FONT)
sectionShowLabel.grid(row=4,column=0)
sectionShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
sectionShowEntry.grid(row=4,column=1)



root.mainloop()
