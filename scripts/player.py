# player.py
import pygame
from scripts.projeteis import Projetil
from scripts.constantes import VIDA_PLAYER, VELOCIDADE_PLAYER, MUNICAO_INICIAL_PLAYER, MOEDAS_INICIAIS_PLAYER, KITMEDS_INICIAIS_PLAYER, ALTURA_TELA

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        walking_spritesheet = pygame.image.load('Imagens/sprite_player.png').convert_alpha()
        shooting_spritesheet = pygame.image.load('Imagens/player_atirando_bg.png').convert_alpha()

        # Lista para guardar os frames da animação de caminhada
        self.walking_frames = []
        self.shooting_frames = []
        
        # Dimensões de cada frame na spritesheet
        FRAME_LARGURA_CAMINHO = 72
        FRAME_ALTURA_CAMINHO = 72
        for j in range(5):
            frame = walking_spritesheet.subsurface((j * FRAME_LARGURA_CAMINHO, 0, FRAME_LARGURA_CAMINHO, FRAME_ALTURA_CAMINHO))
            self.walking_frames.append(pygame.transform.scale(frame, (120, 120)))
        frame = walking_spritesheet.subsurface((0, FRAME_ALTURA_CAMINHO, FRAME_LARGURA_CAMINHO, FRAME_ALTURA_CAMINHO))
        self.walking_frames.append(pygame.transform.scale(frame, (120, 120)))

        FRAME_LARGURA_TIRO = 107
        FRAME_ALTURA_TIRO = 70
        for i in range(3): # Linhas
            for j in range(3): # Colunas
                # Para a extração se chegar no 8º frame 
                if len(self.shooting_frames) >= 8:
                    break
                frame = shooting_spritesheet.subsurface((j * FRAME_LARGURA_TIRO, i * FRAME_ALTURA_TIRO, FRAME_LARGURA_TIRO, FRAME_ALTURA_TIRO))
                self.shooting_frames.append(pygame.transform.scale(frame, (120, 120))) # Ajusta o tamanho do frame de tiro

        # Atributos de controle da animação
        self.frame_atual = 0
        self.imagem = self.walking_frames[self.frame_atual]# Começa com a imagem de "parado"
        self.rect = self.imagem.get_rect(center=(x, y))

        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 100  # ms, velocidade da animação de caminhada
        
        # Atributo para controlar o estado (parado ou movendo)
        self.andando = False
        self.atirando = False
        self.tempo_ultimo_tiro = 0
        self.duracao_animacao_tiro = 200 # Animação de tiro dura 300ms
        
        self.direcao = 1 # 1 para direita, -1 para esquerda

        self.vida = VIDA_PLAYER
        self.vida_maxima = VIDA_PLAYER
        self.municao = MUNICAO_INICIAL_PLAYER
        self.moedas = MOEDAS_INICIAIS_PLAYER
        self.kitmeds = KITMEDS_INICIAIS_PLAYER
        self.velocidade = VELOCIDADE_PLAYER
        
    def _animar(self):
        agora = pygame.time.get_ticks()

        if self.atirando:
            frames_atuais = self.shooting_frames
            velocidade_anim = 50 # Animação de tiro mais rápida
        elif self.andando:
            frames_atuais = self.walking_frames
            velocidade_anim = self.velocidade_animacao
        else: # Parado
            frames_atuais = self.walking_frames
            self.frame_atual = 0 # Fica no primeiro frame se parado

        # Lógica de animação
        if self.atirando or self.andando:
             if agora - self.ultima_atualizacao_anim > velocidade_anim:
                self.ultima_atualizacao_anim = agora
                self.frame_atual = (self.frame_atual + 1) % len(frames_atuais)
        
        # Pega a imagem base do frame correto
        imagem_base = frames_atuais[self.frame_atual]
        centro = self.rect.center

        # Vira a imagem se a direção for para a esquerda
        if self.direcao == -1:
            self.imagem = pygame.transform.flip(imagem_base, True, False)
        else:
            self.imagem = imagem_base
            
        # Atualiza o rect com a nova imagem e restaura o centro
        self.rect = self.imagem.get_rect()
        self.rect.center = centro  

    def update(self, largura_mundo):
        # Verifica se a animação de tiro deve terminar
        if self.atirando and pygame.time.get_ticks() - self.tempo_ultimo_tiro > self.duracao_animacao_tiro:
            self.atirando = False
            self.frame_atual = 0
        self.andando = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # Impede o jogador de sair pela esquerda do mundo
            if self.rect.left > self.velocidade:
                self.rect.x -= self.velocidade
            else:
                self.rect.left = 0
            self.direcao = -1
            self.andando = True

        if keys[pygame.K_RIGHT]:
            # Impede o jogador de sair pela direita do mundo
            if self.rect.right < largura_mundo - self.velocidade:
                self.rect.x += self.velocidade
            else:
                self.rect.right = largura_mundo
            self.direcao = 1 
            self.andando = True

        if keys[pygame.K_UP]:
            # Impede o jogador de sair por cima
            if self.rect.top > self.velocidade:
                self.rect.y -= self.velocidade
            else:
                self.rect.top = 0
            self.andando = True

        if keys[pygame.K_DOWN]:
            # Impede o jogador de sair por baixo
            if self.rect.bottom < ALTURA_TELA - self.velocidade:
                self.rect.y += self.velocidade
            else:
                self.rect.bottom = ALTURA_TELA
            self.andando = True
        
        self._animar()
        
        self._animar()

    def atirar(self,grupos_inimigos, grupo_obstaculos, grupo_coletaveis, grupo_todos_sprites, grupo_particulas):
        if self.municao > 0:
            self.municao -= 1
            # ATIVA O ESTADO E O TIMER DE TIRO
            self.atirando = True
            self.tempo_ultimo_tiro = pygame.time.get_ticks()
            self.frame_atual = 0 # Reinicia a animação de tiro

            return Projetil(self.rect.centerx, self.rect.centery, self.direcao, grupos_inimigos, grupo_obstaculos, grupo_coletaveis, grupo_todos_sprites, grupo_particulas)
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