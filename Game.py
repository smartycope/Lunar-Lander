from MoonLander  import MoonLander
from Config import *
from GlobalFuncs import *
from DeathMenu import DeathMenu

class Game:
    def __init__(self, size = [None, None], title = 'Hello World!', args=None):

        self.args = args
        self.fps = FPS

        self.initPygame(size, title)        

        self.scenes = {
            'MoonLander': MoonLander, #(self.mainSurface),
            'DeathMenu':  DeathMenu #(self.mainSurface)
        }

        self.currentScene = self.scenes['MoonLander'](self.mainSurface)

        self.sceneStack = ['MoonLander']

    def run(self):
        while True:
            deltaTime = self.clock.tick(self.fps) / 1000.0
            # print(self.sceneStack)
            for event in pygame.event.get():
                # if event.type != pygame.MOUSEMOTION: print(event)
                self.currentScene.handleEvent(event)
                

            # self.currentScene = self.scenes[self.currentScene.run(deltaTime)]
            sceneCommand = self.currentScene.run(deltaTime)
            # print(sceneCommand)
            if sceneCommand == '':
                pass
            elif sceneCommand == 'prev':
                self.sceneStack.pop()
                switchToScene = self.sceneStack.pop()
                self.currentScene = self.scenes[switchToScene](self.mainSurface)
                self.sceneStack.append(switchToScene)
            else:
                self.sceneStack.append(sceneCommand)
                self.currentScene = self.scenes[sceneCommand](self.mainSurface)


            pygame.display.flip()
            pygame.display.update()
            if type(self.currentScene.background) is list or tuple:
                self.mainSurface.fill(self.currentScene.background)
            else:
                self.mainSurface = self.currentScene.background.copy()


    def initPygame(self, size, title):
        #* Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        # pygame.mouse.set_visible(False)
        tmp = pygame.display.Info(); self.screenSize = (tmp.current_w, tmp.current_h)
        # pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        pygame.display.set_caption(title)

        self.fullscreenWindowFlags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN | pygame.NOFRAME
        self.windowedWindowFlags   = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE

        if pygame.__version__ >= '2.0.0':
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.set_allow_screensaver(True)
            self.windowedWindowFlags = self.windowedWindowFlags | pygame.SCALED

        #* Set the icon
        # with open(DIR + 'data/' + self.settings['iconFile'], 'r') as icon:
        #     pygame.display.set_icon(pygame.image.load(icon))

        self.windowedSize = size
        if size[0] is None:
            self.windowedSize[0] = round(self.screenSize[0] / 1.5)
        if size[1] is None:
            self.windowedSize[1] = round(self.screenSize[1] / 1.5)

        if START_FULLSCREEN:
            self.mainSurface = pygame.display.set_mode(self.screenSize, self.fullscreenWindowFlags)
        else:
            self.mainSurface = pygame.display.set_mode(self.windowedSize, self.windowedWindowFlags)
        
        #* Get info about the graphics
        vidInfo = pygame.display.Info()
        if self.args.verbose:
            print('Backend video driver being used:', pygame.display.get_driver())
            print('The display is', 'not' if not vidInfo.hw else '', 'hardware accelerated')
            print('The display has', vidInfo.video_mem, 'MB of video memory')
            print('The current width and height of the window are:', (vidInfo.current_w, vidInfo.current_h))
            print('The width and height of the display is:', self.screenSize)


'''
# self.lander.thrusters['bottom'] = self.keysPressed['up']
        # self.lander.thrusters['left']   = self.keysPressed['left']
        # self.lander.thrusters['right']  = self.keysPressed['right']
        # self.lander.rotate(self.keysPressed['a'])
        # self.lander.rotate(not self.keysPressed['d'])
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit()

            if event.key == pygame.K_UP:
                self.keysPressed['up'] = True

            if event.key == pygame.K_DOWN:
                self.keysPressed['down'] = True

            if event.key == pygame.K_LEFT:
                self.keysPressed['left'] = True

            if event.key == pygame.K_RIGHT:
                self.keysPressed['right'] = True

            if event.unicode == 'f':
                self.keysPressed['f'] = True

            if event.unicode == 'r':
                self.keysPressed['r'] = True
                if self.lander.exploded:
                    self.relativePoint = Pointf(0, 0)
                    loc = Pointf(self.getSize()[0] / 2, self.getSize()[1] / 2) + self.relativePoint
                    self.lander.reset(loc)
                else:
                    pass
                    # self.lander.reset()

            if event.unicode == 'w':
                self.keysPressed['w'] = True

            if event.unicode == 's':
                self.keysPressed['s'] = True

            if event.unicode == 'a':
                self.keysPressed['a'] = True

            if event.unicode == 'd':
                self.keysPressed['d'] = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.keysPressed['up'] = False

            if event.key == pygame.K_DOWN:
                self.keysPressed['down'] = False

            if event.key == pygame.K_LEFT:
                self.keysPressed['left'] = False

            if event.key == pygame.K_RIGHT:
                self.keysPressed['right'] = False

            try:
                if event.unicode == 'f':
                    self.keysPressed['f'] = False

                if event.unicode == 'r':
                    self.keysPressed['r'] = False

                if event.unicode == 'w':
                    self.keysPressed['w'] = False

                if event.unicode == 's':
                    self.keysPressed['s'] = False

                if event.unicode == 'a':
                    self.keysPressed['a'] = False

                if event.unicode == 'd':
                    self.keysPressed['d'] = False
            except:
                pass

            # if event.key == pygame.K_UP:
            #     self.lander.thrusters['bottom'] = False

            # if event.key == pygame.K_LEFT:
            #     self.lander.thrusters['left'] = False

            # if event.key == pygame.K_RIGHT:
            #     self.lander.thrusters['right'] = False
'''