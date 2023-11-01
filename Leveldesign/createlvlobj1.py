import os
import json
data = []

def addalien(x, y):
    alien = dict()
    alien["pos"] = [x, y]
    data["aliens"].append(alien)

def addexit(x, y, tolvl):
    exit = dict()
    exit["tolvl"] = tolvl
    exit["pos"] = [x, y]
    data["exits"].append(exit)

data = dict()
data["musicfile"] = "lvl1.mp3"
data["playerstartpos"] = [20,11]

data["aliens"] = []
addalien(6, 13)
addalien(13, 3)
#data["aliens"].append(alien)

data["exits"] = []
addexit(4, 17, 2)
#data["exits"].append(exits)

dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
lf = open(dir_path + "level1.lvlobj", 'w')
json.dump(data,  lf)
lf.close()
