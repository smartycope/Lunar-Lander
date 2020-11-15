from Config import *
from GlobalFuncs import *
from Lander import Lander
from Text   import Text
from Item   import Coin, GasCan

import pygame_gui
import os, random, copy
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# import pygame
import pygame.gfxdraw

# This is so I can use money in a pass-by-reference manner
class Money: money = 0

class Scene:
    def __init__(self, surface):
        self.mainSurface = surface
        self.updateMouse()
        self.fullscreen = False
        self.backgroundColor = None

    def run(self, deltaTime):
        self.uiManager.update(deltaTime)
        self.uiManager.draw_ui(self.mainSurface)

    def getSize(self):
        return self.mainSurface.get_size()

    def updateMouse(self):
        self.mouseLoc = Pointf(pygame.mouse.get_pos())

    def handleEvent(self, event):
        pygame.event.pump()

        #* Exit the window
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.exit()

        #* Mouse moves
        if event.type == pygame.MOUSEMOTION:
            self.updateMouse()
            self.mouseMotion()

        #* If the left mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouseLeftButtonDown()

        #* If the left mouse button is released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouseLeftButtonUp()
            
        #* Right mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.mouseRightButtonDown()

        #* Right mouse button released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.mouseRightButtonDUp()

        #* If a file is dropped into the window
        if event.type == pygame.DROPFILE: #and event.file[-4:0] == '':
            self.fileDropped()

        #* If you scroll up
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.scrollUp()

        #* If you scroll down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.scrollDown()

        if event.type == pygame.KEYDOWN:
            self.keyDown(event)

        if event.type == pygame.KEYUP:
            self.keyUp(event)

    def mouseLeftButtonDown(self):
        pass

    def mouseLeftButtonUp(self):
        pass

    def mouseRightButtonDown(self):
        pass

    def mouseRightButtonUp(self):
        pass

    def mouseMotion(self):
        pass

    def fileDropped(self):
        pass

    def scrollUp(self):
        pass

    def scrollDown(self):
        pass

    def keyDown(self, event):
        if event.key == pygame.K_f:
            self.fullscreen = not self.fullscreen
        return pygame.key.name(event.key)

    def keyUp(self, event):
        return pygame.key.name(event.key)

    def exit(self):
        pygame.quit()
        quit()



class MoonLander(Scene):
    def __init__(self, surface):
        super().__init__(surface)
        self.backgroundColor = [10, 10, 10]
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
        # self.numGasCans = 3
        # self.gasImage = loadImage('gasCan.png')
        # self.coinImage = loadImage('coin.png')
        # self.gasCanLocs = [landerStartPoint]
        # self.coinLocs = []
        # self.prevCoinLoc = Pointf(0, 0)
        self.paused = False
        self.pausedText = Text("PAUSED", Pointi(self.mainSurface.get_rect().center), size=50)
        self.checkPaused = True
        self.items = (Coin(), GasCan())
        landerStartPoint.x -= self.items[1].image.get_rect().center[0]
        landerStartPoint.y += 150
        self.items[1].locs.append(landerStartPoint)
        

    def run(self, deltaTime):
        super().run(deltaTime)

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
                    self.lander.explode(self.mainSurface, initial=self.explosionTime < (EXPLODE_TIME / 5), offset=self.relativePoint)
                    self.explosionTime += 1
            else:
                self.explosionTime = 0

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
            self.lander.fuel = 5000

    
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



'''
# The class that the main Game class talks to, and that initializes all of the specific GUIs
class MenuManager:
    def __init__(self, rootWindowSurface):
        

        self.passDataToGame = dict(zip(menu, [None] * len(menu)))


    def handleInput(self, event, type=None):
        

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_WINDOW_CLOSE:
            return False
        else:
            return True

    def createWindow(self, type):
        # print(f'Creating {type.name}')
        if type == menu.REPEAT:
            self.repeatWindow   = Window([None, None], self.uiManager, 'Repeat Pattern' , '#repeat_window',   RepeatMenu,   Point(self.size) / 1.25)
            return self.repeatWindow
        if type == menu.OPTION:
            self.optionWindow   = Window([None, None], self.uiManager, 'Options'        , '#options_window',  OptionMenu,   (300, self.height / 1.05))
            return self.optionWindow
        # if type == menu.SAVE:
        #     # self.saveWindow     = Window([None, None], self.uiManager, 'Save Pattern'   , '#save_window',     SaveMenu,     (500, 400))
        #     self.saveWindow = SaveMenu(self.uiManager)
        #     return self.saveWindow
        # if type == menu.OPEN:
        #     self.openWindow     = Window([None, None], self.uiManager, 'Open Pattern'   , '#open_window',     OpenMenu,     (500, 400))
        #     return self.openWindow
        # if type == menu.EXPORT:
        #     self.exportWindow   = Window([None, None], self.uiManager, 'Export Pattern' , '#export_window',   ExportMenu,   (500, 400))
        #     return self.exportWindow
        if type == menu.CONTROLS:
            self.controlsWindow = Window([None, None], self.uiManager, 'Edit Controls'  , '#controls_window', ControlsMenu, (500, 400))
            return self.controlsWindow
        if type == menu.WELCOME:
            self.welcomeWindow  = Window([0, 0],       self.uiManager, 'Welcome!'       , '#welcome_window',  WelcomeMenu,   Point(self.size) - 10)
            return self.welcomeWindow
        if type == menu.TOOLBAR:
            self.toolbar = Toolbar(self.uiManager, self.toolbarPos.data(), self.toolbarSize)
            return self.toolbar

    def getWindow(self, type):
        if type == menu.OPTION:
            return self.optionWindow
        if type == menu.WELCOME:
            return self.welcomeWindow
        if type == menu.CONTROLS:
            return self.controlsWindow
        if type == menu.TOOLBAR:
            return self.toolbar
        if type == menu.REPEAT:
            return self.repeatWindow
        if type == menu.SAVE:
            return self.saveWindow
        if type == menu.OPEN:
            return self.openWindow
        if type == menu.EXPORT:
            return self.exportWindow

    def killWindow(self, type):
        # print(f'Killing {type.name}')
        if type == menu.OPTION:
            if self.optionWindow is not None:
                self.optionWindow.kill()
            self.optionWindow = None
        if type == menu.WELCOME:
            if self.welcomeWindow is not None:
                self.welcomeWindow.kill()
            self.welcomeWindow = None
        if type == menu.CONTROLS:
            if self.controlsWindow is not None:
                self.controlsWindow.kill()
            self.controlsWindow = None
        if type == menu.TOOLBAR:
            if self.toolbar is not None:
                self.toolbar.toolbar.kill()
            self.toolbar = None
        if type == menu.REPEAT:
            if self.repeatWindow is not None:
                self.repeatWindow.kill()
            self.repeatWindow = None
        if type == menu.SAVE:
            if self.saveWindow is not None:
                self.saveWindow.filePicker.element.kill()
            self.saveWindow = None
        if type == menu.OPEN:
            if self.openWindow is not None:
                self.openWindow.filePicker.element.kill()
            self.openWindow = None
        if type == menu.EXPORT:
            if self.exportWindow is not None:
                self.exportWindow.filePicker.element.kill()
            self.exportWindow = None

    def draw(self, deltaTime, activate, context):
        if self.getWindow(activate) is None:
            self.createWindow(activate)

        # Get Game to talk to the induvidual GUIs
        self.getWindow(activate).updateContextData(context)

        # Get the menu-based GUIs to talk to Game
        for m in [menu.WELCOME, menu.OPTION, menu.REPEAT, menu.CONTROLS]:
            if self.getWindow(m) is not None and self.getWindow(m).active:
                self.passDataToGame[m] = self.getWindow(m).menu.passDataBack()
            else:
                self.passDataToGame[m] = None

        # Get induvidual GUIs to talk to Game
        if activate in [menu.TOOLBAR, menu.OPEN, menu.SAVE, menu.EXPORT]:
            if self.getWindow(activate) is not None and self.getWindow(activate).active:
                self.passDataToGame[activate] = self.getWindow(activate).passDataBack()
            else:
                self.passDataToGame[activate] = None

        

        return self.passDataToGame
'''