import pygame
from os import path
import json, math
from Assets.util.file_handler import write_save

# Menus between the game
class Menu():
    def __init__(self, game):
        self.game = game
        self.font_name = "Assets/images/november.ttf"
        self.font = pygame.font.Font(self.font_name, 40)
        self.run_display = False
        self.img_dir = path.join(self.game.img_dir, 'menu_images')
        self.cursor_img = pygame.image.load(path.join(self.img_dir, 'cursor.png')).convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()
        self.mid_w = self.game.DISPLAY_W / 2
        self.mid_h = self.game.DISPLAY_H / 2
        self.font_size = 40


        # Draws text to the screen
    def draw_text(self, text, size, color, x, y):
        text_surface = self.font.render(text, True, color, size)
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, text_rect)

    def draw_cursor(self):
        self.game.display.blit(self.cursor_img, self.cursor_rect)

    def loading(self):
        self.game.display.fill((0, 0, 0))
        self.draw_text("Loading", 20, (255, 255, 255), self.game.DISPLAY_W / 2,self.game.DISPLAY_H / 2 - 20)
        self.blit_screen()

    def blit_screen(self):
        self.game.screen.blit(
            pygame.transform.scale(self.game.display, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)), (0, 0))
        pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.playing = False
                self.game.running = False
                self.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.playing = False
                    self.game.running = False
                    self.run_display = False
                    return
                if event.key == self.game.START_CONTROL or event.key == pygame.K_KP_ENTER:
                    self.game.START_KEY = True
                if event.key == pygame.K_BACKSPACE: #or self.game.RUN_CONTROL:
                    self.game.BACK_KEY = True
                if event.key == self.game.LEFT_CONTROL:
                    self.game.LEFT_KEY = True
                if event.key == self.game.RIGHT_CONTROL:
                    self.game.RIGHT_KEY = True
                if event.key == self.game.DOWN_CONTROL:
                    self.game.DOWN_KEY = True
                if event.key == self.game.UP_CONTROL:
                    self.game.UP_KEY = True
                if event.key == self.game.RUN_CONTROL:
                    self.game.RUN_KEY = True
                if event.key == self.game.JUMP_CONTROL:
                    self.game.JUMP_KEY = True
            if event.type == pygame.KEYUP:
                if event.key == self.game.LEFT_CONTROL:
                    self.game.LEFT_KEY = False
                if event.key == self.game.RIGHT_CONTROL:
                    self.game.RIGHT_KEY = False
                if event.key == self.game.DOWN_CONTROL:
                    self.game.DOWN_KEY = False
                if event.key == self.game.UP_CONTROL:
                    self.game.UP_KEY = False
                if event.key == self.game.START_CONTROL or event.key == pygame.K_KP_ENTER:
                    self.game.START_KEY = False
                if event.key == self.game.RUN_CONTROL:
                    self.game.RUN_KEY = False
                if event.key == self.game.JUMP_CONTROL:
                    self.game.JUMP_KEY = False

    # Main Menu Screen
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.blit_screen()
            self.check_events()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        self.state = 'Start'
        self.load_title()
        self.offset = -100 * 1.5
        self.startx, self.starty = self.mid_w, self.mid_h + 30 * 2 - 20
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50 * 2 - 10
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70 * 2 + 10
        self.cursor_rect.center = (self.startx + self.offset,self.starty)


    def display_menu(self):
        self.run_display = True
        self.game.reset_keys()
        while self.run_display:
            self.game.get_delta()
            self.check_events()
            self.check_input()
            self.animate()
            self.game.display.blit(self.images[self.current_frame], (0,0))
            pygame.draw.polygon(self.game.display,(9,8,6), self.shadows)
            self.draw_text("Natural Selection Demo", 100, (0, 0, 0), self.game.DISPLAY_W / 2,self.game.DISPLAY_H / 3 )
            self.draw_text("Start Game", 20, pygame.Color((0,0,0)), self.startx, self.starty)
            self.draw_text("Options", 20, pygame.Color((0,0,0)), self.optionsx,self.optionsy)
            self.draw_text("Credits", 20, pygame.Color((0,0,0)), self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
            self.game.reset_keys()


    def check_input(self):
        self.move_cursor()
        if (self.game.START_KEY or self.game.JUMP_KEY):
            if self.state == 'Start':
                #self.game.playing = True
                self.game.menu = self.game.level_select
                self.run_display = False
                self.game.sound_effects['select'].play()
                #self.game.fade_screen()
            if self.state == 'Options':
                self.game.menu = self.game.options
                self.run_display = False
            if self.state == 'Credits':
                self.game.menu = self.game.credits
                self.run_display = False

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.sound_effects['select'].play()
            if  self.state == 'Start':
                self.cursor_rect.center = (self.optionsx + self.offset,self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.center = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.center = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            self.game.sound_effects['select'].play()
            if  self.state == 'Start':
                self.cursor_rect.center = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.center = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.center = (self.optionsx + self.offset,self.optionsy)
                self.state = 'Options'

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 400:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.images)

    def load_title(self):
        self.current_frame, self.last_updated = 0, 0
        self.images = [pygame.image.load(path.join(self.img_dir, 'MenuScreen1.png')).convert_alpha(),
                       pygame.image.load(path.join(self.img_dir, 'MenuScreen2.png')).convert_alpha() ]
        self.outline  = pygame.mask.from_surface(pygame.image.load(path.join(self.img_dir, 'hatch1.png'))).outline()
        self.outline = [(x + 702 - 60, y + 288 - 34 ) for x,y in self.outline]
        self.sun_position = pygame.Vector2(0,0)
        self.target_position = pygame.Vector2(960,540)
        self.sun_angle = math.atan2((self.sun_position.x - self.target_position.x), (self.sun_position.y - self.target_position.y) )
        self.shadows = []
        for x, y in self.outline:
            shadow_height = (508 - y) * 1.5
            shadow_width = shadow_height * math.tan(self.sun_angle)
            shadow_point = (x + shadow_width, y + shadow_height)
            self.shadows.append(shadow_point)


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.offset = -50 * 2
        self.volx, self.voly = self.mid_w, self.mid_h
        self.contrx, self.contry = self.mid_w, self.mid_h + 50 * 2
        self.cursor_rect.center = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_inputs()
            self.game.display.fill((198,215,185))
            self.draw_text("Options", 20, pygame.Color((0,0,0)), self.mid_w, self.game.DISPLAY_H /4)
            self.draw_text("Volume", 20, pygame.Color((0,0,0)), self.volx, self.voly)
            self.draw_text("Controls", 20, pygame.Color((0,0,0)), self.contrx, self.contry)
            self.draw_cursor()
            self.blit_screen()
            self.game.reset_keys()

    def check_inputs(self):
        if self.game.BACK_KEY or self.game.RUN_KEY:
            self.game.menu = self.game.Main
            self.run_display = False
            return
        elif self.game.START_KEY or self.game.JUMP_KEY:
            if self.state == 'Volume':
                self.game.menu = self.game.volume_menu
                self.run_display = False
            elif self.state == 'Controls':
                self.game.menu = self.game.controls_menu
                self.run_display = False
        elif self.game.UP_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.center = (self.contrx + self.offset, self.contry)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.center = (self.volx + self.offset , self.voly)
        elif self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.center = (self.contrx + self.offset, self.contry)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.center = (self.volx + self.offset , self.voly)

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.sound_effects['select'].play()
            if  self.state == 'Volume':
                self.cursor_rect.center = (self.volx + self.offset,self.voly)


class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = '+'
        self.offset = -20
        self.volx, self.voly = self.mid_w, self.mid_h
        self.plusx, self.plusy = self.mid_w + 100, self.game.DISPLAY_H * 3/4
        self.minx, self.miny = self.mid_w - 100, self.game.DISPLAY_H * 3 / 4
        self.cursor_rect.center = (self.plusx + self.offset, self.plusy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_inputs()
            self.game.display.fill((198,215,185))
            self.draw_text("Options", 20, pygame.Color((0,0,0)), self.mid_w, self.game.DISPLAY_H / 4)
            self.draw_text("Volume", 20, pygame.Color((0,0,0)), self.volx, self.voly)
            self.draw_text(f"Volume Level: {self.game.volume_setting}% ", 20, pygame.Color((0,0,0)), self.mid_w, self.mid_h + 60)
            self.draw_text("+", 20, pygame.Color((0,0,0)), self.plusx, self.plusy)
            self.draw_text("-", 20, pygame.Color((0,0,0)), self.minx, self.miny)
            self.draw_cursor()
            self.blit_screen()
            self.game.reset_keys()

    def check_inputs(self):
        if self.game.BACK_KEY or self.game.RUN_KEY:
            self.game.menu = self.game.options
            self.run_display = False
            return
        elif self.game.LEFT_KEY:
            self.game.sound_effects['select'].play()
            self.state = '-'
            self.cursor_rect.center = (self.minx + self.offset, self.miny)
        elif self.game.RIGHT_KEY:
            self.game.sound_effects['select'].play()
            self.state = '+'
            self.cursor_rect.center = (self.plusx + self.offset, self.plusy)
        elif (self.game.START_KEY or self.game.JUMP_KEY):
            self.adjust_audio()

    def adjust_audio(self):
        if self.state == '+':
            if self.game.volume_setting >= 100:
                self.game.volume_setting = 100
            else:
                self.game.volume_setting += 5
        elif self.state == '-':
            if self.game.volume_setting <= 0 :
                self.game.volume_setting = 0
            else:
                self.game.volume_setting -= 5
        self.game.volume_mult = self.game.volume_setting / 100
        self.game.save_data["volume"] = self.game.volume_setting
        write_save(self.game.options_dir,self.game.save_data)
        pygame.mixer.music.set_volume(self.game.volume_mult)
        for sound in self.game.sound_effects:
            self.game.sound_effects[sound].set_volume(self.game.volume_mult)

class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.offset = -50 * 2
        self.volx, self.voly = self.mid_w, self.mid_h
        self.cursor_rect.center = (self.game.DISPLAY_W/2 + self.offset * 2, self.game.DISPLAY_H/2.5)
        self.cursor_pos, self.curr_index = 0, 0

    def display_menu(self):
        self.run_display = True
        self.game.START_KEY = False
        self.game.BACK_KEY, self.game.RUN_KEY = False, False
        #pygame.mixer.pause()
        while self.run_display:
            self.game.get_delta()
            self.check_events()
            self.check_input()
            self.game.display.fill((198,215,185))
            self.draw_text('Change Controls',20, pygame.Color((0,0,0)), self.game.DISPLAY_W/2, self.game.DISPLAY_H/4)
            self.display_current_controls()
            self.draw_cursor()
            self.blit_screen()
            self.game.reset_keys()

    def display_current_controls(self):
        i = 0
        for control in self.game.CONTROLS:
            self.draw_text(control + ':' + pygame.key.name(self.game.CONTROLS[control]),20, pygame.Color((0,0,0)), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2.5 + i)
            i += 40

    def check_input(self):
        if self.game.BACK_KEY or self.game.RUN_KEY:
            self.game.menu = self.game.options
            self.run_display = False
            return
        elif self.game.START_KEY or self.game.JUMP_KEY:
            self.get_new_control()
        elif self.game.DOWN_KEY:
            self.curr_index += 1
            if self.curr_index > 6:
                self.curr_index = 0
            self.cursor_rect.center = (self.game.DISPLAY_W/2 + self.offset * 2, self.game.DISPLAY_H/2.5 + self.curr_index * 40)
        elif self.game.UP_KEY:
            self.curr_index -= 1
            if self.curr_index < 0:
                self.curr_index = 6
            self.cursor_rect.center = (self.game.DISPLAY_W/2 + self.offset * 2, self.game.DISPLAY_H/2.5 + self.curr_index * 40)

    def get_new_control(self):
        done = False
        while not done:
            self.game.display.fill((198,215,185))
            self.draw_text('Enter a New ' + self.game.CONTROL_LIST[self.curr_index] + ' Key', 20,
                           pygame.Color((0,0,0)), self.game.DISPLAY_W / 2,self.game.DISPLAY_H / 4)
            self.blit_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.playing = False
                    self.run_display = False
                    self.game.running = False
                    done = True
                elif event.type == pygame.KEYDOWN:
                    self.game.CONTROLS[self.game.CONTROL_LIST[self.curr_index]] = event.key
                    with open(path.join(self.game.options_dir, 'controls.json'), 'w') as file:
                        json.dump(self.game.CONTROLS, file)
                    self.game.reassign_controls()
                    done = True




class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        self.state = 'Continue'
        self.text_box = pygame.transform.scale(pygame.image.load(path.join(self.img_dir, 'pausebox.png')).convert(), (400,220))
        self.rect = self.text_box.get_rect()
        self.rect.center = (self.mid_w, self.mid_h)
        self.offset = -100
        self.contx, self.conty = self.mid_w, self.mid_h
        self.retx, self.rety = self.mid_w, self.mid_h + 40
        self.cursor_rect.center = (self.contx + self.offset, self.conty)

    def display_menu(self):
        #self.store_events()
        self.run_display = True
        self.game.START_KEY, self.game.BACK_KEY, self.game.DOWN_KEY, self.game.RUN_KEY = False, False, False, False
        self.state = 'Continue'
        #pygame.mixer.music.pause()
        #pygame.mixer.pause()
        while self.run_display:
            self.game.get_delta()
            self.game.get_events()
            self.check_inputs()
            self.game.display.blit(self.text_box, self.rect)
            self.draw_text("Pause", 20, pygame.Color((0,0,0)), self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 40)
            self.draw_text("Continue", 20, pygame.Color((0,0,0)), self.contx, self.conty)
            self.draw_text("Return to Menu", 20, pygame.Color((0,0,0)), self.retx, self.rety)
            self.draw_cursor()
            self.blit_screen()
        #pygame.mixer.music.unpause()



    def check_inputs(self):
        if self.game.BACK_KEY or self.game.RUN_KEY:
            self.run_display = False
            self.cursor_rect.center = (self.contx + self.offset, self.conty)
        elif self.game.START_KEY:
            self.cursor_rect.center = (self.contx + self.offset, self.conty)
            self.run_display = False
            if self.state == 'Return':
                self.game.menu = self.game.Main
                self.game.playing = False
                self.game.fade_screen()

        elif self.game.UP_KEY:
            if self.state == 'Return':
                self.state = 'Continue'
                self.cursor_rect.center = (self.contx + self.offset, self.conty)
        elif self.game.DOWN_KEY:
            if self.state == 'Continue':
                self.state = 'Return'
                self.cursor_rect.center = (self.retx + self.offset * 1.5 , self.rety)


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.credx, self.credy = self.mid_w, self.mid_h / 4

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.display.fill((225, 161, 142))
            self.draw_text("Credits", 20, pygame.Color((0,0,0)), self.credx, self.credy)
            self.draw_text("Created by Christian Duenas", 14, pygame.Color((0,0,0)), self.credx, self.mid_h * .5)
            self.draw_text("\"November\" Font by Tepid Monkey Fonts", 14, pygame.Color((0,0,0)), self.credx, self.mid_h + 30)
            self.draw_text("Spritework Assistance by Phoebe Ly", 14, pygame.Color((0, 0, 0)), self.credx,
                           self.mid_h + 100)
            self.blit_screen()
            self.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.JUMP_KEY or self.game.RUN_KEY:
                self.run_display = False
                self.game.menu = self.game.Main
            self.game.reset_keys()




