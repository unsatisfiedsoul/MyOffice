import tkinter as tk
from tkinter import ttk, END
import customtkinter as ctk
import mysql.connector as my
from tkcalendar import Calendar,DateEntry
import os

os.system("sudo systemctl start mariadb")

#Function Portion:
def info():
    id = idShowDataEntry.get()

    idShowEntry.delete(0,END)

    idcsShowEntry.delete(0,END)
    nameShowEntry.delete(0,END)
    joinShowEntry.delete(0,END)
    sectionShowEntry.delete(0,END)

    mydb = my.connect(
        host = "127.0.0.1",
        user = "root",
        password = "766900",
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
    idShowDataEntry.delete(0,END)

    #lists = []

def delete():
    id = idDeleteDataEntry.get()
    mydb = my.connect(
            host = "127.0.0.1",
            user = "root",
            password = "766900",
            database = "my_app_db"
            )
    query = "delete from operator_data where dcs_id = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    idDeleteDataEntry.delete(0,END)


def insert():
    id = idInsertEntry.get()
    name = nameInsertEntry.get()
    join = joinInsertDateEntry.get_date()
    section = sectionInsertOption.get()

    mydb = my.connect(
        host = "127.0.0.1",
        user = "root",
        password = "766900",
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
    idInsertEntry.delete(0,END)
    nameInsertEntry.delete(0,END)
    
def section_info():

    id = sectionShowDataOption.get()
    
    top = tk.Toplevel(root)
    #top.geometry("600x600")
    top.title("Section Data")

    showFrame = ctk.CTkFrame(top)
    showFrame.pack(expand="yes")
    showTextbox = ctk.CTkTextbox(showFrame,wrap="none",width=600)
    showTextbox.grid(row=0,column=0)
    #showTextbox.insert(1.0,i)
    
    mydb = my.connect(
            host = "127.0.0.1",
            user = "root",
            password = "766900",
            database = "my_app_db"
            )
    query = "select * from operator_data where section = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    info = mycursor.fetchall()
    for i in info:

        print(i)
        showTextbox.insert(END,"".join(str(i))+"\n")
    mydb.close()

def update():

    id = idcsUpdateEntry.get()
    name = nameUpdateEntry.get()
    join = joinUpdateEntry.get_date()
    section = sectionUpdateOption.get()

    print(type(join))

    mydb = my.connect(
        host = "127.0.0.1",
        user = "root",
        password = "766900",
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    values = (name,join,section,id)
    query = "update  operator_data set name=%s,join_date=%s,section=%s where dcs_id=%s"

    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    idcsUpdateEntry.delete(0,END)
    nameUpdateEntry.delete(0,END)


#Design Portion:
root = ctk.CTk()
root.title("My App")
root.geometry("800x600")
rootFrame = ctk.CTkFrame(root)
rootFrame.pack(expand="Yes")

#Data Frame Section:
firstFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
firstFrame.grid(row=0,column=0)

operatorShowDataFrame = ctk.CTkFrame(firstFrame,width=200,height=100)
operatorShowDataFrame.grid(row=0,column=0,padx=40,pady=20)

idShowDataLabel = ctk.CTkLabel(operatorShowDataFrame,text="DCS ID:")
idShowDataLabel.grid(row=0,column=0)
idShowDataEntry = ctk.CTkEntry(operatorShowDataFrame,width=200,placeholder_text="DCS0000")
idShowDataEntry.grid(row=0,column=1)
enterShowDataButton = ctk.CTkButton(operatorShowDataFrame,text="Show",command=info)
enterShowDataButton.grid(row=1,columnspan=2)

operatorDeleteDataFrame = ctk.CTkFrame(firstFrame,width=200,height=100)
operatorDeleteDataFrame.grid(row=2,column=0,padx=40,pady=20)
idDeleteDataLabel = ctk.CTkLabel(operatorDeleteDataFrame,text="DCS ID:")
idDeleteDataLabel.grid(row=2,column=0)
idDeleteDataEntry = ctk.CTkEntry(operatorDeleteDataFrame,width=200,placeholder_text="DCS0000")
idDeleteDataEntry.grid(row=2,column=1)
enterDeleteDataButton = ctk.CTkButton(operatorDeleteDataFrame,text="Delete",command=delete)
enterDeleteDataButton.grid(row=3,columnspan=2)

sectionShowDataLabel = ctk.CTkLabel(operatorShowDataFrame,text="Select Section:")
sectionShowDataLabel.grid(row=4,column=0)
sectionShowDataOption = ctk.CTkOptionMenu(operatorShowDataFrame,values = ["Hydrated Lime","Lime Kiln","Pmcc","Store","Boiler","Power House","Utility","Crane","Mechanic","Workshop","Feeding"])
sectionShowDataOption.grid(row=4,column=1)
enterShowDataButton = ctk.CTkButton(operatorShowDataFrame,text="Show Section",command=section_info)
enterShowDataButton.grid(row=5,columnspan=2)


#Insert Frame Section:
secondFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
secondFrame.grid(row=0,column=1)

operatorInsertFrame = ctk.CTkFrame(secondFrame,width=200,height=200)
operatorInsertFrame.grid(row=0,column=0,padx=40,pady=56)
idInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="DCS ID: ")
idInsertLabel.grid(row=0,column=0)
idInsertEntry = ctk.CTkEntry(operatorInsertFrame,width=200,placeholder_text="DCS0000")
idInsertEntry.grid(row=0,column=1)
nameInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="Name: ")
nameInsertLabel.grid(row=1,column=0)
nameInsertEntry = ctk.CTkEntry(operatorInsertFrame,width=200,placeholder_text="Firstname Lastname")
nameInsertEntry.grid(row=1,column=1)
joinInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="Join Date: ")
joinInsertLabel.grid(row=2,column=0)
joinInsertDateEntry = DateEntry(operatorInsertFrame,width=20,date_pattern='YYYY-mm-dd', background="darkblue", foreground="white", borderwidth=2)
joinInsertDateEntry.grid(row=2,column=1)
#joinInsertCalendar = Calendar(operatorInsertFrame,width=20)
#joinInsertCalendar.grid(row=3,columnspan=2)
sectionInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="Section: ")
sectionInsertLabel.grid(row=4,column=0)
sectionInsertOption = ctk.CTkOptionMenu(operatorInsertFrame,values=["Hydrated Lime","Power House","Utility","Lime Kiln","Boiler","Crane","Mechanic","Workshop","Store","Pmcc","Feeding"],)
sectionInsertOption.grid(row=4,column=1)
enterInsertButton = ctk.CTkButton(operatorInsertFrame,text="Insert",command=insert)
enterInsertButton.grid(row=5,columnspan=2)

#Show Frame Section:
thirdFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
thirdFrame.grid(row=1,column=0)

operatorShowFrame = ctk.CTkFrame(thirdFrame,width=200,height=200)
operatorShowFrame.grid(row=0,column=0,padx=40,pady=40)

idShowLabel = ctk.CTkLabel(operatorShowFrame,text="ID:")
idShowLabel.grid(row=0,column=0)
idShowEntry = ctk.CTkEntry(operatorShowFrame,width=200)
idShowEntry.grid(row=0,column=1)
idcsShowLabel = ctk.CTkLabel(operatorShowFrame,text="DCS_ID:")
idcsShowLabel.grid(row=1,column=0)
idcsShowEntry = ctk.CTkEntry(operatorShowFrame,width=200)
idcsShowEntry.grid(row=1,column=1)
nameShowLabel = ctk.CTkLabel(operatorShowFrame,text="NAME:")
nameShowLabel.grid(row=2,column=0)
nameShowEntry = ctk.CTkEntry(operatorShowFrame,width=200)
nameShowEntry.grid(row=2,column=1)
joinShowLabel = ctk.CTkLabel(operatorShowFrame,text="JOIN DATE:")
joinShowLabel.grid(row=3,column=0)
joinShowEntry = ctk.CTkEntry(operatorShowFrame,width=200)
joinShowEntry.grid(row=3,column=1)
sectionShowLabel = ctk.CTkLabel(operatorShowFrame,text="SECTION:")
sectionShowLabel.grid(row=4,column=0)
sectionShowEntry = ctk.CTkEntry(operatorShowFrame,width=200)
sectionShowEntry.grid(row=4,column=1)


#Update Frame Section:
fourthFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
fourthFrame.grid(row=1,column=1)

operatorUpdateFrame = ctk.CTkFrame(fourthFrame,width=200,height=200)
operatorUpdateFrame.grid(row=0,column=0,padx=40,pady=30)

tagUpdateLabel = ctk.CTkLabel(operatorUpdateFrame,text="Update Operator Data")
tagUpdateLabel.grid(row=0,columnspan=2)
idcsUpdateLabel = ctk.CTkLabel(operatorUpdateFrame,text="DCS_ID:")
idcsUpdateLabel.grid(row=1,column=0)
idcsUpdateEntry = ctk.CTkEntry(operatorUpdateFrame,width=200)
idcsUpdateEntry.grid(row=1,column=1)
nameUpdateLabel = ctk.CTkLabel(operatorUpdateFrame,text="NAME:")
nameUpdateLabel.grid(row=2,column=0)
nameUpdateEntry = ctk.CTkEntry(operatorUpdateFrame,width=200)
nameUpdateEntry.grid(row=2,column=1)
joinUpdateLabel = ctk.CTkLabel(operatorUpdateFrame,text="Join Date: ")
joinUpdateLabel.grid(row=3,column=0)
joinUpdateEntry = DateEntry(operatorUpdateFrame,width=20,date_pattern='YYYY-mm-dd', background="darkblue", foreground="white", borderwidth=2)
joinUpdateEntry.grid(row=3,column=1)
sectionUpdateLabel = ctk.CTkLabel(operatorUpdateFrame,text="Section: ")
sectionUpdateLabel.grid(row=4,column=0)
sectionUpdateOption = ctk.CTkOptionMenu(operatorUpdateFrame,values=["Hydrated Lime","Power House","Utility","Lime Kiln","Boiler","Crane","Mechanic","Workshop","Store","Pmcc","Feeding"],)
sectionUpdateOption.grid(row=4,column=1)
updateUpdateButton = ctk.CTkButton(operatorUpdateFrame,text="Update",command=update)
updateUpdateButton.grid(row=5,columnspan=2)

root.mainloop()
