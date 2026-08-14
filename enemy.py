import pygame
from pathfinding import astar
import settings
from image import load_image
class Enemy:
    def __init__(self,x,y,game_map,enemy_type):
        self.map=game_map
        self.path_timer=0
        self.path=[]
        stats=settings.ENEMY_TYPES[enemy_type]
        self.speed=stats["speed"]
        self.damage=stats["damage"]
        self.rect=pygame.Rect(x,y,stats["width"],stats["height"])
        self.image=load_image(stats["image"],stats["width"],stats["height"])
        self.view_radius=stats["view_radius"]
        self.state="wander"
    def check_collision(self, rect):
        left = rect.left//settings.TILE_SIZE
        right = (rect.right-1)//settings.TILE_SIZE  # occupies 0-31 tiles hence the -1
        top = rect.top//settings.TILE_SIZE
        bottom = (rect.bottom-1)//settings.TILE_SIZE
        for row in range(top,bottom+1):
            for column in range(left,right+1):
                if self.map[row][column] == 0:
                    return True
        return False
    def move(self,dx,dy):
        new_rect = self.rect.copy()
        new_rect.x += dx
        # if not self.check_collision(new_rect):
        self.rect.x = new_rect.x

        new_rect = self.rect.copy()
        new_rect.y += dy
        # if not self.check_collision(new_rect):
        self.rect.y = new_rect.y

    def update(self,player):
        distance=pygame.Vector2(self.rect.center).distance_to(player.rect.center)#builtin vector methods to calc distance
        if distance < self.view_radius:
            self.state="chase"
        else:
            self.state="wander"
        if self.state=="wander":
            self.wander()
        elif self.state=="chase":
            self.chase(player)
    def chase(self,player):
        enemy_tile=(self.rect.centerx//settings.TILE_SIZE,self.rect.centery//settings.TILE_SIZE)
        player_tile=(player.rect.centerx//settings.TILE_SIZE,player.rect.centery//settings.TILE_SIZE)
        self.path_timer-=1
        if self.path_timer<0:
            self.path=astar(enemy_tile,player_tile,self.map)#list of tuples
            self.path_timer=15#runs 4 times a second for iimproved performance
        if self.path and len(self.path) > 1:  # non empty, existent path
            next=self.path[1]
            goal_x=next[0]*settings.TILE_SIZE+settings.TILE_SIZE//2#xcoordinate
            goal_y=next[1]*settings.TILE_SIZE+settings.TILE_SIZE//2#ycoordinate
            direction=pygame.Vector2(goal_x-self.rect.centerx,goal_y-self.rect.centery)
            if direction.length()>0: #pythagoras here
                direction=direction.normalize()
            self.move(direction.x*self.speed,direction.y*self.speed)
    def wander(self,):
        pass
    def draw(self,window,camera):
        window.blit(self.image,(self.rect.x-camera.x,self.rect.y-camera.y))

