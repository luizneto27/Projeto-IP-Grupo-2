# tank_zombie.py
import pygame
from scripts.zombie import Zombie
from scripts.constantes import VIDA_ZUMBI_TANQUE, VELOCIDADE_ZUMBI_TANQUE, DANO_ZUMBI_TANQUE

class ZombieTank(Zombie):
    def __init__(self, x, y):
        # Chama o __init__ da classe pai (Zombie) para aproveitar o código
        super().__init__(x, y)

        self.imagem = pygame.image.load('Imagens/monstrinho_v2.png').convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (120, 120))
        self.rect = self.imagem.get_rect(center=(x, y))

        self.vida = VIDA_ZUMBI_TANQUE
        self.vida_maxima = VIDA_ZUMBI_TANQUE
        self.velocidade = VELOCIDADE_ZUMBI_TANQUE
        self.dano = DANO_ZUMBI_TANQUE