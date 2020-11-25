from GuiScene import *
from pygame import gfxdraw
from Animation import Animation

class PickPlanetMenu(GuiScene):
    def init(self, **params):
        # This must be in the same order as self.planets!
        self.planetNames = ['moon', 'mars', 'mercury', 'venus', 'uranus', 'neptune', 'jupiter', 'saturn', 'makemake', 'eris', 'haumea', 'sun']
        self.animations = {}
        for i in self.planetNames:
            self.animations[i] = params[i + 'Animation']

        self.dir += 'planets/planetAnimations/'


    def renderUI(self):
        selectButtonsSize = [80, 400]
        selectButtonsLocY = self.center.y - 200

        self.selectedIndex = 0

        self.positionSelected = [self.center.x - 135, self.center.y - 70]
        self.positionLeft     = [self.center.x - 665, self.center.y - 70]
        self.positionRight    = [self.center.x + 400, self.center.y - 70]


        self.backgroundColors = []
        for i in self.planetNames:
            self.backgroundColors.append(pygame.transform.average_color(self.animations[i][0]))

        # If you're getting an error here, it quite possible it's because data isn't getting passed between scenes correctly. Check startScene in Game.py

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

        moon     = Animation(preloadedFrames=self.animations['moon'],     secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        mars     = Animation(preloadedFrames=self.animations['mars'],     secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        mercury  = Animation(preloadedFrames=self.animations['mercury'],  secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        venus    = Animation(preloadedFrames=self.animations['venus'],    secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        uranus   = Animation(preloadedFrames=self.animations['uranus'],   secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        neptune  = Animation(preloadedFrames=self.animations['neptune'],  secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        jupiter  = Animation(preloadedFrames=self.animations['jupiter'],  secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        saturn   = Animation(preloadedFrames=self.animations['saturn'],   secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        makemake = Animation(preloadedFrames=self.animations['makemake'], secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        eris     = Animation(preloadedFrames=self.animations['eris'],     secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        haumea   = Animation(preloadedFrames=self.animations['haumea'],   secondsPerLoop=PLANET_SECONDS_PER_ROTATION)
        sun      = Animation(preloadedFrames=self.animations['sun'],      secondsPerLoop=PLANET_SECONDS_PER_ROTATION)

        self.planets = [
            AnimationButton(moonLoc,     self.uiManager, moon,     self.switchMenu, 'UpgradeMenu', planet='Moon',     background=self.background),
            AnimationButton(marsLoc,     self.uiManager, mars,     self.switchMenu, 'UpgradeMenu', planet='Mars',     background=self.background),
            AnimationButton(mercuryLoc,  self.uiManager, mercury,  self.switchMenu, 'UpgradeMenu', planet='Mercury',  background=self.background),
            AnimationButton(venusLoc,    self.uiManager, venus,    self.switchMenu, 'UpgradeMenu', planet='Venus',    background=self.background),
            AnimationButton(uranusLoc,   self.uiManager, uranus,   self.switchMenu, 'UpgradeMenu', planet='Uranus',   background=self.background),
            AnimationButton(neptuneLoc,  self.uiManager, neptune,  self.switchMenu, 'UpgradeMenu', planet='Neptune',  background=self.background),
            AnimationButton(jupiterLoc,  self.uiManager, jupiter,  self.switchMenu, 'UpgradeMenu', planet='Jupiter',  background=self.background),
            AnimationButton(saturnLoc,   self.uiManager, saturn,   self.switchMenu, 'UpgradeMenu', planet='Saturn',   background=self.background),
            AnimationButton(makemakeLoc, self.uiManager, makemake, self.switchMenu, 'UpgradeMenu', planet='Makemake', background=self.background),
            AnimationButton(erisLoc,     self.uiManager, eris,     self.switchMenu, 'UpgradeMenu', planet='Eris',     background=self.background),
            AnimationButton(haumeaLoc,   self.uiManager, haumea,   self.switchMenu, 'UpgradeMenu', planet='Haumea',   background=self.background),
            AnimationButton(sunLoc,      self.uiManager, sun,      self.switchMenu, 'UpgradeMenu', planet='Sun',      background=self.background),
        ]

        self.leftButton  = Button([self.center.x - 250 - selectButtonsSize[0], selectButtonsLocY], self.uiManager, '<', self.moveSelection, LEFT,  size=selectButtonsSize)
        self.rightButton = Button([self.center.x + 250, selectButtonsLocY], self.uiManager, '>', self.moveSelection, RIGHT, size=selectButtonsSize)

        self.titleText = Text('Select Planet', [self.center.x, 80], size=50)
        self.planetText = Text(self.planetNames[0].title(), [self.center.x, 120], size=50)

        self.elements += tuple(self.planets) + (
            self.leftButton,
            self.rightButton,
        )


        # Animate them all once so all their surfaces are ready
        for i in self.planets:
            i.animate()

        # self.menuParams['lander'] = params['lander']


    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.switchMenu('SaveMenu')
        if key == 'left':
            self.moveSelection(LEFT)
        if key == 'right':
            self.moveSelection(RIGHT)
        if key == 'enter' or key == 'return':
            self.switchMenu('UpgradeMenu', planet=self.planetNames[self.selectedIndex].title())


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
        if self.selectedIndex >= len(self.planets):
            self.selectedIndex = len(self.planets) - 1

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
