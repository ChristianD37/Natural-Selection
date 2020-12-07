import pygame
import json

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.filename = filename + '.png'
        self.spritesheet_file = filename + '.json'
        self.spritesheet = pygame.image.load(self.filename).convert()
        with open(self.spritesheet_file) as f:
            self.data = json.load(f)


    def get_image(self, x, y, w, h):
        # grab the image out of a larger sprite sheet
        image = pygame.Surface((w, h))
        image.set_colorkey((0,0,0))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        return image

    def get_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x,y,w,h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_image(x,y,w,h)
        return image

