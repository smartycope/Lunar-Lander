import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Text:
    def __init__(self, text, pos, color=[200, 200, 200], font=None, size=24):
        if font is None:
            self.font = pygame.font.Font(None, size)
        else:
            self.font = font

        self.text = text
        self.textSurface = self.font.render(self.text, True, pygame.Color(200, 200, 200))
        self.pos = pos
        
    def getSize(self):
        return self.textSurface.get_rect()

    def draw(self, surface, offset=[0, 0]):
        surface.blit(self.textSurface, (self.pos + offset).data())

    def updateText(self, text):
        self.text = text
        self.textSurface = self.font.render(self.text, True, pygame.Color(200, 200, 200))

