import pygame, os,json
from Assets.menus.menu import Menu
from Assets.util.file_handler import write_save

class LevelComplete(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.credx, self.credy = self.mid_w, self.mid_h / 4
        self.text_display = ""
        self.text = list("You got the bread!")
        self.last_update = pygame.time.get_ticks()
        self.text_displayed, self.done_counting, self.display_collect = False, False, False
        self.count = 0
        self.count_color = (255, 255, 255)
        self.background_update = 0
        self.R, self.G, self.B = 0,0,0
        self.continue_timer = 0
        self.draw_continue = True
        self.sleep_frames = []
        self.sleep_index, self.sleep_timer = 0,0
        for i in range(1,7):
            self.sleep_frames.append(pygame.transform.scale(
                self.game.duck_sheet.get_sprite('duck_sleep' + str(i) + '.png'), (152,152)))

    def display_menu(self):
        pygame.mixer.music.load(os.path.join(self.game.menu_music, "Safe Place.ogg"))
        pygame.mixer.music.play(loops=-1)
        self.run_display = True
        while self.run_display:
            self.game.get_delta()
            self.handle_background()
            self.game.display.fill((self.R,self.G,self.B))
            self.game.display.blit(self.sleep_frames[self.sleep_index], (self.credx - 78, self.game.DISPLAY_H * .5))
            if not self.text_displayed: self.update_text()
            self.draw_text(self.text_display, 20, pygame.Color((255, 255, 255)), self.credx, self.credy)
            if self.text_displayed: self.show_collectibles()
            if self.done_counting: self.draw_fruit()
            if self.display_collect:
                self.continue_text()
                if self.draw_continue:
                    self.draw_text('Press Start to Continue', 20, (255, 255, 255), self.credx, self.game.DISPLAY_H * .90)
            self.blit_screen()
            self.check_events()
            if (self.game.START_KEY or self.game.BACK_KEY or self.game.JUMP_KEY or self.game.RUN_KEY) and self.display_collect:
                self.run_display = False
                self.game.playing = True
            self.game.reset_keys()
        pygame.mixer.music.stop()
        self.reset_counts()
        self.write_data()

    def update_text(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 125:
            self.last_update = now
            if self.text:
                self.text_display += self.text.pop(0)
            else: self.text_displayed = True

    def continue_text(self):
        now = pygame.time.get_ticks()
        if now - self.continue_timer > 700:
            self.continue_timer = now
            self.draw_continue = not self.draw_continue


    def show_collectibles(self):
        if not self.done_counting:
            now = pygame.time.get_ticks()
            if now - self.last_update > 100:
                self.last_update = now
                if self.count < self.game.player.berry_count:
                    self.count += 1
                    self.game.sound_effects['berry_collect'].play()
                else: self.done_counting = True;
            if self.count == 30: self.count_color = (255, 223, 0)
        self.game.display.blit(self.game.berries_hud.image, (self.credx - 100 , self.credy + 85))
        self.draw_text(' x ' + str(self.count), 20, pygame.Color(self.count_color), self.credx , self.credy + 100)


    def draw_fruit(self):
        i = 0
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000:
            for sprite in self.game.hud.sprites[2:]:
                self.game.display.blit(sprite.image, (self.credx - 100 + i , self.credy + 165))
                i += 50
            self.display_collect = True


    def reset_counts(self):
        self.text_displayed, self.done_counting, self.display_collect = False, False, False
        self.count = 0
        self.count_color = (255, 255, 255)
        self.text_display = ""
        self.text = list("You got the bread!")

    def handle_sleep(self):
        now = pygame.time.get_ticks()
        if now - self.sleep_timer > 230:
            self.sleep_timer = now
            self.sleep_index = (self.sleep_index + 1) % len(self.sleep_frames)

    def handle_background(self):
        now = pygame.time.get_ticks()
        if now - self.background_update > 20:
            self.background_update = now
            self.R = min(self.R+1, 25)
            self.G = min(self.G + 1, 25)
            self.B = min(self.B + 1, 65)
        self.handle_sleep()

    def write_data(self):
        # Check how many berries were collected
        berry_max = False
        if self.game.player.berry_count > self.game.save_data["level"][str(self.game.levelnum - 1)]["berries"]:
            self.game.save_data["level"][str(self.game.levelnum - 1)]["berries"] = self.game.player.berry_count
            berry_max = True
        # Check for fruit collected
        for fruit in self.game.player.fruits:
            if not self.game.save_data["level"][str(self.game.levelnum - 1)]["items"][fruit]:
                self.game.save_data["level"][str(self.game.levelnum - 1)]["items"][fruit] = True
        # Check if level is complete
        if berry_max and len(self.game.player.fruits) > 2:
            self.game.save_data["level"][str(self.game.levelnum)]["complete"] = True
        # Unlock next level
        self.game.save_data["level"][str(self.game.levelnum)]["unlocked"] = True
        write_save(self.game.options_dir, self.game.save_data)
        with open(os.path.join(self.game.options_dir, "save.json"), 'r+') as file:
            self.save_data = json.load(file)

class GameOver(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game_over_text = self.font.render('Game Over', True, (255,255,255))
        self.gox, self.goy = self.mid_w -100, -40
        self.last_update, self.current_frame = 0,0
        self.duck_frames = []
        for i in range(1,9):
            self.duck_frames.append(self.game.duck_sheet.get_sprite('ghost_duck' + str(i) + '.png'))
        self.ghost_image = self.duck_frames[0]

    def display_menu(self):
        self.gox, self.goy = self.mid_w - 100, -40
        pygame.mixer.music.load(os.path.join(self.game.menu_music, "Game Over.ogg"))
        pygame.mixer.music.play(loops=1)
        self.run_display = True
        now, marker = pygame.time.get_ticks(), pygame.time.get_ticks()
        while self.run_display:
            now = pygame.time.get_ticks()
            self.game.get_delta()
            self.game.display.fill((0, 0, 0))
            self.handle_text()
            self.animate_ghost()
            self.blit_screen()
            self.check_events()
            if  now - marker > 7000:
                self.run_display = False
                self.game.playing = False
            self.game.reset_keys()
        self.game.menu = self.game.Main

    def handle_text(self):
        if self.goy < self.mid_h:
            self.goy += 1 * self.game.dt
        self.game.display.blit(self.game_over_text, (self.gox,self.goy))

    def animate_ghost(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 175:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.duck_frames)
            self.ghost_image = self.duck_frames[self.current_frame]
        self.game.display.blit(self.ghost_image, (self.game.DISPLAY_W * .65, self.game.DISPLAY_H * .60))


