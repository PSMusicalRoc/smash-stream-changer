import os
dir = "ImgCache\\_FullArt\\"
folderList = []
for folder in os.walk(dir):
  output = folder[0].replace(dir, "")
  if output != "":
    folderList.append(output + "\n")
  else:
    pass

try:
  os.remove("FolderList.txt")
except:
  pass
file = open("FolderList.txt", "w")
file.writelines(folderList)
file.close()