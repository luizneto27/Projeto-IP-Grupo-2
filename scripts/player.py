# player.py
import pygame
from scripts.projeteis import Projetil
from scripts.constantes import PLAYER_HEALTH, PLAYER_SPEED, PLAYER_START_AMMO, PLAYER_START_COINS, PLAYER_START_MEDKITS

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_original = pygame.image.load('Imagens/soldado_comum_parado.png').convert_alpha()
        self.image_original = pygame.transform.scale(self.image_original, (100, 100))
        self.image = self.image_original
        self.rect = self.image.get_rect(center=(x, y))

        self.health = PLAYER_HEALTH
        self.ammo = PLAYER_START_AMMO
        self.coins = PLAYER_START_COINS
        self.medkits = PLAYER_START_MEDKITS

        self.direction = 1 # 1 para direita, -1 para esquerda
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1 # Atualiza a direção
            self.image = pygame.transform.flip(self.image_original, True, False) # Vira a imagem
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1 # Atualiza a direção
            self.image = self.image_original # Imagem original
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def shoot(self,enemies_group, obstacles_group, collectibles_group, all_sprites_group):
        if self.ammo > 0:
            self.ammo -= 1
            return Projetil(self.rect.centerx, self.rect.centery, self.direction, enemies_group, obstacles_group, collectibles_group, all_sprites_group)
        return None

    def collect(self, item):
        if item.type == 'kitmedico':
            self.medkits += 1 # Adiciona ao inventário
        elif item.type == 'moeda':
            self.coins += 1
        elif item.type == 'municao':
            self.ammo += 20
        item.kill()

    #Método para usar o kit médico
    def use_medkit(self):
        if self.medkits > 0 and self.health < PLAYER_HEALTH:
            self.medkits -= 1
            self.health += 25
            if self.health > PLAYER_HEALTH:
                self.health = PLAYER_HEALTH

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()