# obstaculos.py
import pygame
from scripts.coletaveis import KitMedico, Municao
from scripts.constantes import VIDA_FLOR, VIDA_CONTAINER

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, caminho_imagem, vida, tipo_coletavel):
        super().__init__()
        self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
        self.rect = self.imagem.get_rect(center=(x, y))
        self.vida = vida
        self.vida_maxima = vida
        self.tipo_coletavel = tipo_coletavel

    def sofrer_dano(self, qtd):
        self.vida -= qtd
        if self.vida <= 0:
            self.kill()
            return True # Indica que foi destruído
        return False
    
    def dropar_item(self):
        if self.tipo_coletavel == 'kitmedico':
            return KitMedico(self.rect.centerx, self.rect.centery)
        elif self.tipo_coletavel == 'municao':
            return Municao(self.rect.centerx, self.rect.centery)
        return None

class Flor(Obstaculo):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/maquina_kitmed.png', VIDA_FLOR, 'kitmedico')
        self.imagem = pygame.transform.scale(self.imagem, (150, 150))

        # Guarda a posição central original
        old_center = self.rect.center
        
        self.rect = pygame.Rect(0, 0, 150, 150) 
        
        # Restaura a posição central
        self.rect.center = old_center


class Container(Obstaculo):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/caixa_municao.png', VIDA_CONTAINER, 'municao')
        self.imagem = pygame.transform.scale(self.imagem, (80, 80))
        
        # Guarda a posição central original
        old_center = self.rect.center
        
        # Redimensiona o retângulo de colisão para ser menor que a imagem
        self.rect = pygame.Rect(0, 0, 80, 80) 
        
        # Restaura a posição central do novo retângulo
        self.rect.center = old_center