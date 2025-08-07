# scripts/monstrinhos.py
import pygame
from scripts.coletaveis import Arma # NOVO

class Monstrinho(pygame.sprite.Sprite): # NOVO: Herda de pygame.sprite.Sprite
    def __init__(self, vida_total, pos_x, pos_y, dano, velocidade):
        super().__init__() # NOVO: Inicializador do Sprite
        
        self.image = pygame.image.load('Imagens/monster_slither_attack_slow.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        self.vida_total = vida_total
        self.vida_atual = vida_total
        self.dano = dano
        self.velocidade = velocidade
        self.alvo_atacando = None

    def update(self, soldados_na_linha):
        self.alvo_atacando = None
        # Verifica colisão com soldados
        for soldado in soldados_na_linha:
            if self.rect.colliderect(soldado.rect):
                self.alvo_atacando = soldado
                break
        
        if self.alvo_atacando:
            # Se colidiu, ataca o soldado
            self.alvo_atacando.levar_dano(self.dano)
        else:
            # Se não, continua andando
            self.rect.x -= self.velocidade

    def draw(self, tela):
        tela.blit(self.image, self.rect)
        # NOVO: Desenha a barra de vida
        if self.vida_atual < self.vida_total:
            pygame.draw.rect(tela, (255,0,0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            barra_vida_largura = self.rect.width * (self.vida_atual / self.vida_total)
            pygame.draw.rect(tela, (0,255,0), (self.rect.x, self.rect.y - 10, barra_vida_largura, 5))

    def levar_dano(self, quantidade): # NOVO
        self.vida_atual -= quantidade
        if self.vida_atual <= 0:
            self.kill() # Remove o monstro dos grupos
            # Retorna o item dropado ao morrer
            return Arma(self.rect.centerx, self.rect.centery)
        return None

    def esta_vivo(self):
        return self.vida_atual > 0