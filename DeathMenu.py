from Config import *
from GlobalFuncs import *
from GuiScene import *

class Pointer:
    def __init__(self, val):
        self.contents = val

def setVal(var, to):
    if type(var) == Pointer:
        var.contents = to
    else:
        var = to




class DeathMenu(GuiScene):
    def renderUI(self):
        super().renderUI()

        # respawnButtonLoc  = self.centerPoint - [50, 30]
        respawnButtonLoc  = [500, 175]
        respawnButtonSize = [200, 80]

        # textLoc  = self.centerPoint
        textLoc  = [300, 550]
        textSize = [100, 50]

        self.elements += (
            Label(textLoc, self.uiManager, 'You Died', textSize),
            Button(respawnButtonLoc, self.uiManager, 'Respawn', self.respawn, size=respawnButtonSize)
        )

    def respawn(self):
        self.menu = 'MoonLander'

    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.exit()
        if key == 'r' or key == 'enter' or key == 'return':
            self.respawn()
            # self.menu = 'prev'