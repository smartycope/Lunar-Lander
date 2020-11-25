from GuiScene import *
from ClassicLander import ClassicLander
from PipSqueekLander import PipSqueekLander

class PickLanderMenu(GuiScene):
    def renderUI(self):
        super().renderUI()

        # self.background = [20, 20, 20]
        # self.dir = 'landers/'
        self.dir = 'other/'

        # self.text = Text('You Died', textLoc, size=textSize)
        landerImage  = self.loadAsset('classicLander-fullSize', [270, 270])
        lander1Image = self.loadAsset('pipSqueek-fullSize', [240, 270])

        self.actualLanders = ['Pip Squeek', 'Classic']

        selectButtonsSize = [80, 400]
        selectButtonsLocY = self.center.y - 200

        self.selectedIndex = 0

        self.positionSelected = [self.center.x - 135, self.center.y - 70]
        self.positionLeft     = [self.center.x - 665, self.center.y - 70]
        self.positionRight    = [self.center.x + 400, self.center.y - 70]

        self.background = pygame.transform.average_color(landerImage)

        self.landers = [
            ImageButton(self.positionSelected, self.uiManager, lander1Image, self.switchMenu, 'PickPlanetMenu', lander=self.actualLanders[0], background=self.background),
            ImageButton(self.positionRight,    self.uiManager, landerImage,  self.switchMenu, 'PickPlanetMenu', lander=self.actualLanders[1], background=self.background),
        ]

        self.landers[1].element.disable()

        self.leftButton  = Button([self.center.x - 250 - selectButtonsSize[0], selectButtonsLocY], self.uiManager, '<', self.moveSelection, LEFT,  size=selectButtonsSize)
        self.rightButton = Button([self.center.x + 250, selectButtonsLocY], self.uiManager, '>', self.moveSelection, RIGHT, size=selectButtonsSize)

        self.titleText = Text('Select Lander', [self.center.x, 80], size=50)


        self.elements += tuple(self.landers) + (
            # Button(self.center.datai(), self.uiManager, '', self.switchMenu, 'PickPlanetMenu', landerImage, size=landerImage.get_size()),
            self.leftButton,
            self.rightButton,
        )

    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.switchMenu('SaveMenu')
        if key == 'left':
            self.moveSelection(LEFT)
        if key == 'right':
            self.moveSelection(RIGHT)
        if key == 'enter' or key == 'return':
            self.switchMenu('PickPlanetMenu', lander=self.actualLanders[self.selectedIndex])

    def moveSelection(self, direction):
        if direction == LEFT:
            self.selectedIndex -= 1
        if direction == RIGHT:
            self.selectedIndex += 1

        if self.selectedIndex < 0:
            self.selectedIndex = 0
        if self.selectedIndex > len(self.landers):
            self.selectedIndex = len(self.landers)

        self.background = pygame.transform.average_color(self.landers[self.selectedIndex].image)

        try: 
            self.landers[self.selectedIndex].pos = self.positionSelected
            self.landers[self.selectedIndex].background = self.background
            self.landers[self.selectedIndex].rebuild()
        except IndexError: pass
        
        try: 
            self.landers[self.selectedIndex - 1].pos = self.positionLeft
            self.landers[self.selectedIndex - 1].background = self.background
            self.landers[self.selectedIndex - 1].rebuild()
        except IndexError: pass
        
        try:
            self.landers[self.selectedIndex + 1].pos = self.positionRight
            self.landers[self.selectedIndex + 1].background = self.background
            self.landers[self.selectedIndex + 1].rebuild()
        except IndexError: pass

        for i in self.landers:
            if i != self.landers[self.selectedIndex]:
                i.element.disable()

    def run(self, deltaTime):
        self.titleText.draw(self.mainSurface)
        if self.selectedIndex <= 0:
            self.leftButton.element.disable()
        else:
            self.leftButton.element.enable()

        if self.selectedIndex >= len(self.landers) - 1:
            self.rightButton.element.disable()
        else:
            self.rightButton.element.enable()
            
        return super().run(deltaTime)
