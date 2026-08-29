import pygame
import database
database.create_database()
pygame.init()
window = pygame.display.set_mode((800, 600))#create window 800x600


clock = pygame.time.Clock()

import menu
from game import Game
game=None
player_id=None
world_id=None
while menu.running:
    time_delta = clock.tick(60) / 1000.0#clock tick 60 returns time between each frame in ms, /1000 turns to seconds
    for event in pygame.event.get():#listens for events
        if event.type == pygame.QUIT:#close window with X
            menu.running = False
        if not player_id:
            # menu.active_screen.handle_event(event)
            login_page=menu.screens[2]
            if login_page.player_id:
                player_id=login_page.player_id
                menu.screens[4].set_player(player_id)
        if menu.screens[4].world_selected:
            choose_world = menu.screens[4]
            world_id = choose_world.world_id
            data=database.load_game(player_id,world_id)
            game=Game(player_id,world_id,data=data)
            database.save_game(game)
            choose_world.world_selected = False


        if not game:    #if game does not exist, then handle the menu
            menu.active_screen.handle_event(event)
            create_page=menu.screens[5]
            # menu.screens[4].set_worlds()
            if create_page.create_pressed:
                difficulty=create_page.difficulty
                print(f"{difficulty} difficulty world created")
                world_id=database.create_world(menu.screens[2].player_id)
                game=Game(menu.screens[2].player_id,world_id, difficulty=difficulty)
                database.save_game(game)
                menu.screens[4].set_worlds()
                create_page.create_pressed = False
        else:
            game.handle_event(event)
            if game.paused:
                menu.screens[6].handle_event(event)
                game.paused = menu.screens[6].paused
                # if not menu.screens[6].game_active:
                #     database.save_game(game)
                #     game = None
                #     menu.screens[4].set_worlds()
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
            # game=Game(difficulty)
            menu.start_game=False
            menu.screens[6].game_active=True
            menu.screens[6].paused=True
    else:
        game.update(window)
        if game.game_over:
            game = None
            menu.screens[4].set_worlds()
            menu.active_screen = menu.screens[8]
        elif game.paused and menu.screens[6].paused:
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