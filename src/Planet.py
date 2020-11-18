import pygame.gfxdraw
# from Lander import Lander
from Text   import Text
from Scene  import *
from time   import sleep
from Item   import GasCan


class Planet(Scene):
    def init(self, **params):
        # super().__init__(surface)
        self.showMouse(False)
        self.setKeyRepeat(20, 20)

        self.dir += 'planets/planetTextures/'
        
        self.landerStartPoint = Pointf(self.getSize()[0] / 2, 0)
        self.lander = params['lander']
        self.lander.loc = self.landerStartPoint

        self.relativePoint = Pointf(0, 0)
        self.groundPoints = []
        self.generateGround()
        self.generateMoreGround(left=True)
        # self.money = Money() 
        self.fuelGuage = Text(f'Fuel: {int(self.lander.fuel)}', Pointf(20, 20))
        self.moneyText = Text(f'ByteCoin: {self.money}',   Pointf(20, 40))
        self.deathText = Text('You have Died!', Pointf((self.getSize()[0] / 2) - 20, 5), color=[200, 20, 20])
        self.explosionTime = 0
        self.paused = False
        self.pausedText = Text("PAUSED", Pointi(self.mainSurface.get_rect().center), size=50)
        self.checkPaused = True

        self.items = (GasCan(),)

        self.landerStartPoint.x -= self.items[0].image.get_rect().center[0]
        self.landerStartPoint.y += 150
        self.items[0].locs.append(self.landerStartPoint)
        self.cnt = 0

        self.menuParams['lander'] = self.lander
        

    def drawSurface(self):
        raise NotImplementedError


    def updateItems(self):
        pass


    def run(self, deltaTime):
        if not self.paused:
            self.updateItems()

            self.lander.update(self.gravity, self.getVisibleGroundPoints(), self.mainSurface, self.relativePoint)

            self.fuelGuage.updateText(f'Fuel: {int(self.lander.fuel)}')
            self.fuelGuage.draw(self.mainSurface)
            self.moneyText.updateText(f'ByteCoin: {self.money}')
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
                    self.switchMenu('DeathMenu')
                    self.lander.reset(self.landerStartPoint)

            tmp = self.updateScroll()
            if tmp:
                self.generateMoreGround()
                for i in self.items:
                    i.generateMore(tmp, self.getSize(), self.groundPoints)

            self.drawSurface()

            for i in self.items:
                i.draw(self.mainSurface)
        
        else:
            # When paused code
            self.pausedText.draw(self.mainSurface)


        # Code that runs every 1/3 second
        self.cnt += 1
        if self.cnt > 10:
            self.cnt = 0
            self.checkPaused = True

        return self._menu


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


    def drawGroundLines(self):
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
        raise NotImplementedError


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
        raise NotImplementedError

