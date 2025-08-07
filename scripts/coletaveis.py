import pygame
import random

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, imagem_path, tipo, altura_tela = 768):
        super().__init__()
        self.image = pygame.image.load(imagem_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.tipo = tipo # "vida", "sangue", "arma"
        self.velocidade_y = 2 # Velocidade de queda
        self.altura_tela = altura_tela

    def update(self):
        # Move o coletável para baixo
        self.rect.y += self.velocidade_y
        # Impede que saia da tela por baixo (opcional)
        if self.rect.top > self.altura_tela:
            self.kill() # Remove o sprite se ele sair da tela

    def draw(self, tela):
        tela.blit(self.image, self.rect)

# --- Classes Específicas de Coletáveis ---
# Por enquanto, elas não precisam de lógica extra, mas a estrutura permite
# adicionar comportamentos únicos no futuro.

class Sangue(Coletavel):
    def __init__(self, pos_x, pos_y, altura_tela=768):
        # TODO: Crie uma imagem para o sangue (ex: 'Imagens/sangue_drop.png')
        super().__init__(pos_x, pos_y, 'Imagens/imagem-soldado-comum.gif', 'sangue', altura_tela)
        self.image = pygame.transform.scale(self.image, (25, 25))

class Arma(Coletavel):
    def __init__(self, pos_x, pos_y, altura_tela=768):
        # TODO: Crie uma imagem para a arma (ex: 'Imagens/arma_drop.png')
        super().__init__(pos_x, pos_y, 'Imagens/imagem-soldado-comum.gif', 'arma', altura_tela)
        self.image = pygame.transform.scale(self.image, (40, 40))

# --- NOVO: Classe para o coletável de Vida ---
class Vida(Coletavel):
    def __init__(self, pos_x, pos_y, altura_tela=768):
        # TODO: Crie uma imagem para a vida (ex: 'Imagens/vida_drop.png')
        super().__init__(pos_x, pos_y, 'Imagens/imagem-soldado-comum.gif', 'vida', altura_tela)
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.valor_cura = 50 # Quanto de vida este item cura