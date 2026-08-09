import settings
from player import Player
from camera import Camera
from minimap import Minimap
from image import load_image
from enemy import Enemy
import map
class Game:
    def __init__(self):
        self.map = map.game_map
        playerx,playery,remaining_rooms=map.find_spawn(map.remaining_rooms)
        enemyx,enemyy,remaining_rooms1=map.find_spawn(map.remaining_rooms)
        self.player = Player(playerx,playery,self.map)
        self.camera = Camera(800,600)
        self.wall=load_image("assets/wall.png",settings.TILE_SIZE,settings.TILE_SIZE)
        self.floor=load_image("assets/floor.png",settings.TILE_SIZE,settings.TILE_SIZE)
        self.enemy=Enemy(enemyx,enemyy,self.map,48,48,"enemy1","assets/enemy1.png")

    def update(self,window):
        self.player.handle_input()
        self.enemy.update()
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
        minimap.draw(window,self.player)
        window.blit(self.player.image,(self.player.rect.x-self.camera.x,self.player.rect.y-self.camera.y))
        self.enemy.draw(window,self.camera)
