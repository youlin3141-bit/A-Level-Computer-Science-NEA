import pygame
from image import load_image
import settings
PLAYER_SIZE=48
SPEED=10
class Player:
    def __init__(self,x,y,game_map):
        self.x = x
        self.y = y
        self.rect=pygame.Rect(x,y,PLAYER_SIZE,PLAYER_SIZE)
        self.speed=SPEED
        self.score=0
        self.items=[]
        self.currency=0
        self.map=game_map
        #directional player sprites
        self.player_up=load_image("assets/player_up.png",PLAYER_SIZE,PLAYER_SIZE)
        self.player_down=load_image("assets/player_down.png",PLAYER_SIZE,PLAYER_SIZE)
        self.player_right=load_image("assets/player_right.png",PLAYER_SIZE,PLAYER_SIZE)
        self.player_left=load_image("assets/player_left.png",PLAYER_SIZE,PLAYER_SIZE)
        self.player_down_right=load_image("assets/player_down_right.png",PLAYER_SIZE,PLAYER_SIZE)
        self.player_down_left=load_image( "assets/player_down_left.png",PLAYER_SIZE,PLAYER_SIZE)
        self.player_up_right=load_image("assets/player_up_right.png",PLAYER_SIZE,PLAYER_SIZE)
        self.player_up_left=load_image( "assets/player_up_left.png",PLAYER_SIZE,PLAYER_SIZE)
        self.image=self.player_down

    def handle_input(self):
        key = pygame.key.get_pressed()#returns list of bool
        direction = [
            key[pygame.K_w] and not key[pygame.K_a] and not key[pygame.K_d] and not key[pygame.K_s],
            key[pygame.K_w] and key[pygame.K_d],
            key[pygame.K_d] and not key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_a],
            key[pygame.K_d] and key[pygame.K_s],
            key[pygame.K_s] and not key[pygame.K_d] and not key[pygame.K_a] and not key[pygame.K_w],
            key[pygame.K_s] and key[pygame.K_a],
            key[pygame.K_a] and not key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_d],
            key[pygame.K_a] and key[pygame.K_w]
        ]
        dx=0
        dy=0
        if key[pygame.K_w]:  #checks the index of the list (true = key pressed)
            dy-=self.speed
        if key[pygame.K_s]:
            dy+=self.speed
        if key[pygame.K_a]:
            dx-=self.speed
        if key[pygame.K_d]:
            dx+=self.speed
        def check_collision(self,rect):
            left=rect.left//settings.TILE_SIZE
            right=(rect.right-1)//settings.TILE_SIZE#occupies 0-31 tiles hence the -1
            top=rect.top//settings.TILE_SIZE
            bottom=(rect.bottom-1)//settings.TILE_SIZE
            for row in range(top,bottom+1):
                for column in range(left,right+1):
                    # print(self.x//settings.TILE_SIZE,self.y//settings.TILE_SIZE,row,column)
                    if self.map[row][column] == 0:
                        return True
            return False
        new_rect=self.rect.copy()
        new_rect.x+=dx
        if not check_collision(self,new_rect):
            self.rect.x=new_rect.x
        new_rect=self.rect.copy()
        new_rect.y+=dy
        if not check_collision(self,new_rect):
            self.rect.y=new_rect.y
        self.x=new_rect.x
        self.y=new_rect.y
        if direction[0]: self.image=self.player_up
        if direction[1]: self.image=self.player_up_right
        if direction[2]: self.image=self.player_right
        if direction[3]: self.image=self.player_down_right
        if direction[4]: self.image=self.player_down
        if direction[5]: self.image=self.player_down_left
        if direction[6]: self.image=self.player_left
        if direction[7]: self.image=self.player_up_left
        if direction[1] or direction[3] or direction[5] or direction[7]:
            self.speed=int(SPEED/(1.2)) # this makes diagonal speed seem relatively tedious and slow
            pass
        else:
            self.speed=SPEED
