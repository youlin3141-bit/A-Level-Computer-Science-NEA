import pygame # user venv 3.14 computerscience nea
#python 3.6??? works occasionally but not always?

pygame.init()
window = pygame.display.set_mode((800, 600))#create window 800x600


clock = pygame.time.Clock()

import menu
from game import Game
game=None
while menu.running:
    time_delta = clock.tick(60) / 1000.0#clock tick 60 returns time between each frame in ms, /1000 turns to seconds
    for event in pygame.event.get():#listens for events
        if event.type == pygame.QUIT:#close window with X
            menu.running = False
        if not game:    #if game does not exist, then handle the menu
            menu.active_screen.handle_event(event)
        else:
            game.handle_event(event)
            if game.paused:
                menu.screens[6].handle_event(event)
                game.paused=menu.screens[6].paused
                if not menu.screens[6].game_active:
                    game=None
            elif game.shop_required:
                shop=menu.screens[7]
                shop.handle_event(event)
                if shop.continue_pressed:
                    game.shop_required=False
                    shop.continue_pressed=False
                    game.generate_level()
    if not game:
        menu.active_screen.update(time_delta,window)
        if menu.start_game:
            game=Game()
            menu.start_game=False
            menu.screens[6].game_active=True
            menu.screens[6].paused=True
    else:
        game.update(window)
        if game.paused and menu.screens[6].paused:
            menu.screens[6].update(time_delta,window)
        elif game.shop_required:
            menu.screens[7].update(time_delta,window)
            menu.screens[7].set_items(game.shop_items)
            if menu.screens[7].selected_item:
                game.buy_shop_item(menu.screens[7].selected_item)
                menu.screens[7].selected_item=None
            game.player.draw_health_bar(window)
            game.player.draw_xp(window)
            game.player.draw_currency(window)
            game.player.draw_inventory(window)

    pygame.display.update()

pygame.quit()