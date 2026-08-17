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
        self.immunity_frames=0

        self.score=0
        self.items=[None,None,None]
        self.item_index=0
        self.currency=0
        self.lives=0 #changes depend on diffculty
        self.max_health=100
        self.current_item=self.items[0]
        self.health=self.max_health
        self.xp=0

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
    def take_damage(self, damage):
        if self.health-damage>0:
            self.health-=damage
            return
        else:
            self.health=0
            #you died!
            return
    def draw_health_bar(self,window):
        if self.health<0:
            self.health=0
        bar_width=130
        bar_height=10
        font=pygame.font.SysFont("Arial",20)
        text=font.render(f"Health: {self.health}/{self.max_health}",True,(255,255,255))
        x = 20
        y = 50
        pygame.draw.rect(window,(200,200,200),(x-2,y-2,bar_width+4,bar_height+4))
        pygame.draw.rect(window, (100,100,100), (x, y, bar_width, bar_height))
        window.blit(text,(20,20))
        bar_ratio=self.health/self.max_health
        pygame.draw.rect(window,(0,200,0),(x,y,bar_width*bar_ratio,bar_height))
        return
    def draw_inventory(self,window):
        slot_size=60
        slot_gap=10
        start_x=300
        start_y=510
        for i in range (3):
            if self.items[i]:
                window.blit(self.items[i].image,(start_x+i*(slot_size+slot_gap),start_y,))
            pygame.draw.rect(
                window,
                (100,100,100),
                (start_x+i*(slot_size+slot_gap),start_y,slot_size,slot_size),2#300-360, 370-430, 440-500

            )
        index=self.item_index
        pygame.draw.rect(
            window,
            (255,0,0),
            (start_x + index * (slot_size + slot_gap), start_y, slot_size, slot_size), 3  # 300-360, 370-430, 440-500

        )
    def check_collision(self, rect):
        left = rect.left // settings.TILE_SIZE
        right = (rect.right-1)//settings.TILE_SIZE  # occupies 0-31 tiles hence the -1
        top = rect.top//settings.TILE_SIZE
        bottom = (rect.bottom-1)//settings.TILE_SIZE
        for row in range(top,bottom+1):
            for column in range(left,right+1):
                if self.map[row][column] == 0:
                    return True
        return False
    def handle_input(self):
        key = pygame.key.get_pressed()#returns list of bool
        mouse=pygame.mouse.get_pressed()
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

        new_rect=self.rect.copy()
        new_rect.x+=dx
        if not self.check_collision(new_rect):
            self.rect.x=new_rect.x
        new_rect=self.rect.copy()
        new_rect.y+=dy
        if not self.check_collision(new_rect):
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

        for item in self.items:
            if item:
                item.update()
        if key[pygame.K_1]:
            self.item_index=0
        if key[pygame.K_2]:
            self.item_index=1
        if key[pygame.K_3]:
            self.item_index=2
        self.current_item=self.items[self.item_index]
        if self.current_item and (key[pygame.K_SPACE] or mouse[0]):
            self.current_item.use()
