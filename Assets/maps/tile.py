import pygame

# Tile class to build the level
class Tile(pygame.sprite.Sprite):
    def __init__(self,game, image, x, y, passable, fallable,ramp=0):
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.game.tiles)
        self.image = self.game.grass_tiles.get_sprite(image)
        self.rect = pygame.Rect(0,0,32,32)
        self.rect.x = x
        self.rect.y = y
        self.passable = passable
        self.fallable = fallable
        self.ramp = ramp
        self.surface = pygame.Surface((self.rect.w,self.rect.h))

    def draw(self):
        # s = pygame.Surface((16,16))
        # self.game.display.blit(s,
        #                        (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= 0 and rel_x <= self.game.DISPLAY_W and rel_y >= 0 and rel_y <= self.game.DISPLAY_H:
            self.game.display.blit(self.image, (rel_x, rel_y))



# Composite class to store sprite components
class SpriteList():
    def __init__(self, game):
        self.game = game
        #pygame.sprite.Sprite.__init__(self)
        self.sprites = []

    # Adds sprite to list
    def addSprite(self, tile):
        self.sprites.append(tile)

    def draw(self):
        for tile in self.sprites:
            tile.draw()

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def size(self):
       print(len(self.sprites))

    def kill(self, sprite):
        self.sprites.remove(sprite)

class Tilemap():
    def __init__(self, game):
        self.game = game
        self.tile_list = game.tileList.sprites
        self.make_surface()

    def chunk(self):
        l1, l2 = [],[]
        for tile in self.tile_list:
            if tile.rect.x < self.game.chunk_mark:
                l1.append(tile)
            else :
                l2.append(tile)
        self.game.chunk = [l1,l2]


    def make_surface(self):
        self.chunk()
        self.image = pygame.Surface((32 * self.game.map_w, 32 *self.game.map_h))
        self.image.set_colorkey((0,0,0))
        # start = 0
        # background = pygame.image.load("Assets/images/decorator_images/hillside.png").convert_alpha()
        # while start < 32 *self.game.map_w + background.get_rect().w:
        #     self.image.blit(background,(start,250) )
        #     start += background.get_rect().w
        # for item in self.game.background.tiles:
        #     self.image.blit(item.image, (0,0))
        for tile in self.game.background_tiles.sprites:
            self.image.blit(tile.image, tile.rect)
        for tile in self.tile_list:
            self.image.blit(tile.image, tile.rect)
        for slope in self.game.slopeList.sprites:
            self.image.blit(slope.image, slope.rect)
        for tile in self.game.foreground_tiles.sprites:
            self.image.blit(tile.image, tile.rect)

    def draw(self):
        self.game.display.blit(self.image,(0 - self.game.camera.offset.x ,0 - self.game.camera.offset.y ))

