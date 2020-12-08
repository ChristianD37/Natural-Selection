from Assets.maps.level import *
from Assets.util.camera import Camera
from Assets.interactables.decorator import *
from Assets.menus.menu import *
from Assets.menus.end_level import *
from Assets.util.spritesheet import *
from Assets.util.fps import FPS
from Assets.enemies.enemies import *
from pygame.locals import *



# Main client for the program
class Game():
    def __init__(self):
        #flags = FULLSCREEN | DOUBLEBUF
        flags = DOUBLEBUF | HWSURFACE
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # Prevents delay in jumping sound
        pygame.init()
        pygame.mixer.init()
        self.SCREEN_WIDTH = 960
        self.SCREEN_HEIGHT = 540
        self.DISPLAY_W = 960
        self.DISPLAY_H = 540
        self.TITLE = "Natural Selection"
        self.camera = Camera(self)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing, self.complete = False, False
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT),flags)
        self.screen.set_alpha(None)
        self.LEFT_KEY,self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY, self.JUMP_KEY, \
        self.START_KEY, self.BACK_KEY, self.RUN_KEY  = False, False, False,False, False, False, False, False
        self.load_directories()
        self.load_controls()
        pygame.display.set_caption(self.TITLE)
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.load_menus()
        self.menu = self.Main
        self.levelnum, self.lives = 2,3
        self.font_name = "Assets/images/november.ttf"
        self.font = pygame.font.Font(self.font_name, 18)
        self.pause_menu = PauseMenu(self)
        self.pause = False
        self.volume_mult = 1
        self.volume_setting = 100
        self.x_mark, self.y_mark = 0,0
        self.map_w, self.map_h, self.deathzone = 0,0, 0
        self.update_dist = 32 * 2
        self.TARGET_FPS = 60
        self.timer = FPS()
        self.dt = 1
        self.load_HUD_text(20, (0, 0, 0))
        self.chunk = [[]]
        self.current_chunk, self.chunk_mark = 0, 0
        self.sound_effects, self.effects_vol = {}, {}

    # Re-initialize assets for a level
    def reset(self):
        #self.menu.loading() # Display loading screen
        self.reset_keys() # Reset all keys
        self.all_Sprites = pygame.sprite.Group() # Load all necessary assets
        self.tiles = pygame.sprite.Group()
        self.enems = pygame.sprite.Group()
        self.tileList = SpriteList(self)
        self.background = SpriteList(self)
        self.background_tiles = SpriteList(self)
        self.foreground_tiles = SpriteList(self)
        self.interactive_tiles = SpriteList(self)
        self.water_tiles = SpriteList(self)
        self.particles = SpriteList(self)
        self.slopeList = SpriteList(self)
        self.enemyList = SpriteList(self)
        self.objectList = SpriteList(self)
        self.platforms = SpriteList(self)
        self.bumpers = SpriteList(self)
        self.water = SpriteList(self)
        self.hud = SpriteList(self)
        self.player = Player(self)
        self.level = Level(self, self.levelnum)
        self.interactive_tiles.sprites += (self.water_tiles.sprites)
        self.map = Tilemap(self)
        self.dt = 1
        self.update_dist = 48 * 2
        self.camera.reset_cam()
        pygame.mixer.music.set_volume(self.volume_mult)
        self.fade_screen()
        self.fade_radius = self.DISPLAY_W * .5
        self.camera.scroll()
        self.current_chunk = 0
        self.bubbles = Bubbles(self, self.player.rect.x, self.player.rect.y)


    # Runs the main game loop
    def gameLoop(self):
        pygame.mixer.music.play(loops=-1)  # Start the music loop
        self.fade = True
        while self.player.alive and self.playing:
            self.get_delta()
            if self.pause:
                self.pause_menu.display_menu()
                self.pause = False
            self.get_events()
            if not self.fade:
                self.update()
            self.draw_screen()
            #self.get_frame()
        pygame.mixer.music.stop()
        if self.complete: self.fade_out()
        self.game_over()



    # Get input from player keyboard
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.pause_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                    self.pause_menu.run_display = False
                    return
                if event.key == self.START_CONTROL or event.key == pygame.K_KP_ENTER:
                    self.START_KEY = True
                    self.pause = True
                if event.key == self.LEFT_CONTROL:
                    self.LEFT_KEY = True
                if event.key == self.RIGHT_CONTROL:
                    self.RIGHT_KEY = True
                if event.key == self.DOWN_CONTROL:
                    self.DOWN_KEY = True
                if event.key == self.UP_CONTROL:
                    self.UP_KEY = True
                if event.key == self.JUMP_CONTROL:
                    self.JUMP_KEY = True
                    if not self.pause_menu.run_display and not self.player.hurt:
                        self.player.space_pressed += 1
                        self.player.jump()
                if event.key == self.RUN_CONTROL:
                    self.RUN_KEY = True

            if event.type == pygame.KEYUP:
                if event.key == self.LEFT_CONTROL:
                    self.LEFT_KEY = False
                if event.key == self.RIGHT_CONTROL:
                    self.RIGHT_KEY = False
                if event.key == self.DOWN_CONTROL:
                    self.DOWN_KEY = False
                if event.key == self.UP_CONTROL:
                    self.UP_KEY = False
                if event.key == self.JUMP_CONTROL:
                    self.JUMP_KEY = False
                    if self.player.space_pressed == 1 and self.player.is_jumping and not self.pause_menu.run_display:
                        self.player.velocity.y *= .3
                if event.key == self.RUN_CONTROL:
                    self.RUN_KEY = False
                if event.key == self.START_CONTROL or event.key == pygame.K_KP_ENTER:
                    self.START_KEY = False

            # Check the PS4 Controller
            if event.type == JOYBUTTONDOWN:
                if event.button == self.PS4_CONTROL['right']:
                    self.RIGHT_KEY = True
                if event.button == self.PS4_CONTROL['left']:
                    self.LEFT_KEY = True
                if event.button == self.PS4_CONTROL['down'] or event.button == self.PS4_CONTROL['L1']:
                    self.DOWN_KEY = True
                if event.button == self.PS4_CONTROL['up'] or event.button == self.PS4_CONTROL['R1']:
                    self.UP_KEY = True
                if event.button == self.PS4_CONTROL['X'] or event.button == self.PS4_CONTROL['circle']:
                    self.JUMP_KEY = True
                    if not self.pause_menu.run_display and not self.player.hurt:
                        self.player.space_pressed += 1
                        self.player.jump()
                if event.button == self.PS4_CONTROL['square'] or event.button == self.PS4_CONTROL['triangle']:
                    self.RUN_KEY = True
                if event.button == self.PS4_CONTROL['options']:
                    self.START_KEY = True
                    self.pause = True

            if event.type == JOYBUTTONUP:
                if event.button == self.PS4_CONTROL['right']:
                    self.RIGHT_KEY = False
                if event.button == self.PS4_CONTROL['left']:
                    self.LEFT_KEY = False
                if event.button == self.PS4_CONTROL['down'] or event.button == self.PS4_CONTROL['L1']:
                    self.DOWN_KEY = False
                if event.button == self.PS4_CONTROL['up'] or event.button == self.PS4_CONTROL['R1']:
                    self.UP_KEY = False
                if event.button == self.PS4_CONTROL['X'] or event.button == self.PS4_CONTROL['circle']:
                    self.JUMP_KEY = False
                    if self.player.space_pressed == 1 and self.player.is_jumping and not self.pause_menu.run_display:
                        # TO-DO FIX momentum stop
                        self.player.velocity.y = 0
                if event.button == self.PS4_CONTROL['square'] or event.button == self.PS4_CONTROL['triangle']:
                    self.RUN_KEY = False
                if event.button == self.PS4_CONTROL['options']:
                    self.START_KEY = False

            if event.type == pygame.JOYAXISMOTION:
                self.thumbstick[event.axis] = round(event.value, 2)
                if abs(self.thumbstick[0]) > .4:
                    if self.thumbstick[0] < .7:
                        self.RIGHT_KEY = False
                    else: self.RIGHT_KEY = True
                    if self.thumbstick[0] < -.7:
                        self.LEFT_KEY = True
                    else:
                        self.LEFT_KEY = False




    # Update all sprites
    def update(self):
        #self.tiles.update()
        self.enemyList.update()
        self.platforms.update()
        self.player.update()
        self.camera.scroll()
        if self.complete:
            self.playing = False
            self.levelnum += 1
            self.menu = self.end_screen
            self.player.victory_sound.play()
            pygame.mixer.music.stop()

        if self.player.checkDeath():
            self.player.alive = False
            self.lives -= 1




    # Draw all sprites on screen
    def draw_screen(self):
        #pygame.display.set_caption('FPS: {}'.format(self.clock.get_fps()))
        self.background.draw()
        #self.tileList.draw()
        self.map.draw() # Draws the tilemap
        self.platforms.draw()
        self.objectList.draw()
        self.enemyList.draw()
        self.player.draw(self.screen)
        self.interactive_tiles.draw()
        self.particles.draw()
        self.hud.draw()
        self.fade_in()
        #self.screen.blit(self.display, (0, 0))
        self.screen.blit(pygame.transform.scale(self.display,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.update()

    def fade_in(self):
        if self.fade:
            pygame.draw.circle(self.display,color=(0,0,0),center=(self.DISPLAY_W *.5,self.DISPLAY_H * .5), radius = self.fade_radius)
            self.fade_radius -= 10 * self.dt
            if self.fade_radius <= 0:
                self.fade = False

    def fade_out(self):
        self.complete = False
        now = pygame.time.get_ticks()
        start = now
        while now - start < 3000 and self.running:
            self.get_delta()
            self.get_events()
            now = pygame.time.get_ticks()
            pygame.draw.circle(self.display, color=(0, 0, 0), center=(self.DISPLAY_W * .5, self.DISPLAY_H * .5),
                               radius=self.fade_radius)
            self.fade_radius += 3.2 * self.dt
            if self.fade_radius >= self.DISPLAY_W:
                self.fade_radius = self.DISPLAY_W
            self.screen.blit(pygame.transform.scale(self.display, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
            pygame.display.update()


    def reset_keys(self):
        self.LEFT_KEY = False
        self.RIGHT_KEY = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.JUMP_KEY = False
        self.BACK_KEY = False
        self.RUN_KEY = False

    def fade_screen(self):
        fade = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        fade.fill((0, 0, 0))
        alpha, now, current_time = 0, pygame.time.get_ticks(), pygame.time.get_ticks()
        while now - current_time < 500:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    self.pause_menu.run_display = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.running = False
                        self.pause_menu.run_display = False
                        return
            self.get_delta()
            alpha += .5 * self.dt
            fade.set_alpha(alpha)
            self.display.blit(fade, (0, 0))
            self.screen.blit( pygame.transform.scale(self.display, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
            pygame.display.update()

    def game_over(self):
        if self.lives < 1:
            self.playing = False
            self.lives = 3
            self.menu = self.game_over_menu


        # Draws text to the screen
    def load_HUD_text(self, size, color):
        self.font = pygame.font.Font(self.font_name, size)
        self.berry_x = self.font.render(' x', True, color)
        self.number_text = []
        for i in range(0,50):
            self.number_text.append(self.font.render(str(i), True, color))


    def load_directories(self):
        self.dir = path.join(path.dirname(path.abspath("game.py")), "Assets")  # Gets the directory name of the game.py file
        self.img_dir = path.join(self.dir,"images")
        self.spriteSheet_dir = path.join(self.img_dir, "spritesheets")
        self.options_dir = path.join(self.dir, "options")
        sound_dir = path.join(self.dir, "sounds")
        self.theme_dir, self.menu_music = path.join(sound_dir, "level_themes"), path.join(sound_dir, "menu_themes")
        self.effects_dir = path.join(sound_dir, "sound_effects")
        self.load_spritesheets()
        self.sounds_list = []
        self.default_vol = []

    def load_menus(self):
        self.Main = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.volume_menu = VolumeMenu(self)
        self.controls_menu = ControlsMenu(self)
        self.end_screen = LevelComplete(self)
        self.game_over_menu = GameOver(self)


    def get_delta(self):
        # Compute
        elapsed_time = self.timer.elapsed_time()
        if elapsed_time == 0: elapsed_time=1
        self.dt = elapsed_time * self.TARGET_FPS
        #self.timer.cap_fps(60,elapsed_time)
        pygame.display.set_caption("{0}: {1:.2f}".format(self.TITLE, self.timer.get_fps()))
        if self.dt > 3: # Cap delta time for when window is held
            self.dt = 3

    def load_spritesheets(self):
        # Load all necessary spritesheets from the spritesheet folder
        dir = os.path.join("Assets", "images", "spritesheets")
        self.spriteSheet = Spritesheet(os.path.join(dir, "duckSheet"))
        self.duck_sheet = Spritesheet(os.path.join(dir, "duckling_sheet"))
        self.snake_sheet = Spritesheet(os.path.join(dir, "snake_sheet"))
        self.hawk_sheet = Spritesheet(os.path.join(dir, "hawk_sheet"))
        self.grass_tiles = Spritesheet(os.path.join(dir, "tiles"))
        self.objects_sheet = Spritesheet(os.path.join(dir, "objects"))
        self.background_sheet = Spritesheet(os.path.join(dir, "decorators"))

    def load_controls(self):
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()
        self.thumbstick = { 0: 0, 1 : 0}
        self.PS4_CONTROL = {'left' : 13, 'right' : 14, 'up': 11, 'down' : 12, 'X' : 0, 'circle' : 1, 'square' : 2, 'triangle' : 3,
                            'PS' : 5, 'options' : 6, 'share' : 4, 'R1' : 10, 'L1' : 9, 'touchpad' : 15}


        # Load in controls from controls.json. If file not found, load the default controls
        self.START_CONTROL, self.JUMP_CONTROL, self.RUN_CONTROL = pygame.K_RETURN, pygame.K_p, pygame.K_o
        self.LEFT_CONTROL, self.RIGHT_CONTROL, self.UP_CONTROL, self.DOWN_CONTROL = pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s
        self.DEF_CONTROLS = {'Left': self.LEFT_CONTROL, 'Right': self.RIGHT_CONTROL,
                         'Up': self.UP_CONTROL, 'Down': self.DOWN_CONTROL,
                         'Start': self.START_CONTROL, 'Jump': self.JUMP_CONTROL,
                         'Run': self.RUN_CONTROL}
        try:
            with open(path.join(self.options_dir, 'controls.json'), 'r+') as file:
                self.CONTROLS = json.load(file)
        except (OSError, ValueError):
            self.CONTROLS = self.DEF_CONTROLS
        self.reassign_controls()
        self.CONTROL_LIST = ['Left', 'Right','Up','Down', 'Start', 'Jump', 'Run']

    def reassign_controls(self):
        # Helper function to reassign controls
        self.START_CONTROL, self.JUMP_CONTROL, self.RUN_CONTROL = self.CONTROLS['Start'], self.CONTROLS['Jump'], self.CONTROLS['Run']
        self.LEFT_CONTROL, self.RIGHT_CONTROL, self.UP_CONTROL, self.DOWN_CONTROL = self.CONTROLS['Left'], self.CONTROLS['Right'],\
                                                                                    self.CONTROLS['Up'], self.CONTROLS['Down']

    def add_sound(self, sound, volume, extension = '.ogg'):
        new_sound  = pygame.mixer.Sound(path.join(self.effects_dir, sound + extension) )
        new_sound.set_volume(volume * self.volume_mult)
        self.sound_effects[sound] = new_sound


    def quit(self):
        pygame.quit()