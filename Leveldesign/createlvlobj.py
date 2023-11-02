import os
import json
data = []

def addalien(x, y):
    alien = dict()
    alien["pos"] = [x, y]
    data["aliens"].append(alien)

def addexit(x, y, tolvl, px, py):
    exit = dict()
    exit["tolvl"] = tolvl
    exit["pos"] = [x, y]
    exit["playerpos"] = [px ,py]
    data["exits"].append(exit)

def createlvlobj(dat,number):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
    filename = dir_path + "level" + str(number) + ".lvlobj"
    print(dat)
    #print(filename)  
    lf = open(filename, 'w')
    json.dump(dat,  lf)
    lf.close()

# Level 1
data = dict()
data["musicfile"] = "lvl1.mp3"
data["playerstartpos"] = [20,11]

data["aliens"] = []
addalien(6, 13)
addalien(13, 3)

data["exits"] = []
addexit(4, 17, 2, 3, 5)

createlvlobj(data, 1)

# Level 2
data = dict()
data["musicfile"] = "lvl1.mp3"
data["playerstartpos"] = [3,5]

data["aliens"] = []
addalien(7, 9)
addalien(20, 9)

data["exits"] = []
addexit(3, 4, 1, 4 ,16)
addexit(20, 17, 3, 3 , 1)

createlvlobj(data, 2)

# Level 3
data = dict()
data["musicfile"] = "lvl1.mp3"
data["playerstartpos"] = [3,5]

data["aliens"] = []
#addalien(7, 9)
#addalien(20, 9)

data["exits"] = []
addexit(3, 0, 2, 20 ,16)
#addexit(20, 17, 1, 0 , 0)

createlvlobj(data, 3)


