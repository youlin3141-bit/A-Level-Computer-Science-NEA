import pygame
import pygame_gui
class Player:
    def __init__(self):
        self.health=100
        self.pos=(3,3)
        self.items=[]
        self.facing=0

class GameScreen:
    def __init__(self):
        self.manager = pygame_gui.UIManager((800, 600))  # manager for game screen
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 700), (200, 50)),
                                                            text='Play',
                                                            manager=self.manager)

