import pygame
import pygame_gui

class MainMenu:
    def __init__(self):
        """
        Creates Buttons and Text for Title Screen
        """
        self.manager=pygame_gui.UIManager((800,600))#manager for title screen
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 200), (200, 50)),
                                                    text='Play',#
                                                    manager=self.manager)
        self.leaderboard_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 275), (200, 50)),
            text="Leaderboard",
            manager=self.manager,
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 400), (100, 50)),
            text="Exit",
            manager=self.manager,
        )
    def update(self,time_delta, window):
        """Update method for the title screen"""
        window.blit(main_bg, (0, 0))
        window.blit(logo, (190, 0))
        self.manager.update(time_delta)
        self.manager.draw_ui(window)

    def handle_event(self,event):
        import main
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element ==self.play_button:
                print(f"game starting")
            if event.ui_element ==self.leaderboard_button:
                main.update_screen(1)
            if event.ui_element ==self.exit_button:
                main.pygame.quit()
        self.manager.process_events(event)

class Leaderboard:
    def __init__(self):
        self.manager = pygame_gui.UIManager((800, 600))
        self.slider = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 200), (200, 50)),
                                                        # rectangle shape
                                                        text='WOrk IN Progress',
                                                        manager=self.manager)
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 400), (100, 50)),
            text="Back",
            manager=self.manager,
        )

    def update(self, time_delta, window):
        window.blit(main_bg, (0, 0))
        window.blit(logo, (190, 0))
        self.manager.update(time_delta)
        self.manager.draw_ui(window)


    def handle_event(self, event):
        import main
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.slider:
                print(f"NUmber 1 is ME")
            if event.ui_element == self.back_button:
                main.update_screen(0)
        self.manager.process_events(event)
main_menu = MainMenu()
leaderboard = Leaderboard()
main_bg=pygame.image.load('main_bg.png')
logo=pygame.image.load('testlogo.png')




