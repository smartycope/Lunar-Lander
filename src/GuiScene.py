from Scene import *
from Elements import *
from Text import Text
import pygame_gui

class GuiScene(Scene):
    def __init__(self, surface, **params):
        self.uiManager = pygame_gui.UIManager(surface.get_size(), GUI_THEME_FILE)
        self.elements = ()
        self.showMouse(True)
        self.setKeyRepeat(200, 20)
        self.background = self.uiManager.get_theme().get_colour('dark_bg')
        self.debug = False
        super().__init__(surface, **params)
        self.renderUI()

        # PackageResource(package='data.themes', resource='theme_2.json'))

        # self.uiManager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
        #                                ])


    def renderUI(self):
        self.uiManager.set_window_resolution(self.getSize())
        self.uiManager.clear_and_reset()

        # self.UIbackgroundSurface = pygame.Surface(self.options.resolution)
        # self.UIbackgroundSurface.fill()


    def handleEvent(self, event):
        for i in self.elements:
            i.handleEvent(event)

        super().handleEvent(event)

        self.uiManager.process_events(event)
                    

    def run(self, deltaTime):
        if self.debug:
            self.uiManager.set_visual_debug_mode(self.debug)
            print("self.uiManager.focused_set:", self.uiManager.focused_set)

        # respond to input
        self.uiManager.update(deltaTime)

        self.uiManager.draw_ui(self.mainSurface)

        return self._menu
