import pygame
from abc import ABC
vec = pygame.math.Vector2

# Handles how the screen behaves
class Camera:
    def __init__(self, game):
        self.game = game
        self.offset = vec(0,0)
        self.scrollval = vec(0,0)

    # Sets the strategy pattern for the scroll algorithm
    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()


    def reset_cam(self):
        self.offset = vec(0, 0)
        self.scrollval = vec(0, 0)
        self.scrollval.x, self.scrollval.y = (self.game.player.rect.x - self.game.camera.scrollval.x - self.game.DISPLAY_W / 4), \
                                       (self.game.player.rect.y - self.game.camera.scrollval.y - self.game.DISPLAY_H / 2)
        self.offset.x, self.offset.y = (self.game.player.rect.x - self.game.camera.scrollval.x - self.game.DISPLAY_W/4), \
                        (self.game.player.rect.y - self.game.camera.scrollval.y - self.game.DISPLAY_H / 2 )
        if type(self.method).__name__ == "Auto":
            self.scrollval.x = self.game.player.rect.x - 50
            self.offset.x = self.scrollval.x



# Abstract base class for scroll algorithm
class CamScroll(ABC):
    def __init__(self, game):
        self.game = game


    def scroll(self):
        pass

    def scroll_lock(self):
        pass

# Algorithm that Follows the player sprite
class Follow(CamScroll):
    def __init__(self, game):
        CamScroll.__init__(self,game)
        self.extra_y = 0

    def scroll(self):
        if not self.game.player.hurt:
            self.game.camera.scrollval.x += (self.game.player.position.x + self.game.player.rect.w - self.game.camera.scrollval.x - self.game.DISPLAY_W/2 + 100) / (32)  # Dividing applies a lag effect to the camera
            self.game.camera.scrollval.y += (self.game.player.position.y - self.game.player.rect.h - self.game.camera.scrollval.y - self.game.DISPLAY_H / 2 + self.extra_y) / (16/self.game.dt)
            self.game.camera.offset.x = min(max(int(self.game.camera.scrollval.x), 0), self.game.map_w*32 - (self.game.DISPLAY_W))
            #self.game.camera.offset.y = int(self.game.camera.scrollval.y)
            self.game.camera.offset.y = min(int(self.game.camera.scrollval.y),self.game.deathzone - self.game.DISPLAY_H  )

    def scroll_lock(self):
        if self.game.camera.offset.x == 0 or self.game.camera.offset.x == self.game.map_w*32 - (self.game.DISPLAY_W):
            return True


# Moves the screen independently of the player
class Auto(CamScroll):
    def __init__(self, game):
        CamScroll.__init__(self,game)
        self.extra_y = 0

    def scroll(self):
        if not self.game.player.hurt:
            self.game.camera.scrollval.x += 1 * self.game.dt
            self.game.camera.scrollval.y += (self.game.player.position.y - self.game.player.rect.h - self.game.camera.scrollval.y - self.game.DISPLAY_H / 2 + self.extra_y) / (
                                                        16 / self.game.dt)
            self.game.camera.offset.x = min(max(int(self.game.camera.scrollval.x), 0),
                                            self.game.map_w * 32 - (self.game.DISPLAY_W))
            self.game.camera.offset.y = min(int(self.game.camera.scrollval.y),self.game.deathzone - self.game.DISPLAY_H  )

            if self.game.player.position.x < self.game.camera.offset.x:
                if self.game.player.tiled: self.game.player.hurt = True
                #self.game.player.velocity.x += self.game.camera.scrollval.x
                self.game.player.position.x = self.game.camera.offset.x
                self.game.player.velocity.x = 0
                self.game.player.velocity.x += 1
            if self.game.player.position.x > self.game.camera.offset.x + self.game.DISPLAY_W - self.game.player.rect.w:
                self.game.player.position.x = self.game.camera.offset.x + self.game.DISPLAY_W - self.game.player.rect.w

class VerticalFollow(CamScroll):
    def __init__(self, game):
        CamScroll.__init__(self,game)
        self.extra_y = 0

    def scroll(self):
        if not self.game.player.hurt:
            self.game.camera.scrollval.x += (self.game.player.position.x + self.game.player.rect.w - self.game.camera.scrollval.x - self.game.DISPLAY_W / 4)  # Dividing applies a lag effect to the camera
            if self.game.player.on_ground:
                self.game.camera.scrollval.y += ( self.game.player.position.y - self.game.player.rect.h - self.game.camera.scrollval.y - self.game.DISPLAY_H / 2 + self.extra_y) / 10
            self.game.camera.offset.x = min(max(int(self.game.camera.scrollval.x), 0), self.game.map_w * 32 - (self.game.DISPLAY_W))
            # self.game.camera.offset.y = int(self.game.camera.scrollval.y)
            self.game.camera.offset.y = min(int(self.game.camera.scrollval.y), self.game.deathzone - self.game.DISPLAY_H)

# class BoundBox(CamScroll):
#     def __init__(self, game):
#         CamScroll.__init__(self,game)
#         self.extra_y = 0
#         self.passed = False
#
#     def scroll(self):
#         self.game.player.bound_box.y = self.game.player.rect.y
#         if self.game.player.velocity.x == 0 and self.passed:
#             self.passed = False
#             self.game.player.bound_box.center = self.game.player.rect.center
#         if self.game.player.rect.left > self.game.player.bound_box.left and self.game.player.rect.right < self.game.player.bound_box.right:
#             pass
#         else:
#             self.passed = True
#             if self.game.player.rect.left > self.game.player.bound_box.left:
#                 self.game.player.bound_box.left += self.game.player.velocity.x
#             elif self.game.player.rect.right < self.game.player.bound_box.right:
#                 self.game.player.bound_box.left += self.game.player.velocity.x
#         if not self.passed:
#             pass
#         else:
#             self.game.camera.scrollval.x += ( self.game.player.rect.x - self.game.camera.scrollval.x - self.game.DISPLAY_W / 4)  # Dividing applies a lag effect to the camera
#             self.game.camera.scrollval.y += ( self.game.player.rect.y - self.game.camera.scrollval.y - self.game.DISPLAY_H / 2 + self.extra_y) / 20
#             self.game.camera.offset.x = int(self.game.camera.scrollval.x)
#             # self.game.camera.offset.y = int(self.game.camera.scrollval.y)
#             self.game.camera.offset.y = min(int(self.game.camera.scrollval.y),
#                                             self.game.deathzone - self.game.DISPLAY_H)