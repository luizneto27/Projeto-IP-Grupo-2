# main.py
import pygame
from scripts.game import Game, tela
from scripts.constantes import LARGURA_TELA, ALTURA_TELA

pygame.init()
pygame.mixer.init()

# Capa
capa_img = pygame.image.load("capa_definitiva.png").convert()
capa_img = pygame.transform.scale(capa_img, (LARGURA_TELA, ALTURA_TELA))

# Botões da capa (ajustar coordenadas conforme imagem)
botao_iniciar_capa = pygame.Rect(460, 500, 240, 50)
botao_sair_capa = pygame.Rect(500, 570, 160, 50)

# Estado inicial
mostrar_capa = True

# Configurações
clock = pygame.time.Clock()
game = Game(LARGURA_TELA, ALTURA_TELA)

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)

# Fontes
fonte_grande = pygame.font.Font(None, 74)
fonte_pequena = pygame.font.Font(None, 36)

# Estado
jogo_rodando = True
jogo_pausado = False
contagem_ativa = False
tempo_inicio_contagem = 0
som_mutado = False
volume_musica = 1.0

#mensagem - informar do pause
MOSTRAR_MSG_INSTRUCAO = True
DURACAO_MSG_INSTRUCAO = 3000  # milissegundos 
inicio_msg_instrucao = pygame.time.get_ticks()

# Música
try:
    pygame.mixer.music.load("jogo_music.mp3")
    pygame.mixer.music.set_volume(volume_musica)
    pygame.mixer.music.play(-1)
except pygame.error as erro:
    print("Erro ao carregar música:", erro)

# Ícones
tamanho_icone = 50
try:
    icone_som_ativo = pygame.image.load("icon_music.png")
    icone_som_mutado = pygame.image.load("icon_music_off.png")
    icone_menu = pygame.image.load("icon_menu.png")
    icone_som_ativo = pygame.transform.scale(icone_som_ativo, (tamanho_icone, tamanho_icone))
    icone_som_mutado = pygame.transform.scale(icone_som_mutado, (tamanho_icone, tamanho_icone))
    icone_menu = pygame.transform.scale(icone_menu, (tamanho_icone, tamanho_icone))
except pygame.error:
    icone_som_ativo = pygame.Surface((tamanho_icone, tamanho_icone)); icone_som_ativo.fill(VERDE)
    icone_som_mutado = pygame.Surface((tamanho_icone, tamanho_icone)); icone_som_mutado.fill(VERMELHO)
    icone_menu = pygame.Surface((tamanho_icone, tamanho_icone)); icone_menu.fill(BRANCO)

# Imagem de pausa
try:
    imagem_pausa = pygame.image.load("tela_pause.png").convert_alpha()
    largura_img = 400
    altura_img = int(imagem_pausa.get_height() * (largura_img / imagem_pausa.get_width()))
    imagem_pausa = pygame.transform.scale(imagem_pausa, (largura_img, altura_img))
except pygame.error as erro:
    print("Erro ao carregar tela de pausa:", erro)
    imagem_pausa = pygame.Surface((500, 450), pygame.SRCALPHA)
    imagem_pausa.fill((10, 10, 30, 185))

# Botões
centro_x = LARGURA_TELA // 2
centro_y = ALTURA_TELA // 2
botao_retomar = pygame.Rect(centro_x - 140, centro_y + 10, 280, 50)
botao_sair = pygame.Rect(centro_x - 100, centro_y + 80, 200, 50)

retangulo_icone_som = icone_som_ativo.get_rect(topright=(LARGURA_TELA - 20, 20))
retangulo_icone_menu = icone_menu.get_rect(topright=(LARGURA_TELA - 80, 20))

# Funções
def alternar_som():
    global som_mutado
    som_mutado = not som_mutado
    pygame.mixer.music.set_volume(0 if som_mutado else volume_musica)

def voltar_para_menu():
    global jogo_pausado, contagem_ativa, mostrar_capa, game
    jogo_pausado = False
    contagem_ativa = False
    mostrar_capa = True
    game = Game(LARGURA_TELA, ALTURA_TELA)

def desenhar_painel_pausa():
    tela.blit(imagem_pausa, imagem_pausa.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2)))
    tela.blit(icone_som_mutado if som_mutado else icone_som_ativo, retangulo_icone_som)
    tela.blit(icone_menu, retangulo_icone_menu)

def desenhar_contagem_regressiva():
    global contagem_ativa, jogo_pausado
    tempo_passado = pygame.time.get_ticks() - tempo_inicio_contagem
    numero_contagem = 3 - (tempo_passado // 1000)

    if numero_contagem > 0:
        game.draw(tela)  # mantém o jogo visível no fundo
        sobreposicao = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 80))  # sombra leve
        tela.blit(sobreposicao, (0, 0))
        texto_contagem = fonte_grande.render(str(numero_contagem), True, BRANCO)
        tela.blit(texto_contagem, texto_contagem.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2)))
    else:
        contagem_ativa = False
        jogo_pausado = False
        game.retomar()  #qnd terminar a contagem, retoma o cronômetro (acumula tempo de pausa)

def tela_capa():
    tela.blit(capa_img, (0, 0))
    pygame.display.flip()

# Loop principal
while jogo_rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_rodando = False
        elif mostrar_capa:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar_capa.collidepoint(evento.pos):
                    mostrar_capa = False  # inicia o jogo
                elif botao_sair_capa.collidepoint(evento.pos):
                    jogo_rodando = False
            continue
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if not contagem_ativa:
                    if jogo_pausado:
                        contagem_ativa = True
                        tempo_inicio_contagem = pygame.time.get_ticks()
                        # NÃO chamar game.retomar() aqui: a retomada será feita quando a contagem acabar
                    else:
                        jogo_pausado = True
                        game.pausar()  #registra o momento da pausa para congelar o cronômetro

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            if jogo_pausado:
                if botao_retomar.collidepoint(pos_mouse):
                    contagem_ativa = True
                    tempo_inicio_contagem = pygame.time.get_ticks()
                elif botao_sair.collidepoint(pos_mouse):
                    jogo_rodando = False
                elif retangulo_icone_som.collidepoint(pos_mouse):
                    alternar_som()
                elif retangulo_icone_menu.collidepoint(pos_mouse):
                    voltar_para_menu()

    # Desenho
    if mostrar_capa:
        tela_capa()
    elif contagem_ativa:
        desenhar_contagem_regressiva()
    elif jogo_pausado:
        game.draw(tela)  # mantém o jogo congelado no fundo
        sobreposicao = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 80))  # sombra leve
        tela.blit(sobreposicao, (0, 0))
        desenhar_painel_pausa()
    else:
        if not game.update():
            jogo_rodando = False
        game.draw(tela)

        #msg de instrução
        if MOSTRAR_MSG_INSTRUCAO:
            agora = pygame.time.get_ticks()
            if agora - inicio_msg_instrucao <= DURACAO_MSG_INSTRUCAO:
                mensagem = fonte_pequena.render("Pressione ESC para pausar", True, BRANCO)
                rect_msg = mensagem.get_rect(midbottom=(LARGURA_TELA // 2, ALTURA_TELA - 10))
                tela.blit(mensagem, rect_msg)
            else:
                MOSTRAR_MSG_INSTRUCAO = False


    pygame.display.flip()

pygame.quit()
