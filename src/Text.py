import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Text:
    def __init__(self, text, pos, color=[200, 200, 200], font=None, size=24):
        pos = [pos[0], pos[1]]
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
        surface.blit(self.textSurface, [self.pos[0] + offset[0], self.pos[1] + offset[1]])

    def updateText(self, text):
        self.text = text
        self.textSurface = self.font.render(self.text, True, pygame.Color(200, 200, 200))


'''
from pygame import freetype

class Text:
    def __init__(self, text, pos, color=[200, 200, 200, 255], font=None, size=24):
        if not pygame.freetype.get_init():
            pygame.freetype.init()
            
        if font is None:
            self.font = pygame.freetype.Font(None, size=size)
        else:
            self.font = font

        self.text = text
        self.color = pygame.Color(*color)
        self.textSurface = self.font.render(self.text, fgcolor=self.color)[0]
        self.pos = pos
        
    def getSize(self):
        return self.textSurface.get_rect()

    def draw(self, surface, offset=[0, 0]):
        surface.blit(self.textSurface, (self.pos + offset).datai())

    def updateText(self, text):
        self.text = text
        self.textSurface = self.font.render(self.text, True, self.color)
'''