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

# tempo de jogo
tempo_limite = 120 # seg
tempo_inicial = pygame.time.get_ticks()
fonte = pygame.font.Font(None, 74)

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

    # Lógica do cronômetro
    tempo_atual = pygame.time.get_ticks()
    tempo_passado = (tempo_atual - tempo_inicial) / 1000  # Converte para segundos
    tempo_restante = tempo_limite - tempo_passado

    # lógica de vitória e derrota
    if tempo_restante <= 0:
        tela.fill((0,0,0))
        texto_derrota = fonte.render("Tempo Esgotado! Você Perdeu.", True, (255,255,255))
        texto_rect = texto_derrota.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        tela.blit(texto_derrota, texto_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
        pygame.quit()

    # Exibir o cronômetro
    minutos = int(tempo_restante) // 60
    segundos = int(tempo_restante) % 60
    texto_tempo = f"{minutos:02}:{segundos:02}"
        
    texto_cronometro = fonte.render(texto_tempo, True, (255,0,0))
    tela.blit(texto_cronometro, (1100, 15))

    # Atualiza a tela
    pygame.display.flip()

# finalizar o pygame ao sair do loop
pygame.quit()