import pygame
import pygame_gui
manager = pygame_gui.UIManager((800, 600))# the "boss" of the GUI components
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 275), (200, 50)),  # rectangle shape
                                                text='Play',
                                                manager=manager)  # button created
title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 100), (200, 50)),
        text="Title Text",
        manager=manager
    )
def handle_event(event):
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element ==play_button:
            print(f"hellow world")
    manager.process_events(event)  # processes the event

def update(time_delta,window):
    manager.update(time_delta)
    manager.draw_ui(window)



