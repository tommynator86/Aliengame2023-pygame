import pygame
import pygame.locals
import player
import random
import os


class Alien(player.Player):

    def __init__(self, surface, bitmapfile, colrects, startx, starty, playerchar, weapon, direction, energy):
        super(Alien, self).__init__(surface, bitmapfile, colrects, startx, starty, energy)
        self.moverect = pygame.Rect((startx * 32) - 64, (starty * 32) - 64, 160, 160)
        self.attentionrect = pygame.Rect((startx * 32) - 128, (starty * 32) - 128, 288, 288)
        pygame.time.set_timer(pygame.USEREVENT + 1, 5) # Timer move
        pygame.time.set_timer(pygame.USEREVENT + 2, 5) # Timer energy
        self.wpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.soundchannel = pygame.mixer.Channel(1)
        self.aliendeadsound = pygame.mixer.Sound(self.wpath + "deadmagier.ogg")
        self.aliendead = False
        self.playerchar = playerchar
        self.weapon = weapon
        self.blockcortop = 32
        self.blockcorbottom = 32
        self.blockcorleft = 32
        self.blockcorright = 32
        self.top = False
        self.left = False
        self.startx = startx
        self.starty = starty
        self.follow = False
        self.direction = direction
        self.reset()

    def reset(self):
        x = self.rect.left - 64
        y = self.rect.top - 64
        self.moverect = pygame.Rect(x, y, 160, 160)
        self.attentionrect = pygame.Rect(self.rect.left - 128, self.rect.top - 128, 288, 288)
        self.blockcortop = 32
        self.blockcorbottom = 32
        self.blockcorleft = 32
        self.blockcorright = 32
        self.follow = False

    def moveleftright(self):
        if self.left is True:
            move = self.moveleft()
            if not self.moverect.contains(self.rect):
                self.left = False
            else:
                if move is True:
                    self.left = False
        else:
            move = self.moveright()
            if not self.moverect.contains(self.rect):
                self.left = True
            else:
                if move is True:
                    self.left = True

    def movetopdown(self):
        if self.top is True:
            move = self.moveup()
            if not self.moverect.contains(self.rect):
                self.top = False
            else:
                if move is True:
                    self.top = False
        else:
            move = self.movedown()
            if not self.moverect.contains(self.rect):
                self.top = True
            else:
                if move is True:
                    self.top = True

    def process(self, playerchar, weapon, events):
        self.playerchar = playerchar
        self.weapon = weapon

        if self.dead is False:
            framerect = pygame.Rect(self.rect.left - 6, self.rect.top - 43, 52, 8)
            energyrect = pygame.Rect(self.rect.left - 5, self.rect.top - 42, (self.energy / 2), 7)
            pygame.draw.rect(self.surface, (0, 0, 0), framerect)
            pygame.draw.rect(self.surface, (0, 255, 0), energyrect)

            timerenergy = False
            for event in events:
                if event.type == pygame.USEREVENT + 2:
                    timerenergy = True

            if self.weapon.rect.colliderect(self.rect):
                if self.energy > 0:
                    if timerenergy is True:
                        self.energy -= 1

            if self.rect.colliderect(self.playerchar.rect):
                if (self.playerchar.energy > 0) and (timerenergy is True):
                    self.playerchar.energy -= 1

            now = False
            for event in events:
                if event.type == pygame.USEREVENT + 1:
                    now = True

            alienx = self.rect.left
            alieny = self.rect.top

            if (self.follow is True) and (now is True):
                weaponblockx, weaponblocky = weapon.getxy()
                playerblockx, playerblocky = playerchar.getxy()
                alienblockx, alienblocky = self.getxy()

                if (weapon.active is True) and (weapon.fill is False):

                    if weaponblockx > playerblockx:
                        move = self.moveright()
                        if move is True:
                            self.movedown()
                    else:
                        move = self.moveleft()
                        if move is True:
                            self.movedown()

                    if weaponblocky > playerblocky:
                        self.movedown()
                    else:
                        self.moveup()

                else:

                    if playerblockx < alienblockx:
                        move = self.moveleft()
                        if move is True:
                            self.movedown()

                    if playerblockx > alienblockx:
                        move = self.moveright()
                        if move is True:
                            self.movedown()

                    if playerblocky < alienblocky:
                        self.moveup()

                    if playerblocky > alienblocky:
                        self.movedown()

            if self.follow is False:
                if self.direction == 1:
                    self.movetopdown()
                else:
                    self.moveleftright()
            else:
                self.moverect = pygame.Rect(alienx - 64, alieny - 64, 160, 160)
                self.attentionrect = pygame.Rect(alienx - 128, alieny - 128, 288, 288)

            if not self.attentionrect.colliderect(self.playerchar.rect):
                if self.follow is True:
                    self.follow = False
                    dirrandom = random.randint(0, 10)
                    if dirrandom < 5:
                        self.direction = 0
                    else:
                        self.direction  = 1
                    self.reset()
            else:
                self.follow = True

            #pygame.draw.rect(self.surface, (0, 255, 0), self.attentionrect)
            #pygame.draw.rect(self.surface, (255, 0, 0), self.moverect)
            self.drawplayer()

        else:
                if self.aliendead is False:
                    self.aliendead = True
                    self.soundchannel.play(self.aliendeadsound)
