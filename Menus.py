import pygame
import pygame_gui

def title_page(manager, window):
    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 275), (200, 50)),  # rectangle shape
                                                text='Play',
                                                manager=manager)  # button created
    window.fill(pygame.Color('white'))

