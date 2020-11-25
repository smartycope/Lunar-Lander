from Item import *

CLUMP_SPAWN_CHANCE = 5
CLUMP_SPAWN_DIST   = 40

class GasCan(Item):
    def init(self):
        self.image = 'gasCan'
        self.minSpawnDist = 2000
        self.maxSpawnDist = 5000

    def generateNext(self, direction, winSize, gp):
        if direction == SCROLLING_RIGHT:
            if self.prevLoc is None:
                self.prevLoc = Pointf(winSize[0] - 5, 0)
            # If the last coin is onscreen
            if self.prevLoc.x < winSize[0]:
                x = random.randint(self.minSpawnDist, self.maxSpawnDist) + self.prevLoc.x
                y = findClosestXPoint(Pointi(x, 0), gp).y - self.image.get_rect().height - ITEM_FLOAT_HEIGHT
                self.locs.append(Pointf(x, y))
        else:
            if self.prevLoc is None:
                self.prevLoc = Pointf(5, 0)
            # If the last coin is onscreen
            if self.prevLoc.x > 0:
                x = random.randint(-self.maxSpawnDist, -self.minSpawnDist) - self.prevLoc.x
                y = findClosestXPoint(Pointi(x, 0), gp).y - self.image.get_rect().height - ITEM_FLOAT_HEIGHT
                self.locs.append(Pointf(x, y))