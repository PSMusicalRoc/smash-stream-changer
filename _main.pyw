from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from SmashScoreboardClass import SmashScoreboard
import os, sys

def start():
  dir = targetDir.get()
  root.destroy()
  board = SmashScoreboard(dir)
  board.mainloop()

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

ttk.Label(root, text="Choose the icon set to use:").grid(column=1, row=1, sticky=(N, S, E, W))
rownum = 2
for name in folderList:
  ttk.Radiobutton(root, text=name.replace("\\", ""), variable=targetDir, value=name).grid(column=1, row=rownum, sticky=(N, S, E, W))
  rownum+=1
  
targetDir.set(folderList[0])

ttk.Button(root, text="Continue!", command=start).grid(column=1, row=rownum, sticky=(N, E, S, W))

root.mainloop()