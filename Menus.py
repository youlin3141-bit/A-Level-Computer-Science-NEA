import pygame
import pygame_gui

def title_page(manager, window):
    play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 275), (200, 50)),  # rectangle shape
                                                text='Play',
                                                manager=manager)  # button created
    title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 100), (200, 50)),
        text="Title Text",
        manager=manager
    )
    buttons=[title,play_button]
    window.fill(pygame.Color('blue'))
    return buttons

