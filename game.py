import pygame
TILE_SIZE = 32
from player import Player
from camera import Camera
from minimap import Minimap
import map
class Game:
    def __init__(self):
        self.map = map.game_map
        self.player = Player(map.find_spawn(map.root)[0],map.find_spawn(map.root)[1],self.map)
        self.camera = Camera(800,600)
        self.wall=pygame.image.load("assets/wall2.png").convert_alpha()
        self.floor = pygame.image.load("assets/floor1.png").convert_alpha()
        self.wall=pygame.transform.scale(self.wall,(TILE_SIZE,TILE_SIZE))
        self.floor=pygame.transform.scale(self.floor,(TILE_SIZE,TILE_SIZE))

    def update(self,window):
        # print("updating")
        self.player.handle_input()
        self.camera.update(self.player)
        self.draw(window)

    def draw(self,window):
        window.fill((0,0,0))
        first_column=self.camera.x//TILE_SIZE
        last_column=first_column + 800 // TILE_SIZE + 2# allows for camera to move smoothly as extra tiles are rendered
        first_row=self.camera.y//TILE_SIZE
        last_row=first_row + 600 // TILE_SIZE + 2
        minimap=Minimap(self.map,TILE_SIZE)

        # print(first_column, last_column)
        # print(first_row, last_row)
        for row in range(first_row,last_row):
            for column in range(first_column,last_column):
                if 0<=column<len(self.map[0]) and 0<=row<len(self.map):#for a 2D list, len(list) returns rows and len(list[0]) returns columns
                    if self.map[row][column]==0:
                        image=self.wall
                    else:
                        image=self.floor
                    window.blit(image,(column*TILE_SIZE-self.camera.x,row*TILE_SIZE-self.camera.y))#converting world coordinate to screen coordinate
        minimap.draw(window,self.player)
        window.blit(self.player.image,(self.player.rect.x-self.camera.x,self.player.rect.y-self.camera.y))
