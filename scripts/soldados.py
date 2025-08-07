import pygame

class Soldado(pygame.sprite.Sprite):
    def __init__(self, vida_total, pos_x, pos_y, dano):
        super().__init__()
        
        self.imagens_nivel = {
            1: pygame.transform.scale(pygame.image.load(r'Imagens/imagem-soldado-comum.gif').convert_alpha(), (100, 100)),
        }
        
        self.nivel_arma = 1
        self.image = self.imagens_nivel[self.nivel_arma]
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.vida_total = vida_total
        self.vida_atual = vida_total
        self.dano_base = dano 
        self.dano = self.dano_base * self.nivel_arma

        self.alcance = 400 
        self.cooldown_max = 60
        self.cooldown_atual = 0

    def draw(self, tela):
        tela.blit(self.image, self.rect)
        if self.vida_atual < self.vida_total:
            barra_vida_largura_total = self.rect.width * 0.8
            barra_vida_altura = 7
            pos_x_barra = self.rect.centerx - (barra_vida_largura_total / 2)
            pos_y_barra = self.rect.top - 15
            
            pygame.draw.rect(tela, (255,0,0), (pos_x_barra, pos_y_barra, barra_vida_largura_total, barra_vida_altura))
            
            barra_vida_largura_atual = barra_vida_largura_total * (self.vida_atual / self.vida_total)
            if barra_vida_largura_atual > 0:
                pygame.draw.rect(tela, (0,255,0), (pos_x_barra, pos_y_barra, barra_vida_largura_atual, barra_vida_altura))

    # Lógica de ataque à distância
    def atacar(self, alvos, coletaveis_grupo, todos_sprites_grupo):
        if self.cooldown_atual > 0:
            self.cooldown_atual -= 1
            return False

        for alvo in alvos:
            if alvo.esta_vivo():
                # Calcula a distância entre a frente do soldado e a frente do alvo
                distancia = alvo.rect.left - self.rect.right
                
                # Verifica se o alvo está na frente e dentro do alcance
                if 0 <= distancia < self.alcance:
                    item_dropado = alvo.levar_dano(self.dano)
                    
                    if item_dropado:
                        coletaveis_grupo.add(item_dropado)
                        todos_sprites_grupo.add(item_dropado)

                    self.cooldown_atual = self.cooldown_max
                    return True # Atacou com sucesso
        
        return False # Não encontrou alvo no alcance

    def levar_dano(self, quantidade):
        self.vida_atual -= quantidade
        if self.vida_atual <= 0:
            self.kill()

    def esta_vivo(self):
        return self.vida_atual > 0
    
    def upgrade(self):
        if self.nivel_arma < 3: 
            self.nivel_arma += 1
            self.dano = self.dano_base * self.nivel_arma
            if self.nivel_arma in self.imagens_nivel:
                self.image = self.imagens_nivel[self.nivel_arma]
    
    def curar(self, quantidade):
        self.vida_atual += quantidade
        if self.vida_atual > self.vida_total:
            self.vida_atual = self.vida_total