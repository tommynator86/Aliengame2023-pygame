import os
import json
data = []

def addalien(x, y):
    alien = dict()
    alien["pos"] = [x, y]
    data["aliens"].append(alien)

# Fireball (new!!!, optional)
# Direction:
# 0 = move right
# 1 = move left
# 2 = move down
# 3 = move up
# Automove: True or False: Random direction change instead of reset to startposition
def addfireball(x, y, direction, automove):
    fb = dict()
    fb["pos"] = [x, y]
    fb["dir"] = direction
    fb["auto"] = automove
    data["fireballs"].append(fb)

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

data["fireballs"] = []
addfireball(1,11,0,True)

data["exits"] = []
addexit(4, 17, 2, 3, 5)

#createlvlobj(data, 1)

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

#createlvlobj(data, 2)

# Level 3
data = dict()
data["musicfile"] = "lvl1.mp3"
data["playerstartpos"] = [3,5]

data["aliens"] = []
#addalien(7, 9)
#addalien(20, 9)

data["fireballs"] = []
addfireball(24,9,1,False)

data["exits"] = []
addexit(3, 0, 2, 20 ,16)
addexit(24, 10, 4, 1 ,8)
#addexit(20, 17, 1, 0 , 0)

#createlvlobj(data, 3)


# Level 4
data = dict()
data["musicfile"] = "lvl1.mp3"
data["playerstartpos"] = [3,5]

data["aliens"] = []
addalien(9, 8)
#addalien(20, 9)

#data["fireballs"] = []
#addfireball(24,9,1,False)

data["exits"] = []
# Gullideckel 4ever
addexit(4, 4, 3, 4 ,9)
addexit(9, 4, 3, 4 ,9)
addexit(14, 4, 3, 4 ,9)
addexit(4, 13, 3, 4 ,9)
addexit(9, 13, 5, 7 ,9)
addexit(14, 13, 3, 4 ,9)

addexit(0, 9, 3, 23 ,11)

createlvlobj(data, 4)

# Level 5
data = dict()
data["musicfile"] = "lvl1.mp3"
data["playerstartpos"] = [3,5]

data["aliens"] = []
addalien(3, 12)
addalien(14, 12)

data["fireballs"] = []
addfireball(23,16,3,False)

data["exits"] = []
addexit(24, 9, 3, 4 ,9)

createlvlobj(data, 5)