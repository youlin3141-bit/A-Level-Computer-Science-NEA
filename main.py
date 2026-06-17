import pygame # user venv 3.14 computerscience nea
pygame.init()

window = pygame.display.set_mode((800, 600))#create window 800x600
running = True
clock = pygame.time.Clock()

import menu
while running:
    time_delta = clock.tick(60) / 1000.0#clock tick 60 returns time between each frame in ms, /1000 turns to seconds
    for event in pygame.event.get():#listens for events
        if event.type == pygame.QUIT:
            running = False
        menu.handle_event(event)
    menu.update(time_delta,window)
    pygame.display.update()
pygame.quit()