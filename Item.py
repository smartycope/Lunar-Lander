from GlobalFuncs import *
from Config import *
import random

class Item:
    def __init__(self, imageFileName):
        self.locs = []
        self.image = loadImage(imageFileName)
        self.prevLoc = Pointf(0, 0)
        self.traveled = 0

    def generateMore(self, direction, winSize, gp):
        """ Generates more of the item when going off screen """

        # This is so that when you go slower, it doesn't run this function disproportionally more
        if abs(self.traveled) > ITEM_GENERATE_MORE_IGNORE_AMOUNT:
            if self.traveled > 0:
                self.traveled -= ITEM_GENERATE_MORE_IGNORE_AMOUNT
            else:
                self.traveled += ITEM_GENERATE_MORE_IGNORE_AMOUNT
                    
            # We want them to be spread out and randomized, but not THAT spread out and randomized.
            if direction == SCROLLING_RIGHT:
                prospectiveLoc = winSize[0] + FLATTNESS
            else:
                prospectiveLoc = -FLATTNESS

            return prospectiveLoc

    def draw(self, surface):
        for i in self.locs:
            surface.blit(self.image, i.datai())

    def update(self, lander, offset, whenCollectedValue):
        try:
            self.prevLoc = copy.deepcopy(self.locs[-1])
        except:
            pass

        mylist = [pygame.Rect(self.image.get_rect(center=i.datai())) for i in self.locs]
        collideIndex = lander.getRect(offset=offset).collidelist(mylist)

        if collideIndex != -1:
            self.locs.pop(collideIndex)
            return self.whenCollected(whenCollectedValue)

    def whenCollected(self, value):
        raise NotImplementedError

    def shift(self, delta):
        self.traveled += delta.x
        for i in self.locs:
            i += delta




class Coin(Item):
    def __init__(self):
        super().__init__('coin.png')

    def generateMore(self, direction, winSize, gp):
        prospectiveLoc = super().generateMore(direction, winSize, gp)

        if prospectiveLoc is not None and abs(abs(self.prevLoc.x) - abs(prospectiveLoc)) > MIN_COIN_SPAWN_DIST:
            spawnChance = COIN_SPAWN_CHANCE
            if abs(abs(self.prevLoc.x) - abs(prospectiveLoc)) > MAX_COIN_SPAWN_DIST:
                spawnChance = 1

            if random.randint(0, spawnChance) == 0:
                justAboveSurface = findClosestXPoint(Pointi(prospectiveLoc), gp).y
                self.locs.append(Pointf(prospectiveLoc, justAboveSurface - self.image.get_rect().height - ITEM_FLOAT_HEIGHT))

    def whenCollected(self, value):
        value.money += COIN_WORTH


class GasCan(Item):
    def __init__(self):
        super().__init__('gasCan.png')

    def generateMore(self, direction, winSize, gp):
        prospectiveLoc = super().generateMore(direction, winSize, gp)

        if prospectiveLoc is not None and abs(abs(self.prevLoc.x) - abs(prospectiveLoc)) > MIN_GAS_CAN_SPAWN_DIST:
            spawnChance = GAS_CAN_SPAWN_CHANCE
            if abs(abs(self.prevLoc.x) - abs(prospectiveLoc)) > MAX_GAS_CAN_SPAWN_DIST:
                spawnChance = 1

            if random.randint(0, spawnChance) == 0:
                justAboveSurface = findClosestXPoint(Pointi(prospectiveLoc), gp).y
                self.locs.append(Pointf(prospectiveLoc, justAboveSurface - self.image.get_rect().height - ITEM_FLOAT_HEIGHT))

    def whenCollected(self, value):
        value.refuel()
        

class SuperCoin(Item):
    def __init__(self):
        super().__init__('superCoin.png')

    def generateMore(self, direction, winSize, gp):
        prospectiveLoc = super().generateMore(direction, winSize, gp)

        if prospectiveLoc is not None and abs(abs(self.prevLoc.x) - abs(prospectiveLoc)) > MIN_SUPER_COIN_SPAWN_DIST:
            spawnChance = SUPER_COIN_SPAWN_CHANCE

            if random.randint(0, spawnChance) == 0:
                justAboveSurface = findClosestXPoint(Pointi(prospectiveLoc), gp).y
                self.locs.append(Pointf(prospectiveLoc, justAboveSurface - self.image.get_rect().height - ITEM_FLOAT_HEIGHT))

    def whenCollected(self, value):
        value.money += SUPER_COIN_WORTH