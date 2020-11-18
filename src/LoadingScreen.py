from GuiScene import *
from pygame import freetype
from Animation import *

class LoadingBar:
    def __init__(self, surface, loc, finsihedFunc, *params, tasks=None, **kwparams):
        self.animation = Animation('other/loadingAnimation/', secondsPerLoop=5, scale=[240, 240])
        if tasks is None:
            self.length = self.animation.numFrames
        else:
            self.length = tasks

        self.surface = surface
        self.loc = loc
        
        self._progress = self.length

        self.func = finsihedFunc
        self.params = params
        self.kwparams = kwparams

    def progress(self, amount=None):
        if amount is None:
            amount = self.length / self.animation.numFrames

        self._progress -= amount

        if self._progress <= 0:
            self.func(*self.params, **self.kwparams)
            return True
        else:
            self.surface.blit(self.animation.animate(), [self.loc[0], self.loc[1]])
            pygame.display.flip()
            pygame.display.update()
            return False
            


class LoadingScreen(Scene):
    def init(self, **params):
        self.text = Text('Solar Lander', Pointi(self.center.x - 175, 200), size=80)
        # self.texts = []
        # Over estimate the amount of tasks
        self.loadingBar = LoadingBar(self.mainSurface, [self.center.x - 120, self.center.y + 100], self.switchMenu, 'PickLanderMenu', tasks=1210)
        self.mainSurface.fill(self.background)
        self.text.draw(self.mainSurface)
        # for cnt, i in enumerate(pygame.font.get_fonts()):
            # p = Pointi(self.center.x, cnt * 24)
            # font = pygame.freetype.Font(pygame.font.match_font(i), (24,))
            # text = Text('Solar Lander', p, font=font, size=24)
            # self.texts.append(text)
            # self.texts.append(Text('Solar Lander', Pointi(self.center.x, cnt * 24)))

        self.dir += 'planets/planetAnimations/'


        self.menuParams['marsAnimation']     = preloadFrames(self.dir + 'marsAnimation/',     scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['moonAnimation']     = preloadFrames(self.dir + 'moonAnimation/',     scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['mercuryAnimation']  = preloadFrames(self.dir + 'mercuryAnimation/',  scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['venusAnimation']    = preloadFrames(self.dir + 'venusAnimation/',    scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['sunAnimation']      = preloadFrames(self.dir + 'sunAnimation/',      scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['makemakeAnimation'] = preloadFrames(self.dir + 'makemakeAnimation/', scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['erisAnimation']     = preloadFrames(self.dir + 'erisAnimation/',     scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['haumeaAnimation']   = preloadFrames(self.dir + 'haumeaAnimation/',   scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['jupiterAnimation']  = preloadFrames(self.dir + 'jupiterAnimation/',  scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['neptuneAnimation']  = preloadFrames(self.dir + 'neptuneAnimation/',  scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['saturnAnimation']   = preloadFrames(self.dir + 'saturnAnimation/',   scale=[270, 270], loadingBar=self.loadingBar)
        self.menuParams['uranusAnimation']   = preloadFrames(self.dir + 'uranusAnimation/',   scale=[270, 270], loadingBar=self.loadingBar)


    def run(self, deltaTime):
        # for i in self.texts:
        #     i.draw(self.mainSurface)

        # self.text = Text('Solar Lander', Pointi(self.center.x - 175, 200), size=80)
        self.text.draw(self.mainSurface)
        self.loadingBar.progress()

        return self._menu

