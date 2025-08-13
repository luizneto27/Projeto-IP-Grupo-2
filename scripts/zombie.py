# zombie.py
import pygame
from scripts.constantes import DANO_ZOMBIE, VIDA_ZOMBIE

class Zombie(pygame.sprite.Sprite):
    # criando o zumbi à direita
    def __init__(self, x, y):
        super().__init__()
        # 1. Carregue a nova imagem. Sugiro salvá-la como 'zumbi_movimento.png' na pasta Imagens.
        self.spritesheet = pygame.image.load('Imagens/zumbi.png').convert_alpha()
        
        self.frames = []
        
        # Em vez de calcular, definimos o tamanho exato de um quadro.
        # Esta é a correção principal para evitar o erro de dimensionamento.
        FRAME_LARGURA = 72 
        FRAME_ALTURA = 72  

        # Extrai os 6 frames da primeira linha
        for j in range(6):
            # Usamos os valores definidos manualmente para o recorte
            frame = self.spritesheet.subsurface((j * FRAME_LARGURA, 0, FRAME_LARGURA, FRAME_ALTURA))
            frame_redimensionado = pygame.transform.scale(frame, (80, 80))
            self.frames.append(frame_redimensionado)

        # Extrai os 2 frames da segunda linha
        for j in range(2):
            # A coordenada y agora é FRAME_ALTURA para pular para a segunda linha
            frame = self.spritesheet.subsurface((j * FRAME_LARGURA, FRAME_ALTURA, FRAME_LARGURA, FRAME_ALTURA))
            frame_redimensionado = pygame.transform.scale(frame, (80, 80))
            self.frames.append(frame_redimensionado)
            
        # O resto da lógica de animação continua a mesma
        self.frame_atual = 0
        self.imagem = self.frames[self.frame_atual]
        self.rect = self.imagem.get_rect(center=(x, y))

        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 150 

        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 150 # Você pode ajustar a velocidade da animação aqui
        self.vida = VIDA_ZOMBIE
        self.vida_maxima = VIDA_ZOMBIE
        self.velocidade = 1
        self.dano = DANO_ZOMBIE

    def _animar(self):
        agora = pygame.time.get_ticks()
        
        # Verifica se já passou tempo suficiente para trocar de frame
        if agora - self.ultima_atualizacao_anim > self.velocidade_animacao:
            self.ultima_atualizacao_anim = agora
            
            # Avança para o próximo frame, voltando ao início se chegar ao fim
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            
            # Armazena a posição central do retângulo antes de atualizar a imagem
            centro = self.rect.center
            
            # Atualiza a imagem do sprite para o novo frame
            self.imagem = self.frames[self.frame_atual]
            
            # Recria o retângulo com as dimensões da nova imagem e restaura sua posição central
            self.rect = self.imagem.get_rect()
            self.rect.center = centro

    def update(self, player):

        self._animar()

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
        