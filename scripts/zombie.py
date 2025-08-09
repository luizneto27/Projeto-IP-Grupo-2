# zombie.py
import pygame

class Zombie(pygame.sprite.Sprite):
    # criando o zumbi à direita
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Imagens/monstrinho_v2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 50
        self.speed = 1

    def update(self, player):
        # Move o zumbi em direção ao jogador

        # Movimento no eixo X (horizontal)
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        # Movimento no eixo Y (vertical)
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

    def take_damage(self, amount):
        self.health -= amount
        