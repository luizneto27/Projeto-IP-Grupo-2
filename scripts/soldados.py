# scripts/soldados.py
import pygame

class Soldado(pygame.sprite.Sprite): # NOVO: Herda de pygame.sprite.Sprite
    def __init__(self, vida_total, pos_x, pos_y, dano):
        super().__init__() # NOVO: Inicializador do Sprite
        
        # Armazena as imagens para cada nível de arma
        self.imagens_nivel = {
            1: pygame.transform.scale(pygame.image.load(r'Imagens/imagem-soldado-comum.gif').convert_alpha(), (100, 100)),
            # ADICIONE AQUI AS IMAGENS PARA OS NÍVEIS 2, 3, etc.
            # Ex: 2: pygame.transform.scale(pygame.image.load(r'Imagens/soldado-nivel-2.png').convert_alpha(), (110, 110))
        }
        
        self.nivel_arma = 1 # NOVO
        self.image = self.imagens_nivel[self.nivel_arma]
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.vida_total = vida_total
        self.vida_atual = vida_total
        self.dano_base = dano # ALTERADO: Dano base que será multiplicado pelo nível
        self.dano = self.dano_base * self.nivel_arma

        self.alcance = 400 # NOVO: Alcance do ataque
        self.cooldown_max = 30 
        self.cooldown_atual = 0

    def draw(self, tela):
        tela.blit(self.image, self.rect)
        # NOVO: Desenha a barra de vida
        if self.vida_atual < self.vida_total:
            pygame.draw.rect(tela, (255,0,0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            barra_vida_largura = self.rect.width * (self.vida_atual / self.vida_total)
            pygame.draw.rect(tela, (0,255,0), (self.rect.x, self.rect.y - 10, barra_vida_largura, 5))


    # ALTERADO: O método agora recebe os grupos para poder adicionar drops
    def atacar(self, alvos, coletaveis_grupo, todos_sprites_grupo):
        if self.cooldown_atual > 0:
            self.cooldown_atual -= 1
            return

        for alvo in alvos:
            if alvo.esta_vivo():
                distancia = alvo.rect.left - self.rect.right
                if 0 <= distancia < self.alcance:
                    # CORRIGIDO: Captura o item retornado pelo método levar_dano
                    item_dropado = alvo.levar_dano(self.dano)
                    
                    # Se um item foi dropado (não é None), adicione-o aos grupos
                    if item_dropado:
                        coletaveis_grupo.add(item_dropado)
                        todos_sprites_grupo.add(item_dropado)

                    self.cooldown_atual = self.cooldown_max
                    break
    
    def levar_dano(self, quantidade): # NOVO
        self.vida_atual -= quantidade
        if self.vida_atual <= 0:
            self.kill() # Remove o sprite dos grupos ao morrer

    def esta_vivo(self): # NOVO
        return self.vida_atual > 0
    
    def upgrade(self): # NOVO
        if self.nivel_arma < 3: # Limite de nível (ex: 3)
            self.nivel_arma += 1
            self.dano = self.dano_base * self.nivel_arma
            # Atualiza a imagem se houver uma para o novo nível
            if self.nivel_arma in self.imagens_nivel:
                self.image = self.imagens_nivel[self.nivel_arma]
            print(f"Soldado fez upgrade para o nível {self.nivel_arma}!")