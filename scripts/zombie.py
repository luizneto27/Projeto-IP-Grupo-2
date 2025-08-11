# zombie.py
import pygame
from scripts.constantes import DANO_ZOMBIE, VIDA_ZOMBIE

class Zombie(pygame.sprite.Sprite):
    # criando o zumbi à direita
    def __init__(self, x, y):
        super().__init__()
        self.imagem = pygame.image.load('Imagens/monstrinho_v2.png').convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (80, 80))
        self.rect = self.imagem.get_rect(center=(x, y))
        self.vida = VIDA_ZOMBIE
        self.vida_maxima = VIDA_ZOMBIE
        self.velocidade = 1
        self.dano = DANO_ZOMBIE

    def update(self, player):
        # Move o zumbi em direção ao jogador
        # Movimento no eixo X (horizontal)
        if self.rect.x < player.rect.x:
            self.rect.x += self.velocidade
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.velocidade

        # Movimento no eixo Y (vertical)
        if self.rect.y < player.rect.y:
            self.rect.y += self.velocidade
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.velocidade

    def sofrer_dano(self, qtd):
        self.vida -= qtd
        