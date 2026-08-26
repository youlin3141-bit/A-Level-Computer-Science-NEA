import menu
import settings
import pygame
from exit import Exit,Generator
import items
from player import Player
from camera import Camera
from minimap import Minimap
from image import load_image
import monster
import map
import random
class Game:
    def __init__(self):
        self.level=1
        self.difficulty="Easy"
        self.paused=False
        self.open_settings=False
        self.camera=Camera(800,600)
        self.wall=load_image("assets/wall.png",settings.TILE_SIZE,settings.TILE_SIZE)
        self.floor=load_image("assets/floor.png",settings.TILE_SIZE,settings.TILE_SIZE)

        self.shop_required=False
        self.projectiles=[]
        self.enemies=[]
        self.generators=[]

        self.generate_level()

    def generate_level(self):
        self.map,self.rooms=map.generate_map(self.level)
        self.valid_spawns=map.find_spawn(self.rooms)
        spawn=random.choice(self.valid_spawns)
        x,y=spawn
        self.valid_spawns.remove(spawn)
        if not hasattr(self,"player"):
            self.player=Player(x,y,self.map)
            self.player.items[0]=items.Mace(self.player,self.enemies)
            self.player.items[1]=items.SpellBook(self.player,self.enemies,self.projectiles)
        else:
            self.player.map=self.map
            self.player.x=x
            self.player.y=y
        self.player.rect.center=spawn
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
        print(self.valid_spawns)
        number_enemies=int((4*self.level)**0.5+1)
        for i in range(number_enemies):#int((4*self.level)**0.5+1)
            if enemy_spawns:
                spawn = random.choice(enemy_spawns)
                x, y = spawn
                enemy_spawns.remove(spawn)
                enemy=monster.RangeEnemy(x,y,self.map,"range1",self.projectiles,self.difficulty)
            else:
                spawn = random.choice(self.valid_spawns)
                x, y = spawn
                enemy = monster.RangeEnemy(x, y, self.map, "range1", self.projectiles, self.difficulty)
            self.enemies.append(enemy)

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
        print(f"New Level Reached:{self.level}")
        if completed_level%3==0:
            self.shop_required=True
            return
        self.generate_level()

    def update(self, window):
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
                self.exit.active=False
            self.camera.update(self.player)
        self.draw(window)

    def draw(self,window):
        window.fill((0,0,0))
        first_column=self.camera.x//settings.TILE_SIZE
        last_column=first_column + 800 // settings.TILE_SIZE + 2# allows for camera to move smoothly as extra tiles are rendered
        first_row=self.camera.y//settings.TILE_SIZE
        last_row=first_row + 600 // settings.TILE_SIZE + 2
        minimap=Minimap(self.map,settings.TILE_SIZE)

        # print(first_column, last_column)
        # print(first_row, last_row)
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
        if self.player.current_item: # to be removed
            self.player.current_item.draw_hitbox(window, self.camera)
        #self.next_level()#DO NOT RUn

