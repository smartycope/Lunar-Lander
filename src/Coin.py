from Item import *

class Coin(Item):
    def init(self):
        self.image = 'coin'
        self.clumpSpawnChance = 2
        self.clumpSpawnDist   = 40
        self.minSpawnDist = 250
        self.maxSpawnDist = 2000
        self.maxClumpSize = 12
        self.minClumpSize = 3

    def generateNext(self, direction, winSize, gp):
        if direction == SCROLLING_RIGHT:
            if self.prevLoc is None:
                self.prevLoc = Pointf(winSize[0] - 5, 0)
            # If the last coin is onscreen
            if self.prevLoc.x < winSize[0]:
                # How many coins in the current clump there are so far
                clumpCount = 0
                for i in reversed(range(len(self.locs))):
                    if closeEnough(self.locs[i].x, self.locs[i - 1].x + self.clumpSpawnDist, self.minSpawnDist - 2):
                        clumpCount += 1
                    else:
                        break
                
                # print(clumpCount)

                if (random.randint(0, self.clumpSpawnChance + clumpCount) != 0 or clumpCount < self.minClumpSize) and clumpCount < self.maxClumpSize:
                    # Create a new coin just above the surface a little bit further along
                    loc = self.prevLoc
                    loc.x += self.clumpSpawnDist
                    justAboveSurface = findClosestXPoint(loc, gp).y - self.image.get_rect().height - ITEM_FLOAT_HEIGHT
                    self.locs.append(Pointf(loc.x, justAboveSurface))
                # Don't clump
                else:
                    x = random.randint(self.minSpawnDist, self.maxSpawnDist) + self.prevLoc.x
                    y = findClosestXPoint(Pointi(x, 0), gp).y - self.image.get_rect().height - ITEM_FLOAT_HEIGHT
                    self.locs.append(Pointf(x, y))
        # This is pretty much a dupilcate of the code above, but reversed to it works going left instead
        else:
            if self.prevLoc is None:
                self.prevLoc = Pointf(5, 0)
            # If the last coin is onscreen
            if self.prevLoc.x > 0:
                # How many coins in the current clump there are so far
                clumpCount = 0
                for i in reversed(range(len(self.locs))):
                    if closeEnough(self.locs[i].x, self.locs[i - 1].x - self.clumpSpawnDist, self.minSpawnDist - 2):
                        clumpCount += 1
                    else:
                        break
                
                # print(clumpCount)

                if (random.randint(0, self.clumpSpawnChance + clumpCount) != 0 or clumpCount < self.minClumpSize) and clumpCount < self.maxClumpSize:
                    # Create a new coin just above the surface a little bit further along
                    loc = self.prevLoc
                    loc.x -= self.clumpSpawnDist
                    justAboveSurface = findClosestXPoint(loc, gp).y - self.image.get_rect().height - ITEM_FLOAT_HEIGHT
                    self.locs.append(Pointf(loc.x, justAboveSurface))
                # Don't clump
                else:
                    x = random.randint(-self.maxSpawnDist, -self.minSpawnDist) - self.prevLoc.x
                    y = findClosestXPoint(Pointi(x, 0), gp).y - self.image.get_rect().height - ITEM_FLOAT_HEIGHT
                    self.locs.append(Pointf(x, y))









        # # This is so that when you go slower, it doesn't run this function disproportionally more
        # if abs(self.traveled) > ITEM_GENERATE_MORE_IGNORE_AMOUNT:
        #     if self.traveled > 0:
        #         self.traveled -= ITEM_GENERATE_MORE_IGNORE_AMOUNT
        #     else:
        #         self.traveled += ITEM_GENERATE_MORE_IGNORE_AMOUNT
                    
        #     # We want them to be spread out and randomized, but not THAT spread out and randomized.
        #     if direction == SCROLLING_RIGHT:
        #         prospectiveLoc = winSize[0] + FLATTNESS
        #     else:
        #         prospectiveLoc = -FLATTNESS

        #     return prospectiveLoc

        # prospectiveLoc = super().generateMore(direction, winSize, gp)

        # if prospectiveLoc is not None and abs(abs(self.prevLoc.x) - abs(prospectiveLoc)) > self.minSpawnDist:
        #     spawnChance = COIN_SPAWN_CHANCE
        #     if abs(abs(self.prevLoc.x) - abs(prospectiveLoc)) > self.maxSpawnDist:
        #         spawnChance = 1

        #     if random.randint(0, spawnChance) == 0:
                
        #         self.locs.append(Pointf(prospectiveLoc, justAboveSurface - self.image.get_rect().height - ITEM_FLOAT_HEIGHT))
