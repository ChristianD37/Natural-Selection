import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.objects_sheet.get_sprite(image)
        self.temp = self.image.get_rect()
        self.rect = self.temp
        self.rect.x, self.rect.y = x, y
        self.position = pygame.math.Vector2(x,y)
        self.velocity = pygame.math.Vector2(0,0)
        self.touched, self.moving = False, False
        self.offset, self.interval = 0, 0
        self.traveled = 0

    def draw(self):
        rel_x, rel_y = self.position.x - self.game.camera.offset.x, self.position.y - self.game.camera.offset.y
        if rel_x >= -self.rect.w and rel_x <= self.game.DISPLAY_W + self.rect.w and rel_y >= -self.rect.h and rel_y <= self.game.DISPLAY_H:
            self.game.display.blit(self.image, (rel_x, rel_y))

    def update(self):
        pass

    def vertical_fall(self, spawn_offset = 0): # Handles platforms that continously fall and respawn
        if self.touched:
            self.game.player.position.y += self.velocity.y * self.game.dt + 1
        if self.position.y > self.game.deathzone:
            self.position.y = spawn_offset
        self.position.y += self.velocity.y * self.game.dt
        self.rect.y = self.position.y

    def back_and_forth(self):
        for bumper in self.game.bumpers.sprites:
            if self.rect.colliderect(bumper):
                self.velocity *= -1
        change = self.velocity.x * self.game.dt
        self.position.x += change
        self.rect.x = self.position.x
        if self.touched:
            self.game.player.position.x += change


class Cloud(Platform):
    def __init__(self, game, x, y):
        Platform.__init__(self, game, x, y, 'cloud.png')
        self.rect = pygame.Rect(x,y + 5,self.temp.w,self.temp.h-5)
        self.offset = 5
        self.touched, self.fading = False, False
        self.last_update, self.current_alpha = 0, 255

    def update(self):
        if self.touched:
            self.fading = True
        if self.fading:
            if self.current_alpha < 80:
                self.kill()
                self.game.platforms.sprites.remove(self)
                return
            now = pygame.time.get_ticks()
            if now - self.last_update > 100:
                self.last_update = now
                if self.current_alpha > 0: self.current_alpha -= 10
                self.image.set_alpha(self.current_alpha)

class Leaf(Platform):
    def __init__(self, game, x, y):
        Platform.__init__(self, game, x, y, 'leaf1.png')
        self.moving = True
        self.rect = pygame.Rect(x, y + 15, self.temp.w, self.temp.h - 15)
        self.offset = 15
        self.velocity.y = 2
        self.last_update, self.current_frame = 0, 0
        self.frames = [self.game.objects_sheet.get_sprite('leaf1.png'), self.game.objects_sheet.get_sprite('leaf2.png'),
                       self.game.objects_sheet.get_sprite('leaf3.png'), self.game.objects_sheet.get_sprite('leaf4.png')]

    def update(self):
        self.animate()
        self.vertical_fall(-100)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 250:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class RedPlatform(Platform):
    def __init__(self, game, x,y, image):
        Platform.__init__(self,game, x, y, image)
        self.moving = True
        self.velocity.x = 1
        self.interval = 2* self.rect.w


    def update(self):
        self.back_and_forth()

    def draw(self):
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        extra = 0
        #if self.touched and self.velocity.x > 0: extra = 1
        #elif self.touched and self.velocity.x <0 : extra = -1
        if rel_x >= -self.rect.w and rel_x <= self.game.DISPLAY_W + self.rect.w and rel_y >= -self.rect.h and rel_y <= self.game.DISPLAY_H:
            self.game.display.blit(self.image, (rel_x, rel_y))

