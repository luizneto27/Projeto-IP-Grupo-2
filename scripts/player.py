# player.py
import pygame
from scripts.projeteis import Projetil
from scripts.constantes import VIDA_PLAYER, VELOCIDADE_PLAYER, MUNICAO_INICIAL_PLAYER, MOEDAS_INICIAIS_PLAYER, KITMEDS_INICIAIS_PLAYER

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagem_original = pygame.image.load('Imagens/soldado_comum_parado.png').convert_alpha()
        self.imagem_original = pygame.transform.scale(self.imagem_original, (100, 100))
        self.imagem = self.imagem_original
        self.rect = self.imagem.get_rect(center=(x, y))

        self.vida = VIDA_PLAYER
        self.vida_maxima = VIDA_PLAYER
        self.municao = MUNICAO_INICIAL_PLAYER
        self.moedas = MOEDAS_INICIAIS_PLAYER
        self.kitmeds = KITMEDS_INICIAIS_PLAYER

        self.direcao = 1 # 1 para direita, -1 para esquerda
        self.velocidade = VELOCIDADE_PLAYER

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
            self.direcao = -1 # Atualiza a direção
            self.imagem = pygame.transform.flip(self.imagem_original, True, False) # Vira a imagem
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
            self.direcao = 1 # Atualiza a direção
            self.imagem = self.imagem_original # Imagem original
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

    def atirar(self,grupos_inimigos, grupo_obstaculos, grupo_coletaveis, grupo_todos_sprites):
        if self.municao > 0:
            self.municao -= 1
            return Projetil(self.rect.centerx, self.rect.centery, self.direcao, grupos_inimigos, grupo_obstaculos, grupo_coletaveis, grupo_todos_sprites)
        return None

    def coletar(self, item):
        if item.type == 'kitmedico':
            self.kitmeds += 1 # Adiciona ao inventário
        elif item.type == 'moeda':
            self.moedas += 1
        elif item.type == 'municao':
            self.municao += 20
        item.kill()

    #Método para usar o kit médico
    def usar_kitmed(self):
        if self.kitmeds > 0 and self.vida < VIDA_PLAYER:
            self.kitmeds -= 1
            self.vida += 25
            if self.vida > VIDA_PLAYER:
                self.vida = VIDA_PLAYER

    def sofrer_dano(self, qtd):
        self.vida -= qtd
        if self.vida <= 0:
            self.kill()