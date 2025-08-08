# scripts/monstrinhos.py
import pygame
from scripts.coletaveis import Arma

class Monstrinho(pygame.sprite.Sprite):
    def __init__(self, vida_total, pos_x, pos_y, dano, velocidade):
        super().__init__()
        
        self.image = pygame.image.load(r'Imagens/monstrinho_v2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        # Garante o alinhamento vertical perfeito na fileira
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.vida_total = vida_total
        self.vida_atual = vida_total
        self.dano = dano
        self.velocidade = velocidade
        
        # NOVO: Define um alcance mínimo para o ataque corpo a corpo
        self.alcance = 5 
        
        self.alvo_em_combate = None

    # ALTERADO: Lógica de ataque por proximidade, não mais por colisão
    def update(self, soldados_na_linha):
        self.alvo_em_combate = None
        
        # 1. ENCONTRAR O ALVO MAIS PRÓXIMO NA FRENTE
        alvo_potencial = None
        menor_distancia = float('inf')

        for soldado in soldados_na_linha:
            # Calcula a distância entre a frente do monstro e a traseira do soldado
            distancia = self.rect.left - soldado.rect.right
            
            # Se o soldado está na frente e mais perto que os outros
            if 0 <= distancia < menor_distancia:
                menor_distancia = distancia
                alvo_potencial = soldado
        
        # 2. VERIFICAR SE O ALVO MAIS PRÓXIMO ESTÁ NO ALCANCE
        if alvo_potencial and menor_distancia <= self.alcance:
            self.alvo_em_combate = alvo_potencial

        # 3. DECIDIR A AÇÃO: ATACAR OU MOVER
        if self.alvo_em_combate:
            # Se encontrou um alvo no alcance, PARA de mover e ataca
            self.alvo_em_combate.levar_dano(self.dano)
        else:
            # Se não há alvo no alcance, continua andando para a esquerda
            self.rect.x -= self.velocidade

    def draw(self, tela):
        # A imagem já é desenhada pelo loop em game.py, aqui só a barra de vida
        if self.vida_atual < self.vida_total:
            pygame.draw.rect(tela, (255,0,0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            barra_vida_largura = self.rect.width * (self.vida_atual / self.vida_total)
            pygame.draw.rect(tela, (0,255,0), (self.rect.x, self.rect.y - 10, barra_vida_largura, 5))

    def levar_dano(self, quantidade):
        self.vida_atual -= quantidade
        if self.vida_atual <= 0:
            self.kill() 
            return Arma(self.rect.centerx, self.rect.centery)
        return None

    def esta_vivo(self):
        return self.vida_atual > 0