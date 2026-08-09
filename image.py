import pygame
def load_image(image,width,height):
    name = pygame.image.load(image).convert_alpha()
    return pygame.transform.scale(name,(width,height))
