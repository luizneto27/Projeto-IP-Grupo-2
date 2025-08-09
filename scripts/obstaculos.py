# obstaculos.py
import pygame
from scripts.coletaveis import KitMedico, Municao
from scripts.constantes import FLOR_HEALTH, CONTAINER_HEALTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, health, collectible_type):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health
        self.collectible_type = collectible_type

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True # Indica que foi destruído
        return False
    
    def drop_item(self):
        """Retorna o coletável correspondente se houver."""
        if self.collectible_type == 'kitmedico':
            return KitMedico(self.rect.centerx, self.rect.centery)
        elif self.collectible_type == 'municao':
            return Municao(self.rect.centerx, self.rect.centery)
        return None

class Flor(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/baron_1.webp', FLOR_HEALTH, 'kitmedico')
        self.image = pygame.transform.scale(self.image, (60, 60))


class Container(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 'Imagens/onibus.png', CONTAINER_HEALTH, 'municao')
        self.image = pygame.transform.scale(self.image, (150, 80))