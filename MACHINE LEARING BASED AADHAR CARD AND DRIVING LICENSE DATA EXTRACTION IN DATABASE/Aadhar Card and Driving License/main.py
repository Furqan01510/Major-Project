import tkinter as tk
from tkinter.filedialog import askopenfilenames
import re
import backend

main_frame = tk.Tk()
main_frame.title("Template recognition")
main_frame.geometry("550x220+30+30")
class GUI:
	def upload(self, main_frame):
		root = tk.Frame(main_frame,bg = "cyan")
		root.place(x=0,y=0,width = 550, height = 220)
		tk.Label(root,text = "Upload Document To DataBase",fg= "blue",bg = "pink",font=("monaco",22,"bold")).place(x = 25,y = 20)
		tk.Label(root,text = "Select the Document",bg = "cyan",font=("monaco",10,"bold")).place(x = 10,y= 120)
		self._file = tk.Entry(root, font=("monaco",10,"bold"))
		self._file.place(x = 190, y=120,width=150)
		tk.Button(root, text = "select file", bg = "white",fg = "green",font=("monaco",10,"bold"), command = lambda :self.fileSelect(self._file)).place(x = 340,y= 119,width = 110,height=23)
		upload_button = tk.Button(root,text ="Upload",font=("monaco",20,"bold"),bg = "white",fg = "green",command = lambda :backend.data_extract(self.file_address,self._file))
		upload_button.place(x = 390,y = 160, height = 50, width = 120)
		retrieve_button = tk.Button(root,text ="Retrieve",font=("monaco",10,"bold"),bg = "white",fg = "green",command = lambda :self.retrieve(root))
		retrieve_button.place(x = 10,y = 180, height = 30, width = 100)

	def retrieve(self,frame):
		frame.destroy()
		frame = tk.Frame(main_frame,bg = "cyan")
		frame.place(x=0,y=0,width = 550, height = 220)
		tk.Label(frame,text = "Retrieve Information from Database",fg= "blue",bg = "pink",font=("monaco",18,"bold")).place(x = 20,y = 10)
		tk.Label(frame,text = "Enter Your Name",bg = "cyan",font=("monaco",10,"bold")).place(x = 10,y= 80)
		name_entry = tk.Entry(frame,font=("monaco",10,"bold"))
		name_entry.place(x = 160,y=80,width=300)
		retrieve_button = tk.Button(frame,text ="Retrieve",font=("monaco",20,"bold"),bg = "white",fg = "green", command = lambda :backend.data_retrieve(name_entry))#,command = lambda :signup(userid,password,name,frame,main_frame,login_gui))
		retrieve_button.place(x = 390,y = 120, height = 70, width = 150)
		Upload_button = tk.Button(frame,text ="Upload",font=("monaco",10,"bold"),bg = "white",fg = "green",command = lambda :self.upload(main_frame))
		Upload_button.place(x = 10,y = 180, height = 30, width = 100)
	
	def fileSelect(self,field):
		data = askopenfilenames()
		self.file_address = data
		list_of_files = []
		for i in data:
			i = i.split("/")
			list_of_files.append(i[-1])
		data = ",".join(list_of_files) 
		print(data)
		field.delete(0,"end")
		field.insert(0,data)

	

gui = GUI()
gui.upload(main_frame)
main_frame.mainloop()