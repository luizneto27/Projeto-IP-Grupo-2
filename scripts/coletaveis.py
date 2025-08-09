#coletaveis.py
import pygame

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, type):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.type = type

class KitMedico(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/imagem-soldado-comum.gif', 'kitmedico')
        self.image = pygame.transform.scale(self.image, (30, 30))

class Moeda(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/imagem-soldado-comum.gif', 'moeda')
        self.image = pygame.transform.scale(self.image, (25, 25))

class Municao(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/imagem-soldado-comum.gif', 'municao')
        self.image = pygame.transform.scale(self.image, (20, 30))