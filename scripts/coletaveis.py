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
        super().__init__(x, y, 'Imagens/kitmed.png', 'kitmedico')
        self.imagem = pygame.transform.scale(self.imagem, (40, 40))

        # Guarda a posição central original
        old_center = self.rect.center
        
        self.rect = pygame.Rect(0, 0, 40, 40) 
        
        # Restaura a posição central
        self.rect.center = old_center

class Moeda(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/moeda.png', 'moeda')
        self.imagem = pygame.transform.scale(self.imagem, (40, 40))

        # Guarda a posição central original
        old_center = self.rect.center

        self.rect = pygame.Rect(0, 0, 40, 40) 
        
        # Restaura a posição central
        self.rect.center = old_center

class Municao(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/caixa_municao.png', 'municao')
        self.imagem = pygame.transform.scale(self.imagem, (50, 50))

        # Guarda a posição central original
        old_center = self.rect.center
        
        self.rect = pygame.Rect(0, 0, 50, 50) 
        
        # Restaura a posição central
        self.rect.center = old_center