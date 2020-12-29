import pygame
from os import path
vec = pygame.math.Vector2

# Create the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.all_Sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.load_images()
        self.rect = self.image.get_rect()
        self.position = vec(0,0)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.hitbox = pygame.Rect(0,0,25,48)
        self.rect = self.hitbox
        self.velocity = vec(0, 0)
        self.acc = vec(0, .5)
        self.berry_count = 0
        self.is_jumping, self.on_ground, self.falling, self.is_running, self.landing  = False, False, False, False, False
        self.jump_frames = 0
        self.lastUpdate = 0
        self.currentFrame, self.currentFrame_l = 0, 0
        self.facing_right = True
        self.space_pressed = 0
        self.slope = False
        self.tiled = False
        self.bump = False
        self.friction = -.15 #.15
        self.hurt = False
        self.hurt_jump, self.alive = False, True
        self.temp = self.rect.y
        self.temp_Rect = pygame.Rect(self.rect.x, self.rect.y + 32, 32,self.rect.h)
        self.last_position = vec(0,0)
        self.max_velocity = 4.7
        self.bound_box = pygame.Rect(self.rect.x, self.rect.y, self.rect.w * 3, self.rect.h)
        self.bound_box.center = self.rect.center
        self.reset_timer = 0
        self.in_water = False
        self.fruits = []


    # Updates player coordinates
    def update(self):
        if self.hurt:
            self.fall_off()
        else:
            self.look_around()
            self.calculate_Position()
            self.check_enemy_collision()
            self.check_object_collision()
            self.check_interactive_collision()
        self.animate()


    # Performs character calculations
    def calculate_Position(self):
        # self.velocity.x = 0
        self.acc.x, self.acc.y = 0, .5
        if self.in_water:
            self.acc.y = .2
        self.bump = False
        # Handle the Run State
        if self.game.RUN_KEY:
            if self.on_ground:
                self.is_running = True
        else:
            if self.on_ground:
                self.is_running = False
        # Adjust acceleration based on key presses
        if self.game.LEFT_KEY and self.game.RIGHT_KEY:
            self.acc.x *= .25 #* self.game.dt
        elif self.game.LEFT_KEY:
            self.acc.x = -.8 #* self.game.dt
        elif self.game.RIGHT_KEY:
            self.acc.x = .8 #* self.game.dt
        # Apply friction

        self.acc.x += self.velocity.x * self.friction
        #self.acc.x *= (self.game.dt*self.game.dt)
        self.velocity.x += self.acc.x * self.game.dt
        if self.is_running:
            if self.velocity.x > self.max_velocity:
                self.velocity.x = self.max_velocity
            elif self.velocity.x < -self.max_velocity :
                self.velocity.x = -self.max_velocity
        else:
            if self.velocity.x > 3:
                self.velocity.x = 3
            elif self.velocity.x < -3:
                self.velocity.x = -3
        if abs(self.velocity.x) < .1 * self.game.dt:
            self.velocity.x = 0
        #self.velocity.x *= self.game.dt
        # Calculate the player position
        # Check X coordiantes

        self.position.x += self.velocity.x * self.game.dt - (self.acc.x * .5 ) * (self.game.dt*self.game.dt)
        self.boundary_check()
        self.rect.x = self.position.x
        self.checkCollisionsx()
        #Handle Y coordinate
        self.velocity.y += self.acc.y * self.game.dt
        if self.in_water:
            if self.velocity.y > 4: self.velocity.y = 4
        if self.velocity.y > 15 :
            self.velocity.y = 15
        self.last_position.y = self.position.y
        self.position.y += self.velocity.y * self.game.dt - (self.acc.y * .5 ) * (self.game.dt*self.game.dt)
        self.rect.bottom = self.position.y
        self.slope_collisions()
        self.rect.bottom = self.position.y
        self.checkCollisionsy()
        if self.on_ground:
            self.jump_frames = 0
            self.velocity.y = 0
        else:
            self.landing = True
            self.jump_frames += 1

    def boundary_check(self):
        if self.position.x < 0:
            self.position.x = 0
            self.game.player.bump = True
        elif self.position.x > self.game.map_w * 32 - self.rect.w:
            self.position.x = self.game.map_w * 32 - self.rect.w
            self.game.player.bump = True



    def animate(self):
        now = pygame.time.get_ticks()
        # Handle death animation
        if self.hurt:
            if now - self.lastUpdate > 80:
                if self.facing_right:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.hurt_frames_right)
                    self.image = self.hurt_frames_right[self.currentFrame]
                else:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.hurt_frames_left)
                    self.image = self.hurt_frames_left[self.currentFrame]
            return


        # Handle jump animation
        if  self.is_jumping or self.velocity.y > 1:
            if self.facing_right:
                self.image = self.jump_image[0]
            else:
                self.image = self.jump_image[1]
            return
        # Handle run animation
        if self.velocity.x > .01:
            if self.is_running:
                if now - self.lastUpdate > 100:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.right_frames_run)
                    self.image = self.right_frames_run[self.currentFrame]
                    self.facing_right = True
            else:
                if now - self.lastUpdate > 50:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.right_frames)
                    self.image = self.right_frames[self.currentFrame]
                    self.facing_right = True
        elif self.velocity.x < 0:
            if self.is_running:
                if now - self.lastUpdate > 80:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.left_frames_run)
                    self.image = self.left_frames_run[self.currentFrame]
                    self.facing_right = False
            else:
                if now - self.lastUpdate > 50:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.left_frames)
                    self.image = self.left_frames[self.currentFrame]
                    self.facing_right = False
        # Handle swim animation
        if self.in_water and not self.on_ground:
            # if now - self.lastUpdate > 150:
            if self.facing_right:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.swim_frames_right)
                self.image = self.swim_frames_right[self.currentFrame]
            else:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.swim_frames_left)
                self.image = self.swim_frames_left[self.currentFrame]
            return
        # Handle look/ide animation
        else:
            if self.game.UP_KEY:
                if self.facing_right:
                    self.image = self.look_up[0]
                else:
                    self.image = self.look_up[1]
                return
            elif self.game.DOWN_KEY:
                if self.facing_right:
                    self.image = self.look_down[0]
                else:
                    self.image = self.look_down[1]
                return
            if now - self.lastUpdate > 130:
                if self.facing_right:
                    if self.landing:
                        self.lastUpdate = now
                        self.currentFrame_l = (self.currentFrame_l + 1) % len(self.land_frames_right)
                        if self.currentFrame_l % len(self.land_frames_right) == 0: self.landing = False
                        self.image = self.land_frames_right[self.currentFrame_l]
                    else:
                        if now - self.lastUpdate > 200:
                            self.lastUpdate = now
                            self.currentFrame = (self.currentFrame + 1) % len(self.idle_frames)
                            self.image = self.idle_frames[self.currentFrame]
                else:
                    if self.landing:
                        self.lastUpdate = now
                        self.currentFrame_l = (self.currentFrame_l + 1) % len(self.land_frames_left)
                        if self.currentFrame_l % len(self.land_frames_left) == 0: self.landing = False
                        self.image = self.land_frames_left[self.currentFrame_l]
                    else:
                        if now - self.lastUpdate > 200:
                            self.lastUpdate = now
                            self.currentFrame = (self.currentFrame + 1) % len(self.idle_frames_left)
                            self.image = self.idle_frames_left[self.currentFrame]
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        self.game.display.blit(self.image, (self.rect.x - self.game.camera.offset.x - 12, self.rect.y -self.game.camera.offset.y ))
        # Uncomment to draw hitbox
        #s = pygame.Surface((25,48))
        #self.game.display.blit(s,(self.rect.x - self.game.camera.offset.x , self.rect.y - self.game.camera.offset.y))


    # def assign_hitbox(self):
    #     self.hitbox.bottom = self.rect.bottom
    #     self.hitbox.x = self.rect.x + 12


    # Occurs when the character jumps
    def jump(self):
        if self.in_water:
            self.velocity.y = -3
        elif self.jump_frames < 2:
            #self.position.y -= 1
            self.game.sound_effects['Jump'].play()
            self.velocity.y = -13.7 # -12
            self.is_jumping = True
            self.on_ground = False


    def look_around(self):
        if self.game.UP_KEY and abs(self.velocity.y) < 1:
            if self.game.camera.method.extra_y >= - 120:
                self.game.camera.method.extra_y -= 2 * self.game.dt
        elif self.game.DOWN_KEY and abs(self.velocity.y) < 1:
            if self.game.camera.method.extra_y <=  120:
                self.game.camera.method.extra_y += 2 * self.game.dt
        else:
            if self.game.camera.method.extra_y < 0:
                self.game.camera.method.extra_y += 4
            else:
                self.game.camera.method.extra_y  = 0

    # Checks if the player is still on the level
    def checkDeath(self):
        if self.hurt:
            now = pygame.time.get_ticks()
            if now - self.reset_timer > 2500:
                return True
        else:
            self.reset_timer = pygame.time.get_ticks()


    # Gets player collisions with tiles
    def collision(self, axis):
        hits = []
        if (axis == 'y'):
            self.rect.bottom += 1
            for tile in self.game.tileList.sprites:
                if self.rect.colliderect(tile):
                    hits.append(tile)
            #self.rect.bottom -= 1
        else:
            for tile in self.game.tileList.sprites:
                if self.rect.colliderect(tile):
                    hits.append(tile)
        return hits

    def checkCollisionsx(self):
        self.tiled = False
        collisions = self.collision('x')
        for tile in collisions:
            if self.velocity.x > 0 and not tile.passable:
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
                self.bump, self.tiled = True, True
                self.velocity.x = 0
            elif self.velocity.x < 0 and not tile.passable:
                self.bump = True
                self.velocity.x = 0
                self.position.x = tile.rect.right
                self.rect.x = self.position.x


    def checkCollisionsy(self):
        #self.rect.bottom += 1
        collisions = self.collision('y')
        # print(self.position.y, self.velocity.y)
        self.on_ground = False
        self.platform_collisions()
        if self.slope:
            self.on_ground = True
            self.rect.y -= 1
        for tile in collisions:
            if tile.passable: # One-Way Tiles you can jump through
                if self.velocity.y > 0 and self.position.y > tile.rect.top :
                    if self.last_position.y  < tile.rect.top + tile.rect.h *.125 :
                        self.space_pressed = 0
                        self.on_ground = True
                        self.is_jumping = False
                        self.velocity.y = 0
                        self.position.y = tile.rect.top
                        self.rect.bottom = self.position.y
            elif self.velocity.y > 0 and self.position.y > tile.rect.top : # Hard tiles
                #print("COLLIDE:", self.position.y, tile.rect.top)
                self.space_pressed = 0
                self.on_ground = True
                self.is_jumping = False
                if self.position.y < tile.rect.bottom:
                    self.velocity.y = 0
                    self.position.y = tile.rect.top
                    self.rect.bottom = self.position.y
            elif self.velocity.y < 0 and self.position.y > tile.rect.top and not tile.passable: # Hitting solid tile from the bottom case
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y

    def slope_collisions(self):
        self.slope = False
        self.temp_Rect.x, self.temp_Rect.y = self.rect.x, self.rect.y + 16
        #temp_rectR.center = self.rect.center
        #temp_rectL = pygame.Rect(self.rect.x - self.rect.w, self.rect.y + 16, 16, self.rect.h)
        for slope in self.game.slopeList.sprites:
            # Check if the player is colliding with a slope
            if self.rect.colliderect(slope.rect) :
                if self.velocity.y > 0 and self.position.y + self.rect.h > slope.rect.top + slope.rect.h:
                    self.slope = True
                    new_y = self.slope_helper(slope)
                    self.position.y = new_y
                    self.on_ground = True
                    self.is_jumping = False
                    self.space_pressed = 0
            # Check if there is a slope below the player
            elif self.temp_Rect.colliderect(slope):
                if self. velocity.y > 0 and self.position.y + self.rect.h > slope.rect.top + slope.rect.h:
                    self.slope = True
                    new_y = self.slope_helper(slope)
                    self.position.y = new_y
                    self.on_ground = True
                    self.is_jumping = False


    def slope_helper(self, slope):
        new_y = self.position.y
        top = None
        if slope.ramp == 1: # Left Slopes
            #print("Left")
            if self.position.x  + self.rect.w <= (slope.rect.x + slope.rect.w):
                x = (slope.rect.x + slope.rect.w) - (self.position.x + self.rect.w)
                top = slope.rect.y + x
        if slope.ramp == 2: # Right Slopes
            #print("Right")
            if self.position.x >= slope.rect.x:
                x = self.position.x - slope.rect.x
                top = slope.rect.y + x
        if top:
            new_y = top
        return new_y

    def platform_collisions(self):
        hits = []
        for plat in self.game.platforms.sprites:
            plat.touched = False
            if self.rect.colliderect(plat):
                hits.append(plat)
        if hits:
            if self.velocity.y > 0 and self.position.y > hits[0].rect.top:
                if self.last_position.y < hits[0].rect.top + hits[0].rect.h*.125:
                    hits[0].touched = True
                    self.space_pressed = 0
                    self.on_ground = True
                    self.is_jumping = False
                    self.velocity.y = 0
                    self.position.y = hits[0].rect.top + 1
                    self.rect.bottom = self.position.y



    def check_enemy_collision(self):
        for enem in self.game.enemyList.sprites:
            # Check Using AABB first, if the rectangles are aligned check the collision mask
            if self.rect.colliderect(enem):
                if pygame.sprite.spritecollide(self,self.game.enems, False,pygame.sprite.collide_mask):
                    self.hurt = True
        if self.rect.y > self.game.deathzone:
            self.hurt = True

    # Checks if the player has passed the flag
    def check_object_collision(self):
        hits = []
        for tile in self.game.objectList.sprites:
            if self.rect.colliderect(tile):
                hits.append(tile)
        for hit in hits:
            self.game.sound_effects['pickup'].play()
            if hit.food == 'bread_loaf':
                self.game.complete = True
            elif hit.food == 'blueberry':
                self.berry_count += 1
                hit.kill()
                self.game.objectList.sprites.remove(hit)
            else:
                hit.collect()

    def check_interactive_collision(self):
        for object in self.game.water_tiles.sprites:
            if self.rect.colliderect(object):
                if self.position.y  > object.rect.top + object.rect.h *.5:
                    self.in_water = True
                    if self.position.y < object.rect.bottom:
                        object.touched = True
                        self.game.sound_effects['splash'].play()
                else:
                    if self.in_water: self.velocity.y -= 3.5
                    self.in_water = False
                    object.touched = False

    def fall_off(self):
        if not self.hurt_jump:
            self.game.sound_effects['hurt'].play()
            self.velocity.y = -10
            self.hurt_jump = True
        self.velocity.y += self.acc.y * self.game.dt
        if self.velocity.y > 15:
            self.velocity.y = 15
        self.rect.y += self.velocity.y * self.game.dt

    def load_images(self):
        self.idle_frames  = [self.game.duck_sheet.get_sprite("idleDuck1.png"),
                             self.game.duck_sheet.get_sprite("idleDuck2.png"),
                             self.game.duck_sheet.get_sprite("idleDuck1.png"),
                             self.game.duck_sheet.get_sprite("idleDuck2.png"),
                             self.game.duck_sheet.get_sprite("idleDuck1.png"),
                             self.game.duck_sheet.get_sprite("idleDuck2.png"),
                             self.game.duck_sheet.get_sprite("idleDuck1.png"),
                             self.game.duck_sheet.get_sprite("idleDuck2.png"),
                             self.game.duck_sheet.get_sprite("idleDuck1.png"),
                             self.game.duck_sheet.get_sprite("DuckBlink.png")
                             ]
        self.idle_frames_left = []
        for frame in self.idle_frames:
            self.idle_frames_left.append(pygame.transform.flip(frame,True,False))
        self.image = self.idle_frames[0]

        self.right_frames = [self.game.duck_sheet.get_sprite("duckwalk1.png"),
                             self.game.duck_sheet.get_sprite("duckwalk2.png"),
                             self.game.duck_sheet.get_sprite("duckwalk3.png"),
                             self.game.duck_sheet.get_sprite("duckwalk4.png")]

        self.left_frames = []
        for frame in self.right_frames:
            self.left_frames.append(pygame.transform.flip(frame,True,False))

        self.right_frames_run = [self.game.duck_sheet.get_sprite("duck_run1.png"),
                             self.game.duck_sheet.get_sprite("duck_run2.png"),
                             self.game.duck_sheet.get_sprite("duck_run3.png"),
                             self.game.duck_sheet.get_sprite("duck_run4.png")]

        self.left_frames_run = []
        for frame in self.right_frames_run:
            self.left_frames_run.append(pygame.transform.flip(frame, True, False))

        self.jump_image = self.game.duck_sheet.get_sprite("duckJump.png"), pygame.transform.flip(self.game.duck_sheet.get_sprite("duckJump.png"),True, False)
        # Load look up frames
        self.look_up = [self.game.duck_sheet.get_sprite("duckUp.png"), pygame.transform.flip(self.game.duck_sheet.get_sprite("duckUp.png"),True,False)]
        self.look_down = [self.game.duck_sheet.get_sprite("duckDown.png"), pygame.transform.flip(self.game.duck_sheet.get_sprite("duckDown.png"),True,False)]

        self.hurt_frames_right = [self.game.duck_sheet.get_sprite("hurt1.png"), self.game.duck_sheet.get_sprite("hurt2.png")]
        self.hurt_frames_left = []
        for frame in self.hurt_frames_right:
            self.hurt_frames_left.append(pygame.transform.flip(frame, True, False))

        self.land_frames_right = []
        for i in range(1,7):
            self.land_frames_right.append(self.game.duck_sheet.get_sprite("duck_land" + str(i) + ".png"))
        self.land_frames_left = []
        for frame in self.land_frames_right:
            self.land_frames_left.append(pygame.transform.flip(frame, True, False))

        self.swim_frames_right = []
        for i in range(1, 6):
            self.swim_frames_right.append(self.game.duck_sheet.get_sprite("duck_swim" + str(i) + ".png"))
        self.swim_frames_left = []
        for frame in self.swim_frames_right:
            self.swim_frames_left.append(pygame.transform.flip(frame, True, False))

