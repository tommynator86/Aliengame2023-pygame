import pygame
import os
import level
import player
import alien
import threading
import time
import weapon

class gameobjs():
    
    def __init__(self): 
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.gamerunning = True
        self.gameevents = []
        self.playerenergy = 200

class gameloop(threading.Thread): 
    
    def __init__(self): 
        threading.Thread.__init__(self)
        self.mleft = False
        self.mright = False
        self.mtop = False
        self.mdown = False
        self.shoot = False
     
    def run(self): 
        while gobj.gamerunning == True:
            try:
                self.handleinput()
                
                if self.shoot == True:
                    laser.shot(player1, True)
                else:
                    laser.shot(player1, False)
                    
                if self.mtop == True:
                    player1.moveup()
                if self.mright == True:
                    player1.moveright()
                if self.mleft == True:
                    player1.moveleft()
                if self.mdown == True:
                    player1.movedown() 
  
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
                    
    def handleenergy(self):
        framerect = pygame.Rect(32, 544, 202, 10)
        energyrect = pygame.Rect(33, 545, gobj.playerenergy, 8)
        pygame.draw.rect(screen, (0, 0, 0), framerect)
        pygame.draw.rect(screen, (255, 0, 0), energyrect)
        framerect = pygame.Rect(32, 554, 102, 10)
        energyrect = pygame.Rect(33, 555, laser.energy, 8)
        pygame.draw.rect(screen, (0, 0, 0), framerect)
        pygame.draw.rect(screen, (0, 255, 0), energyrect)
        gobj.playerenergy = player1.energy


if __name__ == '__main__':

    pygame.init()
    
    #pygame.display.set_caption("Raumsonde Gate3k")

    screen = pygame.display.set_mode((800,576),  pygame.DOUBLEBUF | pygame.SCALED) #pygame.DOUBLEBUF

    #print("Treiber: " + str(pygame.display.get_driver()))
    #print("Videoinfo: " + str(pygame.display.Info()))
    #print("SDL Version: " + str(pygame.get_sdl_version()))

    pygame.mixer.pre_init(44100, -16, 2, 3072)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(8)
    soundchannel = pygame.mixer.Channel(3)
    
    clock = pygame.time.Clock()
    
    gobj = gameobjs()

    buildlevel = level.Level(screen, 1)
    musicfile = buildlevel.lvlobjects.levelobj['musicfile']
    playerx = buildlevel.lvlobjects.levelobj['playerstartpos'][0]
    playery = buildlevel.lvlobjects.levelobj['playerstartpos'][1]
    alienjson = buildlevel.lvlobjects.levelobj['aliens']

    playerenergy = 200
    player1 = player.Player(screen, gobj.dir_path + "player2.png", buildlevel.col.rects,20,11, playerenergy)
    player1.setpos(2)
        
    laser = weapon.Weapon(screen, player1)

    alienarray = []
    for a in alienjson:
        x = a['pos'][0]
        y = a['pos'][1]
        alienarray.append(alien.Alien(screen, gobj.dir_path + "magier1.png", buildlevel.col.rects, x, y, player1, laser, 0, 100))


    pygame.mixer.music.load(gobj.dir_path + musicfile)
    pygame.mixer.music.play(loops= - 1)
    
    tgameloop = gameloop()
    tgameloop.start()
    
    print(buildlevel.lvlobjects.levelobj)
    while gobj.gamerunning == True:

        gobj.gameevents = []
        for gameevent in pygame.event.get():
            gobj.gameevents.append(gameevent)
        
        pygame.event.pump()    
            
        screen.fill((0,0,0))
        
        buildlevel.drawlayers()
        player1.drawplayer()
        buildlevel.drawupperlayer()
        
        for a in alienarray:
            a.process(player1, laser, gobj.gameevents)

        #TODO: handle level exits :D
        
        tgameloop.handleenergy()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
