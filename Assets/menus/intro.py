import pygame, os
from Assets.menus.menu import Menu

class Intro(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.image = pygame.image.load(os.path.join(self.img_dir, 'intro_theme.png')).convert_alpha()
        self.egg_frames = []
        for i in range(1,6):
            self.egg_frames.append(self.game.egg_sheet.get_sprite("egg" + str(i) +".png"))
        self.current_frame, self.last_update = 0,0
        self.display_time = 5000
        self.text = self.font.render("Created by Christian Duenas", True, (255, 255, 255))
        self.text.set_alpha(0)
        self.cancel = False
        self.text_alpha = 0
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 3
        self.egg_rect = self.egg_frames[0].get_rect()
        self.egg_rect.midbottom = (self.game.DISPLAY_W / 2 , self.game.DISPLAY_H)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.get_delta()
            self.exit()
            self.animate()
            self.game.display.blit(self.image, (0, 0))
            self.game.display.blit(self.egg_frames[self.current_frame], self.egg_rect)
            self.game.display.blit(self.text, self.text_rect)
            self.blit_screen()
        if not self.cancel: self.game.fade_screen()

    def animate(self):
        self.text.set_alpha(min(self.text_alpha, 300))
        self.text_alpha += 2 * self.game.dt
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.egg_frames)

        if now > self.display_time:
            self.run_display = False

    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.playing = False
                self.game.running = False
                self.run_display = False
                self.cancel = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.playing = False
                    self.game.running = False
                    self.run_display = False
                    self.cancel = True
                else: self.run_display = False