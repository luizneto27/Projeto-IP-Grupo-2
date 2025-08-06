import pygame

class Soldado:
    def __init__(self, vida_total, pos_x, pos_y, dano):
        # 1. Armazena a imagem como um atributo da classe (self.image)
        self.image = pygame.image.load(r'Imagens/imagem-soldado-comum.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        
        # 2. Cria um retângulo (rect) para a imagem e define sua posição
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        # 3. Armazena os outros atributos corretamente
        self.vida_total = vida_total
        self.vida_atual = vida_total # A vida atual começa como total
        self.dano = dano

    # 4. Cria um método para desenhar o boss na tela
    def draw(self, tela):
        tela.blit(self.image, self.rect)
