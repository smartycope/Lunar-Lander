import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from Config import CENTER_ALIGN, LEFT_ALIGN

class Text:
    def __init__(self, text, pos, color=[200, 200, 200], font=None, size=24, lineSpacing=5, align=CENTER_ALIGN):
        pos = [pos[0], pos[1]]
        if font is None:
            self.font = pygame.font.Font(None, size)
        else:
            self.font = font

        self.pos = pos
        self.renderedLines = []
        self.color = color
        self.lineSpacing = lineSpacing

        self.__parseText(text)

        # self.pos = self.getRect().center

        if align == CENTER_ALIGN:
            size = self.getSize()
            self.pos = [-size[0] / 2 + self.pos[0], -size[1] / 2 + self.pos[1]]

    def getSize(self):
        return [max(self.renderedLines, key=lambda x: x.get_width()).get_width(),
                (self.renderedLines[0].get_height() * len(self.renderedLines)) + ((len(self.renderedLines) - 1) * self.lineSpacing)]

    def getRect(self):
        return pygame.Rect(self.pos, self.getSize())

    def draw(self, surface):
        for cnt, i in enumerate(self.renderedLines):
            surface.blit(i, [self.pos[0], self.pos[1] + (self.lineSpacing + self.renderedLines[0].get_height()) * cnt])

    def updateText(self, text):
        self.__parseText(text)

    def __parseText(self, text):
        self.renderedLines = []
        for i in text.split('\n'):
            self.renderedLines.append(self.font.render(i, True, self.color))


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