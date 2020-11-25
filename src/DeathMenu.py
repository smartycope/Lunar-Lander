from GuiScene import *


class DeathMenu(GuiScene):
    def renderUI(self):
        super().renderUI()

        textLoc = Pointi(self.center.x, 175)

        self.text = Text('You Died', textLoc, size=50)
        # self.text = Text('You have Died!', Pointf((self.getSize()[0] / 2), 20), color=[200, 20, 20], size=50)

        self.text.draw(self.mainSurface)

        self.background = None

        pygame.display.flip()
        pygame.display.update()

        respawnButtonLoc  = [300, 550]
        respawnButtonSize = [100, 50]

        toUpgradeButtonLoc  = Pointi(830, 550)
        toUpgradeButtonSize = respawnButtonSize

        self.elements += (
            Button(respawnButtonLoc, self.uiManager, 'Respawn', self.switchMenu, 'prev', size=respawnButtonSize),
            Button(toUpgradeButtonLoc.datai(), self.uiManager, 'Go to Menu', self.switchMenu, 'PickLanderMenu', size=toUpgradeButtonSize),
        )

    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.switchMenu('SaveMenu')
        if key == 'r' or key == 'enter' or key == 'return':
            self.switchMenu('prev')
        if key.lower() == 'm':
            self.switchMenu('PickLanderMenu')
