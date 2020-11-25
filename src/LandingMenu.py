from GuiScene import *


class LandingMenu(GuiScene):
    def renderUI(self):
        super().renderUI()

        textSize = 50
        textLoc  = Pointi(self.center.x, self.center.y - 200)

        playButtonSize = [300, 100]
        playButtonLoc  = Pointi(self.center.x - playButtonSize[0] / 2, self.center.y + 200)

        aboutButtonSize = [150, 50]
        aboutButtonLoc  = Pointi(self.center.x - aboutButtonSize[0] / 2, self.center.y + 305)

        # toUpgradeButtonLoc  = Pointi(, 550)
        # toUpgradeButtonSize = respawnButtonSize

        self.text = Text('Solar Lander', textLoc, size=textSize)

        self.elements += (
            Button(playButtonLoc,  self.uiManager, 'Play',  self.switchMenu, 'PickLanderMenu', size=playButtonSize),
            Button(aboutButtonLoc, self.uiManager, 'About', self.switchMenu, 'CreditsMenu',    size=aboutButtonSize),
        )

    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.exit()
        if key == 'p' or key == 'enter' or key == 'return':
            self.switchMenu('PickLanderMenu')


    def run(self, deltaTime):
        self.text.draw(self.mainSurface)
        return super().run(deltaTime)