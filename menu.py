import pygame
# pygame.init()
import pygame_gui
start_game=False
running=True
class Page:
    def __init__(self):
        self.manager = pygame_gui.UIManager((800, 600))
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 535), (100, 50)),
            text="Back",
            manager=self.manager,
        )
        self.page_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 200), (100, 50)),
            text="",
            manager=self.manager,
        )

    def update(self, time_delta, window):
        window.blit(main_bg, (0, 0))#block image transfer, set 1 image onto another
        window.blit(main_logo, (250, 50))
        self.manager.update(time_delta)
        self.manager.draw_ui(window)

class MainMenu(Page):
    def __init__(self):
        super().__init__()
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (200, 50)),  # rectangle shape
                                                    text='Play',
                                                    manager=self.manager)
        self.leaderboard_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 375), (200, 50)),
            text="Leaderboard",
            manager=self.manager,
        )
        self.back_button.set_text("Exit")
        self.test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 400), (200, 50)), text='Test',manager=self.manager)

    def handle_event(self,event):
        global running
        global start_game
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element ==self.play_button:
                update_screen(2)
            if event.ui_element ==self.leaderboard_button:
                update_screen(1)
            if event.ui_element ==self.test_button:
                start_game = True
            if event.ui_element ==self.back_button:#
                running=False
        self.manager.process_events(event)

class Leaderboard(Page):
    def __init__(self):
        super().__init__()
        self.slider = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (200, 50)),
                                                        # rectangle shape
                                                        text='Work In Progress',
                                                        manager=self.manager)
        self.page_label.set_text("Leaderboard")
    def handle_event(self, event):
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.slider:
                print(f"NUmber 1 is ME")
            if event.ui_element == self.back_button:
                update_screen(0)
        self.manager.process_events(event)

class LoginPage(Page):
    def __init__(self):
        super().__init__()
        self.page_label.set_text("Login")
        self.enter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 450), (150, 50)),
                                                        text='Enter',
                                                        manager=self.manager)
        self.register_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 400), (200, 25)),
                                                            text='No account? Register',
                                                            manager=self.manager)
        self.username_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 300), (300, 50)),
            placeholder_text="Enter Username",
            manager=self.manager
        )

        self.password_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 350), (300, 50)),
            placeholder_text="Enter Password",
            manager=self.manager
        )
        self.password_box.set_text_hidden(True)
    def handle_event(self, event):
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.enter:
                self.username_box.set_text("")
                self.password_box.set_text("")
                print(f"No account matches these credentials")
                update_screen(4)
            if event.ui_element == self.register_button:
                update_screen(3)
            if event.ui_element == self.back_button:
                update_screen(0)
        self.manager.process_events(event)

class RegisterPage(Page):
    def __init__(self):
        super().__init__()
        self.page_label.set_text("Register")
        self.username_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 250), (300, 50)),
            placeholder_text="Create Username",
            manager=self.manager
        )
        self.enter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 450), (150, 50)),
                                                  text='Enter',
                                                  manager=self.manager)
        self.confirm_password_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 350), (300, 50)),
            placeholder_text="Confirm Password",
            manager=self.manager
        )
        self.password_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 300), (300, 50)),
            placeholder_text="Create Password",
            manager=self.manager
        )
        self.password_box.set_text_hidden(True)
        self.confirm_password_box.set_text_hidden(True)
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                update_screen(2)
        self.manager.process_events(event)

class ChooseWorld(Page):
    def __init__(self):
        super().__init__()
        self.page_label.set_text("Choose World")
        self.current_account = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 200), (150, 150)),
            text=f"Logged in as:",
            manager=self.manager
        )
        self.new_world_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((340, 470), (120, 50)),
            text="Create New",
            manager=self.manager,
        )
        self.play_world=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 400), (75, 50)),
            text="Play",
            manager=self.manager,
        )
        self.world_save_select=pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((300, 400), (150, 50)),
            options_list=["World Save1","World Save2","World Save3","a","b","c","d","e"],
            starting_option="World Save1",
            manager=self.manager,)
        self.save="World Save1"
        self.back_button.set_text("Logout")
    def handle_event(self, event):
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.world_save_select:
                self.save = event.text
                print(f"World selected: {self.save}")
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_world_button:
                update_screen(5)
            if event.ui_element == self.play_world:
                print(f"Opening World: {self.save}")
            if event.ui_element == self.back_button:
                update_screen(2)
        self.manager.process_events(event)

class CreateNewWorld(Page):
    def __init__(self):
        super().__init__()
        self.page_label.set_text("Create New World")
        self.difficulty_select = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((280, 400), (150, 50)),
            options_list=["Easy", "Medium", "Hard", "Hardcore"],
            starting_option="Easy",
            manager=self.manager
        )
        self.difficulty_stats = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((450, 350), (150, 150)),
            text=f"Number of lives:",
            manager=self.manager
        )
        self.create_world = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 470), (150, 50)),
                                                         text='Create World',
                                                         manager=self.manager)
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.create_world:
                print(f"World created")
            if event.ui_element == self.back_button:
                update_screen(4)
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.difficulty_select:
                print(f"Difficulty set to: {event.text}")
        self.manager.process_events(event)
main_bg=pygame.image.load('assets/main_bg.png')
main_bg=pygame.transform.scale(main_bg,(800,600))
main_logo=pygame.image.load('assets/main_logo.png')
main_logo=pygame.transform.scale(main_logo,(300,100))
main_menu = MainMenu()
leaderboard = Leaderboard()
login_page = LoginPage()
register_page= RegisterPage()
choose_world = ChooseWorld()
create_new_world= CreateNewWorld()
screens=[
     main_menu,
     leaderboard,
     login_page,
     register_page,
     choose_world,
     create_new_world
    ]
active_screen=screens[0]

def update_screen(index):
    """updates screen to given index"""
    global active_screen
    active_screen=screens[index]
    




