from GuiScene import *


class LandingMenu(GuiScene):
    def init(self, **params):
        super().init()
        self.menuParams['lander'] = params['lander']

    def renderUI(self):
        super().renderUI()

        self.background = None

        # respawnButtonLoc  = self.centerPoint - [50, 30]
        respawnButtonLoc  = [300, 550]
        respawnButtonSize = [100, 50]

        # textLoc  = self.centerPoint
        textLoc  = Pointi(500, 175)
        textSize = 50

        toUpgradeButtonLoc  = Pointi(830, 550)
        toUpgradeButtonSize = respawnButtonSize

        self.text = Text('You Died', textLoc, size=textSize)

        self.elements += (
            # Label(textLoc.datai(), self.uiManager, 'You Died', textSize),
            Button(respawnButtonLoc, self.uiManager, 'Respawn', self.switchMenu, 'prev', size=respawnButtonSize),
            Button(toUpgradeButtonLoc.datai(), self.uiManager, 'Go to Menu', self.switchMenu, 'PickLanderMenu', size=toUpgradeButtonSize)
        )

    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.exit()
        if key == 'r' or key == 'enter' or key == 'return':
            self.menu = 'prev'

    def run(self, deltaTime):
        # self.text.draw(self.mainSurface)
        return super().run(deltaTime)