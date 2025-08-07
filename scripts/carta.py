import pygame

class Carta:
    def __init__(self, imagem_path, pos_x, pos_y, tipo_soldado, custo=100,imagem_soldado_path = ''):
        self.image = pygame.image.load(imagem_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        self.tipo_soldado = tipo_soldado  # Ex: "comum", "arqueiro"
        self.custo = custo
        self.imagem_soldado_path = imagem_soldado_path

        self.cooldown_max = 120  # frames até poder usar de novo (2 segs a 60fps)
        self.cooldown_atual = 0

    def draw(self, tela):
        # Se estiver no cooldown, desenha "escurecida"
        if self.cooldown_atual > 0:
            temp = self.image.copy()
            temp.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
            tela.blit(temp, self.rect)
        else:
            tela.blit(self.image, self.rect)

    def update(self):
        if self.cooldown_atual > 0:
            self.cooldown_atual -= 1

    def pode_usar(self):
        return self.cooldown_atual == 0

    def usar(self):
        if self.pode_usar():
            self.cooldown_atual = self.cooldown_max
            return True
        return False

    def clicou_em_cima(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)
