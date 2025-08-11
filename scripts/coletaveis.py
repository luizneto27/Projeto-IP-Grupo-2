#coletaveis.py
import pygame

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, caminho_imagem, type):
        super().__init__()
        self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
        self.rect = self.imagem.get_rect(center=(x, y))
        self.type = type

class KitMedico(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/imagem-soldado-comum.gif', 'kitmedico')
        self.imagem = pygame.transform.scale(self.imagem, (30, 30))

class Moeda(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/imagem-soldado-comum.gif', 'moeda')
        self.imagem = pygame.transform.scale(self.imagem, (25, 25))

class Municao(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/imagem-soldado-comum.gif', 'municao')
        self.imagem = pygame.transform.scale(self.imagem, (20, 30))