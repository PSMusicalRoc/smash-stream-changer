import os, json
import time

dirFile = open("directory.txt", "r")
currDir = dirFile.read()
print(currDir)
jsontext = json.load(open("OBS Template\\OBS_Templates.json", "r"))

workstation = jsontext['sources']

def findFileTag(jsonSource):
  try:
    jsonSource['settings']['file']
    return True
  except:
    return False

for source in workstation:
  if findFileTag(source):
    filename = ""
    stopped = False
    for num in range(len(source['settings']['file'])-1, -1, -1):
      if source['settings']['file'][num] == "/" or source['settings']['file'][num] == "\\" or stopped == True:
        stopped = True
      else:
        filename = source['settings']['file'][num] + filename
        
    source['settings']['file'] = currDir + "Output\\" + filename
    
jsontext['sources'] = workstation

with open("OBS Template\\OBS_Templates.json", "w") as outfile:
  json.dump(jsontext, outfile)
  
print("Changes Complete! You can either close this window, or it will automatically close in 10 seconds.")
time.sleep(10)