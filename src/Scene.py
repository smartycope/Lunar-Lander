from Config import *
from GlobalFuncs import *
import os, random, copy


class Scene:
    def __init__(self, surface, **params):
        self.mainSurface = surface
        self.updateMouse()
        self.fullscreen = False
        self.background = [20, 20, 20]
        self.backgroundBlitOffset = [0, 0]
        self.money = params['money']
        #* This is genius
        # print(type(self), '\t ', self.money)

        # This is the directory in which the assets are loaded from
        self.dir = ''

        self.center = Pointf(self.mainSurface.get_rect().center)

        # This determines what menu to switch to.
        # Fill it with the name of the class
        self._menu = ''
        self.menuParams = params

        self.init(**params)

    def loadAsset(self, name, scale=None, extension='png'):
        if scale is None:
            return loadAsset(self.dir, name, extension)
        else:
            return pygame.transform.scale(loadAsset(self.dir, name, extension), scale)

    def init(self, **params):
        pass

    def run(self):
        raise NotImplementedError
        return ''

    def switchMenu(self, menu, **passParams):
        self._menu = menu
        self.menuParams['money'] = self.money
        self.menuParams.update(passParams)
        # print(type(self), '\t ', self.money)
        # print('just before menu switch:', self.menuParams)

    def addMoney(self, amount):
        self.money += amount
        # self.menuParams['money'] = self.money

    def showMouse(self, show):
        pygame.mouse.set_visible(show)

    def setKeyRepeat(self, delay, interval):
        pygame.key.set_repeat(delay, interval)

    def getSize(self):
        return self.mainSurface.get_size()

    def updateMouse(self):
        self.mouseLoc = Pointf(pygame.mouse.get_pos())

    def handleEvent(self, event):
        pygame.event.pump()

        #* Exit the window
        if event.type == pygame.QUIT:
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
            
        #* Middle button pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.mouseMiddleButtonDown()

        #* Middle button released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.mouseMiddleButtonUp()
        
        #* Right mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.mouseRightButtonDown()

        #* Right mouse button released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.mouseRightButtonUp()

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


        # There's more, but I'm lazy
        if event.type in [pygame.USEREVENT, pygame.ACTIVEEVENT, 
                          pygame.QUIT, pygame.JOYAXISMOTION, 
                          pygame.JOYBALLMOTION, pygame.JOYBUTTONDOWN, 
                          pygame.JOYBUTTONUP, pygame.JOYHATMOTION, 
                          pygame.VIDEOEXPOSE, pygame.VIDEORESIZE]:
            self.handleOtherEvent(event)

    def mouseLeftButtonDown(self):
        pass

    def mouseLeftButtonUp(self):
        pass

    def mouseRightButtonDown(self):
        pass

    def mouseRightButtonUp(self):
        pass

    def mouseMiddleButtonDown(self):
        self.updateMouse()
        print(self.mouseLoc)

    def mouseMiddleButtonUp(self):
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

    def handleOtherEvent(self, event):
        pass

    def exit(self):
        pygame.quit()
        quit()

