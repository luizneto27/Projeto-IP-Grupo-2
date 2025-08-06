import pygame

# classe soldado
class Soldado:

    def __init__(self, main, tipo_soldado, posicao, vida_total):
        self.main = main # referencia ao arquivo principal
        self.tipo_soldado = tipo_soldado # qual carta é
        self.posicao = posicao # posicao no grid
        self.vida_total = vida_total # vida total inicial
        self.vida_atual = vida_total # vida durante a partida

        self.dano_causado = 20

    # desenhar o personagem na tela
    def mostrar_na_tela(tela):
        pygame.draw.rect(tela, (255, 0, 0), (200, 300, 40, 50)) # recebe a tela, cor, local na tela, e dimensoes