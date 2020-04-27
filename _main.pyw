from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from SmashScoreboardClass import SmashScoreboard
from DoublesScoreboardClass import DoublesScoreboard
import os, sys, json

def jsonInit():
  jsontext = json.load(open(BaseDir+"Options\\Options.json", "r"))
  if jsontext['doubles'] == 1:
    DoublesCheck.set("Yes")
  elif jsontext['doubles'] == 0:
    DoublesCheck.set("No")
  return jsontext

def start():
  print(options)
  if options['doubles'] == 1:
    startDoubles()
  elif options['doubles'] == 0:
    startSingles()
  else:
    messagebox.showerror("Error", "Oops! Somehow, you aren't doing singles OR doubles! Go to 'Tools -> Options' and click the checkbox at least once!")

def startSingles():
  dir = targetDir.get()
  root.destroy()
  board = SmashScoreboard(dir)
  board.mainloop()
  
def startDoubles():
  dir = targetDir.get()
  root.destroy()
  board = DoublesScoreboard(dir)
  board.mainloop()

class OptionsMenu(Toplevel):
  def __init__(self, *args, **kwargs):
    Toplevel.__init__(self, *args, **kwargs)
    self.options = json.load(open(BaseDir + "Options\\Options.json"))
    
    self.iconbitmap("StreamScoreboard.ico")
    
    self.doubles = IntVar(value=int(self.options['doubles']))
    
    Label(self, text="Options", font=("Calibri", 20, "bold")).grid(column=2, row=1, sticky=(N, S, E, W))
    
    self.doubCheckbox = Checkbutton(self, variable=self.doubles, offvalue=0, onvalue=1)
    self.doubCheckbox['text'] = "Doubles Mode"
    self.doubCheckbox.grid(column=2, row=2, sticky=(N, S))
    
    self.okButton = Button(self, text="OK")
    self.okButton['command'] = self.applyChanges
    self.okButton.grid(column=2, row=99, sticky=(S))
    self.cancelButton = Button(self, text="Cancel")
    self.cancelButton['command'] = self.cancelChanges
    self.cancelButton.grid(column=3, row=99, sticky=(S))
    
  def applyChanges(self):
    self.options['doubles'] = int(self.doubles.get())
    
    with open(BaseDir + "Options\\Options.json", "w") as outfile:
      json.dump(self.options, outfile)
    global options
    options = jsonInit()
    self.destroy()
  
  def cancelChanges(self):
    self.destroy()

def showOptions():
  optionswindow = OptionsMenu()
  optionswindow.mainloop()

folderList = []
BaseDirFile = open("directory.txt", "r")
BaseDir = r"" + BaseDirFile.read()

for folder in os.walk(BaseDir + "ImgCache\\"):
  output = folder[0].replace(BaseDir + "ImgCache\\", "")
  if output != "" and not "\\" in output:
    folderList.append(output+"\\")
  else:
    pass

if folderList == []:
  messagebox.showerror("Error", "The directory 'ImgCache' in 'My Documents' or the folders inside it do not exist.")
  sys.exit()

root = Tk()
root.title("Smash Stream Scoreboard")
root.iconbitmap("StreamScoreboard.ico")
targetDir = StringVar()

DoublesCheck = StringVar()
options = jsonInit()

"""MENUBAR STARTS HERE"""

menubar = Menu(root)
optionsmenu = Menu(menubar, tearoff=0)
optionsmenu.add_command(label="Options", command=showOptions)
menubar.add_cascade(label="Options", menu=optionsmenu)

root.config(menu=menubar)
"""MENUBAR ENDS HERE"""

ttk.Label(root, text="Choose the icon set to use:").grid(column=1, row=1, sticky=(N, S, E, W))
rownum = 2
for name in folderList:
  ttk.Radiobutton(root, text=name.replace("\\", ""), variable=targetDir, value=name).grid(column=1, row=rownum, sticky=(N, S, E, W))
  rownum+=1
  
targetDir.set(folderList[0])

ttk.Button(root, text="Continue!", command=start).grid(column=1, row=rownum, sticky=(N, E, S, W))

ttk.Frame(root, padding="50 50 50 50").grid(row=1, column=2)

Label(root, text="Settings", anchor="center", font=("Calibri", 14, "bold")).grid(row=1, column=3, columnspan=2)
Label(root, text="Doubles Activated? ", anchor="e").grid(row=2, column=3, sticky=E)
Label(root, textvariable=DoublesCheck, font=("Calibri", 12, "bold"), anchor="w").grid(row=2, column=4, sticky=W)

root.mainloop()