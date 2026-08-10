import pygame
import settings
from image import load_image
class Enemy:
    def __init__(self,x,y,game_map,enemy_type):
        self.map=game_map
        stats=settings.ENEMY_TYPES[enemy_type]
        self.speed=stats["speed"]
        self.damage=stats["damage"]
        self.rect=pygame.Rect(x,y,stats["width"],stats["height"])
        self.image=load_image(stats["image"],stats["width"],stats["height"])
        self.view_radius=200
        self.state="wander"
    def update(self,player):
        distance=pygame.Vector2(self.rect.center).distance_to(self.rect.center)#builtin vector methods to calc distance
        if distance < self.view_radius:
            self.state="chase"
        else:
            self.state="wander"
        if self.state=="wander":
            self.wander()
        elif self.state=="chase":
            self.chase(player)
    def chase(self,player):
        direction=pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length()>0: #pythagoras here
            direction=direction.normalize()
            self.rect.x+=direction.x*self.speed
            self.rect.y+=direction.y*self.speed
    def wander(self,):
        pass
    def draw(self,window,camera):
        window.blit(self.image,(self.rect.x-camera.x,self.rect.y-camera.y))

