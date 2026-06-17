import pygame
import pygame_gui
manager = pygame_gui.UIManager((800, 600))# the "boss" of the GUI components
main_bg=pygame.image.load('main_bg.png')
def title_page():
    play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 200), (200, 50)),  # rectangle shape
                                                    text='Play',
                                                    manager=manager)  # button created
    leaderboard_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300,275), (200, 50)),  # rectangle shape
                                                    text='Leaderboard',
                                                    manager=manager)  # button created

    title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 100), (200, 50)),
            text="Title Text",
            manager=manager
        )
    exit_button = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 100), (200, 50)),
        text="Title Text",
        manager=manager)
    buttons=[play_button,leaderboard_button,exit_button,title]
    return buttons

def leaderboard(window):
    window.fill("black")
    window.blit(main_bg,(0,0))
    title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 100), (200, 50)),
            text="Leaderboard",
            manager=manager
        )
    
title_buttons=title_page()

def update(time_delta,window):
    manager.update(time_delta)
    manager.draw_ui(window)



