# importar as bibliotecas
import pygame, random
from soldados import Soldado

pygame.init() # inicializar o pygame
clock = pygame.time.Clock() # coloca o jogo pra rodar numa velocidade constante

largura_tela, altura_tela = (1240, 768)

tela = pygame.display.set_mode((largura_tela, altura_tela)) # dimensao da tela
cor_tela = (50, 50, 50)

tela.fill(cor_tela) # cor da tela

pygame.display.set_caption('Bem Vindo ao Jogo!')
running = True

while running: # enquanto running verdeade o jogo roda
    clock.tick(60) # fps do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grid = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ] # grid jogo

    mouse_pos = pygame.mouse.get_pos()

    Soldado.mostrar_na_tela(tela) # chama o objeto e mostra na tela
    
    pygame.display.update()