import pygame
import settings
from image import load_image
class Exit:
    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,settings.TILE_SIZE*2,settings.TILE_SIZE*3)
        self.active=False
    def draw(self,window,camera):
        if self.active:
            image=load_image("assets/active_exit.png",settings.TILE_SIZE*2,settings.TILE_SIZE*3)
        else:
            image=load_image("assets/inactive_exit.png",settings.TILE_SIZE*2,settings.TILE_SIZE*3)
        screen_x=self.rect.x-camera.x
        screen_y=self.rect.y-camera.y
        window.blit(image,(screen_x,screen_y))
    def update(self,player):
        if self.active and self.rect.colliderect(player.rect):
            return True
        return False

class Generator:
    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,4*settings.TILE_SIZE,4*settings.TILE_SIZE)
        self.x=x
        self.y=y
        self.active=False
        self.e_pressed=False
    def update(self,player):
        key = pygame.key.get_pressed()
        if self.rect.colliderect(player.rect):
            if key[pygame.K_e] and not self.e_pressed:
                self.active= not self.active
        self.e_pressed=key[pygame.K_e]

    def draw(self,window,camera,player):
        if self.active:
            image=load_image("assets/active_gen.png",2*settings.TILE_SIZE,2*settings.TILE_SIZE)
        else:
            image=load_image("assets/inactive_gen.png",2*settings.TILE_SIZE,2*settings.TILE_SIZE)
        screen_x=self.rect.x-camera.x+settings.TILE_SIZE
        screen_y=self.rect.y-camera.y+settings.TILE_SIZE
        window.blit(image,(screen_x,screen_y))
        if self.rect.colliderect(player.rect):
            if not self.active:
                message="E to Activate"
            else:
                message="Generator is Active"
            font=pygame.font.SysFont("Arial",15)
            text=font.render(message,True,(255,255,255))
            window.blit(text,(screen_x,screen_y+2*settings.TILE_SIZE))