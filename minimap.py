import pygame

MINIMAP_SIZE=180
MINIMAP_RADIUS=30
MINIMAP_TILE_SIZE=4
class Minimap:
    def __init__(self,map,tile_size):
        self.map=map
        self.tile_size = tile_size
        self.surface = pygame.Surface((MINIMAP_SIZE,MINIMAP_SIZE))
    def draw(self,window,player):
        self.surface.fill((0,0,0))
        centre_x = player.rect.centerx//self.tile_size
        centre_y = (player.rect.centery+16)//self.tile_size
        for row in range(centre_y-MINIMAP_RADIUS,centre_y+MINIMAP_RADIUS+1):
            for column in range(centre_x-MINIMAP_RADIUS,centre_x+MINIMAP_RADIUS+1):
                if 0<=row<len(self.map) and 0<=column<len(self.map[0]):
                    screen_x=(column-centre_x)*MINIMAP_TILE_SIZE
                    screen_y=(row-centre_y)*MINIMAP_TILE_SIZE
                    screen_x+=MINIMAP_SIZE//2
                    screen_y+=MINIMAP_SIZE//2
                    if self.map[row][column]==0:
                        colour=(50,50,50)
                    if self.map[row][column]==1:
                        colour=(100,100,100)
                    pygame.draw.rect(self.surface,colour,(screen_x,screen_y,MINIMAP_TILE_SIZE,MINIMAP_TILE_SIZE))
        pygame.draw.circle(self.surface,
                           (255,0,0),
                           (MINIMAP_SIZE//2,MINIMAP_SIZE//2),
                           3)
        window.blit(self.surface,(600,20))



