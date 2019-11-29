from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font

import os, glob, datetime
import re
import subprocess

# Setting variables
c_d = 'Z:\\Clients Files\\*\\'
rep = c_d.rstrip('*\\')
year_now = datetime.datetime.now()

def typing(event):
	# refresh listbox items
	Lb1.delete(0,5)

	# update listbox items from entry value
	textval = Input.get()

	# setting variables
	global dic
	dic = {}
	x = 0
	y = 0
	sub_count = len(glob.glob(c_d))

	# search for a directory from Entry value
	for xy in glob.iglob(c_d):
		lcase = xy.lower()
		if lcase.find(textval.lower()) != -1:
			directory = xy.replace(rep,'> ').replace('\\','')
			dic[directory] = xy
			x = x + 1
			# limiting search results to 5
			if x == 5:
				for keys in dic:
					num = 1
					Lb1.insert(num, keys)
					num = num + 1
				break
		y = y + 1
		# if search results are below 5
		if y == sub_count:
			for keys in dic:
				num = 1
				Lb1.insert(num, keys)
				num = num + 1
	if Lb1.size() == 0:
		Lb1.insert(1,'No results found')

def open_selection(event):
	# setting variables
	key = Lb1.get(ACTIVE)
	cyear = scale.get()
	parent = dic[key]
	parent_subs = parent + '*\\'

	# setting directory
	for folders in glob.iglob(parent_subs):
		if folders.find(str(cyear)) != -1:
			cyear_folder = folders

	# opening the workpaper folder
	try:
		wp_folder = cyear_folder + 'Annual Workpapers\\'
		if var.get() == 0:
			if not os.path.exists(wp_folder):
				subprocess.Popen(r'explorer /open, "' + cyear_folder + '"', shell=True)
				return
			subprocess.Popen(r'explorer /open, "' + wp_folder + '"', shell=True)
		else:
			for i in glob.iglob(wp_folder + '*'):
				if i.endswith('.xlsm'):
					print(i)
					subprocess.Popen(r'explorer /open, "' + i + '"', shell=True)
					return
				elif len(glob.glob(wp_folder + '*.xlsm')) == 0:
					messagebox.showinfo(title='Error', message='No workpapers found.')
					return
			messagebox.showinfo(title='Error',message='No files detected')
	except:
		messagebox.showinfo(title='Error',message='Annual Workpapers folder not found.')

# Setting the main window
root = Tk()
root.title('Clients File Browser')
root.configure(bg='#757474')

# Setting Font
myfont = Font(family='Helvetica', size=16)
tickfont = Font(family='Helvetica', size=13, weight='bold')
sfont = Font(family='Helvetica', size=12, weight='bold')
efont = Font(family='Helvetica', size=11, weight='bold')
ffont = Font(family='Helvetica', size=12, weight='bold')
afont = Font(family='Helvetica', size=6, weight='bold')

#Setting color
fgcolor = '#f2f5fa'
bgcolor = '#505b6b'
lcolor = '#8292a1'
entrycolor =  '#282929'
entrytcolor = '#ebeced'
# Frames
frame = LabelFrame(root, width=40, bg=bgcolor,
                   text='SEARCH', font=ffont, fg=fgcolor)
frame2 = LabelFrame(root, width=55, bg=bgcolor,
                    text='PARAMETERS', font=efont, fg=fgcolor)
frame3 = Frame(root, bg=bgcolor)

# Input boxes
Input = Entry(frame, width=40, font=myfont, fg=entrytcolor, bg=entrycolor\
              , selectbackground='#a3a2a2',relief=FLAT)
Input.bind('<Return>', typing)

#Labels
label = Label(frame3,text='CREATED BY EDWARD JOHN',font=afont,anchor=E,fg=fgcolor,bg=bgcolor)

# Tick Boxes
var = IntVar()
Tick = Checkbutton(frame2, text='OPEN WORKPAPERS', \
                   font=tickfont, variable=var, bg=bgcolor, fg=entrytcolor \
                   , relief=FLAT, selectcolor='#344866')

# Scale
scale = Scale(frame2,orient=HORIZONTAL, from_=2015, \
              to=year_now.year + 1, relief=RIDGE, length=350, bg='#435363', fg=fgcolor,\
			   troughcolor=lcolor, width=20, font=sfont)

# Listboxes
Lb1 = Listbox(frame3,width=40,height=5,font=tickfont,\
	fg='white',selectbackground=bgcolor,relief=FLAT)
Lb1.bind('<Double-Button-1>', open_selection)

# Widgets list
w_color = [Lb1]
w_packtop = [frame,frame2,frame3,Input,Lb1,label]
w_packright = [Tick,scale]

# Looping colors
for i in w_color:
	i.configure(background=lcolor)

# packing widgets
for i in w_packtop:
	i.pack(side=TOP,fill=X)

for i in w_packright:
	i.pack(side=RIGHT,fill=X)

# Opening main window
root.mainloop()
