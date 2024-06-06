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
    id = motoridDataEntry.get()

    idShowEntry.delete(0,END)
    motoridShowEntry.delete(0,END)
    motornameShowEntry.delete(0,END)
    hpShowEntry.delete(0,END)
    rpmShowEntry.delete(0,END)
    ampShowEntry.delete(0,END)
    updateShowEntry.delete(0,END)
    sectionShowEntry.delete(0,END)

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    query = "select * from motor_list where motor_id = %s"
    values = [id]
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    for i in data:
        print(i)
    idShowEntry.insert(0,i[0])
    motoridShowEntry.insert(0,i[1])
    motornameShowEntry.insert(0,i[2])
    hpShowEntry.insert(0,i[3])
    rpmShowEntry.insert(0,i[4])
    ampShowEntry.insert(0,i[5])
    updateShowEntry.insert(0,i[6])
    sectionShowEntry.insert(0,i[7])

    mydb.close()
    motoridDataEntry.delete(0,END)

    #lists = []

def delete():
    id = motoridDataEntry.get()
    mydb = my.connect(
            host = "127.0.0.1",
            user = USER,
            password = PASSWORD,
            database = "my_app_db"
            )
    query = "delete from motor_list where motor_id = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    motoridDataEntry.delete(0,END)


def insert():
    id = motoridInsertEntry.get()
    name = motornameInsertEntry.get()
    hp = hpInsertDateEntry.get()
    rpm = rpmInsertDateEntry.get()
    amp = ampInsertDateEntry.get()
    updates = updateInsertDateEntry.get_date()
    section = sectionInsertOption.get()

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    values = (id,name,hp,rpm,amp,updates,section)
    query = "insert into motor_list(motor_id,motor_name,hp,rpm,amp,updates,section) values(%s,%s,%s,%s,%s,%s,%s)"
    try:
        mycursor.execute(query,values)
        mydb.commit()
    except:
        try:

            query = "create table motor_list(id int not null auto_increment, motor_id varchar(100) not null, motor_name varchar(100) not null, hp varchar(50) not null, rpm varchar(50) not null, amp varchar(50) not null,updates date not null, section varchar(100) not null, primary key(id))"
            mycursor.execute(query)
            mydb.commit()
        except:
            print("Table already existed")
        query = "insert into motor_list(motor_id,motor_name,hp,rpm,amp,updates,section) values(%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(query,values)
        mydb.commit()
    mydb.close()
    motoridInsertEntry.delete(0,END)
    motornameInsertEntry.delete(0,END)
    hpInsertDateEntry.delete(0,END)
    rpmInsertDateEntry.delete(0,END)
    ampInsertDateEntry.delete(0,END)

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
    

    showTable = ttk.Treeview(showFrame,column=("id","motor_id","motor_name","hp","rpm","amp","update","section"))
    showTable.heading("id",text="ID")
    showTable.heading("motor_id",text="Motor ID")
    showTable.heading("motor_name",text="Motor Name")
    showTable.heading("hp",text="Horse Power")
    showTable.heading("rpm",text="RPM")
    showTable.heading("amp",text="Ampere")
    showTable.heading("update",text="Update")
    showTable.heading("section",text="Section")

    showTable.column('0', minwidth=50,anchor="center", width=50, stretch=False)
    showTable.column("1", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("2", minwidth=200,anchor="center", width=200, stretch=False)
    showTable.column("3", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("4", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("5", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("6", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("7", minwidth=100,anchor="center", width=100, stretch=False)

    showTable["show"]="headings"
    showTable.grid(row=1,column=0)
    

    
    mydb = my.connect(
            host = "127.0.0.1",
            user = USER,
            password = PASSWORD,
            database = "my_app_db"
            )
    query = "select * from motor_list where section = %s"
    values = [id]
    mycursor = mydb.cursor()
    mycursor.execute(query,values)
    info = mycursor.fetchall()
    """for i in info:

        print(i)
        showTextbox.insert(END,"".join(str(i))+"\n")"""
    for i in info:
        showTable.insert("",END,values=i)
    
    """
    for entry in info:
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
    
    

    showTable = ttk.Treeview(showFrame,column=("id","motor_id","motor_name","hp","rpm","amp","update","section"))
    showTable.heading("id",text="ID")
    showTable.heading("motor_id",text="MOTOR ID")
    showTable.heading("motor_name",text="MOTOR Name")
    showTable.heading("hp",text="Horse Power")
    showTable.heading("rpm",text="RPM")
    showTable.heading("amp",text="Ampere")
    showTable.heading("update",text="Update")
    showTable.heading("section",text="Section")

    showTable.column('0', minwidth=50,anchor="center", width=50, stretch=False)
    showTable.column("1", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("2", minwidth=200,anchor="center", width=200, stretch=False)
    showTable.column("3", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("4", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("5", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("6", minwidth=100,anchor="center", width=100, stretch=False)
    showTable.column("7", minwidth=100,anchor="center", width=100, stretch=False)

    showTable["show"]="headings"
    showTable.grid(row=1,column=0)
    

    
    mydb = my.connect(
            host = "127.0.0.1",
            user = USER,
            password = PASSWORD,
            database = "my_app_db"
            )
    query = "select * from motor_list order by section,motor_id"
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

    id = motoridInsertEntry.get()
    name = motornameInsertEntry.get()
    hp = hpInsertDateEntry.get()
    rpm = rpmInsertDateEntry.get()
    amp = ampInsertDateEntry.get()
    updates = updateInsertDateEntry.get_date()
    section = sectionInsertOption.get()

    print(type(hp))

    mydb = my.connect(
        host = "127.0.0.1",
        user = USER,
        password = PASSWORD,
        database = "my_app_db"
    )
    print(mydb)
    mycursor = mydb.cursor()
    values = (name,hp,rpm,amp,section,updates,id)
    query = "update  motor_list set motor_name=%s,hp=%s,rpm=%s,amp=%s,updates=%s,section=%s where motor_id=%s"

    mycursor.execute(query,values)
    mydb.commit()
    mydb.close()
    motoridInsertEntry.delete(0,END)
    motornameInsertEntry.delete(0,END)


#Design Portion:
root = ctk.CTk()
root.title("My App")
root.geometry("800x800")
rootFrame = ctk.CTkFrame(root)
rootFrame.pack(expand="Yes")

#Data Frame Section:
firstFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
firstFrame.grid(row=0,column=0,padx=10,pady=10)

operatorDataFrame = ctk.CTkFrame(firstFrame,width=200,height=200)
operatorDataFrame.grid(row=0,column=0,padx=10,pady=10)

motoridDataLabel = ctk.CTkLabel(operatorDataFrame,text="MOTOR ID:",font=FONT)
motoridDataLabel.grid(row=0,column=0)
motoridDataEntry = ctk.CTkEntry(operatorDataFrame,width=200,placeholder_text="000",font=FONT)
motoridDataEntry.grid(row=0,column=1)
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

motorInsertFrame = ctk.CTkFrame(secondFrame,width=200,height=200)
motorInsertFrame.grid(row=0,column=0,padx=10,pady=20)
motoridInsertLabel = ctk.CTkLabel(motorInsertFrame,text="MOTOR ID: ",font=FONT)
motoridInsertLabel.grid(row=0,column=0)
motoridInsertEntry = ctk.CTkEntry(motorInsertFrame,width=200,placeholder_text="000",font=FONT)
motoridInsertEntry.grid(row=0,column=1)
motornameInsertLabel = ctk.CTkLabel(motorInsertFrame,text="MOTOR NAME: ",font=FONT)
motornameInsertLabel.grid(row=1,column=0)
motornameInsertEntry = ctk.CTkEntry(motorInsertFrame,width=200,placeholder_text="Motor Name",font=FONT)
motornameInsertEntry.grid(row=1,column=1)
hpInsertLabel = ctk.CTkLabel(motorInsertFrame,text="HP: ",font=FONT)
hpInsertLabel.grid(row=2,column=0)
hpInsertDateEntry = ctk.CTkEntry(motorInsertFrame,width=200,placeholder_text="Horse Power",font=FONT)
hpInsertDateEntry.grid(row=2,column=1)
rpmInsertLabel = ctk.CTkLabel(motorInsertFrame,text="RPM: ",font=FONT)
rpmInsertLabel.grid(row=3,column=0)
rpmInsertDateEntry = ctk.CTkEntry(motorInsertFrame,width=200,placeholder_text="Rotation Per Minute",font=FONT)
rpmInsertDateEntry.grid(row=3,column=1)
ampInsertLabel = ctk.CTkLabel(motorInsertFrame,text="A: ",font=FONT)
ampInsertLabel.grid(row=4,column=0)
ampInsertDateEntry = ctk.CTkEntry(motorInsertFrame,width=200,placeholder_text="Ampere",font=FONT)
ampInsertDateEntry.grid(row=4,column=1)
updateInsertLabel = ctk.CTkLabel(motorInsertFrame,text="Last Update: ",font=FONT)
updateInsertLabel.grid(row=5,column=0)
updateInsertDateEntry = DateEntry(motorInsertFrame,width=20,date_pattern='YYYY-mm-dd', background="darkblue", foreground="white", borderwidth=2)
updateInsertDateEntry.grid(row=5,column=1)

sectionInsertLabel = ctk.CTkLabel(motorInsertFrame,text="SECTION: ",font=FONT)
sectionInsertLabel.grid(row=6,column=0)
sectionInsertOption = ctk.CTkOptionMenu(motorInsertFrame,values=["Hydrated Lime","Power House","Utility","Lime Kiln","Boiler","Crane","Mechanic","Workshop","Store","Pmcc","Feeding"],)
sectionInsertOption.grid(row=6,column=1)
enterInsertButton = ctk.CTkButton(motorInsertFrame,text="Insert",command=insert,width=10)
enterInsertButton.grid(row=7,column=0)
updateInsertButton = ctk.CTkButton(motorInsertFrame,text="Update",command=update,width=10)
updateInsertButton.grid(row=7,column=1)

#Show Frame Section:
thirdFrame = ctk.CTkFrame(rootFrame,width=600,height=600)
thirdFrame.grid(row=0,column=1,padx=10,pady=10)

operatorShowFrame = ctk.CTkFrame(thirdFrame,width=200,height=300)
operatorShowFrame.grid(row=0,column=0,padx=10,pady=10)

idShowLabel = ctk.CTkLabel(operatorShowFrame,text="ID:",font=FONT)
idShowLabel.grid(row=0,column=0)
idShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
idShowEntry.grid(row=0,column=1)
motoridShowLabel = ctk.CTkLabel(operatorShowFrame,text="MOTOR ID:",font=FONT)
motoridShowLabel.grid(row=1,column=0)
motoridShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
motoridShowEntry.grid(row=1,column=1)
motornameShowLabel = ctk.CTkLabel(operatorShowFrame,text="MOTOR NAME:",font=FONT)
motornameShowLabel.grid(row=2,column=0)
motornameShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
motornameShowEntry.grid(row=2,column=1)
hpShowLabel = ctk.CTkLabel(operatorShowFrame,text="HP:",font=FONT)
hpShowLabel.grid(row=3,column=0)
hpShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
hpShowEntry.grid(row=3,column=1)
rpmShowLabel = ctk.CTkLabel(operatorShowFrame,text="RPM:",font=FONT)
rpmShowLabel.grid(row=4,column=0)
rpmShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
rpmShowEntry.grid(row=4,column=1)
ampShowLabel = ctk.CTkLabel(operatorShowFrame,text="AMP:",font=FONT)
ampShowLabel.grid(row=5,column=0)
ampShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
ampShowEntry.grid(row=5,column=1)
updateShowLabel = ctk.CTkLabel(operatorShowFrame,text="LAST UPDATE:",font=FONT)
updateShowLabel.grid(row=6,column=0)
updateShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
updateShowEntry.grid(row=6,column=1)
sectionShowLabel = ctk.CTkLabel(operatorShowFrame,text="SECTION:",font=FONT)
sectionShowLabel.grid(row=7,column=0)
sectionShowEntry = ctk.CTkEntry(operatorShowFrame,width=200,font=FONT)
sectionShowEntry.grid(row=7,column=1)



root.mainloop()
