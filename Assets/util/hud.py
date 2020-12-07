class HUD_Item():
    def __init__(self, game, image, x, y):
        self.game = game
        self.image =  self.game.objects_sheet.get_sprite(image + '.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self):
        self.game.display.blit(self.image,self.rect)

class Lives_HUD(HUD_Item):
    def __init__(self, game, image, x, y):
        super(Lives_HUD, self).__init__(game, image, x, y)
        self.count_image = self.game.number_text[self.game.lives]

    def draw(self):
        self.game.display.blit(self.image, self.rect)
        self.game.display.blit(self.game.berry_x, (self.rect.x + self.rect.w, self.rect.y + self.rect.h / 4))
        self.game.display.blit(self.count_image, (self.rect.x + self.rect.w + 20, self.rect.y + self.rect.h / 4))

class Berries_HUD(HUD_Item):
    def __init__(self, game, image, x, y):
        super(Berries_HUD, self).__init__(game, image, x, y)
        self.prev_count = self.game.player.berry_count
        self.count_image = self.game.number_text[0]

    def update_count(self):
        if self.prev_count < self.game.player.berry_count:
            self.count_image = self.game.number_text[self.game.player.berry_count]
            self.prev_count = self.game.player.berry_count

    def draw(self):
        self.update_count()
        self.game.display.blit(self.image, self.rect)
        self.game.display.blit(self.game.berry_x, (self.rect.x + self.rect.w, self.rect.y + self.rect.h / 4))
        self.game.display.blit(self.count_image, (self.rect.x + self.rect.w + 20, self.rect.y + self.rect.h / 4))
