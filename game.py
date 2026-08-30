import menu
import settings
import pygame
from exit import Exit,Generator
import items
from player import Player
from camera import Camera
from minimap import Minimap
from image import load_image
import database
import monster
import map
import random
class Game:
    def __init__(self,player_id,world_id,difficulty=None,data=None):
        self.player_id = player_id
        self.world_id = world_id
        self.camera = Camera(800, 600)
        self.wall = load_image("assets/wall.png", settings.TILE_SIZE, settings.TILE_SIZE)
        self.floor = load_image("assets/floor.png", settings.TILE_SIZE, settings.TILE_SIZE)

        self.shop_required = False
        self.projectiles = []
        self.enemies = []
        self.generators = []
        self.paused = False
        self.has_mace=1
        self.has_spellbook=0
        self.game_over=False

        if not data:
            self.level=1
            self.difficulty=difficulty
            self.generate_level()
        else:
            (
                player_level,
                self.difficulty,
                currency,
                xp,
                self.level,
                speed,
                damage_upgrade,
                health,
                max_health,
                self.has_mace,
                self.has_spellbook,
            )=data
            self.generate_level()
            self.player.progression.level=player_level
            self.player.progression.currency=currency
            self.player.progression.xp=xp
            self.player.speed=speed
            self.player.damage_upgrade=damage_upgrade
            self.player.health=health
            self.player.max_health=max_health
    def generate_level(self):
        self.map,self.rooms=map.generate_map(self.level)
        self.valid_spawns=map.find_spawn(self.rooms)
        spawn=random.choice(self.valid_spawns)
        x,y=spawn
        self.valid_spawns.remove(spawn)
        if not hasattr(self,"player"):
            self.player=Player(x,y,self.map)
            if self.has_mace:
                self.player.items[0] = items.Mace(self.player, self.enemies)
            if self.has_spellbook:
                self.player.items[1] = items.SpellBook(self.player, self.enemies, self.projectiles)
        else:
            self.player.map=self.map
            self.player.x=x
            self.player.y=y

        self.player.rect.center = spawn
        self.enemies.clear()
        self.projectiles.clear()
        self.generators.clear()
        self.exit_location=map.find_exit(self.valid_spawns,spawn)
        self.exit=Exit(self.exit_location[0],self.exit_location[1])
        self.valid_spawns.remove(self.exit_location)
        self.spawn_generators()
        self.spawn_enemy()

    def spawn_generators(self):
        number_generators=min(int((self.level-1)**0.5+1),len(self.valid_spawns))
        spawns_list=self.valid_spawns.copy()
        for i in range(number_generators):
            if not spawns_list:
                break
            rand_spawn=random.choice(spawns_list)
            x,y=rand_spawn
            spawns_list.remove(rand_spawn)
            if ((x - self.player.x) ** 2 + (y - self.player.y)**2) ** 0.5 >= 20 * settings.TILE_SIZE:
                self.generators.append(Generator(x,y))

    def spawn_enemy(self):
        enemy_spawns=self.valid_spawns.copy()
        # print(self.valid_spawns)
        number_enemies=int((4*self.level)**0.5+1)
        for i in range(number_enemies):#int((4*self.level)**0.5+1)
            if enemy_spawns:
                spawn = random.choice(enemy_spawns)
                x, y = spawn
                enemy_spawns.remove(spawn)
                range_enemy = monster.RangeEnemy(x, y, self.map, "range1", self.projectiles, self.difficulty)
                melee_enemy = monster.MeleeEnemy(x, y, self.map, "melee1", self.difficulty)
            else:
                spawn = random.choice(self.valid_spawns)
                x, y = spawn
                range_enemy = monster.RangeEnemy(x, y, self.map, "range1", self.projectiles, self.difficulty)
                melee_enemy=monster.MeleeEnemy(x,y,self.map,"melee1",self.difficulty)
            enemies = [range_enemy, melee_enemy]
            self.enemies.append(random.choice(enemies))

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused=not self.paused
                if self.paused:
                    menu.active_screen=menu.screens[6]
                    menu.screens[6].paused=True
                else:
                    menu.screens[6].paused = False


    def next_level(self):
        completed_level=self.level
        self.level+=1
        # print(f"New Level Reached:{self.level}")
        if completed_level%3==0:
            self.shop_required=True
            self.generate_shop()
            return
        self.generate_level()
        database.save_game(self)

    def generate_shop(self):
        available_items=[]
        for item in settings.SHOP_ITEMS["items"]:
            if not self.player_has_item(item):
                available_items.append(item)
        available_upgrades=list(settings.SHOP_ITEMS["upgrades"].keys())
        if available_items:
            self.shop_items=[random.choice(available_items)]+ [random.choice(available_upgrades),random.choice(available_upgrades)]
        else:
            self.shop_items=[random.choice(available_upgrades),random.choice(available_upgrades),random.choice(available_upgrades)]

    def player_has_item(self,target_item):
        for item in self.player.items:
            if item and item.name==target_item:
                return True
        return False
    def buy_shop_item(self,item_name):
        if item_name in settings.SHOP_ITEMS["items"]:
            item=None
            price=settings.SHOP_ITEMS["items"][item_name]
            # if self.player.progression.currency<price:
                # print("Not Enough Coins")
            if self.player.progression.currency>=price:
                if item_name=="Mace":
                    self.has_mace = 1
                    item=items.Mace(self.player,self.enemies)
                elif item_name=="SpellBook":
                    self.has_spellbook = 1
                    item=items.SpellBook(self.player,self.enemies,self.projectiles)
                if item:
                    if self.player.add_item(item):
                        if item_name=="Mace":
                            self.has_mace=1
                        elif item_name=="SpellBook":
                            self.has_spellbook=1
                            # print(self.has_spellbook)
                        self.player.progression.currency-=price
        elif item_name in settings.SHOP_ITEMS["upgrades"]:
            price=settings.SHOP_ITEMS["upgrades"][item_name]
            if self.player.progression.currency>=price:
                self.player.progression.currency-=price
                self.player.apply_upgrade(item_name)

    def update(self, window):
        if self.player.health<=0:
            self.player_dies()
            return
        if not self.paused and not self.shop_required:
            if self.exit.update(self.player):
                self.next_level()
            self.player.handle_input()

            for enemy in self.enemies:
                enemy.update(self.player)
                enemy.attack(self.player)
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
                    self.player.progression.add_xp(enemy.xp_yield)
                    self.player.progression.add_currency(enemy.currency_yield)

            for projectile in self.projectiles:
                projectile.update()
                projectile.projectile_timer-=1
                if projectile.projectile_timer <= 0:
                    self.projectiles.remove(projectile)

            active_gen_list=[]
            for gen in self.generators:
                gen.update(self.player)
                active_gen_list.append(gen.active)
            if all(active_gen_list):
                self.exit.active=True
            else:
                self.exit.active=False#ISUNNNOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
            self.camera.update(self.player)
        self.draw(window)
    def player_dies(self):
        database.highest_level(self)
        database.delete_worlds(self.world_id)
        self.game_over=True

    def draw(self,window):
        window.fill((0,0,0))
        first_column=self.camera.x//settings.TILE_SIZE
        last_column=first_column + 800 // settings.TILE_SIZE + 2# allows for camera to move smoothly as extra tiles are rendered
        first_row=self.camera.y//settings.TILE_SIZE
        last_row=first_row + 600 // settings.TILE_SIZE + 2
        minimap=Minimap(self.map,settings.TILE_SIZE)
        for row in range(first_row,last_row):
            for column in range(first_column,last_column):
                if 0<=column<len(self.map[0]) and 0<=row<len(self.map):#for a 2D list, len(list) returns rows and len(list[0]) returns columns
                    if self.map[row][column]==0:
                        image=self.wall
                    else:
                        image=self.floor
                    window.blit(image,(column*settings.TILE_SIZE-self.camera.x,row*settings.TILE_SIZE-self.camera.y))#converting world coordinate to screen coordinate
        self.exit.draw(window, self.camera)



        for enemy in self.enemies:
            enemy.draw(window,self.camera)
        for projectile in self.projectiles:
            projectile.draw(window,self.camera)
        for gen in self.generators:
            gen.draw(window,self.camera,self.player)
        minimap.draw(window,self.player)
        window.blit(self.player.image,(self.player.rect.x-self.camera.x,self.player.rect.y-self.camera.y))
        self.player.draw_health_bar(window)
        self.player.draw_inventory(window)
        self.player.draw_xp(window)
        self.player.draw_currency(window)
        self.player.draw_upgrade(window)
        if self.player.current_item=="Mace":
            if self.player.current_item.use(): # to be removed
                self.player.current_item.flash_timer=5
        if self.player.current_item:
            if self.player.current_item.flash_timer>0:
                self.player.current_item.draw_hitbox(window,self.camera)
                self.player.current_item.flash_timer-=1
        #self.next_level()#DO NOT RUn

