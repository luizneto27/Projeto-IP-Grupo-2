# importar as bibliotecas
import pygame, random
from soldados import Soldado
from boss import Boss

pygame.init() # inicializar o pygame
clock = pygame.time.Clock() # coloca o jogo pra rodar numa velocidade constante

x = 1240
y = 768

tela = pygame.display.set_mode((x, y)) # dimensao da tela
cor_tela = (50, 50, 50)

tela.fill(cor_tela) # cor da tela

pygame.display.set_caption('Bem Vindo ao Jogo!')

ideiainicialtela = pygame.image.load('Imagens/ideiainicialtela.png').convert_alpha()
ideiainicialtela =pygame.transform.scale(ideiainicialtela,(x,y))

running = True

while running: # enquanto running verdade o jogo roda
    clock.tick(60) # fps do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tela.blit(ideiainicialtela, (0,0))
    
    mouse_pos = pygame.mouse.get_pos()

    grid = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ] # grid jogo

    sold_comum = Soldado(vida_total=100, pos_x = 230, pos_y =500, dano=20)
    sold_comum.draw(tela)
    meu_boss = Boss(vida_total=1000, pos_x = 1000, pos_y =300, dano=20)
    meu_boss.draw(tela)

    pygame.display.update()