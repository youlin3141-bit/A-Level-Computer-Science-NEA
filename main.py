import pygame
import pygame_gui
import Menus
pygame.init()

window = pygame.display.set_mode((800, 600))#create window 800x600
running = True
manager = pygame_gui.UIManager((800, 600))# the "boss" of the GUI components
clock = pygame.time.Clock()
Menus.title_page(manager,window)
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