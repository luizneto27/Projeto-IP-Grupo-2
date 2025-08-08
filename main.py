# importar as bibliotecas
import pygame
from scripts.game import Game

pygame.init() # inicializar o pygame
pygame.font.init() #inicializa o módulo de fontes

clock = pygame.time.Clock() # coloca o jogo pra rodar numa velocidade constante

x, y = 1240, 768
tela = pygame.display.set_mode((x, y)) # dimensao da tela
pygame.display.set_caption('Humans Vs Monsters')

game = Game(x, y)

running = True
while running: # enquanto running verdade o jogo roda
    clock.tick(60) # fps do jogo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        game.handle_event(event)

    game.update()
    game.draw(tela)
    
    pygame.display.flip()

pygame.quit()