import pygame as pg

pg.init()


class Button:
    def __init__(self, screen, text):
        self.font = pg.font.SysFont(None, 50)
        self.text = text
        self.rect = self.font.render(text, False, (0, 0, 0)).get_rect()
        self.screen = screen

    def draw(self, x, y, color):
        self.rect.centerx = x
        self.rect.centery = y
        self.screen.blit(self.font.render(self.text, False, color), self.rect)

    def is_touching_mouse(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            return True
