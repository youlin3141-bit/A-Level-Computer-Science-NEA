import pygame


class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed=5
        self.score=0
        self.items=[]
        self.currency=0
        self.image=pygame.image.load("player.png").convert_alpha()
    def handle_input(self):
        key = pygame.key.get_pressed()#returns list of bool
        if key[pygame.K_w]:  #checks the index of the list (true = key pressed)
            self.y=self.y-self.speed
        if key[pygame.K_s]:
            self.y=self.y+self.speed
        if key[pygame.K_a]:
            self.x=self.x-self.speed
        if key[pygame.K_d]:
            self.x=self.x+self.speed

