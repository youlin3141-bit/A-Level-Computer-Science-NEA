import pygame

from game import TILE_SIZE
PLAYER_SIZE=48
SPEED=5
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
        self.player_up=pygame.image.load("assets/player_up.png").convert_alpha()
        self.player_down=pygame.image.load("assets/player_down.png").convert_alpha()
        self.player_right=pygame.image.load("assets/player_right.png").convert_alpha()
        self.player_left=pygame.image.load("assets/player_left.png").convert_alpha()
        self.player_down_right=pygame.image.load("assets/player_down_right.png").convert_alpha()
        self.player_down_left=pygame.image.load("assets/player_down_left.png").convert_alpha()
        self.player_up_right=pygame.image.load("assets/player_up_right.png").convert_alpha()
        self.player_up_left=pygame.image.load("assets/player_up_left.png").convert_alpha()
        #resize scaled sprites
        self.player_down_right=pygame.transform.scale(self.player_down_right,(PLAYER_SIZE,PLAYER_SIZE))
        self.player_down_left=pygame.transform.scale(self.player_down_left,(PLAYER_SIZE,PLAYER_SIZE))
        self.player_up_right=pygame.transform.scale(self.player_up_right,(PLAYER_SIZE,PLAYER_SIZE))
        self.player_up_left=pygame.transform.scale(self.player_up_left,(PLAYER_SIZE,PLAYER_SIZE))
        self.player_left=pygame.transform.scale(self.player_left,(PLAYER_SIZE,PLAYER_SIZE))
        self.player_up=pygame.transform.scale(self.player_up,(PLAYER_SIZE,PLAYER_SIZE))
        self.player_down=pygame.transform.scale(self.player_down,(PLAYER_SIZE,PLAYER_SIZE))
        self.player_right=pygame.transform.scale(self.player_right,(PLAYER_SIZE,PLAYER_SIZE))
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
            left=rect.left//TILE_SIZE
            right=(rect.right-1)//TILE_SIZE#occupies 0-31 tiles hence the -1
            top=rect.top//TILE_SIZE
            bottom=(rect.bottom-1)//TILE_SIZE
            for row in range(top,bottom+1):
                for column in range(left,right+1):
                    print(self.x//TILE_SIZE,self.y//TILE_SIZE,row,column)
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
