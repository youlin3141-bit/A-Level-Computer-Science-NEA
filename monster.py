import pygame
import random
from pathfinding import astar
import settings
from image import load_image
from projectile import EnemyProjectile


class Enemy:
    def __init__(self,x,y,game_map,enemy_type):
        self.x=float(x)
        self.y=float(y)
        self.map=game_map
        self.path_timer=0
        self.path=[]
        self.seen_before=False
        self.last_seen=None
        self.wander_timer=0
        self.search_duration=210
        self.immunity_frames=0
        self.cooldown=0
        self.enemy_type=enemy_type

        stats=settings.ENEMY_TYPES[enemy_type]
        self.health=stats["health"]
        self.speed=stats["speed"]
        self.damage=stats["damage"]
        self.rect=pygame.Rect(x,y,stats["width"],stats["height"])
        self.image=load_image(stats["image"],stats["width"],stats["height"])
        self.view_radius=stats["view_radius"]

        self.state="wander"
    # def check_collision(self, rect):
    #     left = rect.left//settings.TILE_SIZE
    #     right = (rect.right-1)//settings.TILE_SIZE  # occupies 0-31 tiles hence the -1
    #     top = rect.top//settings.TILE_SIZE
    #     bottom = (rect.bottom-1)//settings.TILE_SIZE
    #     for row in range(top,bottom+1):
    #         for column in range(left,right+1):
    #             if self.map[row][column] == 0:
    #                 return True
    #     return False
    def take_damage(self,damage):
        if self.immunity_frames<=0:
            self.health-=damage
            print(f"enemy new health:{self.health}")
            if self.health<=0:
                self.health=0
            self.immunity_frames=30
            return
        return
    def can_see_player(self,player):
        distance = pygame.Vector2(self.rect.center).distance_to(player.rect.center)  # builtin vector methods to calc distance
        if distance < self.view_radius:
            steps=2*int(distance)+1
            for i in range(steps+1):
                x_parameter=pygame.math.lerp(self.rect.centerx,player.rect.centerx,i/steps)
                y_parameter = pygame.math.lerp(self.rect.centery, player.rect.centery,i/steps)
                tile_x=int(x_parameter//settings.TILE_SIZE)
                tile_y=int(y_parameter//settings.TILE_SIZE)
                if self.map[tile_y][tile_x]!=1:
                    return False
            return True
        return False
    def move(self,dx,dy):
        # new_rect = self.rect.copy()
        # new_rect.x += dx
        # # if not self.check_collision(new_rect):
        # self.rect.x = new_rect.x
        #
        # new_rect = self.rect.copy()
        # new_rect.y += dy
        # # if not self.check_collision(new_rect):
        # self.rect.y = new_rect.y
        self.x+=dx
        self.y+=dy
        self.rect.x=round(self.x)
        self.rect.y=round(self.y)

    def update(self,player):
        if self.cooldown>0:
            self.cooldown-=1
        if self.state=="wander":
            self.wander(player)
        if self.state=="chase":
            self.chase(player)
        if self.state=="search":
            self.search(player)
        if self.immunity_frames>0:
            self.immunity_frames-=1
    def traverse_path(self,path):
        if not path or len(path) <= 1:
            return
        next = path[1]
        target_x = next[0] * settings.TILE_SIZE + settings.TILE_SIZE // 2  # xcoordinate
        target_y = next[1] * settings.TILE_SIZE + settings.TILE_SIZE // 2  # ycoordinate
        direction = pygame.Vector2(target_x - self.rect.centerx, target_y - self.rect.centery)
        if direction.length()==0:
            self.path.pop(0)
            return
        if direction.length()<=self.speed:
            self.x=target_x-self.rect.width/2
            self.y=target_y-self.rect.height/2
            self.rect.x=round(self.x)
            self.rect.y=round(self.y)
            self.path.pop(0)
            return
        # print(direction.length())
        # if 0 < direction.length() < settings.TILE_SIZE/math.sqrt(2):#sqrt(2(32*2)^2)=sqrt()
        #      self.move(direction.x, direction.y)
        #      print("moving less than max speed")
        if direction.length() > 0:  # pythagoras here
            direction = direction.normalize()
            self.move(direction.x * self.speed, direction.y * self.speed)

    def chase(self,player):
        # print("chase start")
        enemy_tile=(self.rect.centerx//settings.TILE_SIZE,self.rect.centery//settings.TILE_SIZE)
        player_tile=(player.rect.centerx//settings.TILE_SIZE,player.rect.centery//settings.TILE_SIZE)
        self.path_timer-=1
        if self.can_see_player(player):
            self.seen_before=True
            self.last_seen = player_tile
            if self.path_timer<0:
                self.path=astar(enemy_tile,player_tile,self.map)#list of tuples
                self.path_timer=15#runs 4 times a second for improved performance
        elif self.seen_before:
            self.state="search"
            self.search_duration=240
            self.path=[]
            return
        self.traverse_path(self.path)

    def search(self,player):
        if self.can_see_player(player):
            self.state="chase"
            return
        # self.search_duration-=1
        # if self.search_duration is not None:
        #     self.state="wander"
        #     return
        # print("search start")
        enemy_tile = (self.rect.centerx // settings.TILE_SIZE, self.rect.centery // settings.TILE_SIZE)
        if enemy_tile==self.last_seen:
            self.state="wander"
            print("arrived at location!!")
            return
        self.path=astar(enemy_tile,self.last_seen,self.map)
        self.traverse_path(self.path)
        target_x=self.last_seen[0]*settings.TILE_SIZE+settings.TILE_SIZE//2
        target_y=self.last_seen[1]*settings.TILE_SIZE+settings.TILE_SIZE//2
        distance = pygame.Vector2(self.rect.centerx,self.rect.centery).distance_to((target_x,target_y))
        # print (distance)
        if distance<=self.speed:
            self.state="wander"
            return
    def wander(self,player):
        self.wander_timer-=1
        if self.can_see_player(player):
            self.state="chase"
            return
        # print("wandering start")
        if self.wander_timer<0:
            enemy_tile=(self.rect.centerx // settings.TILE_SIZE, self.rect.centery // settings.TILE_SIZE)
            possible_tiles=[]
            for x in range(max(0,enemy_tile[0]-5),min(len(self.map[0]),enemy_tile[0]+5)):
                for y in range(max(0,enemy_tile[1]-5),min(len(self.map),enemy_tile[1]+5)):
                    if self.map[y][x]!=0:
                        possible_tiles.append((x,y))
            if possible_tiles:
                target=random.choice(possible_tiles)
                self.path=astar(enemy_tile,target,self.map)
            self.wander_timer=210
        self.traverse_path(self.path)
    def draw(self,window,camera):
        window.blit(self.image,(self.rect.x-camera.x,self.rect.y-camera.y))

class MeleeEnemy(Enemy):
    def attack(self,player):
        if self.cooldown<=0:
            if self.rect.colliderect(player.rect):
                player.take_damage(self.damage)
                self.cooldown=30

class RangeEnemy(Enemy):#
    def __init__(self,x,y,game_map,enemy_type,projectiles):
        super().__init__(x,y,game_map,enemy_type)
        self.projectiles=projectiles
    def attack(self,player):
        if self.cooldown<=0:
            if self.can_see_player(player):
                projectile=EnemyProjectile(
                    self.rect.centerx,self.rect.centery,
                    2,
                    self.damage,
                    player,
                    self.enemy_type
                )
                self.projectiles.append(projectile)
                self.cooldown=60
                print("enemyshoot")

