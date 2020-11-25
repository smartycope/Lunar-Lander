from GuiScene import *


class CreditsMenu(GuiScene):
    def renderUI(self):
        super().renderUI()

        self.mainSurface.fill(self.background)
        pygame.display.flip()
        pygame.display.update()

        self.background = None

        credits = \
        '''
                                                                                                                                     Game created by: Copeland Carter



        All assets in this game (models, textures, etc.) are as accurate as possible to the current knowledge of our solar system.
        Some are compeletly made up, but of the parts we do know, they're accurate.


        If you liked this game, check out my other projects at github.com/smartycope
        To send me bug reports or feature ideas, email me at smartycope@gmail.com



        This game is open source under the GPL v3.0 liscence. No Rights Reserved.
        '''

        backSize = [150, 50]
        backLoc  = Pointi(self.center.x - backSize[0] / 2, self.center.y + 305)

        self.text = Text(credits, [0, 0])

        self.elements += (
            Button(backLoc, self.uiManager, 'Back', self.switchMenu, 'LandingMenu', size=backSize),
        )

        self.text.draw(self.mainSurface)

    def keyDown(self, event):
        key = super().keyDown(event)
        
        if key == 'escape':
            self.exit()
        # if key == 'r' or key == 'enter' or key == 'return':
        #     self.menu = 'prev'


    # def run(self, deltaTime):
        # self.text.draw(self.mainSurface)
        # return super().run(deltaTime)