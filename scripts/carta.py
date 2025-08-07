import pygame

class Carta:
    # ALTERADO: Adicionado 'cost_type' para diferenciar custo de tempo e de sangue
    def __init__(self, imagem_path, pos_x, pos_y, tipo_soldado, custo=100, cost_type='blood', imagem_soldado_path = ''):
        self.image = pygame.image.load(imagem_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        self.tipo_soldado = tipo_soldado 
        self.custo = custo
        self.cost_type = cost_type # 'blood' ou 'time'
        self.imagem_soldado_path = imagem_soldado_path

        self.cooldown_max = custo if cost_type == 'time' else 10 # Cooldown pequeno para cartas de sangue
        self.cooldown_atual = 0

    # ALTERADO: O método draw agora recebe o sangue atual para escurecer a carta se necessário
    def draw(self, tela, recurso_sangue_atual=0):
        escurecer = False
        if self.cost_type == 'time' and self.cooldown_atual > 0:
            escurecer = True
        elif self.cost_type == 'blood' and (recurso_sangue_atual < self.custo or self.cooldown_atual > 0):
            escurecer = True

        if escurecer:
            temp = self.image.copy()
            temp.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
            tela.blit(temp, self.rect)
        else:
            tela.blit(self.image, self.rect)

    def update(self):
        if self.cooldown_atual > 0:
            self.cooldown_atual -= 1

    # ALTERADO: Verifica o tipo de custo para ver se a carta pode ser usada
    def pode_usar(self, recurso_sangue_atual=0):
        if self.cooldown_atual > 0:
            return False
        
        if self.cost_type == 'time':
            return True # Cooldown já foi verificado
        elif self.cost_type == 'blood':
            return recurso_sangue_atual >= self.custo
        
        return False

    def usar(self):
        # A verificação de 'pode_usar' é feita no game.py antes de chamar este método
        self.cooldown_atual = self.cooldown_max
        return True

    def clicou_em_cima(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)
