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
        # Usamos spritecollide com True para matar o projétil e False para não matar o inimigo
        collided_enemies = pygame.sprite.spritecollide(self, self.enemies_group, False)
        if collided_enemies:
            for enemy in collided_enemies:
                enemy.take_damage(BULLET_DAMAGE)
            self.kill() # Destrói o projétil
            return

        # o erro com o tiro no onibus vem daqui ->
        # Colisão com obstáculos
        for obstacle in pygame.sprite.spritecollide(self, self.obstacles_group, False):
            if obstacle.take_damage(BULLET_DAMAGE):
                item = obstacle.drop_item()
                if item:
                    # Adiciona o item ao grupo de coletáveis e a todos os sprites
                    self.collectibles_group.add(item)
                    self.all_sprites_group.add(item)
            self.kill()
            return
        