from GlobalFuncs import *
from Config import *
import random, copy

class Item:
    def __init__(self):
        self.locs = []
        self.prevLoc = Pointf(0, 0)
        self.traveled = 0
        self.dir = 'items/'

        self.init()

        self.image = self.loadAsset(self.image)

    def init(self):
        raise NotImplementedError

    def generateNext(self, direction, winSize, gp):
        raise NotImplementedError

    def loadAsset(self, name, extension='png'):
        return loadAsset(self.dir, name, extension)

    def draw(self, surface):
        for i in self.locs:
            surface.blit(self.image, i.datai())

    def update(self, lander, offset, whenCollectedFunc, *params):
        try:
            self.prevLoc = copy.deepcopy(self.locs[-1])
        except IndexError: 
            self.prevLoc = None

        mylist = [pygame.Rect(self.image.get_rect(center=i.datai())) for i in self.locs]
        collideIndex = lander.getRect(offset=offset).collidelist(mylist)

        if collideIndex != -1:
            self.locs.pop(collideIndex)
            return whenCollectedFunc(*params)

    def shift(self, delta):
        self.traveled += delta.x
        for i in self.locs:
            i += delta
