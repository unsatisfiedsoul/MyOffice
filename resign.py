import tkinter as tk
from tkinter import ttk, END
import customtkinter as ctk
import mysql.connector as my
from tkcalendar import Calendar,DateEntry
import os
import babel.numbers

#os.system("sudo systemctl start mariadb")

#Constant Portion:
USER = "root"
PASSWORD = "746589"

FONT = ("Arial",16,"bold")

#Function Portion:
def info():
    id = idcsDataEntry.get()

    
    idcsShowEntry.delete(0,END)
    nameShowEntry.delete(0,END)
    joinShowEntry.delete(0,END)
    resignShowEntry.delete(0,END)
    sectionShowEntry.delete(0,END)

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    query = "select operator_data.dcs_id, operator_data.name, operator_data.join_date,operator_resign.resign_date,operator_data.section from operator_data inner join operator_resign on operator_data.dcs_id = operator_resign.dcs_id where operator_data.dcs_id = %s"
    values = [id]
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    for i in data:
        print(i)
    
    idcsShowEntry.insert(0,i[0])
    nameShowEntry.insert(0,i[1])
    joinShowEntry.insert(0,i[2])
    resignShowEntry.insert(0,i[3])
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
    query = "delete from operator_resign where dcs_id = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    idcsDataEntry.delete(0,END)


def insert():
    id = idcsInsertEntry.get()
    resign = resignInsertDateEntry.get_date()
    

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    values = (id,resign)
    query = "insert into operator_resign(dcs_id,resign_date) values(%s,'%s')"
    try:
        mycursor.execute(query,values)
        mydb.commit()
    except:
        try:

            query = "create table operator_resign(id int not null auto_increment,dcs_id varchar(100) not null, resign_date date not null, primary key(id))"
            mycursor.execute(query)
            mydb.commit()
        except:
            print("Table already existed")
        query = "insert into operator_resign(dcs_id,resign_date) values(%s,%s)"
        mycursor.execute(query,values)
        mydb.commit()
    mydb.close()
    idcsInsertEntry.delete(0,END)
    
    
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
    
    entries = []
    for i in range(0,500):
	    args = (i,"dcs_id","name","join_date","resign_date","section")
	    entries.append(args)    

    showTable = ttk.Treeview(showFrame,column=("dcs_id","name","join_date","resign_date","section"))
    
    showTable.heading("dcs_id",text="DCS ID")
    showTable.heading("name",text="Name")
    showTable.heading("join_date",text="Join Date")
    showTable.heading("resign_date",text="Resign Date")
    showTable.heading("section",text="Section")

    showTable.column('0', minwidth=50,anchor="center", width=100, stretch=False)
    showTable.column("1", minwidth=100,anchor="center", width=200, stretch=False)
    showTable.column("2", minwidth=200,anchor="center", width=200, stretch=False)
    showTable.column("3", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("4", minwidth=100,anchor="center", width=100, stretch=False)
    

    showTable["show"]="headings"
    showTable.grid(row=1,column=0)
    

    
    mydb = my.connect(
            host = "127.0.0.1",
            user = USER,
            password = PASSWORD,
            database = "my_app_db"
            )
    query = "select operator_data.dcs_id, operator_data.name, operator_data.join_date,operator_resign.resign_date,operator_data.section from operator_data inner join operator_resign on operator_data.dcs_id = operator_resign.dcs_id where operator_data.section = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    info = mycursor.fetchall()
    """for i in info:

        print(i)
        showTextbox.insert(END,"".join(str(i))+"\n")"""
    for i in info:
        showTable.insert("",END,values=i)
    
    """for entry in info:
	    showTable.insert("",END,text=entry[0],values=(entry[1], entry[2], entry[3], entry[4]))
    """
    vs = ttk.Scrollbar(showFrame,orient="vertical",command=showTable.yview)
    showTable.configure(yscrollcommand=vs.set)
    vs.grid(row=1,column=2,sticky="ns")
    mydb.close()

def all_info():
    top = tk.Toplevel(root)
    #top.geometry("600x600")
    top.title("All Data")

    showFrame = ctk.CTkFrame(top)
    showFrame.pack(expand="yes")
    #showTextbox = ctk.CTkTextbox(showFrame,wrap="none",width=600)
    #showTextbox.grid(row=0,column=0)
    #showTextbox.insert(1.0,i)
    
    entries = []
    for i in range(0,500):
	    args = (i,"dcs_id","name","join_date","resign_date","section")
	    entries.append(args)    

    showTable = ttk.Treeview(showFrame,column=("dcs_id","name","join_date","resign_date","section"))
    
    showTable.heading("dcs_id",text="DCS ID")
    showTable.heading("name",text="Name")
    showTable.heading("join_date",text="Join Date")
    showTable.heading("resign_date",text="Resign Date")
    showTable.heading("section",text="Section")

    showTable.column('0', minwidth=50,anchor="center", width=100, stretch=False)
    showTable.column("1", minwidth=100,anchor="center", width=200, stretch=False)
    showTable.column("2", minwidth=200,anchor="center", width=200, stretch=False)
    showTable.column("3", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("4", minwidth=100,anchor="center", width=100, stretch=False)

    showTable["show"]="headings"
    showTable.grid(row=1,column=0)
    

    
    mydb = my.connect(
            host = "127.0.0.1",
            user = USER,
            password = PASSWORD,
            database = "my_app_db"
            )
    query = "select operator_data.dcs_id, operator_data.name, operator_data.join_date,operator_resign.resign_date,operator_data.section from operator_data inner join operator_resign on operator_data.dcs_id = operator_resign.dcs_id"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query)
    info = mycursor.fetchall()
    """for i in info:

        print(i)
        showTextbox.insert(END,"".join(str(i))+"\n")"""
    for i in info:
        showTable.insert("",END,values=i)
    
    """for entry in info:
	    showTable.insert("",END,text=entry[0],values=(entry[1], entry[2], entry[3], entry[4]))
    """
    vs = ttk.Scrollbar(showFrame,orient="vertical",command=showTable.yview)
    showTable.configure(yscrollcommand=vs.set)
    vs.grid(row=1,column=2,sticky="ns")
    mydb.close()

def update():

    id = idcsInsertEntry.get()
    
    resign = resignInsertDateEntry.get_date()
    

    print(type(join))

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    values = (resign,id)
    query = "update  operator_resign set resign_date=%s where dcs_id=%s"

    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    idcsInsertEntry.delete(0,END)
    


#Design Portion:
root = ctk.CTk()
root.title("Resign App")
root.geometry("400x500")
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
enterDataButton.grid(row=5,column=0)
allDataButton = ctk.CTkButton(operatorDataFrame,text="Show All",command=all_info,width=10)
allDataButton.grid(row=5,column=1)


#Insert Frame Section:
secondFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
secondFrame.grid(row=1,column=0,padx=10,pady=10)

operatorInsertFrame = ctk.CTkFrame(secondFrame,width=200,height=200)
operatorInsertFrame.grid(row=0,column=0,padx=10,pady=20)
idcsInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="DCS ID: ",font=FONT)
idcsInsertLabel.grid(row=0,column=0)
idcsInsertEntry = ctk.CTkEntry(operatorInsertFrame,width=200,placeholder_text="DCS0000",font=FONT)
idcsInsertEntry.grid(row=0,column=1)

resignInsertLabel = ctk.CTkLabel(operatorInsertFrame,text="Resign Date: ",font=FONT)
resignInsertLabel.grid(row=2,column=0)
resignInsertDateEntry = DateEntry(operatorInsertFrame,width=20,date_pattern='YYYY-mm-dd', background="darkblue", foreground="white", borderwidth=2)
resignInsertDateEntry.grid(row=2,column=1)
#joinInsertCalendar = Calendar(operatorInsertFrame,width=20)
#joinInsertCalendar.grid(row=3,columnspan=2)

enterInsertButton = ctk.CTkButton(operatorInsertFrame,text="Insert",command=insert,width=10)
enterInsertButton.grid(row=5,column=0)
updateInsertButton = ctk.CTkButton(operatorInsertFrame,text="Update",command=update,width=10)
updateInsertButton.grid(row=5,column=1)

#Show Frame Section:
thirdFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
thirdFrame.grid(row=2,column=0,padx=10,pady=10)

operatorShowFrame = ctk.CTkFrame(thirdFrame,width=200,height=300)
operatorShowFrame.grid(row=0,column=0,padx=10,pady=10)


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
resignShowLabel = ctk.CTkLabel(operatorShowFrame,text="RESIGN DATE:",font=FONT)
resignShowLabel.grid(row=4,column=0)
resignShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
resignShowEntry.grid(row=4,column=1)
sectionShowLabel = ctk.CTkLabel(operatorShowFrame,text="SECTION:",font=FONT)
sectionShowLabel.grid(row=5,column=0)
sectionShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
sectionShowEntry.grid(row=5,column=1)



root.mainloop()
