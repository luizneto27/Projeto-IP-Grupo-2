#projeteis.py
import pygame
from scripts.constantes import BULLET_SPEED, BULLET_DAMAGE

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, enemies_group, obstacles_group, collectibles_group, all_sprites_group):
        super().__init__()
        self.image = pygame.Surface((15, 5)) # Aparência da bala
        self.image.fill((255, 255, 0)) # Cor da bala
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED
        self.direction = direction # 1 para direita, -1 para esquerda
        self.enemies_group = enemies_group
        self.obstacles_group = obstacles_group
        self.collectibles_group = collectibles_group
        self.all_sprites_group = all_sprites_group

    def update(self):
        # O projétil se move apenas na horizontal e na direção do jogador
        self.rect.x += self.speed * self.direction

        # Remove o projétil se ele sair da tela para não consumir memória
        if self.rect.left > 2500 or self.rect.right < 0:
            self.kill()

        # Colisão com inimigos
        for enemy in pygame.sprite.spritecollide(self, self.enemies_group, False):
            enemy.take_damage(BULLET_DAMAGE)
            self.kill()
            return

        # Colisão com obstáculos
        for obstacle in pygame.sprite.spritecollide(self, self.obstacles_group, False):
            if obstacle.take_damage(BULLET_DAMAGE):
                item = obstacle.drop_item()
                if item:
                    obstacle.kill()
                    self.obstacles_group.add(item)  # será adicionado no Game
            self.kill()
            return