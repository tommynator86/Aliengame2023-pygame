import pygame
import pygame.locals


class Player(object):

    def __init__(self, surface, bitmapfile, colrects, startx, starty, energy):
        self.playertiles = self.load_tile_table(bitmapfile, 32, 64)
        self.surface = surface
        self.rect = pygame.Rect(startx * 32, starty * 32, 32, 32)
        self.pos = 2
        self.colrects = colrects
        self.dead = False
        self.energy = energy

    def load_tile_table(self, filename, width, height):
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_y in range(0, int(image_height / height)):
            for tile_x in range(0, int(image_width / width)):
                rect = (tile_x * width, tile_y * height, width, height)
                tile_table.append(image.subsurface(rect))
        return tile_table

    def rectcol(self, newrect):
        col = False
        for rect in self.colrects:
            if rect.colliderect(newrect):
                col = True
        return col

    def drawplayer(self):
        if not self.dead:
            playerimg = self.playertiles[self.pos]
            self.surface.blit(playerimg, (self.rect.left, self.rect.top - 32))
        if self.energy == 0:
            self.dead = True

    def moveup(self):
        col = False
        newrect = pygame.Rect(self.rect.left, self.rect.top - 1, 32, 32)
        if not self.rectcol(newrect):
            self.rect = newrect
        else:
            col = True
        self.pos = 0
        return col

    def movedown(self):
        col = False
        newrect = pygame.Rect(self.rect.left, self.rect.top + 1, 32, 32)
        if not self.rectcol(newrect):
            self.rect = newrect
        else:
            col = True
        self.pos = 2
        return col

    def moveleft(self):
        col = False
        newrect = pygame.Rect(self.rect.left - 1, self.rect.top, 32, 32)
        if not self.rectcol(newrect):
            self.rect = newrect
        else:
            col = True
        self.pos = 3
        return col

    def moveright(self):
        col = False
        newrect = pygame.Rect(self.rect.left + 1, self.rect.top, 32, 32)
        if not self.rectcol(newrect):
            self.rect = newrect
        else:
            col = True
        self.pos = 1
        return col

    def setxy(self, x, y):
        self.rect.x = x * 32
        self.rect.y = y * 32

    def setpos(self, pos):
        self.pos = pos

    def getxy(self):
        x = int(self.rect.left / 32)
        y = int(self.rect.top / 32)
        return x, y
