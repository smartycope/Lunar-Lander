from Item import Coin, GasCan
from Planet import *

# This is so I can use money in a pass-by-reference manner
class Money: money = 0

class Moon(Planet):
    def init(self, **params):
        super().init(**params)
        self.background = [10, 10, 10]
        # landerStartPoint = Pointf(self.getSize()[0] / 2, 0)
        # self.lander = Lander(copy.deepcopy(landerStartPoint))
        self.gravity = 1.6
        self.moonTexture = self.loadAsset('moonTexture')
        self.items += (Coin(),)

        # self.menuParams += (self.money,)
        
    def updateItems(self):
        self.items[0].update(self.lander, self.relativePoint, self.lander.refuel)
        self.items[1].update(self.lander, self.relativePoint, self.addMoney, COIN_VALUE)


    def drawSurface(self, dots=False, lines=False, filled=False, texture=True):
        if dots:
            drawAllGroundPoints(self.mainSurface, self.groundPoints)
        if lines:
            self.drawGround1()
        if filled:
            self.fillMoonWithCheese()
        if texture:
            self.fillMoonWithCottageCheese()


    def drawGroundLines(self):
        for i in range(len(self.groundPoints) - 1):
            pygame.draw.aaline(self.mainSurface, GROUND_COLOR, (self.groundPoints[i] + self.relativePoint).data(), (self.groundPoints[i + 1] + self.relativePoint).data())


    def generateGround(self):
        adjY = self.getSize()[1] - GROUND_START_Y
        groundWidth = [GROUND_X_WIDTH, 100 - GROUND_X_WIDTH]
        lastPoint = Pointf(0, random.randint(*groundWidth) + adjY)
        self.groundPoints.append(lastPoint)

        while lastPoint.x < self.getSize()[1] * 2:
            newPoint = Pointf(random.randint(*groundWidth) + lastPoint.x,
                              random.randint(*(Pointi(groundWidth) / 2).data()) + lastPoint.y - SLOPE)
            self.groundPoints.append(newPoint)
            lastPoint = copy.deepcopy(newPoint)

        firstPoint = self.groundPoints[0]
        
        while firstPoint.x > -self.relativePoint.x:
            newPoint = Pointf(-random.randint(GROUND_X_WIDTH, FLATTNESS - GROUND_X_WIDTH) + firstPoint.x, 
                                random.randint(*(Pointf(GROUND_X_WIDTH, FLATTNESS - GROUND_X_WIDTH) / 2).data()) + firstPoint.y - SLOPE)
            self.groundPoints.insert(0, newPoint)
            firstPoint = copy.deepcopy(newPoint)


    def generateMoreGround(self, left=False, right=False):
        #* If the lander is going right, generate more points in that direction
        if self.lander.loc.x - self.relativePoint.x > self.getSize()[0] - SCROLL_WIDTH or right:
            lastPoint = self.groundPoints[-1]

            # I don't know why this is negative as of yet
            while lastPoint.x < self.getSize()[0] - self.relativePoint.x:
                newPoint = Pointf(random.randint(GROUND_X_WIDTH, FLATTNESS - GROUND_X_WIDTH) + lastPoint.x, 
                                 random.randint(*(Pointi(GROUND_X_WIDTH, FLATTNESS - GROUND_X_WIDTH) / 2).data()) + lastPoint.y - SLOPE)

                if newPoint.y > self.getSize()[1]:
                    newPoint.y = self.getSize()[1]
                if newPoint.y < self.getSize()[1] - GROUND_START_Y:
                    newPoint.y = self.getSize()[1] - GROUND_START_Y

                self.groundPoints.append(newPoint)
                lastPoint = copy.deepcopy(newPoint)


        #* The lander is going left, generate more points in that direction
        if self.lander.loc.x < SCROLL_WIDTH or left:
            firstPoint = self.groundPoints[0]

            # I don't know why this is negative as of yet
            while firstPoint.x > -self.relativePoint.x:
                newPoint = Pointf(-random.randint(GROUND_X_WIDTH, FLATTNESS - GROUND_X_WIDTH) + firstPoint.x, 
                                  random.randint(*(Pointi(GROUND_X_WIDTH, FLATTNESS - GROUND_X_WIDTH) / 2).data()) + firstPoint.y - SLOPE)

                if newPoint.y > self.getSize()[1]:
                    newPoint.y = self.getSize()[1]
                if newPoint.y < self.getSize()[1] - GROUND_START_Y:
                    newPoint.y = self.getSize()[1] - GROUND_START_Y

                self.groundPoints.insert(0, newPoint)
                firstPoint = copy.deepcopy(newPoint)


    def fillMoonWithCheese(self):
        tmpPoints = [[i.x, i.y + 1] for i in getGroundPoints(self.groundPoints)]
        tmpPoints.append([self.getSize()[0], self.getSize()[1]])
        tmpPoints.append([0, self.getSize()[1]])
        pygame.gfxdraw.filled_polygon(self.mainSurface, tmpPoints, GROUND_COLOR)


    def fillMoonWithCottageCheese(self):
        # Make an array full of [x, y] points corresponding to the gound points
        tmpPoints = [[int(i.x), int(i.y + 1)] for i in getGroundPoints(self.getVisibleGroundPoints())]
        # Add the bottom right corner
        tmpPoints.append([self.getSize()[0], self.getSize()[1]])
        # Add the bottom left corner
        tmpPoints.append([0, self.getSize()[1]])
        # Draw a textured polygon using those points
        pygame.gfxdraw.textured_polygon(self.mainSurface, tmpPoints, self.moonTexture, *self.relativePoint.datai())
