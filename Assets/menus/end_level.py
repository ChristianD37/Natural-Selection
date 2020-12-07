import pygame, os
from Assets.menus.menu import Menu

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

    def display_menu(self):
        pygame.mixer.music.load(os.path.join(self.game.menu_music, "Safe Place.ogg"))
        pygame.mixer.music.play(loops=-1)
        self.run_display = True
        while self.run_display:
            self.game.get_delta()
            self.game.display.fill((0,0,0))
            if not self.text_displayed: self.update_text()
            self.draw_text(self.text_display, 20, pygame.Color((255, 255, 255)), self.credx, self.credy)
            if self.text_displayed: self.show_collectibles()
            if self.done_counting: self.draw_fruit()
            self.blit_screen()
            self.check_events()
            if (self.game.START_KEY or self.game.BACK_KEY) and self.display_collect:
                self.run_display = False
                self.game.playing = True
            self.game.reset_keys()
        pygame.mixer.music.stop()
        self.reset_counts()

    def update_text(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 125:
            self.last_update = now
            if self.text:
                self.text_display += self.text.pop(0)
            else: self.text_displayed = True

    def show_collectibles(self):
        if not self.done_counting:
            now = pygame.time.get_ticks()
            if now - self.last_update > 100:
                self.last_update = now
                if self.count < self.game.player.berry_count:
                    self.count += 1
                else: self.done_counting = True;''
            if self.count == 30: self.count_color = (255, 223, 0)
        self.game.display.blit(self.game.berries_hud.image, (self.credx - 100 , self.credy + 85))
        self.draw_text(' x ' + str(self.count), 20, pygame.Color(self.count_color), self.credx , self.credy + 100)


    def draw_fruit(self):
        i = 0
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000:
            for sprite in self.game.hud.sprites[2:]:
                self.game.display.blit(sprite.image, (self.credx - 100 + i , self.credy + 185))
                i += 50
            self.display_collect = True

    def reset_counts(self):
        self.text_displayed, self.done_counting, self.display_collect = False, False, False
        self.count = 0
        self.count_color = (255, 255, 255)
        self.text_display = ""
        self.text = list("You got the bread!")

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
