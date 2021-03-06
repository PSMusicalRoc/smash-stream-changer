from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from SmashScoreboardClass import SmashScoreboard
from PIL import Image, ImageTk
import shutil
import sys, os, json, math, time
import pywinauto as pwa

class DoublesScoreboard(SmashScoreboard):
  def __init__(self, directory, *args, **kwargs):
    SmashScoreboard.__init__(self, directory, *args, **kwargs)
    self.title("Smash Stream Scoreboard - Doubles")
    
    self.nametowidget(".main.midpanel.p1label")['text'] = "Team 1 Name"
    self.nametowidget(".main.midpanel.p2label")['text'] = "Team 2 Name"
    
    self.SkinP3 = StringVar()
    self.SkinP4 = StringVar()
    self.Char3 = StringVar()
    self.Char3.set(self.characterList[0])
    self.Char4 = StringVar()
    self.Char4.set(self.characterList[0])
    self.OldChar3 = None
    self.OldChar4 = None

    #charSelect3 = OptionMenu(self.midpanel, self.Char3, *self.characterList)
    self.charSelect3 = ttk.Treeview(self.midpanel)
    self.charSelect3.grid(column=1, row=98, sticky=(N, S, E, W))
    Label(self.midpanel, text="Doubles Character Selectors").grid(row=98, column=2, sticky=(W, E))
    #charSelect4 = OptionMenu(self.midpanel, self.Char4, *self.characterList)
    self.charSelect4 = ttk.Treeview(self.midpanel)
    self.charSelect4.grid(column=3, row=98, sticky=(N, S, E, W))
    
    self.charSelect1.delete(*self.charSelect1.get_children())
    self.charSelect2.delete(*self.charSelect2.get_children())
    
    for character in self.characterList:
      if self.stockToggle:
        try:
          stockImg = Image.open(self.dir+"_Stocks\\"+character+".png")
          stockImg = stockImg.resize((self.stockWidth, self.stockHeight))
          tkimg = ImageTk.PhotoImage(stockImg)
          self.stockImgDict[character] = tkimg
          self.charSelect1.insert('', 'end', character, text=character, image=self.stockImgDict[character])
          self.charSelect2.insert('', 'end', character, text=character, image=self.stockImgDict[character])
          self.charSelect3.insert('', 'end', character, text=character, image=self.stockImgDict[character])
          self.charSelect4.insert('', 'end', character, text=character, image=self.stockImgDict[character])
        except:
          self.charSelect1.insert('' , 'end', character, text=character)
          self.charSelect2.insert('' , 'end', character, text=character)
          self.charSelect3.insert('' , 'end', character, text=character)
          self.charSelect4.insert('' , 'end', character, text=character)
      else:
        self.charSelect1.insert('' , 'end', character, text=character)
        self.charSelect2.insert('' , 'end', character, text=character)
        self.charSelect3.insert('' , 'end', character, text=character)
        self.charSelect4.insert('' , 'end', character, text=character)
        
    self.charSelect3.bind("<Double-1>", self.getCharNameFromTreeview)
    self.charSelect4.bind("<Double-1>", self.getCharNameFromTreeview)
    
    self.Char3.trace_variable("w",self.getButtonsDoubs)
    self.Char4.trace_variable("w",self.getButtonsDoubs)
    
    self.getButtonsDoubs()

  def getCharNameFromTreeview(self, *args):
    try:
      self.Char1.set(self.charSelect1.selection()[0])
    except:
      pass
    try:
      self.Char2.set(self.charSelect2.selection()[0])
    except:
      pass
    try:
      self.Char3.set(self.charSelect3.selection()[0])
    except:
      pass
    try:
      self.Char4.set(self.charSelect4.selection()[0])
    except:
      pass
    
  def getButtonsDoubs(self, var1=0, var2=0, var3=0):
    if self.OldChar3 != self.Char3.get():
      try:
        self.lowleftpanel.destroy()
      except:
        pass
      self.lowleftpanel = ttk.Frame(self.leftpanel, padding="10 10 10 10", name="lowleftpan")
      self.lowleftpanel.grid(column=1, row=2, sticky=(N, W, E, S))
      char3 = str(self.Char3.get())
      dir1 = self.dir+char3+"\\"
      list1 = self.ButtonInstanceDictionary[char3]
      rownum = 1
      colnum = 1
      i = 1
      for img in list1:
        if i < 10:
          button = Button(self.lowleftpanel, image=img, text="Skin #"+str(i), name="button0"+str(i))
          tbutton = ".main.leftcanv.leftpan.lowleftpan.button0"+str(i)
        elif i >= 10:
          button = Button(self.lowleftpanel, image=img, text="Skin #"+str(i), name="button"+str(i))
          tbutton = ".main.leftcanv.leftpan.lowleftpan.button"+str(i)
        button['command'] = lambda  dir=self.imgDirList[self.ButtonInstanceDictionary[char3+"ID"]][i-1], kw="3", targButton=tbutton: self.buttonDo(dir, targPlayer=kw, buttonID=targButton)
        button.image = img
        button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
        colnum += 1
        if colnum == 4:
          colnum = 1
          rownum += 1
        i+=1
      self.OldChar3 = self.Char3.get()

      
      #RIGHT PANEL
    if self.OldChar4 != self.Char4.get():
      try:
        self.lowrightpanel.destroy()
      except:
        pass
      self.lowrightpanel = ttk.Frame(self.rightpanel, padding="10 10 10 10", name="lowrightpan")
      self.lowrightpanel.grid(column=1, row=2, sticky=(N, W, E, S))
      char4 = str(self.Char4.get())
      dir2 = self.dir+char4+"\\"
      list2 = self.ButtonInstanceDictionary[char4]
      rownum = 1
      colnum = 1
      i = 1
      for img in list2:
        if i < 10:
          button = Button(self.lowrightpanel, image=img, text="Skin #"+str(i), name="button0"+str(i))
          tbutton = ".main.rightcanv.rightpan.lowrightpan.button0"+str(i)
        elif i >= 10:
          button = Button(self.lowrightpanel, image=img, text="Skin #"+str(i), name="button"+str(i))
          tbutton = ".main.rightcanv.rightpan.lowrightpan.button"+str(i)
        button['command'] = lambda dir=self.imgDirList[self.ButtonInstanceDictionary[char4+"ID"]][i-1], kw="4", targButton=tbutton: self.buttonDo(dir, targPlayer=kw, buttonID=targButton)
        button.image = img
        button.grid(column=colnum, row=rownum, sticky=(N, S, E, W))
        colnum += 1
        if colnum == 4:
          colnum = 1
          rownum += 1
        i+=1
      self.OldChar4 = self.Char4.get()

  def buttonDo(self, *args, **kwargs):
    targetImg = args[0]
    targetButton = kwargs['buttonID']
    if kwargs['targPlayer'] == "1":
      self.SkinP1.set(targetImg)
      self.changeButtonColor(targetButton, self.Char1.get())
    elif kwargs['targPlayer'] == "2":
      self.SkinP2.set(targetImg)
      self.changeButtonColor(targetButton, self.Char2.get())
    elif kwargs['targPlayer'] == "3":
      self.SkinP3.set(targetImg)
      self.changeButtonColor(targetButton, self.Char3.get())
    elif kwargs['targPlayer'] == "4":
      self.SkinP4.set(targetImg)
      self.changeButtonColor(targetButton, self.Char4.get())
    else:
      pass
      
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

  def updateStream(self, *args):
    self.statusText['text'] = "Working..."
    self.statusText['fg'] = "black"
    failed = False
    #====================Delete Old Files==============================
    try:
      os.remove(r"" + self.BaseDir + "Output\\Name1.txt")
    except:
      pass
    try:
      os.remove(r"" + self.BaseDir + "Output\\Name2.txt")
    except:
      pass
    try:
      os.remove(r"" + self.BaseDir + "Output\\CommentatorList.txt")
    except:
      pass
    try:
      os.remove(r"" + self.BaseDir + "Output\\BracketPhase.txt")
    except:
      pass
    
    try:
      name1 = str(self.Name1.get())
      file = open(r"" + self.BaseDir + "Output\\Name1.txt", "w")
      file.write(name1)
      file.close()
    except:
      self.statusText['text'] = "Error - Check Team 1 Text - Are there non-ASCII characters there?"
      self.statusText['fg'] = "red"
      failed = True
      
    try:
      name2 = str(self.Name2.get())
      file = open(r"" + self.BaseDir + "Output\\Name2.txt", "w")
      file.write(name2)
      file.close()
    except:
      self.statusText['text'] = "Error - Check Team 2 Text - Are there non-ASCII characters there?"
      self.statusText['fg'] = "red"
      failed = True
      
    try:
      comment = str(self.Commentators.get())
      file = open(r"" + self.BaseDir + "Output\\CommentatorList.txt", "w")
      file.write(comment)
      file.close()
    except:
      self.statusText['text'] = "Error - Check Commentator List - Are there non-ASCII characters there?"
      self.statusText['fg'] = "red"
      failed = True
      
    try:
      phase = str(self.BracketPhase.get())
      file = open(r"" + self.BaseDir + "Output\\BracketPhase.txt", "w")
      file.write(phase)
      file.close()
    except:
      self.statusText['text'] = "Error - Check Bracket Phase - Are there non-ASCII characters there?"
      self.statusText['fg'] = "red"
      failed = True
    
    try:
      self.outputImage(self.SkinP1.get(), self.SkinP3.get(), r"" + self.BaseDir + "Output\\", 1)
      self.outputImage(self.SkinP2.get(), self.SkinP4.get(), r"" + self.BaseDir + "Output\\", 2)
    except:
      self.statusText['text'] = "Error - Check Skin Selector Panels - Did you select a skin for each player?"
      self.statusText['fg'] = "red"
      failed = True
      
    """try:
      self.obsWindow.type_keys("^%s")
    except:
      pass"""
      
    p1s = self.Score1.get()
    p2s = self.Score2.get()
    #shutil.copyfile(self.dir + "_ScoreNumbers\\_num_"+str(p1s)+".png", r"" + self.BaseDir + "Output\\p1Score.png")
    #shutil.copyfile(self.dir + "_ScoreNumbers\\_num_"+str(p2s)+".png", r"" + self.BaseDir + "Output\\p2Score.png")
    
    try:
      self.updateScore()
    except:
      self.statusText['text'] = "Error - Check Score Inputs - Is it above 999 or below 0?"
      self.statusText['fg'] = "red"
      failed = True
    
    if not failed:
      self.statusText['text'] = "Stream Update Completed!"
      self.statusText['fg'] = "green"

  def outputImage(self, skinDir1, skinDir2, outputDir, num):
    if self.outWidth == None or self.outHeight == None:
      messagebox.showerror("Error!", "Make sure that your 'config.json' file has the attributes 'outWidth' and 'outHeight'.")
    else:
      outImg = Image.new("RGBA", (math.ceil(self.outWidth*1.3), math.ceil(self.outHeight*1.3)))
      outSize = self.outWidth, self.outHeight
      charbackImg = Image.open(skinDir2)
      w, h = charbackImg.size
      ratio = self.getRatio(w, h, self.outWidth, self.outHeight)
      charbackImg = charbackImg.resize((math.floor(w*ratio), math.floor(h*ratio)))
      charfrontImg = Image.open(skinDir1)
      w, h = charfrontImg.size
      ratio = self.getRatio(w, h, self.outWidth, self.outHeight)
      charfrontImg = charfrontImg.resize((math.floor(w*ratio), math.floor(h*ratio)))
      w, h = charfrontImg.size
      outw, outh = outImg.size
      newwidth = outw - w
      newheight = outh - h
      outImg.paste(charbackImg, (0, 0))
      outImg.paste(charfrontImg, (newwidth, newheight), charfrontImg)
      outImg.save(outputDir + "tmp" + str(num) + ".png")
      shutil.copyfile(outputDir+"tmp"+str(num)+".png", outputDir+"p"+str(num)+"Img.png")
      os.remove(outputDir+"tmp"+str(num)+".png")
      
  def getRatio(self, width, height, outWidth, outHeight):
    if width >= height:
      ratio = outWidth/width
    elif height > width:
      ratio = outHeight/height
    return ratio