from GuiScene import *


class UpgradeMenu(GuiScene):
    def renderUI(self):
        super().renderUI()

        self.background = [200, 200, 200]

        # self.text = Text('You Died', textLoc, size=textSize)

        self.elements += (
        )

    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.exit()

    def run(self, deltaTime):
        # self.text.draw(self.mainSurface)
        return super().run(deltaTime)

