from GuiScene import *
import json

class SaveMenu(GuiScene):
    def init(self, **params):
        self.saveMe = params
        # We don't need to (and can't) save these
        for i in ['moon', 'mars', 'mercury', 'venus', 'uranus', 'neptune', 'jupiter', 'saturn', 'makemake', 'eris', 'haumea', 'sun']:
            self.saveMe.pop(i + 'Animation')
        # This is handled by UpgradeMenu already
        self.saveMe.pop('lander')
        # We don't need this...
        self.saveMe.pop('planet')
        # 
        # self.saveMe.pop('killButton')


    def renderUI(self):
        super().renderUI()

        textSize = 50
        textLoc  = Pointi(self.center.x, self.center.y - 200)

        self.text = Text('Exit? Are you sure? Don\'t leave me...', textLoc, size=textSize)

        # self.background = pygame.Surface(self.getSize(), flags=pygame.SRCALPHA)
        # self.background.fill([30, 30, 30, 200], special_flags=pygame.BLEND_RGBA_ADD)

        self.mainSurface.fill([50, 50, 50, 200], special_flags=pygame.BLEND_RGBA_SUB)

        self.text.draw(self.mainSurface)

        self.background = None

        pygame.display.flip()
        pygame.display.update()

        saveButtonSize     = [200, 50]
        saveButtonLoc      = Pointi(self.center.x - 410, self.center.y + 200)

        saveExitButtonSize = [200, 50]
        saveExitButtonLoc  = Pointi(self.center.x - 205, self.center.y + 200)

        cancelButtonSize   = [200, 50]
        cancelButtonLoc    = Pointi(self.center.x, self.center.y + 200)

        exitButtonSize     = [200, 50]
        exitButtonLoc      = Pointi(self.center.x + 205, self.center.y + 200)

        killButtonSize     = [100, 25]
        killButtonLoc      = Pointi(self.center.x - 50, self.center.y + 60)

        self.elements += (
            Button(saveButtonLoc,     self.uiManager, 'Save',                self.save, size=saveButtonSize),
            Button(saveExitButtonLoc, self.uiManager, 'Save & Exit',         self.leave, True, size=saveExitButtonSize),
            Button(cancelButtonLoc,   self.uiManager, 'Stay!',               self.switchMenu, 'prev', size=cancelButtonSize),
            Button(exitButtonLoc,     self.uiManager, 'Exit without Saving', self.leave, False, size=exitButtonSize),
            # Button(killButtonLoc,     self.uiManager, 'Kill',                self.switchMenu, False, size=exitButtonSize),
        )


    def leave(self, save=True):
        if save:
            self.save()
        self.exit()


    def save(self):
        # If you don't do this twice, it just appends everything to the end of the file
        with open(DATA + '/saves/save.json', 'r') as f:
            tmp = json.load(f)

        with open(DATA + '/saves/save.json', 'w') as f:
            json.dump(dict(tmp, **self.saveMe), f, sort_keys=True, indent=4, separators=(',', ': '))
       


    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.switchMenu('prev')
        if key == 'enter' or key == 'return':
            self.save()
