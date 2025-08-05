# importar as bibliotecas
import pygame, random

pygame.init() # inicializar o pygame
clock = pygame.time.Clock() # coloca o jogo pra rodar numa velocidade constante

tela = pygame.display.set_mode((1024, 600)) # dimensao da tela
cor_tela = (50, 50, 50)

tela.fill(cor_tela)

pygame.display.set_caption('Bem Vindo ao Jogo!')
running = True

while running: # enquanto running verdeade o jogo roda
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

    humanos = [[], [], []]
    monstros = []
    coletaveis = []

    mouse_pos = pygame.mouse.get_pos()
