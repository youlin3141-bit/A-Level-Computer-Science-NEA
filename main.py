import pygame # user venv 3.14 computerscience nea

from menu import login_page

pygame.init()
window = pygame.display.set_mode((800, 600))#create window 800x600

running = True
clock = pygame.time.Clock()

import menu
current_page="Main Menu"

screens=[menu.main_menu , menu.leaderboard , menu.login_page]
active_screen=screens[0]

def update_screen(index):
    """updates screen to given index"""
    global active_screen
    active_screen=screens[index]

while True:
    time_delta = clock.tick(60) / 1000.0#clock tick 60 returns time between each frame in ms, /1000 turns to seconds
    for event in pygame.event.get():#listens for events
        if event.type == pygame.QUIT:
            pygame.quit()
        active_screen.handle_event(event)
    active_screen.update(time_delta,window)
    pygame.display.update()
pygame.quit()#why does it make an error?