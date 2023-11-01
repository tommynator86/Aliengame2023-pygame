import pygame
import pygame.locals
import json
import os

class Level:

    def __init__(self, surface, levelnum):
        self.levelnum = levelnum
        self.surface = surface
        wpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.lvldata = self.loadlvlfile(wpath + "level" + str(levelnum) + ".tmj")
        self.tiletable = Tileset(wpath +  self.lvldata["tilesets"][0]["image"])
        self.tileset = self.tiletable.tileset
        self.buffersurface = pygame.Surface((800, 576),pygame.SRCALPHA | pygame.DOUBLEBUF)
        self.buffersurface2 = pygame.Surface((800, 576),pygame.SRCALPHA | pygame.DOUBLEBUF)
        self.draw_layer(0, self.buffersurface)
        self.draw_layer(1, self.buffersurface)
        self.draw_layer(2, self.buffersurface)
        self.draw_layer(3, self.buffersurface2)
        self.col = Collision(self.lvldata["layers"][4])
        self.lvlobjects = LVLObjects(wpath + 'level1.lvlobj')
        
    def loadlvlfile(self, levelfile):
        lf = open(levelfile, 'r')
        level = json.load(lf)
        lf.close()
        return level

    def draw_layer(self, number, blitbuffer):
        lnum = number
        bnum = 0
        h = self.lvldata["height"]
        w = self.lvldata["width"]
        for col in range(0,  h):
            for row in range(0,  w):
                tilenr = self.lvldata["layers"][lnum]["data"][bnum] - 1
                if tilenr > 1:
                    tile_image = self.tiletable.tileset[tilenr]
                    blitbuffer.blit(tile_image, (row * 32, col * 32))
                bnum = bnum + 1

    def drawlayers(self):
        self.surface.blit(self.buffersurface, (0, 0))

    def drawupperlayer(self):
        self.surface.blit(self.buffersurface2, (0, 0))

class Tileset:

    def __init__(self, filename):
        self.tileset = self.load_tile_table(filename, 32, 32)

    def load_tile_table(self, filename, width, height):
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_y in range(0, int(image_height / height)):
            for tile_x in range(0, int(image_width / width)):
                rect = (tile_x * width, tile_y * height, width, height)
                tile_table.append(image.subsurface(rect))
        return tile_table
        
class Collision:

    def __init__(self, coldat):
        self.collisions =coldat
        self.rects = []
        self.createrects()
                    
    def createrects(self):
        h = self.collisions["height"]
        w = self.collisions["width"]
        bnum = 0
        for y in range(0, h):
            ypos = y * 32
            for x in range(0, w):
                xpos = x * 32
                blocknr = int(self.collisions["data"][bnum])
                bnum = bnum + 1
                if blocknr == 2:
                    rect = pygame.Rect(xpos, ypos, 32, 32)
                    self.rects.append(rect)
                    
class LVLObjects:

    def __init__(self, olevelfile):
        lvlobjf = open(olevelfile, 'r')
        self.levelobj = json.load(lvlobjf)
        lvlobjf.close()
        
        
