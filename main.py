import pygame
import os
import level
import player
import alien
import threading
import time
import random
import weapon
import fireball

class gameobjs():
    
    def __init__(self,scr): 
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.gamerunning = True
        self.gameevents = []
        self.playerenergy = 200
        self.scr = scr
        self.switchlevel(1, 0, 0)

    def switchlevel(self,lvlnum, playerx, playery):
        self.buildlevel = level.Level(self.scr, lvlnum)
        self.currentlevel = lvlnum
        self.musicfile = self.buildlevel.lvlobjects.levelobj['musicfile']
        if playerx < 1:
                self.playerx = self.buildlevel.lvlobjects.levelobj['playerstartpos'][0]
                self.playery = self.buildlevel.lvlobjects.levelobj['playerstartpos'][1]
        else:
            self.playerx = playerx
            self.playery = playery
        self.aliendict = self.buildlevel.lvlobjects.levelobj['aliens']
        self.exitsdict = self.buildlevel.lvlobjects.levelobj['exits']

        self.player1 = player.Player(screen, self.dir_path + "player2.png", self.buildlevel.col.rects,self.playerx,self.playery, self.playerenergy)
        self.player1.setpos(2)
            
        self.laser = weapon.Weapon(screen, self.player1)

        self.alienarray = []
        for a in self.aliendict:
            x = a['pos'][0]
            y = a['pos'][1]
            self.alienarray.append(alien.Alien(screen, self.dir_path + "magier1.png", self.buildlevel.col.rects, x, y, self.player1, self.laser, 0, 100))
        
        self.exitrects = []
        for e in self.exitsdict:
            x = e['pos'][0]
            y = e['pos'][1]
            self.exitrects.append(pygame.Rect(x * 32, y * 32, 32, 32))

        self.fireballs = []
        try:
            self.fbdict = self.buildlevel.lvlobjects.levelobj['fireballs']
            for f in self.fbdict:
                x = f['pos'][0]
                y = f['pos'][1]
                auto = f['auto']
                direction = f['dir']
                self.fireballs.append(fireball.Fireball(screen, self.dir_path + "fireball.png", x, y, self.buildlevel.col.rects,direction,auto))
        except:
            print("no fireball enemys")


        pygame.mixer.music.load(self.dir_path + self.musicfile)
        pygame.mixer.music.play(loops= - 1)

    def aliendeadenergy(self):
        if self.player1.energy < 150:
            self.player1.energy += random.randint(0, 50)

class gameloop(threading.Thread): 
    
    def __init__(self): 
        threading.Thread.__init__(self)
        self.mleft = False
        self.mright = False
        self.mtop = False
        self.mdown = False
        self.shoot = False
        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count > 0:
            self.joystick = pygame.joystick.Joystick(0)
            print("Joystick found!")
     
    def run(self): 
        while gobj.gamerunning == True:
            try:
                self.handleinput()
                
                if self.shoot == True:
                    gobj.laser.shot(gobj.player1, True)
                else:
                    gobj.laser.shot(gobj.player1, False)
                    
                if self.mtop == True:
                    gobj.player1.moveup()
                if self.mright == True:
                    gobj.player1.moveright()
                if self.mleft == True:
                    gobj.player1.moveleft()
                if self.mdown == True:
                    gobj.player1.movedown() 
  
            except:
                print("mope")
            time.sleep(0.009)

    def handleinput(self):

        for event in gobj.gameevents:
            if event.type == pygame.QUIT:
                gobj.gamerunning = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.mtop = True
                if event.key == pygame.K_RIGHT:
                    self.mright = True
                if event.key == pygame.K_DOWN:
                    self.mdown = True
                if event.key == pygame.K_LEFT:
                    self.mleft = True
                if  event.key == pygame.K_SPACE:
                    self.shoot = True
                if event.key == pygame.K_ESCAPE:
                    gobj.gamerunning = False
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.mtop = False
                if event.key == pygame.K_RIGHT:
                    self.mright = False
                if event.key == pygame.K_DOWN:
                    self.mdown = False
                if event.key == pygame.K_LEFT:
                    self.mleft = False
                if  event.key == pygame.K_SPACE:
                    self.shoot = False

            if self.joystick_count > 0:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0: self.shoot = True
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 0: self.shoot = False

                if event.type == pygame.JOYAXISMOTION:
                    axis0 = self.joystick.get_axis(0)
                    axis1 = self.joystick.get_axis(1)
                    if axis0 < -0.5:
                        self.mleft = True
                    else:
                        self.mleft = False
                    if axis0 > 0.5:
                        self.mright = True
                    else:
                        self.mright = False
                    if axis1 < -0.5:
                        self.mtop = True
                    else:
                        self.mtop = False
                    if axis1 > 0.5:
                        self.mdown = True
                    else:
                        self.mdown = False

                    
    def handleenergy(self):
        framerect = pygame.Rect(32, 544, 202, 10)
        energyrect = pygame.Rect(33, 545, gobj.playerenergy, 8)
        pygame.draw.rect(screen, (0, 0, 0), framerect)
        pygame.draw.rect(screen, (255, 0, 0), energyrect)
        framerect = pygame.Rect(32, 554, 102, 10)
        energyrect = pygame.Rect(33, 555, gobj.laser.energy, 8)
        pygame.draw.rect(screen, (0, 0, 0), framerect)
        pygame.draw.rect(screen, (0, 255, 0), energyrect)
        gobj.playerenergy = gobj.player1.energy


if __name__ == '__main__':

    pygame.init()
    
    pygame.display.set_caption("Aliengame 0.1.23, by Thomasg")

    screen = pygame.display.set_mode((800,576),  pygame.DOUBLEBUF | pygame.SCALED | pygame.FULLSCREEN) #pygame.DOUBLEBUF

    #print("Treiber: " + str(pygame.display.get_driver()))
    #print("Videoinfo: " + str(pygame.display.Info()))
    #print("SDL Version: " + str(pygame.get_sdl_version()))

    pygame.mixer.pre_init(44100, -16, 2, 3072)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(8)
    soundchannel = pygame.mixer.Channel(3)
    
    clock = pygame.time.Clock()
    
    gobj = gameobjs(screen)
    
    tgameloop = gameloop()
    tgameloop.start()

    # debug fireball
    #fb = fireball.Fireball(screen, gobj.dir_path + "fireball.png", 1, 13, gobj.buildlevel.col.rects,0,True)

    while gobj.gamerunning == True:

        gobj.gameevents = []
        for gameevent in pygame.event.get():
            gobj.gameevents.append(gameevent)
        
        pygame.event.pump()    
            
        screen.fill((0,0,0))
        
        gobj.buildlevel.drawlayers()
        gobj.player1.drawplayer()

        #debug fireball
        #fb.process(gobj.player1,gobj.gameevents)   

        for i in range(0,len(gobj.alienarray)):
            gobj.alienarray[i].process(gobj.player1, gobj.laser, gobj.gameevents)
            if gobj.alienarray[i].aliendead == True:
                print("alien down!")
                gobj.alienarray.pop(i)
                gobj.aliendeadenergy()
                break

        for j in range(0,len(gobj.fireballs)):
            gobj.fireballs[j].process(gobj.player1,gobj.gameevents)  

        gobj.buildlevel.drawupperlayer()

        for e in range(0,len(gobj.exitsdict)):
            if gobj.exitrects[e].colliderect(gobj.player1.rect):
                tolvl = gobj.exitsdict[e]['tolvl']
                print("found! To lvl: ", tolvl)
                px = gobj.exitsdict[e]['playerpos'][0]
                py = gobj.exitsdict[e]['playerpos'][1]
                gobj.switchlevel(tolvl,px,py)
                break
        
        tgameloop.handleenergy()
        
        pygame.display.flip()
        clock.tick(60)

        #pygame.display.set_caption("FPS: " + str(clock.get_fps()))
    
    pygame.quit()
