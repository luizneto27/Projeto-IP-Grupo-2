# tank_zombie.py
import pygame
from scripts.zombie import Zombie
from scripts.constantes import VIDA_ZUMBI_TANQUE, VELOCIDADE_ZUMBI_TANQUE, DANO_ZUMBI_TANQUE

class ZombieTank(Zombie):
    def __init__(self, x, y):
        # Chama o __init__ da classe pai (Zombie) para aproveitar o código
        super().__init__(x, y)
        self.spritesheet = pygame.image.load('Imagens/zombie_tank.png').convert_alpha()
        
        self.frames = []
        
        # Em vez de calcular, definimos o tamanho exato de um quadro
        FRAME_LARGURA = 64
        FRAME_ALTURA = 96

        # Extrai os 6 frames da primeira linha
        for j in range(6):
            # Usamos os valores definidos manualmente para o recorte
            frame = self.spritesheet.subsurface((j * FRAME_LARGURA, 0, FRAME_LARGURA, FRAME_ALTURA))
            frame_redimensionado = pygame.transform.scale(frame, (140, 140))
            self.frames.append(frame_redimensionado)

        # Extrai o frame da segunda linha
        for j in range(1):
            # A coordenada y é FRAME_ALTURA para pular para a segunda linha
            frame = self.spritesheet.subsurface((j * FRAME_LARGURA, FRAME_ALTURA, FRAME_LARGURA, FRAME_ALTURA))
            frame_redimensionado = pygame.transform.scale(frame, (140, 140))
            self.frames.append(frame_redimensionado)
            
        # O resto da lógica de animação
        self.frame_atual = 0
        self.imagem = self.frames[self.frame_atual]
        self.rect = self.imagem.get_rect(center=(x, y))

        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 150 

        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 150 # ajustar a velocidade da animação aqui

        self.vida = VIDA_ZUMBI_TANQUE
        self.vida_maxima = VIDA_ZUMBI_TANQUE
        self.velocidade = VELOCIDADE_ZUMBI_TANQUE
        self.dano = DANO_ZUMBI_TANQUE

        self.direcao = 1

    def _animar(self):
        agora = pygame.time.get_ticks()
        
        # Verifica se já passou tempo suficiente para trocar de frame
        if agora - self.ultima_atualizacao_anim > self.velocidade_animacao:
            self.ultima_atualizacao_anim = agora
            
            # Avança para o próximo frame, voltando ao início se chegar ao fim
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            
            # Armazena a posição central do retângulo antes de atualizar a imagem
            centro = self.rect.center
            
            # Pega a imagem base (sempre virada para a direita)
            imagem_base = self.frames[self.frame_atual]
            
            # Vira a imagem SE o zumbi estiver indo para a esquerda
            if self.direcao == -1:
                self.imagem = pygame.transform.flip(imagem_base, True, False)
            else:
                self.imagem = imagem_base
            
            # Atualiza o retângulo com a imagem correta (virada ou não)
            self.rect = self.imagem.get_rect()
            self.rect.center = centro