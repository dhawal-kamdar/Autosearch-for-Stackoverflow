from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
from subprocess import Popen, PIPE
import requests
import webbrowser

def openFile():
	global filePath
	file = askopenfile(mode='r')
	filePath = file.name
	l2.configure(text=filePath,bg="#b7e9f7")
	
def getData(cmd):
	cmd_list = cmd.split(" ", 1)
	process = Popen(cmd_list, stdout = PIPE, stderr = PIPE)
	output, error = process.communicate()
	return output, error

def make_request(error):
	print("Searching for " + error)
	response = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
	return response.json()

def get_urls(json_dict):
	url_list = []
	count = 0
	for i in json_dict["items"]:
		if i["is_answered"]:
			url_list.append(i["link"])
		count += 1
		if count == 3:
			break
	for i in url_list:
		webbrowser.open(i)

def autoSearch():
	output, error = getData("python {}".format(filePath))
	error = error.decode("utf-8").strip().split("\r\n")[-1]
	print("Error => ",error)
	if(error):
		error_list = error.split(":",1)
		json1 = make_request(error_list[0])
		json2 = make_request(error_list[1])
		json3 = make_request(error)
		get_urls(json1)
		get_urls(json2)
		get_urls(json3)
	else:
		print("No Error")

def keyShort(event):
	autoSearch()
	
root = Tk()

# root.iconphoto(False, PhotoImage(file= 'images/logo.png'))
root.title('Autosearch for StackOverflow')
root.geometry('280x370')

path = "images/banner.png"
a = Image.open(path)
a = a.resize((280,110),Image.ANTIALIAS)
img = ImageTk.PhotoImage(a)
panel = Label(root,image = img)
panel.pack(side=TOP)

l1 = Label(root,text="*Only Supported for Python*",font=('bold',12))
l2 = Label(root,text="Select a File")
btn1 = Button(root, text="Choose File", command= lambda:openFile())
btn2 = Button(root,text="Search(Ctrl+Q)",command = autoSearch)
l3 = Label(root,text="Instructions : ")
l4 = Label(root,text="1. Select a Code File")
l5 = Label(root,text="2. Click the Search Button(Ctrl+Q)")
l6 = Label(root,text="3. You will get all the error solutions")
l7 = Label(root,text="for the selected code file.")


l1.pack(pady=5)
l2.pack(fill=BOTH)
btn1.pack()
btn2.pack(pady=20)
l3.pack()
l4.pack()
l5.pack()
l6.pack()
l7.pack()

root.bind("<Control_L><q>",keyShort)
root.bind("<Control_L><Q>",keyShort)

root.mainloop()