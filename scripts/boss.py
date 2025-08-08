# scripts/boss.py
import pygame
from scripts.coletaveis import Sangue

class Boss(pygame.sprite.Sprite):
    def __init__(self, vida_total, pos_x, pos_y, dano):
        super().__init__()

        self.image = pygame.image.load(r'Imagens/baron_1.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 400))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.vida_total = vida_total
        self.vida_atual = vida_total
        self.dano = dano
    
    def update(self):
        # A lógica de invocar monstros será controlada pelo game.py
        pass

    def draw(self, tela):
        tela.blit(self.image, self.rect)
        # Desenha a barra de vida do Boss
        barra_vida_largura_total = 400
        barra_vida_altura = 20
        pos_x_barra = (tela.get_width() - barra_vida_largura_total) / 2
        
        pygame.draw.rect(tela, (255,0,0), (pos_x_barra, 20, barra_vida_largura_total, barra_vida_altura))
        
        barra_vida_largura_atual = barra_vida_largura_total * (self.vida_atual / self.vida_total)
        if barra_vida_largura_atual > 0:
            pygame.draw.rect(tela, (0,255,0), (pos_x_barra, 20, barra_vida_largura_atual, barra_vida_altura))

    def levar_dano(self, quantidade):
        self.vida_atual -= quantidade
        if self.vida_atual < 0:
            self.vida_atual = 0
        # Dropar sangue ao ser atingido
        return Sangue(self.rect.centerx - 50, self.rect.centery)

    def esta_vivo(self):
        return self.vida_atual > 0