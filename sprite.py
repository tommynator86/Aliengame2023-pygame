import pygame
import pygame.locals


class Sprite(object):

    def __init__(self, surface, spritetiles, tilewidth, tileheight, posx, posy):
        self.surface = surface
        self.tiles = self.load_tile_table(spritetiles, tilewidth, tileheight)
        self.posx = posx * 32
        self.posy = posy * 32
        self.frame = 0
        pygame.time.set_timer(pygame.USEREVENT + 3, 100)

    def load_tile_table(self, filename, width, height):
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_y in range(0, int(image_height / height)):
            for tile_x in range(0, int(image_width / width)):
                rect = (tile_x * width, tile_y * height, width, height)
                tile_table.append(image.subsurface(rect))
        return tile_table

    def drawsprite(self, events):
        switch = False
        for event in events:
            if event.type == pygame.USEREVENT + 3:
                switch = True

        blocks = len(self.tiles) - 1
        if self.frame <= blocks:
            spriteimg = self.tiles[self.frame]
            self.surface.blit(spriteimg, (self.posx, self.posy))
        else:
            self.frame = 0

        if switch is True:
            self.frame += 1