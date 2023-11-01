import pygame
import pygame.locals
import os

class Weapon:

    def __init__(self, surface, player):
        self.active = False
        self.surface = surface
        self.player = player
        self.pos = 0
        self.energy = 100
        self.fill = False
        wpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.bitmaphor = pygame.image.load(wpath + "weapon1.png").convert_alpha()
        self.bitmapver = pygame.image.load(wpath + "weapon2.png").convert_alpha()
        self.bitmap = self.bitmaphor
        self.soundchannel = pygame.mixer.Channel(0)
        self.sound1 = pygame.mixer.Sound(wpath + "laser.wav")
        self.sound2 = pygame.mixer.Sound(wpath + "laser2.wav")
        self.rect = pygame.Rect(0, 0, 32, 64)

    def calcrect(self):
        if self.player.pos == 0:
            self.rect.left = self.player.rect.left
            self.rect.top = self.player.rect.top - 96
            self.bitmap = self.bitmaphor
            if not self.soundchannel.get_busy():
                self.soundchannel.play(self.sound1)
                self.soundchannel.set_volume(1.0, 1.0)
        if self.player.pos == 1:
            self.rect.left = self.player.rect.left + 32
            self.rect.top = self.player.rect.top
            self.bitmap = self.bitmapver
            if not self.soundchannel.get_busy():
                self.soundchannel.play(self.sound1)
                self.soundchannel.set_volume(0, 1.0)
        if self.player.pos == 2:
            self.rect.left = self.player.rect.left
            self.rect.top = self.player.rect.top + 32
            self.bitmap = self.bitmaphor
            if not self.soundchannel.get_busy():
                self.soundchannel.play(self.sound1)
                self.soundchannel.set_volume(1.0, 1.0)
        if self.player.pos == 3:
            self.rect.left = self.player.rect.left - 64
            self.rect.top = self.player.rect.top
            self.bitmap = self.bitmapver
            if not self.soundchannel.get_busy():
                self.soundchannel.play(self.sound1)
                self.soundchannel.set_volume(1.0, 0)

    def shot(self, player, shot):
        self.active = shot
        if (shot is True) and (self.energy > 0) and (self.fill is False):
            self.player = player
            self.calcrect()
            self.surface.blit(self.bitmap, (self.rect.left, self.rect.top))
        else:
            self.rect = pygame.Rect(0, 0, 32, 64)

        if shot is True:
            if self.energy > 0:
                self.energy -= 1
            if self.fill is True:
                if not self.soundchannel.get_busy():
                    self.soundchannel.play(self.sound2)
        else:
            if self.energy == 0:
                self.fill = True
            if self.fill is True:
                self.energy += 1
                if self.energy == 100:
                    self.fill = False

    def getxy(self):
        x = int(self.rect.left / 32)
        y = int(self.rect.top / 32)
        return x, y
