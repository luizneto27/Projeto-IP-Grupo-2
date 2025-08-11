# main.py
import pygame
from scripts.game import Game, tela
from scripts.constantes import LARGURA_TELA, ALTURA_TELA

# Inicializar o pygame e o módulo de fontes
pygame.init()

# controla o fps
clock = pygame.time.Clock()

# instância da classe principal do jogo
game = Game(LARGURA_TELA, ALTURA_TELA)

#loop principal do jogo
running = True
while running:
    clock.tick(60) # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     

    # lógica do jogo
    game.update()

    # desenha todos os elementos na tela
    game.draw(tela)

    # Atualiza a tela
    pygame.display.flip()

# finalizar o pygame ao sair do loop
pygame.quit()