import pygame.gfxdraw
from Lander import Lander
from Text   import Text
from Item   import Coin, GasCan
from Scene  import *
from time   import sleep


# This is so I can use money in a pass-by-reference manner
class Money: money = 0



class MoonLander(Scene):
    def __init__(self, surface):
        super().__init__(surface)
        self.showMouse(False)
        self.setKeyRepeat(20, 20)
        # self.menu = 'MoonLander'
        self.background = [10, 10, 10]
        landerStartPoint = Pointf(self.getSize()[0] / 2, 0)
        self.lander = Lander(copy.deepcopy(landerStartPoint))
        self.gravity = GRAVITY
        self.relativePoint = Pointf(0, 0)
        self.groundPoints = []
        self.generateGround()
        self.generateMoreGround(left=True)
        self.money = Money() 
        self.fuelGuage = Text(f'Fuel: {int(self.lander.fuel)}', Pointf(20, 20))
        self.moneyText = Text(f'ByteCoin: {self.money.money}',   Pointf(20, 40))
        self.deathText = Text('You have Died!', Pointf((self.getSize()[0] / 2) - 20, 5), color=[200, 20, 20])
        self.moonTexture = loadImage('moonSurface.png')
        self.explosionTime = 0
        self.paused = False
        self.pausedText = Text("PAUSED", Pointi(self.mainSurface.get_rect().center), size=50)
        self.checkPaused = True
        self.items = (Coin(), GasCan())
        landerStartPoint.x -= self.items[1].image.get_rect().center[0]
        landerStartPoint.y += 150
        self.items[1].locs.append(landerStartPoint)
        

    def run(self, deltaTime):
        cnt = 0
        if not self.paused:
            self.items[0].update(self.lander, self.relativePoint, self.money)
            self.items[1].update(self.lander, self.relativePoint, self.lander)

            self.lander.update(self.gravity, self.getVisibleGroundPoints(), self.mainSurface, self.relativePoint)

            self.fuelGuage.updateText(f'Fuel: {int(self.lander.fuel)}')
            self.fuelGuage.draw(self.mainSurface)
            self.moneyText.updateText(f'ByteCoin: {self.money.money}')
            self.moneyText.draw(self.mainSurface)

            if self.lander.exploded:
                self.deathText.draw(self.mainSurface)
                if self.explosionTime <= EXPLODE_TIME:
                    self.lander.explode(self.mainSurface, initial=self.explosionTime < (EXPLODE_TIME / 4), offset=self.relativePoint)
                    self.explosionTime += 1
            else:
                self.explosionTime = 0

            # If we're done exploding
            if self.lander.exploded and self.explosionTime >= EXPLODE_TIME:
                self.explosionTime += 1
                if self.explosionTime >= EXPLODE_TIME + DEATH_DELAY_TIME:
                    self.menu = 'DeathMenu'

            tmp = self.updateScroll()
            if tmp:
                self.generateMoreGround()
                for i in self.items:
                    i.generateMore(tmp, self.getSize(), self.groundPoints)

            self.drawMoon()

            for i in self.items:
                i.draw(self.mainSurface)
        
        else:
            # When paused code
            self.pausedText.draw(self.mainSurface)


        # Code that runs every 1/3 second
        cnt += 1
        if cnt > 10:
            cnt = 0
            self.checkPaused = True

        return self.menu


    def drawMoon(self, dots=False, lines=False, filled=False, texture=True):
        if dots:
            drawAllGroundPoints(self.mainSurface, self.groundPoints)
        if lines:
            self.drawGround1()
        if filled:
            self.fillMoonWithCheese()
        if texture:
            self.fillMoonWithCottageCheese()


    def keyDown(self, event):
        key = super().keyDown(event)

        if key == 'up':
            self.lander.thrusters['bottom'] = True

        if key == 'down':
            pass

        if key == 'left':
            self.lander.thrusters['left'] = True

        if key == 'right':
            self.lander.thrusters['right'] = True

        if key == 'r':
            if self.lander.exploded:
                self.relativePoint = Pointf(0, 0)
                loc = Pointf(self.getSize()[0] / 2, self.getSize()[1] / 2) + self.relativePoint
                self.lander.reset(loc)
            else:
                pass
                # self.lander.reset()

        if key == 'a':
            self.lander.rotate(True)

        if key == 'd':
            self.lander.rotate(False)

        if key == 'p':
            if self.checkPaused:
                self.paused = not self.paused
                self.checkPaused = False

        if key == 'o':
            self.lander.fuel = 1000
    
        if key == 'escape':
            self.exit()


    def keyUp(self, event):
        key = super().keyUp(event)

        if key == 'up':
            self.lander.thrusters['bottom'] = False

        if key == 'left':
            self.lander.thrusters['left'] = False

        if key == 'right':
            self.lander.thrusters['right'] = False


    def drawGround1(self):
        for i in range(len(self.groundPoints) - 1):
            pygame.draw.aaline(self.mainSurface, GROUND_COLOR, (self.groundPoints[i] + self.relativePoint).data(), (self.groundPoints[i + 1] + self.relativePoint).data())


    def getVisibleGroundPoints(self):
        returnMe = []
        # for i in self.groundPoints:
        #     # I don't know why I'm multiplying it by 16, but it makes it work.
        #     # if i.x > GROUND_X_WIDTH * 6 and i.x < self.getSize()[0] - self.relativePoint.x + (GROUND_X_WIDTH * 6) + 2:
        #     #     returnMe.append(i)
        #     if i.x > self.relativePoint.x - GROUND_X_WIDTH and i.x < 
        # return returnMe

        # screenRect = pygame.Rect(self.relativePoint.data(), (Pointf(self.getSize()) + self.relativePoint).data())
        screenRect = pygame.Rect([0, 0], self.getSize())
        screenRect.inflate_ip((GROUND_X_WIDTH + FLATTNESS) * 2, 0)

        for p in self.groundPoints:
            if screenRect.collidepoint(p.data()):
                returnMe.append(p)

        # print(f'visible ground points: {len(returnMe)}\t total ground points: {len(self.groundPoints)}')

        return returnMe


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


    def updateScroll(self):
        dontMoveArea = pygame.Rect(SCROLL_WIDTH, 0, self.getSize()[0] - (SCROLL_WIDTH * 2), self.getSize()[1])

        prevRelPoint = copy.deepcopy(self.relativePoint)
        if not dontMoveArea.collidepoint((self.lander.loc + self.relativePoint).data()):
            # print('adjusting relative point')
            if self.lander.loc.x > self.getSize()[0] / 2:
                self.relativePoint.x -= self.lander.momentum['horz'] / MOMENTUM_SENSITIVITY
                direction = SCROLLING_RIGHT
            else:
                self.relativePoint.x -= self.lander.momentum['horz'] / MOMENTUM_SENSITIVITY
                direction = SCROLLING_LEFT

            # self.relativePoint.x = int(self.relativePoint.x)
            # self.relativePoint.y = int(self.relativePoint.y)

            for i in self.groundPoints:
                i += self.relativePoint - prevRelPoint
            for i in self.items:
                i.shift(self.relativePoint - prevRelPoint)

            # print('relative point:', self.relativePoint)

            return direction

        return NOT_SCROLLING


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
