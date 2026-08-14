import settings
from player import Player
from camera import Camera
from minimap import Minimap
from image import load_image
from enemy import Enemy
import map
import random
class Game:
    def __init__(self):
        self.map = map.game_map
        self.valid_spawns=map.find_spawn(map.rooms)
        spawn=random.choice(self.valid_spawns)
        x,y=spawn
        self.valid_spawns.remove(spawn)
        self.player = Player(x,y,self.map)
        self.camera = Camera(800,600)
        self.wall=load_image("assets/wall.png",settings.TILE_SIZE,settings.TILE_SIZE)
        self.floor=load_image("assets/floor.png",settings.TILE_SIZE,settings.TILE_SIZE)
        self.enemies=[]
        self.spawn_enemy()

    def spawn_enemy(self):
        for i in range(settings.ENEMY_COUNT):
            spawn = random.choice(self.valid_spawns)
            x, y = spawn
            print(spawn)
            self.valid_spawns.remove(spawn)
            enemy=Enemy(x,y,self.map,"monster0")
            self.enemies.append(enemy)

    def update(self, window):
        self.player.handle_input()
        for enemy in self.enemies:
            enemy.update(self.player)
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
        for enemy in self.enemies:
            enemy.draw(window,self.camera)
        minimap.draw(window,self.player)
        window.blit(self.player.image,(self.player.rect.x-self.camera.x,self.player.rect.y-self.camera.y))

