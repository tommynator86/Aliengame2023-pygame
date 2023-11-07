import pygame
import pygame.locals
import sprite
import random

class Fireball(sprite.Sprite):

    def __init__(self, surface, bmpfile, posx, posy, lvlcol, direction, automove):
        super(Fireball, self).__init__(surface, bmpfile, 32, 32, posx, posy)
        self.empty = False
        self.startx = self.posx
        self.starty = self.posy
        self.rect = pygame.Rect(self.startx, self.starty, 32, 32)
        self.automove = automove
        self.direction = direction
        self.colrects = lvlcol
        pygame.time.set_timer(pygame.USEREVENT + 4, 20) # Timer move

    def rectcol(self, newrect):
        col = False
        for rect in self.colrects:
            if rect.colliderect(newrect):
                col = True
        return col
    
    def move(self):
        col = False
        if self.direction == 0: # Move right
            newrect = pygame.Rect(self.rect.left + 2, self.rect.top, 32, 32)
        if self.direction == 1: # Move left
            newrect = pygame.Rect(self.rect.left - 2, self.rect.top, 32, 32)
        if self.direction == 2: # Move down
            newrect = pygame.Rect(self.rect.left, self.rect.top + 2, 32, 32)
        if self.direction == 3: # Move up
            newrect = pygame.Rect(self.rect.left, self.rect.top - 2, 32, 32)

        if not self.rectcol(newrect):
            self.rect = newrect
            self.posx = self.rect.left
            self.posy = self.rect.top
        else:
            col = True

        if col is True:
            if self.automove is True:
                self.direction = random.randint(0, 3)
            else:
                self.reset()
        
        return col
    
    def reset(self):
        self.rect = pygame.Rect(self.startx, self.starty, 32, 32)
        self.posx = self.startx
        self.posy = self.starty

    def process(self, playerchar, events):
        if not self.empty:
            self.playerchar = playerchar
            now = False
            for event in events:
                if event.type == pygame.USEREVENT + 4:
                    now = True

            if now: self.move()

            if self.rect.colliderect(self.playerchar.rect):
                if (self.playerchar.energy > 0):
                    self.playerchar.energy -= 5

            self.drawsprite(events)