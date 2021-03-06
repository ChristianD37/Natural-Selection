import pygame, random
from math import sqrt, hypot
vec = pygame.math.Vector2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.enems
        pygame.sprite.Sprite.__init__(self, self.groups)

    def draw(self):
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= -self.rect.w and rel_x <= self.game.DISPLAY_W and rel_y >= -self.rect.h and rel_y <= self.game.DISPLAY_H + self.rect.h:
            self.game.display.blit(self.image, (rel_x, rel_y))


class Snake(pygame.sprite.Sprite):
    def __init__(self, game,x,y):
        self.game = game
        self.groups = self.game.enems
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game.enemyList.addSprite(self)
        self.load_images()
        self.image = self.left_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.velocity = vec(-1,0)
        self.position = vec(x,y)
        self.gravity, self.current_chunk = .5, 0
        self.last_update, self.current_frame = 0, 0
        self.bump = False
        if self.position.x < self.game.map_w * 16:
            self.current_chunk = 0
        else: self.current_chunk = 1


    def draw(self):
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= -self.rect.w and rel_x <= self.game.DISPLAY_W and rel_y >= -self.rect.h and rel_y <= self.game.DISPLAY_H + self.rect.h:
            self.game.display.blit(self.image, (rel_x, rel_y))

    def update(self):
        #print(self.game.SCREEN_WIDTH + self.game.camera.offset.x)
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= -self.game.update_dist and rel_x <= self.game.DISPLAY_W + 144 and rel_y >= -48 and rel_y <= self.game.DISPLAY_H + self.game.update_dist:
            if self.bump:
                self.bump = False
                self.velocity.x *= -1
            self.position.x += self.velocity.x * self.game.dt
            self.rect.x = self.position.x
            self.checkCollisionsx()
            self.rect.x = self.position.x
            # Check y cooardinates
            #self.velocity.y += self.gravity * self.game.dt
            # if self.velocity.y > 7:
            #     self.velocity.y = 7
            # self.rect.y += self.velocity.y * self.game.dt
            #self.checkCollisionsy()
            #self.assign_hitbox()
            self.animate()

    def calc_distance(self, player):
        distance = hypot((self.rect.x-player.rect.x),(self.rect.y - player.rect.y))
        return distance

    def load_images(self):
        self.left_frames = [self.game.enemy_sheet.get_sprite("snake1.png"), self.game.enemy_sheet.get_sprite("snake2.png"),self.game.enemy_sheet.get_sprite("snake3.png"),
                            self.game.enemy_sheet.get_sprite("snake4.png"),self.game.enemy_sheet.get_sprite("snake5.png"),self.game.enemy_sheet.get_sprite("snake6.png"),
                            self.game.enemy_sheet.get_sprite("snake7.png"),self.game.enemy_sheet.get_sprite("snake8.png"),self.game.enemy_sheet.get_sprite("snake9.png"),
                            self.game.enemy_sheet.get_sprite("snake10.png")]
        self.right_frames = []
        for frame in self.left_frames:
            self.right_frames.append(pygame.transform.flip(frame,True,False))

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            if self.velocity.x < 0:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left_frames)
                self.image = self.left_frames[self.current_frame]
            else:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right_frames)
                self.image = self.right_frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self):
        hits = []
        for tile in self.game.chunk[self.current_chunk]:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self):
        hits = []
        for bumper in self.game.bumpers.sprites:
            if self.rect.colliderect(bumper):
                hits.append(bumper)
        for tile in hits:
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.w
                self.bump = True
            if self.velocity.x < 0:
                self.position.x = tile.rect.right
                self.bump = True


    def checkCollisionsy(self):
        collisions = self.collision()
        for tile in collisions:
            if self.velocity.y > 0 and self.rect.bottom < tile.rect.top + tile.rect.h/2: # only snap to the platrorm if above half the platform
                self.rect.bottom = tile.rect.top
            if self.rect.bottomleft < tile.rect.bottomleft and len(collisions) == 1 :
                self.bump = True
            elif self.rect.bottomright > tile.rect.bottomright and len(collisions) == 1:
                self.bump = True

class Hawk(pygame.sprite.Sprite):
    def __init__(self, game,x, y):
        self.game = game
        self.groups = self.game.enems
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game.enemyList.addSprite(self)
        self.load_images()
        self.last_update = 0
        self.current_frame = 0
        self.image = self.left_frames[0]
        self.rect = self.image.get_rect()
        self.startx, self.starty = x,y
        self.rect.x, self.rect.y = x, y
        self.position = vec(x,y)
        self.distance = 1
        self.facing_left = True
        self.speedx,self.speedy = 1.65, 1.65
        #self.hitbox = pygame.Surface(size=(41, 36)).get_rect()

    def update(self):
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= -self.rect.w and rel_x <= self.game.DISPLAY_W  and rel_y >= -self.rect.h \
                and rel_y <= self.game.DISPLAY_H + self.rect.h:
            self.animate()
            self.calc_distance(self.game.player)
            print(self.distance)
            if self.distance < 300 and self.distance_from_start() < 608:
                self.move_towards(self.game.player)
            else:
                self.move_back()
        #self.assign_hitbox()

    def draw(self):
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= -self.rect.w and rel_x <= self.game.DISPLAY_W and rel_y >= -self.rect.h and rel_y <= self.game.DISPLAY_H + self.rect.h:
            self.game.display.blit(self.image, (rel_x, rel_y))

    def load_images(self):
        self.left_frames = [self.game.enemy_sheet.get_sprite("hawk1.png"), self.game.enemy_sheet.get_sprite("hawk2.png"),
                            self.game.enemy_sheet.get_sprite("hawk3.png"), self.game.enemy_sheet.get_sprite("hawk4.png"),
                            self.game.enemy_sheet.get_sprite("hawk5.png")]

        self.right_frames = []
        for frame in self.left_frames:
            self.right_frames.append(pygame.transform.flip(frame, True, False) )

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            if self.facing_left:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.left_frames)
                self.image = self.left_frames[self.current_frame]
            else:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.right_frames)
                self.image = self.right_frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)


    def calc_distance(self, player):
        self.distance = hypot((self.position.x-player.position.x),(self.position.y - player.position.y))
        #self.distance = sqrt(   (self.rect.x-player.rect.x)**2 + (self.rect.y - player.rect.y)**2  )
        if self.distance == 0:
            self.distance =1
    def distance_from_start(self):
        distance = hypot((self.position.x - self.startx), (self.position.y - self.starty))
        if distance == 0:
            distance = 1
        return distance

    def move_towards(self, player):
            # Find the direction of the player
            dx, dy = player.position.x - self.position.x, player.position.y - self.position.y
            # Normalize and get unit vector
            dx, dy  = dx / self.distance, dy / self.distance
            if dx > 0:
                self.facing_left = False
            else:
                self.facing_left = True
            self.position.x += dx * self.speedx * self.game.dt
            self.rect.x = self.position.x
            #self.checkCollisionsx()
            self.position.y += dy * self.speedy * self.game.dt
            if self.position.y > 576 - self.rect.h: #FIXXXXXX!!!!!
                self.position.y = 576 - self.rect.h
            self.rect.y = self.position.y
            #self.checkCollisionsy()

    def move_back(self,):
        # Find the direction of start spot
        dx, dy = self.startx - self.position.x, self.starty - self.position.y
        # Normalize and get unit vector
        dx, dy  = dx / self.distance, dy / self.distance
        if dx > 0:
            self.facing_left = False
        else:
            self.facing_left = True
        self.position.x += dx * self.speedx * self.game.dt
        self.rect.x = self.position.x
        #self.checkCollisionsx()
        self.position.y += dy * self.speedy * self.game.dt
        self.rect.y = self.position.y
        if self.rect.y > 576 - self.rect.h:
            self.rect.y = 576 - self.rect.h
        #self.checkCollisionsy()


    def collision(self):
        hits = []
        for tile in self.game.tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self):
        collisions = self.collision()
        for tile in collisions:
            if not self.facing_left and not tile.passable:
                self.rect.right = tile.rect.left

            if self.facing_left and not tile.passable:
                self.rect.left = tile.rect.right



    def checkCollisionsy(self):
        collisions = self.collision()
        for tile in collisions:
            if  self.rect.bottom < tile.rect.top + tile.rect.h and not tile.passable:  # only snap to the platform if above half the platform
                self.rect.bottom = tile.rect.top



class Gopher(Enemy):
    def __init__(self, game,x,y):
        self.game = game
        self.groups = self.game.enems
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game.enemyList.addSprite(self)
        self.load_images()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.current_frame, self.last_update = 0,0
        self.rock_update, self.drop, self.rock_dropped = 0,0,0
        self.buffer = 2000 + random.randint(0,1000)

    def update(self):
        rel_x, rel_y = self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y
        if rel_x >= -self.rect.w and rel_x <= self.game.DISPLAY_W and rel_y >= -self.rect.h \
        and rel_y <= self.game.DISPLAY_H + self.rect.h:
            self.throw_rock()
            self.animate()

    def animate(self):
        now = pygame.time.get_ticks()
        if self.rock_dropped:
            self.image = self.drop_image
            if now - self.last_update > 500:
                self.rock_dropped = False
            return
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def throw_rock(self):
        now = pygame.time.get_ticks()
        self.drop = False
        if now - self.rock_update > self.buffer:
            self.drop = True
            self.rock_update = now

        if self.drop:
            self.rock_dropped = True
            rock = Gopher_Rock(self.game,self.rect.x,self.rect.y + 20)
            self.game.enemyList.addSprite(rock)

    def load_images(self):
        self.frames = []
        for i in range (1,11):
            self.frames.append(self.game.enemy_sheet.get_sprite('gopher' + str(i) + '.png'))
        self.image = self.frames[0]
        self.drop_image = self.game.enemy_sheet.get_sprite("gopher_throw1.png")

class Gopher_Rock(Enemy):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.enems
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game.enemyList.addSprite(self)
        self.image = self.game.enemy_sheet.get_sprite("gopher_rock.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.position = vec(x,y)
        self.velocity = 3
        self.accumulated = 0

    def update(self):
        self.position.y += self.velocity * self.game.dt
        self.rect.y = self.position.y
        self.accumulated += self.velocity * self.game.dt
        hits = []
        for tile in self.game.tileList.sprites:
            if self.rect.colliderect(tile):
                hits.append(tile)
        if hits:
            self.game.sound_effects['rock_smash'].play()
            self.game.particles.addSprite(Gopher_Rock_Particle(self.game, self.rect.x, hits[0].rect.y, 1))
            self.game.particles.addSprite(Gopher_Rock_Particle(self.game, self.rect.x, hits[0].rect.y, -1))
            self.game.particles.addSprite(Gopher_Rock_Particle(self.game, self.rect.x-5, hits[0].rect.y-5, 1))
            self.game.particles.addSprite(Gopher_Rock_Particle(self.game, self.rect.x-8, hits[0].rect.y-5, -1))
            self.game.enemyList.kill(self)
            self.game.camera.screen_shake = 20

class Gopher_Rock_Particle():
    def __init__(self, game, x, y, direction):
        self.game = game
        self.image = self.game.enemy_sheet.get_sprite("rock_particle.png")
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(direction, -2)
        self.rect.x, self.rect.y = self.position.x, self.position.y
        self.limit = y

    def update(self):
        self.position += self.velocity * self.game.dt
        self.velocity.x += .01 * self.game.dt
        self.velocity.y += .1 * self.game.dt
        self.rect.x, self.rect.y = self.position.x, self.position.y
        if self.rect.y > self.limit:
            self.game.particles.kill(self)

    def draw(self):
        self.update()
        self.game.display.blit(self.image,(self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))

