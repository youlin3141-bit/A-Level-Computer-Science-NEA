import pygame
import settings
from image import load_image
class Projectile:
    def __init__(self,x,y,speed,damage):
        self.x=float(x)
        self.y=float(y)
        self.speed=speed
        self.damage=damage
        self.rect=pygame.Rect(x,y,10,10)
        self.projectile_timer=120
    def update(self):
        pass


class PlayerProjectile(Projectile):
    def __init__(self,x,y,speed,damage,projectile_image,direction,enemies,damage_upgrade):
        super().__init__(x,y,speed,damage)
        self.image=load_image(projectile_image,10,10)
        self.direction=direction.normalize()
        self.damage_upgrade=damage_upgrade
        self.enemies=enemies
    def update(self):
        self.x+=self.direction.x* self.speed
        self.y+=self.direction.y* self.speed
        self.rect.center=round(self.x),round(self.y)
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage+self.damage_upgrade)
    def get_hitbox(self,):
        return pygame.Rect(
            self.rect.x,
            self.rect.y,
            10,10
        )
    def draw(self,window,camera):
        window.blit(self.image,(self.rect.x-camera.x,self.rect.y-camera.y))

class EnemyProjectile(Projectile):
    def __init__(self,x,y,speed,damage,target,enemy_type):
        super().__init__(x,y,speed,damage)
        self.target=target
        self.projectile_timer=300
        self.image = load_image(settings.ENEMY_TYPES[enemy_type]["projectile_image"], 10, 10)
        direction = pygame.Vector2(target.rect.centerx - x, target.rect.centery - y)
        if direction.length() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)  # distance =0
    def update(self):
        self.x +=  self.direction.x* self.speed
        self.y += self.direction.y * self.speed
        self.rect.center = (round(self.x), round(self.y))
        if self.rect.colliderect(self.target.rect):
            self.target.take_damage(self.damage)
    def draw(self,window,camera):
        window.blit(self.image,(self.rect.x-camera.x,self.rect.y-camera.y))
