from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import shutil
import sys, os, json, math, time
import pywinauto as pwa

class SmashScoreboard(Tk):
  def __init__(self, directory, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)
    self.iconbitmap("StreamScoreboard.ico")
    self.title("Smash Stream Scoreboard - Singles")
    self.BaseDirFile = open("directory.txt", "r")
    self.BaseDir = self.BaseDirFile.read()
    
    self.dir = r"" + self.BaseDir + "ImgCache\\" + directory
    
    try:
      self.obsInstance = pwa.application.Application(backend="win32").connect(path=r"C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe")
      self.obsWindow = self.obsInstance.top_window()
    except:
      messagebox.showerror("Warning", "WARNING: OBS is not currently active, some image display errors may occur.")
    
#------------CONFIG.JSON LOAD-----------------------------------------
    self.configLoad()
    
    
#------------CONFIG.JSON LOADED---------------------------------------
    
    self.characterList = open(self.dir+"_CharList.txt").readlines()
    i = 0
    for i in range(len(self.characterList)):
      self.characterList[i] = self.characterList[i].replace("\n", "")
      
    self.setupInitButtons()
    
    self.CanvasWidth = self.ButtonInstanceDictionary[self.characterList[0]][0].width() * 3 + 100
    
    self.mainframe = ttk.Frame(self, padding="3 3 12 12", name="main")
    self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    #Defining the Left Panel's Functionality
    self.SkinP1 = StringVar()
    self.SkinP1.set(self.dir + "Mario\\Mario_01.png")
    
    self.leftCanvas = Canvas(self.mainframe, width=self.CanvasWidth, name="leftcanv")
    self.leftCanvas.grid(column=1, row=1, sticky=(N, S, E, W))
    self.leftScroll = ttk.Scrollbar(self.mainframe, orient="vertical", command=self.leftCanvas.yview)
    self.leftScroll.grid(column=2, row=1, rowspan=2)
    self.leftpanel = ttk.Frame(self.leftCanvas, padding="10 10 10 10", name="leftpan")
    self.leftCanvas.configure(yscrollcommand=self.leftScroll.set, scrollregion=self.leftCanvas.bbox("ALL"))
    self.leftpanel.bind("<Configure>", self.onFrameConfigure)
    self.leftScroll = ttk.Scrollbar(self.mainframe, orient="vertical", command=self.leftCanvas.yview)
    self.leftScroll.grid(column=2, row=1, rowspan=2, sticky=(N, S))
    self.leftCanvas.grid(column=1, row=1, sticky=(N, S, E, W))
    self.leftCanvas.create_window((0, 0), window=self.leftpanel, anchor="nw")
    
    #Defining the Middle Panel's Functionality
    self.midpanel = ttk.Frame(self.mainframe, padding="10 10 10 10")
    self.midpanel.grid(column=3, row=1, sticky=(N, W, S, E))

    #INSIDE THE PANEL
    self.Name1 = StringVar()
    self.Name2 = StringVar()
    self.Char1 = StringVar()
    self.Char1.set(self.characterList[0])
    self.Char2 = StringVar()
    self.Char2.set(self.characterList[0])
    self.OldChar1 = None
    self.OldChar2 = None

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

    charSelect1 = OptionMenu(self.midpanel, self.Char1, *self.characterList)
    charSelect1.grid(column=1, row=3, sticky=(N, S, E, W))
    charSelect2 = OptionMenu(self.midpanel, self.Char2, *self.characterList)
    charSelect2.grid(column=3, row=3, sticky=(N, S, E, W))
    
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
    
    self.statusText = Label(self.midpanel, anchor="center", text="Status Text")
    self.statusText.grid(row=99, column=2, sticky=(N, S))
    #INSIDE THE PANEL

    #Defining the Right Panel's Functionality
    self.SkinP2 = StringVar()
    self.SkinP2.set(self.dir + "Mario\\Mario_01.png")
    
    self.rightCanvas = Canvas(self.mainframe, height=1080, width=self.CanvasWidth, name="rightcanv")
    self.rightCanvas.grid(column=4, row=1, sticky=(N, S, E, W))
    self.rightScroll = ttk.Scrollbar(self.mainframe, orient="vertical", command=self.rightCanvas.yview)
    self.rightScroll.grid(column=5, row=1, sticky=(N, S))
    self.rightpanel = ttk.Frame(self.rightCanvas, padding="10 10 10 10", name="rightpan")
    self.rightCanvas.configure(yscrollcommand=self.rightScroll.set, scrollregion=self.rightCanvas.bbox("ALL"))
    self.rightpanel.bind("<Configure>", self.onFrameConfigure)
    self.rightScroll = ttk.Scrollbar(self.mainframe, orient="vertical", command=self.rightCanvas.yview)
    self.rightCanvas.create_window((0, 0), window=self.rightpanel, anchor="nw")
    
    self.Char1.trace_variable("w",self.getButtons)
    self.Char2.trace_variable("w",self.getButtons)
    
    self.getButtons()
  
  def onFrameConfigure(self, event):
    '''Reset the scroll region to encompass the inner frame'''
    self.leftCanvas.configure(scrollregion=self.leftCanvas.bbox("all"))
    self.rightCanvas.configure(scrollregion=self.rightCanvas.bbox("all"))

  def updateStream(self):
    self.statusText['text'] = "Working..."
    failed = False
    try:
      os.remove(r"" + self.BaseDir + "Output\\Name1.txt")
    except:
      pass
    name1 = str(self.Name1.get())
    file = open(r"" + self.BaseDir + "Output\\Name1.txt", "w")
    file.write(name1)
    file.close()
    try:
      os.remove(r"" + self.BaseDir + "Output\\Name2.txt")
    except:
      pass
    name2 = str(self.Name2.get())
    file = open(r"" + self.BaseDir + "Output\\Name2.txt", "w")
    file.write(name2)
    file.close()
    try:
      os.remove(r"" + self.BaseDir + "Output\\CommentatorList.txt")
    except:
      pass
    comment = str(self.Commentators.get())
    file = open(r"" + self.BaseDir + "Output\\CommentatorList.txt", "w")
    file.write(comment)
    file.close()
    try:
      os.remove(r"" + self.BaseDir + "Output\\BracketPhase.txt")
    except:
      pass
    phase = str(self.BracketPhase.get())
    file = open(r"" + self.BaseDir + "Output\\BracketPhase.txt", "w")
    file.write(phase)
    file.close()
    
    try:
      self.obsWindow = self.obsInstance.top_window()
      self.obsWindow.type_keys("^%h")
    except:
      pass
    
    try:
      self.outputImage(self.SkinP1.get(), r"" + self.BaseDir + "Output\\p1Img.png")
      self.outputImage(self.SkinP2.get(), r"" + self.BaseDir + "Output\\p2Img.png")
    except:
      self.statusText['text'] = "Failed - Error!"
      failed = True
      
    try:
      self.obsWindow.type_keys("^%s")
    except:
      pass
      
    p1s = self.Score1.get()
    p2s = self.Score2.get()
    shutil.copyfile(self.dir + "_ScoreNumbers\\_num_"+str(p1s)+".png", r"" + self.BaseDir + "Output\\p1Score.png")
    shutil.copyfile(self.dir + "_ScoreNumbers\\_num_"+str(p2s)+".png", r"" + self.BaseDir + "Output\\p2Score.png")
    
    if not failed:
      self.statusText['text'] = "Job Completed!"
    
  def buttonDo(self, *args, **kwargs):
    targetImg = args[0]
    targetButton = kwargs['buttonID']
    if kwargs['targPlayer'] == "1":
      self.SkinP1.set(targetImg)
      self.changeButtonColor(targetButton, self.Char1.get())
    elif kwargs['targPlayer'] == "2":
      self.SkinP2.set(targetImg)
      self.changeButtonColor(targetButton, self.Char2.get())
    else:
      pass
      
  def getButtons(self, var1=0, var2=0, var3=0):
    if self.OldChar1 != self.Char1.get():
      try:
        self.newleftpanel.destroy()
      except:
        pass
      self.newleftpanel = ttk.Frame(self.leftpanel, padding="10 10 10 10", name="newleftpan")
      self.newleftpanel.grid(column=1, row=1, sticky=(N, W, E, S))
      char1 = str(self.Char1.get())
      dir1 = self.dir+char1+"\\"
      list1 = self.ButtonInstanceDictionary[char1]
      rownum = 1
      colnum = 1
      i = 1
      
      for img in list1:
        if i < 10:
          button = Button(self.newleftpanel, image=img, text="Skin #"+str(i), name="button0"+str(i))
          tbutton = ".main.leftcanv.leftpan.newleftpan.button0"+str(i)
        elif i >= 10:
          button = Button(self.newleftpanel, image=img, text="Skin #"+str(i), name="button"+str(i))
          tbutton = ".main.leftcanv.leftpan.newleftpan.button"+str(i)
        button['command'] = lambda dir=self.imgDirList[self.ButtonInstanceDictionary[char1+"ID"]][i-1], kw="1", targButton=tbutton: self.buttonDo(dir, targPlayer=kw, buttonID=targButton)
        button.image = img
        button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
        colnum += 1
        if colnum == 4:
          colnum = 1
          rownum += 1
        i+=1
      self.OldChar1 = self.Char1.get()

    if self.OldChar2 != self.Char2.get():
      #RIGHT PANEL
      try:
        self.newrightpanel.destroy()
      except:
        pass
      self.newrightpanel = ttk.Frame(self.rightpanel, padding="10 10 10 10", name="newrightpan")
      self.newrightpanel.grid(column=1, row=1, sticky=(N, W, E, S))
      char2 = str(self.Char2.get())
      dir2 = self.dir+char2+"\\"
      list2 = self.ButtonInstanceDictionary[char2]
      rownum = 1
      colnum = 1
      i = 1
      for img in list2:
        if i < 10:
          button = Button(self.newrightpanel, image=img, text="Skin #"+str(i), name="button0"+str(i))
          tbutton = ".main.rightcanv.rightpan.newrightpan.button0"+str(i)
        elif i >= 10:
          button = Button(self.newrightpanel, image=img, text="Skin #"+str(i), name="button"+str(i))
          tbutton = ".main.rightcanv.rightpan.newrightpan.button"+str(i)
        button['command'] = lambda dir=self.imgDirList[self.ButtonInstanceDictionary[char2+"ID"]][i-1], kw="2", targButton=tbutton: self.buttonDo(dir, targPlayer=kw, buttonID=targButton)
        button.image = img
        button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
        colnum += 1
        if colnum == 4:
          colnum = 1
          rownum += 1
        i+=1
      self.OldChar2 = self.Char2.get()
      
  def changeButtonColor(self, targetButton, character):
    for i in range(1, len(self.ButtonInstanceDictionary[character])+1):
      if i < 10:
        if targetButton.endswith("0" + str(i)):
          self.nametowidget(targetButton)['bg'] = "blue"
        else:
          self.nametowidget(targetButton[:-2]+ "0" +str(i))['bg'] = 'white'
      elif i >= 10:
        if targetButton.endswith(str(i)):
          self.nametowidget(targetButton)['bg'] = "blue"
        else:
          self.nametowidget(targetButton[:-2]+str(i))['bg'] = 'white'
    
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
    #SET OUTPUT STANDARD SIZE
    try:
      self.outWidth = abs(int(self.configfile['outWidth']))
      self.outHeight = abs(int(self.configfile['outHeight']))
    except:
      self.outWidth = None
      self.outHeight = None
      
  def outputImage(self, skinDir, outputDir):
    if self.outWidth == None or self.outHeight == None:
      shutil.copyfile(skinDir, outputDir)
    else:
      outImg = Image.new("RGBA", (self.outWidth, self.outHeight))
      charImg = Image.open(skinDir)
      w, h = charImg.size
      ratio = self.getRatio(w, h, self.outWidth, self.outHeight)
      charImg = charImg.resize((math.floor(w*ratio), math.floor(h*ratio)))
      w, h = charImg.size
      newwidth = math.ceil((self.outWidth - w)/2)
      newheight = math.ceil((self.outHeight - h)/2)
      outImg.paste(charImg, (newwidth, newheight))
      outImg.save(outputDir)
      outImg.close()
      
  def setupInitButtons(self):
    #list of the directories where images are
    i = 0
    self.imgDirList = []
    for character in self.characterList:
      self.imgDirList.append(self.getImgList(character, self.dir+character+"\\"))
      i += 1
    self.ButtonInstanceDictionary = {}
    i = 0
    for character in self.characterList:
      self.ButtonInstanceDictionary[character] = []
      for skinRef in self.imgDirList[i]:
        image = Image.open(skinRef)
        w, h = image.size
        if self.sizeratio == None and self.imgWidth != None and self.imgHeight != None:
          resized = image.resize((self.imgWidth, self.imgHeight))
          tkimg = ImageTk.PhotoImage(resized)
        elif self.sizeratio != None and self.imgWidth == None and self.imgHeight == None:
          resized = image.resize((math.ceil(w*self.sizeratio), math.ceil(h*self.sizeratio)))
          tkimg = ImageTk.PhotoImage(resized)
        else:
          tkimg = ImageTk.PhotoImage(image)
        self.ButtonInstanceDictionary[character].append(tkimg)
      self.ButtonInstanceDictionary[character+"ID"] = i
      i += 1
      
  def getImgList(self, char, dir):
    fail = False
    i = 1
    list = []
    while not fail:
      try:
        if i < 10:
          open(dir+char+"_0"+str(i)+".png")
          list.append(dir+char+"_0"+str(i)+".png")
        elif i >= 10:
          open(dir+char+"_"+str(i)+".png")
          list.append(dir+char+"_"+str(i)+".png")
      except:
        fail=True
      i += 1
    return list
    
  def getRatio(self, width, height, outWidth, outHeight):
    if width >= height:
      ratio = outWidth/width
    elif height > width:
      ratio = outHeight/height
    return ratio