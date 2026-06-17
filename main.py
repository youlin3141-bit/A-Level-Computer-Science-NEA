import pygame # user venv 3.14 computerscience nea
import pygame_gui
pygame.init()
window = pygame.display.set_mode((800, 600))#create window 800x600

running = True
clock = pygame.time.Clock()

import menu
manager=menu.manager
current_page="Main Menu"
window.blit(menu.main_bg,(0,0))
def handle_event(event):
    global running, current_page
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == menu.title_buttons[0]:
            print(f"game start")
        if event.ui_element ==menu.title_buttons[1]:
            current_page="Leaderboard"
            for button in menu.title_buttons:
                button.hide()
            menu.leaderboard(window)
        if event.ui_element ==menu.title_buttons[2]:
            running = False
    manager.process_events(event)  # processes the event

while running:
    time_delta = clock.tick(60) / 1000.0#clock tick 60 returns time between each frame in ms, /1000 turns to seconds
    for event in pygame.event.get():#listens for events
        if event.type == pygame.QUIT:
            running = False
        handle_event(event)
    menu.update(time_delta,window)
    pygame.display.update()
pygame.quit()