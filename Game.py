# from Point  import Point
from Lander import Lander
from Text   import Text
from GlobalFuncs import *

import os, random, copy
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# import pygame
import pygame.gfxdraw

DIR = os.path.dirname(__file__) + '/../'
KEY_REPEAT_DELAY = 20
KEY_REPEAT_INTERVAL = 20
FPS = 30
START_FULLSCREEN = False
GRAVITY = 1.6 # Moon's gravity
# GRAVITY = 1
GROUND_COLOR = [200, 200, 200]
GROUND_START_Y = 200
EXPLODE_TIME = 35
STEEPNESS = 1
ROTATION_SPEED = 1
SCROLL_WIDTH = 200
SLOPE = 24

class Game:
    def __init__(self, size = [None, None], title = 'Hello World!', args=None):

        self.args = args
        self.backgroundColor = [10, 10, 10]
        self.fps = FPS

        #* Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        tmp = pygame.display.Info(); self.screenSize = (tmp.current_w, tmp.current_h)
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
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


        self.lander = Lander(Point(self.getSize()[0] / 2, 0))
        self.gravity = GRAVITY
        self.groundPoints = []
        self.generateGround1()
        self.fuelGuage = Text(f'Fuel: {self.lander.fuel}', Point(20, 20))
        self.deathText = Text('You have Died!', Point((self.getSize()[0] / 2) - 20, 5), color=[200, 20, 20])
        self.moonTexture = loadImage('moonSurface.png')
        self.explosionTime = 0
        self.relativePoint = Point(0, 0)


    def getSize(self):
        #* This won't work until pygame 2.0.0
        # return pygame.display.get_window_size()
        tmp = pygame.display.Info()
        return [tmp.current_w, tmp.current_h]


    def updateMouse(self):
        self.mouseLoc = Point(*pygame.mouse.get_pos())


    def run(self):
        run = True
        cnt = 0
        fullscreen = False
        thrusters = {
            'right':  False,
            'left':   False,
            'bottom': False
        }

        while run:
            deltaTime = self.clock.tick(self.fps) / 1000.0
            
            for event in pygame.event.get():
                #* Exit the window
                if event.type == pygame.QUIT:
                    self.exit()

                #* Mouse moves
                if event.type == pygame.MOUSEMOTION:
                    self.updateMouse()

                #* If the left mouse button is released
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pass
                    
                #* Right mouse button clicked or c is pressed
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    pass

                #* If a file is dropped into the window
                if event.type == pygame.DROPFILE and event.file[-4:0] == '.gdl':
                    pass

                #* If you scroll up
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    pass

                #* If you scroll down
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    pass

                #? Keys here
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit()
                    if event.key == pygame.K_UP:
                        thrusters['bottom'] = True
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_LEFT:
                        thrusters['left'] = True
                    if event.key == pygame.K_RIGHT:
                        thrusters['right'] = True
                    if event.unicode == 'f':
                        pass
                    if event.unicode == 'r':
                        self.relativePoint = Point(0, 0)
                        if self.lander.exploded:
                            loc = Point(self.getSize()[0] / 2, self.getSize()[1] / 2) + self.relativePoint
                            self.lander.reset(loc)
                        else:
                            self.lander.reset()
                    # if event.unicode == 'w':
                    #     self.lander
                    # if event.unicode == 's':
                    #     self.lander
                    if event.unicode == 'a':
                        self.lander.rotation += ROTATION_SPEED
                    if event.unicode == 'd':
                        self.lander.rotation -= ROTATION_SPEED


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        thrusters['bottom'] = False
                    if event.key == pygame.K_LEFT:
                        thrusters['left'] = False
                    if event.key == pygame.K_RIGHT:
                        thrusters['right'] = False
                    
                    
            #* Draw stuff here
            # self.fillMoonWithCottageCheese()
            self.update(thrusters)
            self.generateMoreGround()            
            # self.drawGround1()
            # drawAllGroundPoints(self.mainSurface, self.groundPoints)
            self.fillMoonWithCottageCheese()


            # Code that runs every 1/3 second
            cnt += 1
            if cnt > 10:
                cnt = 0

                # self.groundPoints = self.getVisibleGroundPoints()
                # for i in self.groundPoints:
                #     if i.x < -2 or i.x > self.getSize()[0] + 2 - self.relativePoint.x:
                #         self.groundPoints.remove(i)


            print(len(self.groundPoints))
            # print(len(self.getVisibleGroundPoints()))

            pygame.display.flip()
            pygame.display.update()
            self.mainSurface.fill(self.backgroundColor)

    
    def update(self, thrusters):
        # self.lander.update(self.gravity, thrusters, self.getVisibleGroundPoints(), self.mainSurface, self.relativePoint)
        self.lander.update(self.gravity, thrusters, self.groundPoints, self.mainSurface, self.relativePoint)
        self.fuelGuage.updateText(f'Fuel: {self.lander.fuel}')
        self.fuelGuage.draw(self.mainSurface, offset=self.relativePoint)
        if self.lander.exploded:
            self.deathText.draw(self.mainSurface)
            if self.explosionTime <= EXPLODE_TIME:
                self.lander.explode(self.mainSurface, initial=self.explosionTime < (EXPLODE_TIME / 5), offset=self.relativePoint)
                self.explosionTime += 1
        else:
            self.explosionTime = 0


    def drawGround1(self):
        for i in range(len(self.groundPoints) - 1):
            pygame.draw.aaline(self.mainSurface, GROUND_COLOR, (self.groundPoints[i] + self.relativePoint).data(), (self.groundPoints[i + 1] + self.relativePoint).data())


    def getVisibleGroundPoints(self):
        returnMe = []
        for i in self.groundPoints:
            # I don't know why I'm multiplying it by 16, but it makes it work.
            if i.x > STEEPNESS * 6 and i.x < self.getSize()[0] - self.relativePoint.x + (STEEPNESS * 6) + 2:
                returnMe.append(i)
        return returnMe
        # return self.groundPoints



    #! Depricated
    def drawGround2(self):
        for i in range(len(self.groundPoints)):
            pygame.gfxdraw.pixel(self.mainSurface, i, int(self.groundPoints[i]), GROUND_COLOR)


    def generateGround1(self):
        adjY = self.getSize()[1] - GROUND_START_Y
        groundWidth = [STEEPNESS, 100 - STEEPNESS]
        lastPoint = Point(0, random.randint(*groundWidth) + adjY)
        self.groundPoints.append(lastPoint)

        while lastPoint.x < self.getSize()[1] * 2:
            newPoint = Point(random.randint(*groundWidth) + lastPoint.x, 
                             random.randint(*(Point(groundWidth) / 2).data()) + lastPoint.y - SLOPE)
            self.groundPoints.append(newPoint)
            lastPoint = copy.deepcopy(newPoint)



    # TODO add going right
    def generateMoreGround(self):
        # If the lander is going left
        if self.lander.loc.x - self.relativePoint.x > self.getSize()[0] - SCROLL_WIDTH:
            # adjY = self.getSize()[1] - GROUND_START_Y
            groundWidth = [STEEPNESS, 100 - STEEPNESS]
            lastPoint = self.groundPoints[-1]

            prevPoint = copy.deepcopy(self.relativePoint)
            self.relativePoint.x = int((self.getSize()[0] - SCROLL_WIDTH) - self.lander.loc.x)

            if prevPoint != self.relativePoint:
                for i in self.groundPoints:
                    i += self.relativePoint - prevPoint
            # self.groundPoints.append(lastPoint)


            # I don't know why this is negative as of yet
            while lastPoint.x < self.getSize()[0] - self.relativePoint.x:
                # print('generating new terrain!')
                newPoint = Point(random.randint(*groundWidth) + lastPoint.x, 
                                 random.randint(*(Point(groundWidth) / 2).data()) + lastPoint.y - SLOPE)
                if newPoint.y > self.getSize()[1]:
                    newPoint.y = self.getSize()[1]
                self.groundPoints.append(newPoint)
                lastPoint = copy.deepcopy(newPoint)

            # self.mainSurface.scroll(dx=int(self.lander.loc.x - self.getSize()[0] - SCROLL_WIDTH))

            
            
        # The lander is going right
        if self.lander.loc.x < SCROLL_WIDTH:
            pass



    def fillMoonWithCheese(self):
        tmpPoints = [[i.x, i.y + 1] for i in getGroundPoints(self.groundPoints)]
        tmpPoints.append([self.getSize()[0], self.getSize()[1]])
        tmpPoints.append([0, self.getSize()[1]])
        pygame.gfxdraw.filled_polygon(self.mainSurface, tmpPoints, GROUND_COLOR)


    def fillMoonWithCottageCheese(self):
        # Make an array full of [x, y] points corresponding to the gound points
        tmpPoints = [[i.x, i.y + 1] for i in getGroundPoints(self.groundPoints)]
        # Add the bottom right corner
        tmpPoints.append([self.getSize()[0], self.getSize()[1]])
        # Add the bottom left corner
        tmpPoints.append([0, self.getSize()[1]])
        # Draw a textured polygon using those points
        pygame.gfxdraw.textured_polygon(self.mainSurface, tmpPoints, self.moonTexture, *self.relativePoint.data())


    def exit(self):
        pygame.quit()
        quit()


    
