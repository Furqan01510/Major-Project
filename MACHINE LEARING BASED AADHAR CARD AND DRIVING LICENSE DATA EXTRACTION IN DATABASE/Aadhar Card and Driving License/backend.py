import tkinter as tk 
import pytesseract
import sqlite3
import cv2
import re
import numpy as np

db = sqlite3.connect("userdb")
db.execute('create table if not exists aadhaar(name text primary key not null, address text, dob text, aadhaarnum text)')
db.execute('create table if not exists licence(name text primary key not null, father text, address text, licencenum text)')
# data = db.execute("select * from sqlite_master")
def data_extract(file_name_list,field_text):
    field_text.delete(0,"end")
    for file_name in file_name_list:
        try:
            img = cv2.imread(file_name,0)
            data = pytesseract.image_to_string(img)
            if "aadhaar" in data.lower() or "government" in data.lower():
                data = pytesseract.image_to_string(img)
                # print(data)
                try:
                    # Aadhaar Extraction
                    # -------------------------------------------------------------------------------------------------------
                    # name extraction
                    count = 0
                    for i in data.split("\n\n"):
                        name = 0
                        if "dob" in i.lower() and "dob" not in i.split("\n")[0].lower():
                            name = "".join(i.split("\n")[0])
                            dob_data = i
                            break
                        elif "dob" in i.lower() and "dob" in i.split("\n")[0].lower():
                            # print("---------------------------")
                            dob_data = i
                            break
                        count+=1
                    if name == 0:
                        name = data.split("\n\n")[count-1]


                    #------------------------------------------------------------------------------------------------------
                    # dob extraction
                    dob = re.search("dob: ",dob_data.lower())
                    dob = dob_data[dob.end():dob.end()+10]

                    # -----------------------------------------------------------------------------------------------------
                    # address extraction
                    # print(data)
                    loc_start = re.search(r"[a-zA-Z]/[oO]",data)
                    if loc_start:
                        loc_start = loc_start.start()
                        print("hello")
                        loc_end = re.search(r"\d{6}",data).end()
                        address = data[loc_start:loc_end]
                    else:
                        loc_start = re.search(r"address", data.lower()).end()
                        ad_data = "\n".join(data[loc_start+2:].split("\n")[:3])
                        address = ad_data.strip()
                        # print(ad_data)
                    # --------------------------------------------------------------------------------------------------------
                    # aadhaar number extraction
                    adhar_num = re.search(r"\d{4}\s\d{4}\s\d{4}",data).group()
                    # inserting
                    db.execute('insert into aadhaar(name,address,dob,aadhaarnum) values("{}","{}","{}","{}")'.format(name,address,dob,adhar_num))
                    db.commit()
                    field_text.insert(0,"Aadhaar Upload Successful")
                except Exception as e:
                    print(e)
                    field_text.insert(0,"Aadhaar already exist")






            elif "driving" in data.lower() or "license" in data.lower():
                data = pytesseract.image_to_string(img)
                # driving licence data extraction
                # # --------------------------------------------------------------------------------------
                # # license number
                loc_data = re.search(r"TS\w+\n",data)
                license_number = loc_data.group().strip()

                # # --------------------------------------------------------------------------------------
                # name
                name = []
                for i in data[loc_data.start():].split("\n")[1:]:
                    if len(str(i)) != 0:
                        name.append(i)
                    if len(name) == 2:
                        break
              

                # # --------------------------------------------------------------------------------------
                # address
                if name[0] == name[1]:
                    data_s = data[re.search(name[1],data).end():]
                    # print(data_s)
                else:
                    data_s = data

                add_data = re.search(name[1],data_s)
                add_data = data_s[add_data.end():].split("\n")[:8]
                address = (" ".join(add_data)).strip()
              

                # # ----------------------------------------------------------------------------------------
                # # issued date
                issued_data = ""
                for i in range(1,6):
                    if len(data.split("\n")[-i]) == 0:
                        continue
                    issued_data = data.split("\n")[-i]
                    break
                # issued_date = re.search(r"\d+/\d+/\d+",issued_data).group()
   

                # # # ---------------------------------------------------------------------------------------
                # Rto = issued_data.split(issued_date)[-1].strip()
                # db.execute('create table licence(name text primary key not null, address text, licencenum text, issued_date text, rto text)')
                # inserting
                try:
                    db.execute('insert into licence(name, father, address, licencenum) values("{}","{}","{}","{}")'.format(name[0], name[1], address, license_number))
                    db.commit()
                    field_text.insert(0,"DL Upload Successful")
                except Exception as e:
                    print(e)
                    field_text.insert(0,"DL data already exist")
            

        except Exception as e:
            print(e)
            field_text.delete(0,"end")
            field_text.insert(0,"Unknown File Format")




def data_retrieve(widget):
    text = widget.get() #to get the user query
    relevant_aadhaar_data = []
    relevant_licence_data = []
    aadhaar_data = db.execute("select name,address,dob,aadhaarnum from aadhaar").fetchall()
    licence_data = db.execute("select name, father, address, licencenum from licence").fetchall()

    for i in aadhaar_data:
        if text.lower() in i[0].lower() or text.lower() in i[2].lower():
            relevant_aadhaar_data.append(i)
    for i in licence_data:
        if text.lower() in i[0].lower():
            relevant_licence_data.append(i)


    print_adhaar_data = '''-----------------------Aadhaar Data------------------------
name: {}
address: {}
dob: {}
aadhaar number: {}
-----------------------------------------------------------
    '''
    print_licence_data = '''----------------------Licence Data----------------------
name: {}
father name: {}
address: {}
licence number: {}
    '''


    if len(relevant_aadhaar_data) == 0:
        print_adhaar_data = "No Aaddhaar data Found\n------------------------------------------------------------------\n"
    else:
        print(relevant_aadhaar_data)
        print_adhaar_data = print_adhaar_data.format(relevant_aadhaar_data[0][0], relevant_aadhaar_data[0][1], relevant_aadhaar_data[0][2], relevant_aadhaar_data[0][3])

    if len(relevant_licence_data) == 0:
        print_licence_data = "No licence data Found\n------------------------------------------------------------------\n"
    else:
        print(relevant_licence_data)
        print_licence_data = print_licence_data.format(relevant_licence_data[0][0], relevant_licence_data[0][1], relevant_licence_data[0][2], relevant_licence_data[0][3])


    widget.delete(0,"end")
    main_frame = tk.Tk()
    main_frame.title("Template Recognition")
    main_frame.geometry("550x220+30+30")
    # main_frame.iconbitmap(default='icon.ico')
    root = tk.Frame(main_frame,bg = "cyan")
    root.place(x=0,y=0,width = 550, height = 220)
    text_field = tk.Text(root)
    text_field.place(x = 10, y = 10, width = 530, height = 200)
    text_field.insert(0.0,print_adhaar_data+print_licence_data)
