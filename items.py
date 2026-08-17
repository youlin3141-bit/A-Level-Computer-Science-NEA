from image import load_image
import pygame
class Items:
    def __init__(self,name,damage,image,cooldown):
        self.name = name
        self.damage=damage
        self.image=image
        self.cooldown=cooldown
    def use(self):
        pass

    def draw_hitbox(self, window, camera):
        hitbox = self.get_hitbox()

        pygame.draw.rect(
            window,
            (255, 0, 0),
            pygame.Rect(
                hitbox.x - camera.x,
                hitbox.y - camera.y,
                hitbox.width,
                hitbox.height),
            2
        )
    def update(self):#
        if self.cooldown>=0:
            self.cooldown-=1
class Mace(Items):
    def __init__(self,player,enemies):
        self.player = player
        self.enemies=enemies
        super().__init__("Mace",
                         30,
                         load_image("assets/mace.png",60,60),0)
    def get_hitbox(self):
        return pygame.Rect(
        self.player.rect.x-50,
        self.player.rect.y-50,
        self.player.rect.width+100,
        self.player.rect.height+100
        )


    def use(self):
        if self.cooldown>0:
            return
        if self.cooldown<=0:
            print(f"attack")
            for enemy in self.enemies:
                if enemy.rect.colliderect(self.get_hitbox()):
                    enemy.take_damage(self.damage)
            self.cooldown = 30