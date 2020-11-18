from GuiScene import *
from pygame import gfxdraw
from Animation import Animation

class PickPlanetMenu(GuiScene):
    def init(self, **params):
        super().init()
        self.dir += 'planets/planetAnimations/'

        selectButtonsSize = [80, 400]
        selectButtonsLocY = self.center.y - 200

        self.selectedIndex = 0

        self.positionSelected = [self.center.x - 90,  self.center.y - 70]
        self.positionLeft     = [self.center.x - 550, self.center.y - 70]
        self.positionRight    = [self.center.x + 350, self.center.y - 70]



        # This must be in the same order as self.planets!
        self.planetNames = ['moon', 'mars', 'mercury', 'venus', 'uranus', 'neptune', 'jupiter', 'saturn', 'makemake', 'eris', 'haumea', 'sun']

        self.backgroundColors = []
        for i in self.planetNames:
            self.backgroundColors.append(pygame.transform.average_color(params[i + 'Animation'][0]))

        self.background = self.backgroundColors[0]


        
        # animationWidth = 275
        nowhere = [10000, 10000]

        moonLoc     = self.positionSelected
        marsLoc     = self.positionRight
        mercuryLoc  = nowhere
        venusLoc    = nowhere
        uranusLoc   = nowhere
        neptuneLoc  = nowhere
        jupiterLoc  = nowhere
        saturnLoc   = nowhere
        makemakeLoc = nowhere
        erisLoc     = nowhere
        haumeaLoc   = nowhere
        sunLoc      = nowhere

        moon     = Animation(preloadedFrames=params['moonAnimation'],     secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        mars     = Animation(preloadedFrames=params['marsAnimation'],     secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        mercury  = Animation(preloadedFrames=params['mercuryAnimation'],  secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        venus    = Animation(preloadedFrames=params['venusAnimation'],    secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        uranus   = Animation(preloadedFrames=params['uranusAnimation'],   secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        neptune  = Animation(preloadedFrames=params['neptuneAnimation'],  secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        jupiter  = Animation(preloadedFrames=params['jupiterAnimation'],  secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        saturn   = Animation(preloadedFrames=params['saturnAnimation'],   secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        makemake = Animation(preloadedFrames=params['makemakeAnimation'], secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        eris     = Animation(preloadedFrames=params['erisAnimation'],     secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        haumea   = Animation(preloadedFrames=params['haumeaAnimation'],   secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        sun      = Animation(preloadedFrames=params['sunAnimation'],      secondsPerLoop=PLANET_SECONDS_PER_ROTATION)

        self.planets = [
            AnimationButton(moonLoc,     self.uiManager, moon,     self.switchMenu, 'Moon', background=self.background),
            AnimationButton(marsLoc,     self.uiManager, mars,     self.switchMenu, 'Mars', background=self.background),
            AnimationButton(mercuryLoc,  self.uiManager, mercury,  self.switchMenu, 'Moon', background=self.background),
            AnimationButton(venusLoc,    self.uiManager, venus,    self.switchMenu, 'Moon', background=self.background),
            AnimationButton(uranusLoc,   self.uiManager, uranus,   self.switchMenu, 'Moon', background=self.background),
            AnimationButton(neptuneLoc,  self.uiManager, neptune,  self.switchMenu, 'Moon', background=self.background),
            AnimationButton(jupiterLoc,  self.uiManager, jupiter,  self.switchMenu, 'Moon', background=self.background),
            AnimationButton(saturnLoc,   self.uiManager, saturn,   self.switchMenu, 'Moon', background=self.background),
            AnimationButton(makemakeLoc, self.uiManager, makemake, self.switchMenu, 'Moon', background=self.background),
            AnimationButton(erisLoc,     self.uiManager, eris,     self.switchMenu, 'Moon', background=self.background),
            AnimationButton(haumeaLoc,   self.uiManager, haumea,   self.switchMenu, 'Moon', background=self.background),
            AnimationButton(sunLoc,      self.uiManager, sun,      self.switchMenu, 'Moon', background=self.background),
        ]

        self.leftButton  = Button([self.center.x - 250, selectButtonsLocY], self.uiManager, '<', self.moveSelection, LEFT,  size=selectButtonsSize)
        self.rightButton = Button([self.center.x + 250, selectButtonsLocY], self.uiManager, '>', self.moveSelection, RIGHT, size=selectButtonsSize)

        self.titleText = Text('Select Planet', [self.center.x - 80, 80], size=50)
        self.planetText = Text(self.planetNames[0].title(), [self.center.x - 80, 120], size=50)

        self.elements += tuple(self.planets) + (
            self.leftButton,
            self.rightButton,
        )


        # Animate them all once so all their surfaces are ready
        for i in self.planets:
            i.animate()

        # self.menuParams['lander'] = params['lander']


    # def renderUI(self):
    #     super().renderUI()

    #     # self.background = [20, 20, 20]

    #     # self.text = Text('You Died', textLoc, size=textSize)

    #     self.elements += (
    #     )


    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.exit()


    def run(self, deltaTime):
        # self.text.draw(self.mainSurface)
        # self.frame += 1
        # if self.frame >= NUM_MARS_FRAMES * TIME_TO_ROTATE:
        #     self.frame = 0

        # print(self.frame)

        # for i in self.elements:
        #     if type(i) == AnimationButton:
        #         i.animate()

        # if self.selectedIndex <= 0:
        #     self.mainSurface.fill(self.backgroundColors[self.selectedIndex]) #, pygame.Rect(self.planets[0].size, self.positionLeft))

        self.titleText.draw(self.mainSurface)
        self.planetText.draw(self.mainSurface)

        #* To animate all the visible planets
        # for i in [self.planets[self.selectedIndex], self.planets[self.selectedIndex - 1], self.planets[self.selectedIndex + 1]]:
        #     i.animate()
        # try:
        #     self.planets[self.selectedIndex].animate()
        # except IndexError: pass
        # try:
        #     self.planets[self.selectedIndex - 1].animate()
        # except IndexError: pass
        # try:
        #     self.planets[self.selectedIndex + 1].animate()
        # except IndexError: pass

        #* To animate only the selected planet
        self.planets[self.selectedIndex].animate()

        if self.selectedIndex <= 0:
            self.leftButton.element.disable()
        else:
            self.leftButton.element.enable()

        if self.selectedIndex >= len(self.planets) - 1:
            self.rightButton.element.disable()
        else:
            self.rightButton.element.enable()

        # if self.selectedIndex >= len(self.planets):
        #     self.mainSurface.fill(self.backgroundColors[self.selectedIndex], pygame.Rect(self.planets[0].size, self.positionRight))

        # if self.selectedIndex <= 0:
            # self.mainSurface.fill(self.backgroundColors[self.selectedIndex], pygame.Rect(self.planets[0].size, self.positionLeft))

        # self.mainSurface.blit(self.mars.animate(), self.marsLoc)
        # self.elements += (ImageButton(self.marsLoc, self.uiManager, self.mars.animate(), self.switchMenu, 'Moon', background=self.background, deltaColor=70),)

        return super().run(deltaTime)



    def moveSelection(self, direction):
        # for i in self.planets:
            # i.animate()

        if direction == LEFT:
            self.selectedIndex -= 1
        if direction == RIGHT:
            self.selectedIndex += 1

        if self.selectedIndex < 0:
            self.selectedIndex = 0
        if self.selectedIndex > len(self.planets):
            self.selectedIndex = len(self.planets)

        self.background = self.backgroundColors[self.selectedIndex]
        # self.background = self.planets[self.selectedIndex].element.disabled_image
        self.planetText.updateText(self.planetNames[self.selectedIndex].title())

        for i in self.planets:
            i.disable()
            i.element.hide()

        self.planets[self.selectedIndex].pos = self.positionSelected
        self.planets[self.selectedIndex].background = self.background
        self.planets[self.selectedIndex].enable()
        # self.planets[self.selectedIndex].element.show()
        self.planets[self.selectedIndex].rebuild()

        # Dont loop
        if self.selectedIndex > 0:
            self.planets[self.selectedIndex - 1].pos = self.positionLeft
            self.planets[self.selectedIndex - 1].background = self.background
            self.planets[self.selectedIndex - 1].disable()
            # self.planets[self.selectedIndex - 1].element.show()
            self.planets[self.selectedIndex - 1].rebuild()
            
        if self.selectedIndex < len(self.planets) - 1:
            self.planets[self.selectedIndex + 1].pos = self.positionRight
            self.planets[self.selectedIndex + 1].background = self.background
            self.planets[self.selectedIndex + 1].disable()
            # self.planets[self.selectedIndex + 1].element.show()
            self.planets[self.selectedIndex + 1].rebuild()
            

        # for i in self.planets:
        #     i.rebuild()
            # i.animate()

        # pygame.display.flip()
        # pygame.display.update()
        # self.mainSurface.fill(self.background)

        # for i in self.planets:
        #     if i != self.planets[self.selectedIndex]:
        #         i.element.disable()

        # for i in self.planets:
        #     try:
        #         if i not in [self.planets[self.selectedIndex], self.planets[self.selectedIndex - 1], self.planets[self.selectedIndex + 1]]:
        #             i.pos = [10000, 10000]
        #             i.rebuild()
        #             # self.mainSurface.fill(self.backgroundColors[self.selectedIndex], pygame.Rect(self.planets[0].size, self.positionLeft))
        #     except IndexError: pass
        # #         i.element.hide()
