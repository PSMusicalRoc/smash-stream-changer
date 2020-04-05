from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import shutil
import sys, os, json, math

class SmashScoreboard(Tk):
  def __init__(self, directory, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)
    self.iconbitmap("StreamScoreboard.ico")
    self.title("Smash Stream Scoreboard")
    
    self.dir = "ImgCache\\" + directory
    
#------------CONFIG.JSON LOAD-----------------------------------------
    self.configLoad()
    
    
#------------CONFIG.JSON LOADED---------------------------------------
    
    characterList = open(self.dir+"_CharList.txt").readlines()
    i = 0
    for i in range(len(characterList)):
      characterList[i] = characterList[i].replace("\n", "")
  #-----------------------COPYPASTE OLD CODE--------------------------
    
    mainframe = ttk.Frame(self, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    #Defining the Left Panel's Functionality
    self.SkinP1 = StringVar()
    self.SkinP1.set(self.dir + "Mario\\Mario_01.png")

    self.leftpanel = ttk.Frame(mainframe, padding="10 10 10 10")
    self.leftpanel.grid(column=1, row=1, sticky=(N, W, E, S))


    #Defining the Middle Panel's Functionality
    self.midpanel = ttk.Frame(mainframe, padding="10 10 10 10")
    self.midpanel.grid(column=2, row=1, sticky=(N, W, S, E))

    #INSIDE THE PANEL
    self.Name1 = StringVar()
    self.Name2 = StringVar()
    self.Char1 = StringVar()
    self.Char1.set("Mario")
    self.Char2 = StringVar()
    self.Char2.set("Mario")

    self.Score1 = IntVar()
    self.Score1.set(0)
    self.Score2 = IntVar()
    self.Score2.set(0)

    ttk.Label(self.midpanel, text="Player 1 Name:").grid(column=1, row=1, sticky=(N, W, S, E))
    ttk.Label(self.midpanel, text="Player 2 Name:").grid(column=3, row=1, sticky=(N, W, S, E))

    nameInput1 = ttk.Entry(self.midpanel, width=20, textvariable=self.Name1)
    nameInput1.grid(column=1, row=2, sticky=(N, W, S, E))

    updateButton = ttk.Button(self.midpanel, text="Update", command=self.updateStream)
    updateButton.grid(column=2, row=2, sticky=(N, W, S, E))

    nameInput1 = ttk.Entry(self.midpanel, width=20, textvariable=self.Name2)
    nameInput1.grid(column=3, row=2, sticky=(N, W, S, E))

    charSelect1 = OptionMenu(self.midpanel, self.Char1, *characterList)
    charSelect1.grid(column=1, row=3, sticky=(N, S, E, W))
    charSelect2 = OptionMenu(self.midpanel, self.Char2, *characterList)
    charSelect2.grid(column=3, row=3, sticky=(N, S, E, W))

    ttk.Label(self.midpanel, textvar=self.Char1).grid(column=1, row=4, sticky=(N, S, E, W))
    ttk.Label(self.midpanel, textvar=self.Char2).grid(column=3, row=4, sticky=(N, S, E, W))
    
    self.BracketPhase = StringVar()
    self.BracketPhase.set("Round 1 Pools")
    self.Commentators = StringVar()
    self.Commentators.set("Commentator List")
    self.midframe = ttk.Frame(self.midpanel, padding="10 10 10 10", borderwidth=8, relief="solid")
    self.midframe.grid(column=1, row=5, columnspan=3, sticky=(N, S, E, W))
    ttk.Label(self.midframe, text="Bracket Phase:", anchor="center").grid(row=1, column=1, sticky=(N, S, E, W))
    ttk.Entry(self.midframe, width=40, textvariable=self.BracketPhase).grid(row=2, column=1, sticky=(N, S, E, W))
    ttk.Label(self.midframe, text="Commentators:", anchor="center").grid(row=3, column=1, sticky=(N, S, E, W))
    ttk.Entry(self.midframe, width=60, textvariable=self.Commentators).grid(row=4, column=1, sticky=(N, S, E, W))

    ttk.Label(self.midpanel, text="P1 Score").grid(column=1, row=6, sticky=(N, S, E, W))
    ttk.Label(self.midpanel, text="P2 Score").grid(column=3, row=6, sticky=(N, S, E, W))

    """   CREATE RADIO BUTTON HERE --------------------------------------------------------   """
    ttk.Radiobutton(self.midpanel, text="0", variable=self.Score1, value=0).grid(column=1, row=7, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="1", variable=self.Score1, value=1).grid(column=1, row=8, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="2", variable=self.Score1, value=2).grid(column=1, row=9, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="3", variable=self.Score1, value=3).grid(column=1, row=10, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="4", variable=self.Score1, value=4).grid(column=1, row=11, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="5", variable=self.Score1, value=5).grid(column=1, row=12, sticky=(N, W, S, E))

    ttk.Radiobutton(self.midpanel, text="0", variable=self.Score2, value=0).grid(column=3, row=7, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="1", variable=self.Score2, value=1).grid(column=3, row=8, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="2", variable=self.Score2, value=2).grid(column=3, row=9, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="3", variable=self.Score2, value=3).grid(column=3, row=10, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="4", variable=self.Score2, value=4).grid(column=3, row=11, sticky=(N, W, S, E))
    ttk.Radiobutton(self.midpanel, text="5", variable=self.Score2, value=5).grid(column=3, row=12, sticky=(N, W, S, E))
    #INSIDE THE PANEL

    #Defining the Right Panel's Functionality
    self.SkinP2 = StringVar()
    self.SkinP2.set(self.dir + "Mario\\Mario_01.png")

    self.rightpanel = ttk.Frame(mainframe, padding="10 10 10 10")
    self.rightpanel.grid(column=3, row=1, sticky=(N, W, S, E))
    
    self.Char1.trace_variable("w",self.getButtons)
    self.Char2.trace_variable("w",self.getButtons)
    
    self.getButtons()
  
  def updateStream(self):
    try:
      os.remove("output\\Name1.txt")
    except:
      pass
    name1 = str(self.Name1.get())
    file = open("output\\Name1.txt", "w")
    file.write(name1)
    file.close()
    try:
      os.remove("output\\Name2.txt")
    except:
      pass
    name2 = str(self.Name2.get())
    file = open("output\\Name2.txt", "w")
    file.write(name2)
    file.close()
    try:
      os.remove("output\\CommentatorList.txt")
    except:
      pass
    comment = str(self.Commentators.get())
    file = open("output\\CommentatorList.txt", "w")
    file.write(comment)
    file.close()
    try:
      os.remove("output\\BracketPhase.txt")
    except:
      pass
    phase = str(self.BracketPhase.get())
    file = open("output\\BracketPhase.txt", "w")
    file.write(phase)
    file.close()
    
    shutil.copyfile(self.SkinP1.get(), "output\\p1Img.png")
    shutil.copyfile(self.SkinP2.get(), "output\\p2Img.png")
    
    p1s = self.Score1.get()
    p2s = self.Score2.get()
    shutil.copyfile(self.dir + "_ScoreNumbers\\_num_"+str(p1s)+".png", "output\\p1Score.png")
    shutil.copyfile(self.dir + "_ScoreNumbers\\_num_"+str(p2s)+".png", "output\\p2Score.png")
    
  def buttonDo(self, *args, **kwargs):
    targetImg = args[0]
    if kwargs['targPlayer'] == "1":
      self.SkinP1.set(targetImg)
    elif kwargs['targPlayer'] == "2":
      self.SkinP2.set(targetImg)
    else:
      pass
      
  def getButtons(self, var1=0, var2=0, var3=0):
    try:
      self.newleftpanel.destroy()
    except:
      pass
    self.newleftpanel = ttk.Frame(self.leftpanel, padding="10 10 10 10")
    char1 = str(self.Char1.get())
    dir1 = self.dir+char1+"\\"
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
    i = 1
    for img in list1:
      image = Image.open(img)
      w, h = image.size
      if self.sizeratio == None and self.imgWidth != None and self.imgHeight != None:
        resized = image.resize((self.imgWidth, self.imgHeight))
        tkimg = ImageTk.PhotoImage(resized)
      elif self.sizeratio != None and self.imgWidth == None and self.imgHeight == None:
        resized = image.resize((math.ceil(w*self.sizeratio), math.ceil(h*self.sizeratio)))
        tkimg = ImageTk.PhotoImage(resized)
      else:
        tkimg = ImageTk.PhotoImage(image)
      button = ttk.Button(self.newleftpanel, image=tkimg, text="Skin #"+str(i))
      button['command'] = lambda dir=img, kw="1" : self.buttonDo(dir, targPlayer=kw)
      button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
      button.image = tkimg
      colnum += 1
      if colnum == 4:
        colnum = 1
        rownum += 1
      i+=1
    self.newleftpanel.grid(column=1, row=1, sticky=(N, W, E, S))

    
    #RIGHT PANEL
    try:
      self.newrightpanel.destroy()
    except:
      pass
    self.newrightpanel = ttk.Frame(self.rightpanel, padding="10 10 10 10")
    char2 = str(self.Char2.get())
    dir2 = self.dir+char2+"\\"
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
    i = 1
    for img in list2:
      image = Image.open(img)
      w, h = image.size
      if self.sizeratio == None and self.imgWidth != None and self.imgHeight != None:
        resized = image.resize((self.imgWidth, self.imgHeight))
        tkimg = ImageTk.PhotoImage(resized)
      elif self.sizeratio != None and self.imgWidth == None and self.imgHeight == None:
        resized = image.resize((math.ceil(w*self.sizeratio), math.ceil(h*self.sizeratio)))
        tkimg = ImageTk.PhotoImage(resized)
      else:
        tkimg = ImageTk.PhotoImage(image)
      button = ttk.Button(self.newrightpanel, image=tkimg, text="Skin #"+str(i))
      button['command'] = lambda dir=img, kw="2" : self.buttonDo(dir, targPlayer=kw)
      button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
      button.image = tkimg
      colnum += 1
      if colnum == 4:
        colnum = 1
        rownum += 1
      i+=1
    self.newrightpanel.grid(column=1, row=1, sticky=(N, W, E, S))
    
  def configLoad(self):
    #Load File
    try:
      self.configfile = json.load(open(self.dir+"config.json"))
    except:
      pass
    #Set resize ratio
    try:
      self.sizeratio = int(self.configfile['size'])
      if self.sizeratio >= 1:
        pass
      elif self.sizeratio <= -1:
        self.sizeratio = 1/abs(self.sizeratio)
      else:
        self.sizeratio = 1
    except:
      self.sizeratio = 1
    try:
      self.imgWidth = abs(int(self.configfile['imgWidth']))
      self.imgHeight = abs(int(self.configfile['imgHeight']))
      self.sizeratio = None
    except:
      self.imgHeight = None
      self.imgWidth = None