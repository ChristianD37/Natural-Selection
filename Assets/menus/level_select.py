from Assets.menus.menu import Menu
import json, os, pygame

class Level_Select(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.index = 0
        self.offset = 80
        self.level_data = {}
        # Load current save file
        self.level_data = self.game.save_data["level"]
        self.cursor_rect.center = (self.game.DISPLAY_W *.25, self.game.DISPLAY_H * .25 )
        self.stats_textx,self.stats_texty = self.game.DISPLAY_W *.6, self.game.DISPLAY_H * .75
        self.berry_image = self.game.objects_sheet.get_sprite("blueberry.png")
        self.load_backgrounds()


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.get_delta()
            self.display_background()
            self.draw_levels()
            self.draw_stats()
            self.draw_cursor()
            self.blit_screen()
            self.check_events()
            self.move_cursor()
            self.game.reset_keys()

    def draw_levels(self):
        self.draw_text("Level Select", 30, (255,255,255), self.game.DISPLAY_W * .5, self.game.DISPLAY_H * .10)
        for i in range(0,len(self.level_data)):
            if self.level_data[str(i + 1)]["unlocked"]:
                self.draw_text(self.level_data[str(i + 1)]["level_name"], 20, (255,255,255), self.game.DISPLAY_W * .25,
                               self.game.DISPLAY_H * .25 + i * 50)
            else:
                self.draw_text("?????", 20, (255,255,255), self.game.DISPLAY_W * .25, self.game.DISPLAY_H *.25 + i * 50)

    def draw_stats(self):
        self.game.display.blit(self.berry_image,(self.stats_textx - 40,self.stats_texty))
        self.draw_text("x ",20,(255,255,255), self.stats_textx + 20,self.stats_texty + 15)
        self.draw_text(str(self.level_data[str(self.index + 1)]["berries"]), 20, (255,255,255),
                       self.stats_textx + 45, self.stats_texty + 15)
        temp_offset = 100
        for item in self.level_data[str(self.index+1)]["items"]:
            # Display Fruit if collected
            if self.level_data[str(self.index+1)]["items"][item]:
                self.game.display.blit(
                    self.game.objects_sheet.get_sprite(item + ".png"),
                    (self.stats_textx + temp_offset, self.stats_texty ))
            # Show grayed image if not yet collected
            else:
                self.game.display.blit(
                    self.game.objects_sheet.get_sprite(item + "_gray.png"),
                    (self.stats_textx + temp_offset, self.stats_texty ))
            temp_offset += 50
        self.animate_star()

    def draw_cursor(self):
        self.game.display.blit(self.cursor_img, (self.cursor_rect.x - self.offset, self.cursor_rect.y) )

    def move_cursor(self):
        if (self.game.START_KEY or self.game.JUMP_KEY) and self.level_data[str(self.index+1)]["unlocked"]:
            self.run_display = False
            self.game.levelnum = self.index + 1
            self.game.playing = True
        if self.game.BACK_KEY or self.game.RUN_KEY:
            self.run_display = False
            self.game.menu = self.game.Main
        if self.game.DOWN_KEY:  # Move the Cursor Down
            self.index = (self.index + 1) % len(self.level_data)
        if self.game.UP_KEY:  # Move the Cursor Down
            self.index = abs((self.index - 1) % len(self.level_data))
        self.cursor_rect.center = (self.game.DISPLAY_W *.15, self.game.DISPLAY_H *.25 + (self.index * 50))

    def display_background(self):
        color = (198,215,185)
        #self.game.display.fill((136, 0, 0)) red
        #self.game.display.fill((52, 107, 49)) chalk
        self.game.display.fill((94, 141, 90))
        if self.level_data[str(self.index + 1)]["unlocked"]:
            self.game.display.blit(self.backgrounds[self.index], (self.game.DISPLAY_W - 500,110))
        else:
            self.game.display.blit(self.blank_background, (self.game.DISPLAY_W - 500,110))

    def animate_star(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.star_frames)
        if self.level_data[str(self.index + 1)]["complete"]:
            self.game.display.blit(self.star_frames[self.current_frame], (self.stats_textx +100, self.stats_texty + 50))

    def load_backgrounds(self):
        self.blank_background = pygame.image.load(os.path.join(self.img_dir, 'blank.png')).convert_alpha()
        self.backgrounds = []
        self.backgrounds.append(
            pygame.image.load(os.path.join(self.img_dir, 'chaparral_background.png')).convert_alpha())
        self.backgrounds.append(self.backgrounds[-1])
        self.backgrounds.append(
            pygame.image.load(os.path.join(self.img_dir, 'beach_background.png')).convert_alpha())
        self.backgrounds.append(self.backgrounds[-1])
        self.star_frames = []
        self.current_frame, self.last_update = 0,0
        for i in range(1,12):
            self.star_frames.append(self.game.objects_sheet.get_sprite("star" + str(i) + ".png"))

