import subprocess
from tkinter import *
from tkinter import font

def open_bulk():
    try:
        for i in msg.get('1.0','end-1c').splitlines():
                if i:
                    subprocess.Popen(r'explorer /open, "' + i + '"', shell=True)
    except:
        messagebox.showinfo(title='Error', message='File not found')


bgcolor = '#282929'
entrycolor = '#505b6b'
bgframes = '#515a5c'


root = Tk()
root.title('Bulk Open File')

lf = LabelFrame(root, width=40, bg=bgframes,text='Enter Directories below',fg='white',font='Helvetica 12 bold')
msg = Text(lf,relief=GROOVE,width=100,bg=bgcolor,fg='white',height=15)
btn = Button(lf, text='Open Files', bg='white', relief=GROOVE,command=open_bulk)
label = Label(lf, text='FOR IOCA',font='Helvetica 6 bold', anchor=E, fg='white', bg=bgcolor)
root.configure(background='#566b70')

lf.pack()
msg.pack()
btn.pack(fill=X)
label.pack(fill=X)
root.mainloop()

