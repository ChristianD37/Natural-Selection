import pygame
from Assets.util.hud import HUD_Item
import random

class Object():
    def __init__(self, game,x,y):
        self.game = game
        self.rect = pygame.Rect(0,0,32,32)
        self.image = pygame.Surface((32,32))
        self.rect.x, self.rect.y = x, y
        self.touched = False
    def animate(self):
        pass
    def draw(self):
        self.animate()
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= -48 and rel_x <= self.game.DISPLAY_W + 48 and rel_y >= -48 and rel_y <= self.game.DISPLAY_H + 48:
            self.game.display.blit(self.image, (rel_x, rel_y))


class Food(pygame.sprite.Sprite):
    def __init__(self, game,x, y, type, HUD = False):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.food = type
        self.image = game.objects_sheet.get_sprite(type + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.HUD = HUD
        self.load_HUD()

    def draw(self):
        self.game.display.blit(self.image, (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))

    def collect(self):
        self.hud_image.image = self.game.objects_sheet.get_sprite(self.food + '.png')
        self.game.player.fruits.append(self.food)
        self.kill()
        self.game.objectList.sprites.remove(self)

    def load_HUD(self):
        if self.HUD:
            self.hud_image = HUD_Item(self.game, self.food + '_gray', self.game.DISPLAY_W - (38 * (len(self.game.hud.sprites) - 1) ), 5)
            self.game.hud.addSprite(self.hud_image)

class Grass(Object):
    def __init__(self, game, x, y):
        Object.__init__(self,game,x,y)
        self.game = game
        self.load_images()
        self.last_update, self.current_frame, self.fps = 0, 0, random.randint(180,240)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.fps:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self):
        self.animate()
        self.game.display.blit(self.image, (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))

    def load_images(self):
        self.image = self.game.objects_sheet.get_sprite('grassblades1.png')
        self.frames = [self.game.objects_sheet.get_sprite('grassblades2.png'),self.game.objects_sheet.get_sprite('grassblades3.png'),
                       self.game.objects_sheet.get_sprite('grassblades4.png'),self.game.objects_sheet.get_sprite('grassblades3.png')]


class Bumper():
    def __init__(self, game, x,y):
        self.game = game
        self.rect = pygame.rect.Rect(x,y,32,32)

class Bubbles():
    def __init__(self, game, x,y):
        self.game = game
        self.frames = []
        for i in range(1,6):
            self.frames.append(self.game.objects_sheet.get_sprite('bubbles' + str(i) + '.png'))
            self.frames[i - 1].set_alpha(70)
        self.rect = self.frames[0].get_rect()
        self.position = pygame.math.Vector2(x,y)
        self.velocity = pygame.math.Vector2(random.choice([-1,1]),-2)
        self.rect.x, self.rect.y = self.position.x, self.position.y
        self.image = self.frames[0]
        self.fps, self.current_frame, self.last_update = random.randint(150,230), 0, 0
        self.limit = y

    def animate(self):
        self.position += self.velocity * self.game.dt
        self.velocity.x += .01 * self.game.dt
        self.velocity.y += .1 * self.game.dt
        self.rect.x, self.rect.y = self.position.x, self.position.y
        if self.rect.y > self.limit:
            self.game.particles.kill(self)

        now = pygame.time.get_ticks()
        if now - self.last_update > self.fps:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame > len(self.frames) - 1: self.current_frame = len(self.frames) - 1
            self.image = self.frames[self.current_frame]

    def draw(self):
        self.animate()
        self.game.display.blit(self.image,(self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))

class WaterSurface(Object):
    def __init__(self, game, x, y):
        Object.__init__(self, game,x,y)
        self.game = game
        self.frames = []
        for i in range(1, 9):
            self.frames.append(self.game.objects_sheet.get_sprite('water_top' + str(i) + '.png'))
            self.frames[i-1].set_alpha(115)
        self.image = self.frames[0]
        self.fps, self.current_frame, self.last_update = 200, 0, 0

    def animate(self):
        if self.touched:
            self.touched = False
            self.game.particles.addSprite(Bubbles(self.game,self.rect.x,self.rect.y))
        now = pygame.time.get_ticks()
        if now - self.last_update > self.fps:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    # def draw(self):
    #     self.animate()
    #     self.game.display.blit(self.image,(self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))

class Mushroom(Object):
    def __init__(self, game ,x ,y):
        Object.__init__(self,game,x,y)
        self.image = game.objects_sheet.get_sprite('mushroom.png')
        self.rect.x, self.rect.y = x, y