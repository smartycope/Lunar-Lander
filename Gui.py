from Config import *
from GlobalFuncs import *
from Scene import Scene

class GuiScene(Scene):
    def __init__(self):
        self.uiManager = pygame_gui.UIManager(self.getSize(), GUI_THEME_FILE)

        
        self.UIbackgroundSurface = None

        self.renderUI()
    
        self.time_delta_stack = deque([])

        self.button_response_timer = pygame.time.Clock()

        self.running = True
        self.debug = True

        self.all_enabled = True
        self.all_shown = True

        # self.button = None

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

        self.UIbackgroundSurface = pygame.Surface(self.options.resolution)
        self.UIbackgroundSurface.fill(self.uiManager.get_theme().get_colour('dark_bg'))

    def handleEvent(self, event):
        self.uiManager.process_events(event)
        super().handleEvent(event)


    def run(self):
        if self.debug:
            self.uiManager.set_visual_debug_mode(self.debug)
            print("self.uiManager.focused_set:", self.uiManager.focused_set)
        

    def process_events(self):


                

    def run(self):
            time_delta = self.clock.tick() / 1000.0


            # respond to input
            self.uiManager.update(time_delta)

            self.uiManager.draw_ui(self.mainSurface)

            pygame.display.update()

        
        
class UpgradeMenu(GuiScene):
        
        self.button = None

        # self.test_button = None
        # self.test_button_2 = None
        # self.test_button_3 = None
        # self.test_slider = None
        # self.test_text_entry = None
        # self.test_drop_down = None
        # self.test_drop_down_2 = None
        # self.panel = None
        # self.fps_counter = None
        # self.frame_timer = None
        # self.disable_toggle = None
        # self.hide_toggle = None

        # self.message_window = None
