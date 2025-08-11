#projeteis.py
import pygame
from scripts.constantes import VELOCIDADE_PROJETIL, DANO_PROJETIL

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, grupo_inimigos, grupo_obstaculos, grupo_coletaveis, grupo_todos_sprites):
        super().__init__()
        self.imagem = pygame.Surface((15, 5)) # Aparência da bala
        self.imagem.fill((255, 255, 0)) # Cor da bala
        self.rect = self.imagem.get_rect(center=(x, y))
        self.velocidade = VELOCIDADE_PROJETIL
        self.direcao = direcao # 1 para direita, -1 para esquerda
        self.grupo_inimigos = grupo_inimigos
        self.grupo_obstaculos = grupo_obstaculos
        self.grupo_coletaveis = grupo_coletaveis
        self.grupo_todos_sprites = grupo_todos_sprites

    def update(self):
        # O projétil se move apenas na horizontal e na direção do jogador
        self.rect.x += self.velocidade * self.direcao

        # Remove o projétil se ele sair da tela para não consumir memória
        if self.rect.left > 2500 or self.rect.right < 0:
            self.kill()

        # Colisão com inimigos
        # Usamos spritecollide com True para matar o projétil e False para não matar o inimigo
        inimigos_colididos = pygame.sprite.spritecollide(self, self.grupo_inimigos, False)
        if inimigos_colididos:
            for inimigo in inimigos_colididos:
                inimigo.sofrer_dano(DANO_PROJETIL)
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
            self.kill()
            return
        