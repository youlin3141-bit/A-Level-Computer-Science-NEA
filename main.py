import pygame
import pygame_gui
pygame.init()

window = pygame.display.set_mode((800, 600))#create window 800x600
running = True
manager = pygame_gui.UIManager((800, 600))# the "boss" of the GUI components
clock = pygame.time.Clock()
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 275), (200, 50)),#rectangle shape
                                            text='Play',
                                            manager=manager)#button created
# title=pygame.image.load('title.png').convert_alpha()
while running:
    time_delta = clock.tick(60) / 1000.0#clock tick 60 returns time between each frame in ms, /1000 turns to seconds
    for event in pygame.event.get():#listens for events
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element==hello_button:
                print(f"hellow world")

        manager.process_events(event)#processes the event
    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.update()
pygame.quit()