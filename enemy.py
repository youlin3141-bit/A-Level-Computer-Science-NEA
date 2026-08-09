import pygame
from image import load_image
class Enemy:
    def __init__(self,x,y,game_map,width,height,name,image):
        self.map=game_map
        self.name=name
        self.rect=pygame.Rect(x,y,width,height)
        self.image=load_image(image,width,height)
    def update(self):
        pass
    def draw(self,window,camera):
        window.blit(self.image,(self.rect.x-camera.x,self.rect.y-camera.y))

