from GuiScene import *


class UpgradeMenu(GuiScene):
    def init(self, **params):
        self.lander = params['lander']
        self.planet = params['planet']
        self.money  = params['money']
        self.dir = 'upgrades/'


    def renderUI(self):
        super().renderUI()

        upgradeSize = [490, 400]

        selectButtonsSize = [80, 400]
        selectButtonsLocY = self.center.y - 200

        self.selectedIndex = 0

        self.positionSelected = Pointi(self.center.x - 245, selectButtonsLocY)
        self.positionLeft     = Pointi(self.center.x - 250 - selectButtonsSize[0] - upgradeSize[0], selectButtonsLocY)
        self.positionRight    = Pointi(self.center.x + 250 + selectButtonsSize[0], selectButtonsLocY)

        nowhere = [10000, 10000]

        with open(DATA + '/saves/save.json', 'r') as file:
            landerUpgrades = json.load(file)[self.lander]

        self.upgrades = [
            Upgrade('Thrust', 1000, self.upgradeVal, 'thrust', 0.2, self.loadAsset('thrust'), self.uiManager, self.money,
                    loc=self.positionSelected, size=upgradeSize, comparisonVal=landerUpgrades['thrust'], comparisonValUnits='kn', enabled=True, increment=lambda x: x * 1.25),

            Upgrade('Side Thrust', 750, self.upgradeVal, 'sideThrust', 0.4, self.loadAsset('sideThrust'), self.uiManager, self.money,
                    loc=self.positionRight, size=upgradeSize, comparisonVal=landerUpgrades['sideThrust'], comparisonValUnits='kn', increment=lambda x: x * 1.25),
        ]

        self.leftButton  = Button([self.center.x - 250 - selectButtonsSize[0], selectButtonsLocY], self.uiManager, '<', self.moveSelection, LEFT,  size=selectButtonsSize)
        self.rightButton = Button([self.center.x + 250, selectButtonsLocY], self.uiManager, '>', self.moveSelection, RIGHT, size=selectButtonsSize)

        self.titleText = Text(f'Upgrade {self.lander}', [self.center.x, 80], size=50)
        self.moneyText = Text(f'ByteCoin: {int(self.money)}', [100, 100], align=LEFT_ALIGN)

        # playButtonLoc = [self.center.x - 245 + 490, selectButtonsLocY + 480]
        playButtonSize = [140, 55]
        playButtonLoc  = Pointi(self.center.x - playButtonSize[0] / 2, self.center.y + 280)

        self.elements += tuple(self.upgrades) + (
            self.leftButton,
            self.rightButton,
            Button(playButtonLoc, self.uiManager, 'Play', self.switchMenu, self.planet, size=playButtonSize),
            # Button(playButtonLoc, self.uiManager, 'Play', print, self.money, size=playButtonSize),

        )

        for i in self.upgrades:
            self.elements += (i.element,)


    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.switchMenu('SaveMenu')
        if key == 'left':
            self.moveSelection(LEFT)
        if key == 'right':
            self.moveSelection(RIGHT)
        if key == 'enter' or key == 'return':
            self.switchMenu(self.planet)
        if key == ' ' or key == 'space':
            self.upgrades[self.selectedIndex].func(self.upgrades[self.selectedIndex].valueParam, self.upgrades[self.selectedIndex].amountParam)

    
    def moveSelection(self, direction):
        if direction == LEFT:
            self.selectedIndex -= 1
        if direction == RIGHT:
            self.selectedIndex += 1

        if self.selectedIndex < 0:
            self.selectedIndex = 0
        if self.selectedIndex > len(self.upgrades):
            self.selectedIndex = len(self.upgrades) - 1

        # self.background = pygame.transform.average_color(self.upgrades[self.selectedIndex].image)

        try:
            self.upgrades[self.selectedIndex].loc = self.positionSelected
            self.upgrades[self.selectedIndex].enable()
            # self.upgrades[self.selectedIndex].background = self.background
            self.upgrades[self.selectedIndex].rebuild()
        except IndexError: pass
        
        try:
            self.upgrades[self.selectedIndex - 1].loc = self.positionLeft
            self.upgrades[self.selectedIndex - 1].disable()
            # self.upgrades[self.selectedIndex - 1].background = self.background
            self.upgrades[self.selectedIndex - 1].rebuild()
        except IndexError: pass
        
        try:
            self.upgrades[self.selectedIndex + 1].loc = self.positionRight
            self.upgrades[self.selectedIndex + 1].disable()
            # self.upgrades[self.selectedIndex + 1].background = self.background
            self.upgrades[self.selectedIndex + 1].rebuild()
        except IndexError: pass

        # for i in self.upgrades:
        #     if i != self.upgrades[self.selectedIndex]:
        #         i.element.disable()


    def upgradeVal(self, var, val):
        if self.money >= self.upgrades[self.selectedIndex].cost:
            # Load the json save file
            with open(DATA + '/saves/save.json', 'r') as file:
                landerUpgrades = json.load(file)

            # Update all the money
            self.money -= self.upgrades[self.selectedIndex].cost
            self.upgrades[self.selectedIndex].money = self.money
            self.moneyText.updateText(f'ByteCoin: {self.money}')

            # Change the value and update the displayed value in the Upgrade
            landerUpgrades[self.lander][var] += val
            self.upgrades[self.selectedIndex].updateVal(landerUpgrades[self.lander][var])

            # Save the changed save file
            with open(DATA + '/saves/save.json', 'w') as file:
                json.dump(landerUpgrades, file, sort_keys=True, indent=4, separators=(',', ': '))

        else:
            self.upgrades[self.selectedIndex].element.element.disable()


    def run(self, deltaTime):
        self.titleText.draw(self.mainSurface)
        self.moneyText.draw(self.mainSurface)

        self.titleText.draw(self.mainSurface)

        
        if self.selectedIndex <= 0:
            self.leftButton.element.disable()
        else:
            self.leftButton.element.enable()

        if self.selectedIndex >= len(self.upgrades) - 1:
            self.rightButton.element.disable()
        else:
            self.rightButton.element.enable()


        for i in self.upgrades:
            i.draw(self.mainSurface, self.background)

        return super().run(deltaTime)




class Upgrade:
    def __init__(self, name, cost, attributeFunc, valueParam, amountParam, image, uiManager, money, 
                 size=[420, 400], loc=Pointi(400, 160), comparisonVal=None, comparisonValUnits='', enabled=False, increment=lambda x: x):
        loc = Pointi(loc)
        self.cost = cost
        self.func = attributeFunc
        self.valueParam = valueParam
        self.amountParam = amountParam
        self.name = name
        self.loc = loc
        self.size = size
        self.comparisonVal = comparisonVal
        self.enabled = enabled
        self.deltaColor = 30
        self.money = money
        self.comparisonValUnits = comparisonValUnits
        self.incrementFunc = increment

        # self.image = pygame.transform.scale(image, self.size)
        self.image = image

        myCenter = (Pointi(self.size) / 2) + self.loc
        imageCenter = Pointi(self.image.get_rect().center) + self.loc
        self.imageLoc = self.loc + (myCenter - imageCenter)

        buttonSize = [185, 60]

        self.element = Button(self.loc + [(self.size[0] / 2) - (buttonSize[0] / 2), self.size[1] + 5], uiManager, f'Upgrade {name}', self.func, self.valueParam, self.amountParam, size=buttonSize)
        if not self.enabled:
            self.element.element.disable()
            self.element.element.hide()
        if self.money < self.cost:
            self.element.element.disable()

        #* Centered
        # self.nameText = Text(name.title(), self.loc + [(self.size[0] / 2), 20], size=35, align=CENTER_ALIGN)
        #* Right aligned
        self.nameText = Text(name.title(), self.loc + 20, size=35, align=LEFT_ALIGN)
        self.costText = Text(f'Cost: {round(self.cost)} ByteCoin', self.loc + [20, 50], size=28, align=LEFT_ALIGN)
        if self.comparisonVal is not None:
            self.currentValText = Text(f'Currently:  {round(self.comparisonVal, UPGRADE_ROUND_PLACES)} {self.comparisonValUnits}', self.loc + [20, 75], size=20, align=LEFT_ALIGN)
            self.upgradeValText = Text(f'Upgraded: {round(self.comparisonVal + self.amountParam, UPGRADE_ROUND_PLACES)} {self.comparisonValUnits}', self.loc + [20, 95], size=20, align=LEFT_ALIGN)


    # I don't know why this is nessicary, but it is, last I checked
    def handleEvent(self, event):
        pass


    def disable(self):
        self.enabled = False
        self.element.element.disable()
        self.element.element.hide()


    def enable(self):
        self.enabled = True
        self.element.element.enable()
        self.element.element.show()


    def rebuild(self, newComparisonVal=None):
        self.element.element.kill()
        buttonSize = [200, 75]
        self.element.pos = (self.loc + [(self.size[0] / 2) - (buttonSize[0] / 2), self.size[1] + 5]).datai()
        self.element.rebuild()

        myCenter = (Pointi(self.size) / 2) + self.loc
        imageCenter = Pointi(self.image.get_rect().center) + self.loc
        self.imageLoc = self.loc + (myCenter - imageCenter)

        self.nameText.pos = self.loc + 20
        self.costText.pos = self.loc + [20, 50]
        if self.comparisonVal is not None:
            self.currentValText.pos = self.loc + [20, 75]
            self.upgradeValText.pos = self.loc + [20, 95]

        if self.comparisonVal is not None and newComparisonVal is not None:
            self.currentValText.updateText(f'Currently:  {round(newComparisonVal, UPGRADE_ROUND_PLACES)} {self.comparisonValUnits}', align=LEFT_ALIGN)
            self.upgradeValText.updateText(f'Upgraded: {round(newComparisonVal + self.amountParam, UPGRADE_ROUND_PLACES)} {self.comparisonValUnits}', align=LEFT_ALIGN)

        if not self.enabled:
            self.element.element.disable()
            self.element.element.hide()
        else:
            self.element.element.enable()
            self.element.element.show()


    def updateVal(self, newVal):
        self.cost = self.incrementFunc(self.cost)
        self.costText.updateText(f'Cost: {round(self.cost)} ByteCoin')
        if self.comparisonVal is not None:
            self.currentValText.updateText(f'Currently:  {round(newVal)} {self.comparisonValUnits}')
            self.upgradeValText.updateText(f'Upgraded: {round(newVal + self.amountParam)} {self.comparisonValUnits}')


    def draw(self, surface, background):
        if self.money < self.cost:
            self.element.element.disable()

        if self.enabled:
            surface.blit(self.image, self.imageLoc.datai())

            self.nameText.draw(surface)        
            self.costText.draw(surface)
            if self.comparisonVal is not None:
                self.currentValText.draw(surface)
                self.upgradeValText.draw(surface)

        else:
             # Create a darker image to blend
            blend = pygame.Surface(self.size, flags=pygame.SRCALPHA)
            blend.fill([self.deltaColor, self.deltaColor, self.deltaColor, 0])

            disabledImage = self.image.copy()
            disabledImage.blit(blend, [0, 0], special_flags=pygame.BLEND_RGBA_ADD)

            # Add the background
            backgroundSurf = pygame.Surface(self.size)
            if type(background) in [list, tuple, pygame.Color]:
                backgroundSurf.fill(background)
            elif type(background) == pygame.Surface:
                backgroundSurf = background
            elif background is None:
                pass
            else:
                assert(False)
            
            backgroundSurf.blit(self.image, [0, 0])

            surface.blit(backgroundSurf, self.imageLoc.datai())

            self.nameText.draw(surface)
            self.costText.draw(surface)
            if self.comparisonVal is not None:
                self.currentValText.draw(surface)
                self.upgradeValText.draw(surface)



'''
The save json file looks something like this:
(This is the default configuration)

{
    "ClassicLander": {
        "fuelCapacity": 2353,
        "legStrength": 10,
        "sideThrust": 4,
        "specificImpulse": 0,
        "thrust": 16,
        "weight": 4740,
        "rotationSpeed": 0
    },
    "PipSqueekLander": {
        "fuelCapacity": 2353,
        "legStrength": 10,
        "sideThrust": 4,
        "specificImpulse": 0,
        "thrust": 16,
        "weight": 4740,
        "rotationSpeed": 0
    },
    "money": 0,
    "planet": "Moon"
}
'''