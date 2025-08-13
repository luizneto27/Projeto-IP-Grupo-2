#projeteis.py
import pygame
import random
from scripts.constantes import VELOCIDADE_PROJETIL, DANO_PROJETIL

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, grupo_inimigos, grupo_obstaculos, grupo_coletaveis, grupo_todos_sprites, grupo_particulas):
        super().__init__()
        self.imagem = pygame.Surface((20, 8), pygame.SRCALPHA) # Aparência da bala
        # Desenha uma elipse amarela para um efeito mais orgânico e visualmente atraente
        pygame.draw.ellipse(self.imagem, (255, 220, 0), self.imagem.get_rect())

        # Vira a imagem se a direção for para a esquerda
        if direcao == -1:
            self.imagem = pygame.transform.flip(self.imagem, True, False)

        self.rect = self.imagem.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_PROJETIL
        self.direcao = direcao # 1 para direita, -1 para esquerda
        self.grupo_inimigos = grupo_inimigos
        self.grupo_obstaculos = grupo_obstaculos
        self.grupo_coletaveis = grupo_coletaveis
        self.grupo_todos_sprites = grupo_todos_sprites
        self.grupo_particulas = grupo_particulas

    def update(self):
        # O projétil se move apenas na horizontal e na direção do jogador
        self.rect.x += self.velocidade * self.direcao

        # Remove o projétil se ele sair da tela 
        if self.rect.left > 4000 or self.rect.right < 0:
            self.kill()

        # Colisão com inimigos
        # Usamos spritecollide com True para matar o projétil e False para não matar o inimigo
        inimigos_colididos = pygame.sprite.spritecollide(self, self.grupo_inimigos, False)
        if inimigos_colididos:
            for inimigo in inimigos_colididos:
                inimigo.sofrer_dano(DANO_PROJETIL)
                self.criar_efeito_impacto()
            self.kill() # Destrói o projétil
            return

        # Colisão com obstáculos
        for obstaculo in pygame.sprite.spritecollide(self, self.grupo_obstaculos, False):
            if obstaculo.sofrer_dano(DANO_PROJETIL):
                item = obstaculo.dropar_item()
                if item:
                    # Adiciona o item ao grupo de coletáveis e a todos os sprites
                    self.grupo_coletaveis.add(item)
                    self.grupo_todos_sprites.add(item)
            self.criar_efeito_impacto()
            self.kill()
            return
        
    def criar_efeito_impacto(self):
        # cria particulas de bala no objeto atingido
        for i in range(random.randint(5, 10)):
            particula = ParticulaImpacto(self.rect.centerx, self.rect.centery)
            self.grupo_particulas.add(particula)
            self.grupo_todos_sprites.add(particula)

class ParticulaImpacto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.raio = random.uniform(1.0, 4.0)
        # Escolhe cores quentes para o efeito de faísca/explosão
        cor = random.choice([(255,50,50), (255,150,0), (255,255,100)])
        self.imagem_original = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.imagem_original, cor, (self.raio, self.raio), self.raio)
        self.imagem = self.imagem_original
        self.rect = self.imagem.get_rect(center=(x,y))
        
        self.velocidade_x = random.uniform(-3, 3)
        self.velocidade_y = random.uniform(-3, 3)
        self.vida_util = 15 # A partícula dura por 15 frames

    def update(self):
        # Movimenta a partícula
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        self.vida_util -= 1
        
        # Reduz o tamanho da partícula ao longo do tempo para um efeito de desaparecimento
        escala = self.vida_util / 15
        if escala < 0: escala = 0
        
        center = self.rect.center
        nova_largura = int(self.raio * 2 * escala)
        nova_altura = int(self.raio * 2 * escala)

        # Garante que a superfície não seja de tamanho zero
        if nova_largura > 0 and nova_altura > 0:
            self.imagem = pygame.transform.scale(self.imagem_original, (nova_largura, nova_altura))
            self.rect = self.imagem.get_rect(center=center)

        # Remove a partícula quando sua vida útil acabar
        if self.vida_util <= 0:
            self.kill()