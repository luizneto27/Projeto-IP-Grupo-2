# main.py
import pygame
from scripts.game import Game

# Inicializar o pygame e o módulo de fontes
pygame.init()


# Definir as dimensões da tela
LARGURA_TELA = 1240
ALTURA_TELA = 768

# configura a tela e o titulo da janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Bem vindo ao jogo!')

# controla o fps
clock = pygame.time.Clock()

# instância da classe principal do jogo
game = Game(LARGURA_TELA, ALTURA_TELA)

#loop principal do jogo
running = True
while running:
    # 60 FPS
    clock.tick(60)

    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     

    # lógica do jogo
    game.update()

    # desenha todos os elementos na tela
    game.draw(tela)

    # atualizar a tela para exibir o que foi desenhado
    pygame.display.flip()

# finalizar o pygame ao sair do loop
pygame.quit()