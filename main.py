import pygame # user venv 3.14 computerscience nea
#python 3.6??? works occasionally but not always?

pygame.init()
window = pygame.display.set_mode((800, 600))#create window 800x600


clock = pygame.time.Clock()

import menu

while menu.running:
    time_delta = clock.tick(60) / 1000.0#clock tick 60 returns time between each frame in ms, /1000 turns to seconds
    for event in pygame.event.get():#listens for events
        if event.type == pygame.QUIT:#close window with X
            menu.running = False
        menu.active_screen.handle_event(event)
    menu.active_screen.update(time_delta,window)
    pygame.display.update()

pygame.quit()