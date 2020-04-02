from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import shutil
import sys, os

def buttonDo(*args, **kwargs):
  targetImg = args[0]
  if kwargs['targPlayer'] == "1":
    SkinP1.set(targetImg)
  elif kwargs['targPlayer'] == "2":
    SkinP2.set(targetImg)
  else:
    pass

def updateStream():
  os.remove("Name1.txt")
  name1 = str(Name1.get())
  file1 = open("Name1.txt", "w")
  file1.write(name1)
  file1.close()
  os.remove("Name2.txt")
  name2 = str(Name2.get())
  file2 = open("Name2.txt", "w")
  file2.write(name2)
  file2.close()
  
  shutil.copyfile(SkinP1.get(), "output\\p1Img.png")
  shutil.copyfile(SkinP2.get(), "output\\p2Img.png")
  
  p1s = Score1.get()
  p2s = Score2.get()
  shutil.copyfile("pics\\_ScoreNumbers\\_num_"+str(p1s)+".png", "output\\p1Score.png")
  shutil.copyfile("pics\\_ScoreNumbers\\_num_"+str(p2s)+".png", "output\\p2Score.png")

def getButtons(var1=0, var2=0, var3=0):
  try:
    newleftpanel.destroy()
  except:
    pass
  newleftpanel = ttk.Frame(leftpanel, padding="10 10 10 10")
  newleftpanel.grid(column=1, row=1, sticky=(N, W, E, S))
  char1 = str(Char1.get())
  dir1 = "pics\\"+char1+"\\"
  fail = False
  list1 = []
  i = 1
  while not fail:
    try:
      if i < 10:
        open(dir1+char1+"_0"+str(i)+".png")
        list1.append(dir1+char1+"_0"+str(i)+".png")
      elif i >= 10:
        open(dir1+char1+"_"+str(i)+".png")
        list1.append(dir1+char1+"_"+str(i)+".png")
    except:
      fail=True
    i += 1
  rownum = 1
  colnum = 1
  buttonlist = []
  i = 1
  for img in list1:
    tkimg = PhotoImage(file=img)
    button = ttk.Button(newleftpanel, image=tkimg, text="Skin #"+str(i))
    button['command'] = lambda dir=img, kw="1" : buttonDo(dir, targPlayer=kw)
    button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
    button.image = tkimg
    buttonlist.append(button)
    colnum += 1
    if colnum == 4:
      colnum = 1
      rownum += 1
    i+=1
  
  #RIGHT PANEL
  try:
    newrightpanel.destroy()
  except:
    pass
  newrightpanel = ttk.Frame(rightpanel, padding="10 10 10 10")
  newrightpanel.grid(column=1, row=1, sticky=(N, W, E, S))
  char2 = str(Char2.get())
  dir2 = "pics\\"+char2+"\\"
  fail = False
  list2 = []
  i = 1
  while not fail:
    try:
      if i < 10:
        open(dir2+char2+"_0"+str(i)+".png")
        list2.append(dir2+char2+"_0"+str(i)+".png")
      elif i >= 10:
        open(dir2+char2+"_"+str(i)+".png")
        list2.append(dir2+char2+"_"+str(i)+".png")
    except:
      fail=True
    i += 1
  rownum = 1
  colnum = 1
  buttonlist = []
  i = 1
  for img in list2:
    tkimg = PhotoImage(file=img)
    button = ttk.Button(newrightpanel, image=tkimg, text="Skin #"+str(i))
    button['command'] = lambda dir=img, kw="2" : buttonDo(dir, targPlayer=kw)
    button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
    button.image = tkimg
    buttonlist.append(button)
    colnum += 1
    if colnum == 4:
      colnum = 1
      rownum += 1
    i+=1

#TTK BEGINS
root = Tk()
root.title("Stream Changer")
root.iconbitmap(default="StreamScoreboard.ico")

#System Variables
characterList = ["Bowser",
"Charizard",
"Climbers",
"Dedede",
"Diddy",
"DK",
"Falco",
"Falcon",
"Fox",
"Gameandwatch",
"Ganon",
"Ike",
"Ivysaur",
"Jigglypuff",
"Kirby",
"Knuckles",
"Link",
"Lucario",
"Lucas",
"Luigi",
"Mario",
"Marth",
"Metaknight",
"Mewtwo",
"Ness",
"Olimar",
"Peach",
"Pika",
"Pit",
"ROB",
"Roy",
"Samus",
"Sheik",
"Snake",
"Sonic",
"Squirtle",
"Toonlink",
"Wario",
"Wolf",
"Yoshi",
"Zelda",
"Zerosuit" ]

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

#Defining the Left Panel's Functionality
SkinP1 = StringVar()
SkinP1.set("pics\\Mario\\Mario_01.png")

leftpanel = ttk.Frame(mainframe, padding="10 10 10 10")
leftpanel.grid(column=1, row=1, sticky=(N, W, E, S))


#Defining the Middle Panel's Functionality
midpanel = ttk.Frame(mainframe, padding="10 10 10 10")
midpanel.grid(column=2, row=1, sticky=(N, W, S, E))

#INSIDE THE PANEL
Name1 = StringVar()
Name2 = StringVar()
Char1 = StringVar()
Char1.set("Mario")
Char2 = StringVar()
Char2.set("Mario")

Score1 = IntVar()
Score1.set(0)
Score2 = IntVar()
Score2.set(0)

ttk.Label(midpanel, text="Player 1 Name:").grid(column=1, row=1, sticky=(N, W, S, E))
ttk.Label(midpanel, text="Player 2 Name:").grid(column=3, row=1, sticky=(N, W, S, E))

nameInput1 = ttk.Entry(midpanel, width=20, textvariable=Name1)
nameInput1.grid(column=1, row=2, sticky=(N, W, S, E))

updateButton = ttk.Button(midpanel, text="Update", command=updateStream)
updateButton.grid(column=2, row=2, sticky=(N, W, S, E))

nameInput1 = ttk.Entry(midpanel, width=20, textvariable=Name2)
nameInput1.grid(column=3, row=2, sticky=(N, W, S, E))

charSelect1 = OptionMenu(midpanel, Char1, *characterList)
charSelect1.grid(column=1, row=3, sticky=(N, S, E, W))
charSelect2 = OptionMenu(midpanel, Char2, *characterList)
charSelect2.grid(column=3, row=3, sticky=(N, S, E, W))

ttk.Label(midpanel, textvar=Char1).grid(column=1, row=4, sticky=(N, S, E, W))
ttk.Label(midpanel, textvar=Char2).grid(column=3, row=4, sticky=(N, S, E, W))

ttk.Frame(midpanel, height=200, width=200).grid(column=2, row=5, sticky=(N, S, E, W))

ttk.Label(midpanel, text="P1 Score").grid(column=1, row=6, sticky=(N, S, E, W))
ttk.Label(midpanel, text="P2 Score").grid(column=3, row=6, sticky=(N, S, E, W))

"""   CREATE RADIO BUTTON HERE --------------------------------------------------------   """
ttk.Radiobutton(midpanel, text="0", variable=Score1, value=0).grid(column=1, row=7, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="1", variable=Score1, value=1).grid(column=1, row=8, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="2", variable=Score1, value=2).grid(column=1, row=9, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="3", variable=Score1, value=3).grid(column=1, row=10, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="4", variable=Score1, value=4).grid(column=1, row=11, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="5", variable=Score1, value=5).grid(column=1, row=12, sticky=(N, W, S, E))

ttk.Radiobutton(midpanel, text="0", variable=Score2, value=0).grid(column=3, row=7, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="1", variable=Score2, value=1).grid(column=3, row=8, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="2", variable=Score2, value=2).grid(column=3, row=9, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="3", variable=Score2, value=3).grid(column=3, row=10, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="4", variable=Score2, value=4).grid(column=3, row=11, sticky=(N, W, S, E))
ttk.Radiobutton(midpanel, text="5", variable=Score2, value=5).grid(column=3, row=12, sticky=(N, W, S, E))
#INSIDE THE PANEL

#Defining the Right Panel's Functionality
SkinP2 = StringVar()
SkinP2.set("pics\\Mario\\Mario_01.png")

rightpanel = ttk.Frame(mainframe, padding="10 10 10 10")
rightpanel.grid(column=3, row=1, sticky=(N, W, S, E))

##FUNCTIONALITY
Char1.trace_variable("w",getButtons)
Char2.trace_variable("w",getButtons)

getButtons()

root.mainloop()