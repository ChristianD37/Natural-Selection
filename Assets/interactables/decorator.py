import pygame
import random, os
from player import Player
# Create base decorator class
class Decorator(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.dir = os.path.join(os.path.dirname(os.path.abspath("game.py")), "Assets", "images", "decorator_images")
        self.game = game
        self.y = 0
        self.x = 0


    def draw(self):
        pass

class OrangeBackground(Decorator):
    def __init__(self, game):
        Decorator.__init__(self, game)
        self.frames = []
        #dir = os.path.join(os.path.dirname(os.path.abspath("game.py")), "Assets","images","decorator_images", "Sunset_background")
        for frame in range(1,9):
            self.frames.append(pygame.transform.scale(
            pygame.image.load(os.path.join(self.dir,"Sunset_background","sunset_background" + str(frame) + ".png")
                              ).convert_alpha(), (960, 540)) )
        self.image = self.frames[0]
        self.last_update, self.current_frame = 0, 0

    def draw(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        self.game.display.blit(self.image, (0, 0))

class BlueBackground(Decorator):
    def __init__(self,game):
        Decorator.__init__(self,game)
        self.image = pygame.transform.scale(pygame.image.load( os.path.join(self.dir,"blue_sky.png")).convert_alpha(), (960, 540))
    def draw(self):
        self.game.display.blit(self.image, (0,0))


class Hills(Decorator):
    def __init__(self, game,type):
        Decorator.__init__(self, game)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.dir,"hills2.png")).convert_alpha(), (1920, 540))
        self.width = self.image.get_rect().w
        self.x2 = self.width
        self.auto = type

    def draw(self):
        if self.auto:
            self.auto_scroll()
        else:
            self.scroll()
        self.game.display.blit(self.image, (self.x, 0))
        self.game.display.blit(self.image, (self.x2, 0))

    def scroll(self):
        # Stops background from scrolling if the player is colliding into a wall.
        if self.game.player.bump or self.game.player.hurt or self.game.camera.method.scroll_lock():
            return
        self.x -= self.game.player.velocity.x * self.game.dt * .06
        self.x2 -= self.game.player.velocity.x * self.game.dt * .06
        # Handle Right Scroll
        if self.game.player.velocity.x > 0:
            if self.x <= -self.width:
                self.x = self.width
            if self.x2 <= -self.width:
                self.x2 = self.width
        # Handle left scroll
        if self.game.player.velocity.x < 0:
            if self.x >= self.width:
                self.x = -self.width
            if self.x2 >= self.width:
                self.x2 = -self.width

    def auto_scroll(self):
        if self.game.player.bump or self.game.player.hurt or self.game.camera.method.scroll_lock():
            return
        if self.game.camera.scrollval.x > 0:
            self.x -= 1 * self.game.dt * .05
            self.x2 -= 1 * self.game.dt * .05
        # Handle Right Scroll
        if self.x <= -self.width:
            self.x = self.width
        if self.x2 <= -self.width:
            self.x2 = self.width

class Sun(Decorator):
    def __init__(self, game):
        Decorator.__init__(self, game)
        self.image = pygame.transform.scale(self.game.background_sheet.get_sprite("sun_day.png"), (200,200))

    def draw(self):
        self.game.display.blit(self.image, (self.game.DISPLAY_W/2 ,10))

class Birds(Decorator):
    def __init__(self, game):
        Decorator.__init__(self,game)
        self.last_update = 0
        self.load_frames()
        self.rect = self.images[0].get_rect()
        self.position_x, self.rect.y = self.game.DISPLAY_W + self.rect.w*3, 50

    def draw(self):
        if self.position_x < 0 - self.rect.w:
            self.position_x = self.game.DISPLAY_W * 2
        self.position_x -= 1 * self.game.dt
        self.rect.x = self.position_x
        if self.rect.x >= -self.rect.w * 2 and self.rect.x <= self.game.DISPLAY_W + self.rect.w:
            self.animate()
            self.game.display.blit(self.images[0], (self.rect.x, self.rect.y))
            self.game.display.blit(self.images[1], (self.rect.x - self.rect.w , self.rect.y + self.rect.h))
            self.game.display.blit(self.images[2], (self.rect.x , self.rect.y + 2* self.rect.h))

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            for index in range(0,3):
                self.current_frame[index] = (self.current_frame[index] + 1) % len(self.frames)
                self.images[index] = self.frames[self.current_frame[index]]

    def load_frames(self):
        frames = [self.game.background_sheet.get_sprite("seagull_silo1.png"),self.game.background_sheet.get_sprite("seagull_silo2.png"),
                       self.game.background_sheet.get_sprite("seagull_silo3.png"),self.game.background_sheet.get_sprite("seagull_silo2.png"),
                       self.game.background_sheet.get_sprite("seagull_silo1.png"),self.game.background_sheet.get_sprite("seagull_silo4.png"),
                       self.game.background_sheet.get_sprite("seagull_silo5.png"), self.game.background_sheet.get_sprite("seagull_silo4.png")]
        self.frames = []
        for frame in frames:
            self.frames.append(pygame.transform.flip(frame,True,False))
        l = len(self.frames)
        self.current_frame = [random.randint(0, l -1 ), random.randint(0, l-1), random.randint(0, l-1)]

        self.images = [self.frames[self.current_frame[0]], self.frames[self.current_frame[1]], self.frames[self.current_frame[2] ] ]

class Large_Tile(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y):
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.game.tiles)
        self.image = self.game.objects_sheet.get_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        # s = pygame.Surface((16,16))
        # self.game.display.blit(s,
        #                        (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= 0 and rel_x <= self.game.DISPLAY_W and rel_y >= 0 and rel_y <= self.game.DISPLAY_H:
            self.game.display.blit(self.image, (rel_x, rel_y))