from image import load_image
import pygame
from projectile import PlayerProjectile
class Items:
    def __init__(self,name,damage,image,cooldown):
        self.name = name
        self.damage=damage
        self.image=image
        self.cooldown=cooldown
        self.flash_timer=0
    def use(self):
        pass
    def update(self):#
        if self.cooldown>=0:
            self.cooldown-=1

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


class Mace(Items):
    def __init__(self,player,enemies):
        self.player = player
        self.enemies=enemies
        self.damage=20
        super().__init__("Mace",
                         self.damage,
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
            return False
        if self.cooldown<=0:
            print(f"melee attack")
            self.flash_timer=5
            for enemy in self.enemies:
                if enemy.rect.colliderect(self.get_hitbox()):
                    enemy.take_damage(self.damage+self.player.damage_upgrade)
            self.cooldown = 30
            return True
        return False

class SpellBook(Items):
    def __init__(self,player,enemies,projectiles_list):
        self.player=player
        self.enemies=enemies
        self.projectiles=[]
        self.directions=[]
        self.projectiles_list=projectiles_list
        self.damage=10
        super().__init__("SpellBook",
                         self.damage,
                         load_image("assets/spellbook.png",60,60),0)
    def use(self):
        if self.cooldown>0:
            return
        if self.cooldown<=0:
            print(f"ranged attack")
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    direction=pygame.Vector2(x,y)
                    new_proj = PlayerProjectile(self.player.rect.centerx,
                                                self.player.rect.centery,
                                                2,10,
                                                "assets/spellbookprojectile.png",
                                                direction,
                                                self.enemies,
                                                self.player.damage_upgrade)
                    self.projectiles.append(new_proj)
                    self.projectiles_list.append(new_proj)
            self.cooldown = 30
    # def get_hitbox(self,projectile):
    #     return pygame.Rect(
    #         projectile.rect.x,
    #         projectile.rect.y,
    #         10,10
    #     )

    def draw_hitbox(self,window,camera):
        # for projectile in self.projectiles:
        #     window.blit(self.image,(projectile.x-camera.x,projectile.y-camera.y))
        pass