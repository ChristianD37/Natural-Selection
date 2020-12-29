from os import path
from Assets.maps.tile import *
from Assets.util.camera import *
from Assets.interactables.decorator import *
from Assets.enemies.enemies import *
from Assets.interactables.objects import *
from Assets.interactables.platforms import *
from Assets.util.hud import *
import os
import csv

# Class that creates the current level
class Level:
    def __init__(self, game, choice):
        self.game = game
        self.choice = choice
        self.dir = os.path.join(os.getcwd(), "Assets", "maps")
        self.level_tiles = ["hawk", "snake", "apple", "cloud", "bread_loaf", "grass.png",
                             "grass2.png", "grass3.png", "grass4.png", "leaves.png", "leaves2.png", "leaves3.png", "leaves_base.png",
                             "shrub1.png","shrub2.png","shrub3.png","shrub4.png","shrub5.png", "shrub6.png",
                             "shrub7.png","shrub8.png","shrub9.png","shrub10.png","shrub11.png", "shrub12.png",
                             "shrub13.png", "shrub14.png", "shrub15.png", "shrub16.png", "slope_left.png", "slope_midleft.png",
                             "slope_midright.png", "slope_right.png", "underground.png", "blueberry", 'strawberry', 'grassblades',
                             'start_flag', 'end_flag', 'z3_leaves_side1.png','z3_leaves_side2.png', 'moving_leaf', "platform.png",
                             "z4_sand1.png","z4_sand2.png", "z4_sand3.png", "z4_sand4.png", "bumper", "z5_water.png", "z5_waterTop.png",
                             "z6_grass_shadow1.png","z6_grass_shadow2.png","z6_grass_shadow3.png", "z6_grass_shadow4.png", "z6_ground.png",
                             "mushroom", "chunk", "z6_ground_dino.png", "z8_ground1.png", "z8_ground2.png", "orange"]
        self.load_level()

    # Loads the appropriate level
    def load_level(self):
        if (self.choice == 1):
            self.tile_list = self.level_tiles
            self.game.background.addSprite(BlueBackground(self.game))
            self.game.background.addSprite(Sun(self.game))
            #self.game.background.addSprite(Birds(self.game))
            self.load_hud()
            self.game.scrolling_background = Hills(self.game)
            self.game.background.addSprite(self.game.scrolling_background)
            pygame.mixer.music.load(path.join(self.game.theme_dir, "Curious Stroll - Clarinet.ogg"))
            self.load_map_csv("chaparall_1.csv")
            self.load_tiles()
            self.game.camera.setmethod(Follow(self.game))

        elif (self.choice == 2):
            self.tile_list = self.level_tiles
            self.game.background.addSprite(BlueBackground(self.game))
            self.game.background.addSprite(Sun(self.game))
            #self.game.background.addSprite(Birds(self.game))
            self.load_hud()
            self.game.scrolling_background = Hills(self.game)
            self.game.background.addSprite(self.game.scrolling_background)
            pygame.mixer.music.load(path.join(self.game.theme_dir, "Curious Stroll - Clarinet.ogg"))
            self.load_map_csv("chaparall_2.csv")
            self.load_tiles()
            self.game.camera.setmethod(Auto(self.game))



        elif (self.choice == 3):
            self.tile_list = self.level_tiles
            self.game.background = SpriteList(self.game)
            self.game.background.addSprite(OrangeBackground(self.game))
            self.game.background.addSprite(Birds(self.game))
            self.load_hud()
            #self.game.scrolling_background = Hills(self.game)
           # self.game.background.addSprite(self.game.scrolling_background)
            pygame.mixer.music.load(path.join(self.game.theme_dir, "glistening dusk.ogg"))
            self.load_map_csv("beach_1.csv")
            self.load_tiles()
            self.game.camera.setmethod(Follow(self.game))




    # Loads tiles by parsing the tilemap
    def load_tiles(self):
        y = 0
        for layer in self.map:
            x = 0
            for tile in layer:
                if tile == '0':
                    h = Hawk(self.game, x * 32, y * 32)
                    self.game.enemyList.addSprite(h)
                elif tile == '1':
                    s = Snake(self.game, x * 32, y * 32 - 8)
                    self.game.enemyList.addSprite(s)
                elif tile == '2'  or tile == '35' or tile == '60':
                    food = Food(self.game, x * 32, y * 32, self.tile_list[int(tile)], HUD = True)
                    self.game.objectList.addSprite(food)
                elif tile == '3':
                    cloud = Cloud(self.game,x*32,y*32)
                    self.game.platforms.addSprite(cloud)
                elif tile == '4':
                    self.game.bread= Food(self.game, x * 32, y * 32 +10, self.tile_list[int(tile)])
                    self.game.x_mark, self.game.y_mark = x * 32, y * 32 +10
                    self.game.objectList.addSprite(self.game.bread)
                elif tile == '34':
                    berry = Food(self.game, x * 32, y * 32, self.tile_list[int(tile)])
                    self.game.objectList.addSprite(berry)
                # Load solid tiles
                elif tile == '5'  or tile == '7' or tile == '8' or tile == '30' or tile == '31' or tile == '43'\
                        or tile == '44' or tile == '45' or tile == '46' or tile == '50' or tile == '51' or tile == '52' or tile == '53'\
                        or  tile == '54' or tile =='58' or tile =='59':
                    t = Tile(self.game, self.tile_list[int(tile)],x*32,y*32, False, True)
                    self.game.tileList.addSprite(t)
                # Load One-Way Platforms
                elif tile == '9' or tile == '10' or tile =='11':
                    t = Tile(self.game, self.tile_list[int(tile)], x * 32, y * 32, True, True)
                    self.game.tileList.addSprite(t)
                # Load Left slopes
                elif tile == '29':
                    slope = Tile(self.game, self.tile_list[int(tile)], x * 32, y * 32, False, True, ramp=1)
                    self.game.slopeList.addSprite(slope)
                # Load Right slopes
                elif tile == '32':
                    slope = Tile(self.game, self.tile_list[int(tile)], x * 32, y * 32, False, True, ramp=2)
                    self.game.slopeList.addSprite(slope)
                # Load Background Tiles
                elif tile == '6' or tile =='12' or tile =='13' or tile =='14' or tile =='15' or tile =='16' \
                        or tile == '17'or tile == '18' or tile == '19' or tile == '20' or tile == '21'\
                        or tile == '22' or tile == '23' or tile == '24' or tile == '25' or tile == '26'\
                        or tile == '27' or tile == '28' or tile == '33' or tile == '39' or tile == '40':
                    t = Tile(self.game, self.tile_list[int(tile)], x * 32, y * 32, True, False)
                    self.game.background_tiles.addSprite(t)
                    t.remove(self.game.tiles)
                # Load interactive tiles:
                elif tile == '36':
                    grass = Grass(self.game, x *32, y* 32)
                    self.game.interactive_tiles.addSprite(grass)
                elif tile == '38':
                    self.game.deathzone = y * 32
                # Set players Starting coordinates
                elif tile == '37':
                    self.game.player.position.x, self.game.player.position.y = x*32, y*32 + 64
                    self.game.player.rect.x, self.game.player.rect.bottom = x*32, y*32 + 64
                elif tile == '41':
                    leaf = Leaf(self.game, x * 32, y * 32)
                    self.game.platforms.addSprite(leaf)
                elif tile == '42':
                    red = RedPlatform(self.game, x* 32, y*32, 'platform.png')
                    self.game.platforms.addSprite(red)
                # Load bumper
                elif tile == '47':
                    bumper = Bumper(self.game,x*32,y*32)
                    self.game.bumpers.addSprite(bumper)
                # Load interactable tiles
                elif tile == '48':
                    water = Tile(self.game,self.tile_list[int(tile)], x * 32, y * 32, True, False)
                    water.image.set_alpha(115)
                    self.game.interactive_tiles.addSprite(water)
                    #self.game.foreground_tiles.addSprite(water)
                # Load surface of water
                elif tile == '49':
                    water_top = WaterSurface(self.game, x* 32, y * 32)
                    self.game.water_tiles.addSprite(water_top)
                elif tile == '55':
                    m = Mushroom(self.game,x*32,y*32)
                    self.game.interactive_tiles.addSprite(m)
                elif tile == '56':
                    self.game.chunk_mark = x * 32
                elif tile == '57':
                    l = Large_Tile(self.game, self.tile_list[int(tile)], x * 32, y * 32)
                    self.game.background_tiles.addSprite(l)
                x += 1
            y += 1
            self.game.map_w, self.game.map_h = x, y # Load the width and height of the map
        # Load extra enemies

    # Loads map from a txt file
    def load_map(self, fpath):
        file = open( os.path.join(self.dir, fpath) )
        data = file.read()
        file.close()
        data = data.split('\n')
        self.map = []
        for row in data:
            self.map.append(list(row))

    # Loads map from a csv file
    def load_map_csv(self, fpath):
        with open(os.path.join(self.dir, fpath)) as data:
            data = csv.reader(data,delimiter = ',')
            self.map = []
            for row in data:
                self.map.append(list(row))

    def load_hud(self):
        self.game.lives_hud = Lives_HUD(self.game,'HuD_duck', 5, 5)
        self.game.berries_hud = Berries_HUD(self.game, 'blueberry', 80, 5)
        self.game.hud.addSprite(self.game.lives_hud)
        self.game.hud.addSprite(self.game.berries_hud)


