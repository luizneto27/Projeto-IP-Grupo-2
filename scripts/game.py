# game.py
import pygame
import random
from scripts.player import Player
from scripts.zombie import Zombie
from scripts.zombie_tank import ZombieTank
from scripts.obstaculos import Flor, Container, Obstaculo
from scripts.coletaveis import KitMedico, Moeda, Municao
from scripts.projeteis import Projetil, ParticulaImpacto
from scripts.constantes import CADENCIA_TIRO, COOLDOWN_DANO_JOGADOR, QTD_ZOMBIES, LARGURA_TELA, ALTURA_TELA, ZOMBIES_POR_HORDA, INTERVALO_ENTRE_HORDAS, INTERVALO_SPAWN_ZUMBI_HORDA, CHANCE_SPAWN_TANQUE 

# configura a tela e o titulo da janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('CIn Defender!')

class Game:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        #CÂMERA E MUNDO
        # Define o tamanho total
        self.largura_mundo = largura * 3
        self.altura_mundo = altura

        #imagem de fundo
        self.imagem_fundo = pygame.image.load('Imagens/fundo_final_3.png').convert()
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (self.largura_mundo, altura))

        #Grupo de Sprites
        self.player = Player(largura // 2, altura // 2)
        self.inimigos = pygame.sprite.Group()
        self.obstaculos = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()
        self.projeteis = pygame.sprite.Group()
        self.particulas = pygame.sprite.Group()
        self.todos_sprites = pygame.sprite.Group(self.player)
        
        # A câmera é um retângulo que representa a área visível da tela
        self.camera = pygame.Rect(0, 0, self.largura, self.altura)

        # tempo de jogo
        self.tempo_limite = 120 # seg
        self.tempo_inicial = pygame.time.get_ticks()
        self.fonte = pygame.font.Font(None, 74)

        self.tempo_pausado_total = 0  # ADICIONADO: acumula tempo total em que o jogo ficou pausado
        self.momento_pausa = None      # ADICIONADO: registra quando a pausa começou (ms)

        self.zumbis_spawnados = 0 # contador de zumbis
        self.zumbis_mortos = 0 

        #CARREGAR ÍCONES 
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.icone_vida = pygame.transform.scale(pygame.image.load('Imagens/coracao.png').convert_alpha(),(50,50))
        self.icone_municao = pygame.transform.scale(pygame.image.load('Imagens/balas.png').convert_alpha(),(60,60))
        self.icone_moeda = pygame.transform.scale(pygame.image.load('Imagens/moeda.png').convert_alpha(),(60,60))
        self.icone_medkit = pygame.transform.scale(pygame.image.load('Imagens/kitmed.png').convert_alpha(),(60,60))
        
        #carregar som do tiro
        self.som_de_tiro_tocando = False # Variável para controlar o som
        self.cadencia_tiro = CADENCIA_TIRO

        self.som_tiro = pygame.mixer.Sound("Sons/Metralhadora_1.mp3")
        self.som_tiro.set_volume(0.5) # Ajuste o volume se necessário (0.0 a 1.0)

        self.spawnar_elementos_iniciais()
        self.ultimo_tiro = 0 # Controle para cadência de tiro
        # Guarda o tempo do último hit no jogador para o cooldown
        self.ultimo_hit_player = 0
        #Flag para controlar o início do jogo
        self.jogo_comecou = False

        #atributos para gerenciamento da horda
        self.horda_em_andamento = False
        self.zumbis_para_spawnar_na_horda = 0
        self.ultimo_spawn_individual_zumbi = 0

        # Controle de estado e timer de fim de jogo
        self.estado_jogo = 'JOGANDO'  # Estados possíveis: JOGANDO, VITORIA, DERROTA, TEMPO_ESGOTADO
        self.tempo_fim_jogo = 0

        self.cooldown_kitmed = 0

    # o método para iniciar pausa (registra o início da pausa)
    def pausar(self):
        self.momento_pausa = pygame.time.get_ticks()
        if self.som_de_tiro_tocando and self.som_tiro:
            self.som_tiro.stop()
            self.som_de_tiro_tocando = False

    #o método para terminar pausa (acumula o tempo que ficou pausado)
    def retomar(self):
        if self.momento_pausa is not None:
            self.tempo_pausado_total += pygame.time.get_ticks() - self.momento_pausa
            self.momento_pausa = None

    def draw_barra_vida(self, superficie, x, y, porcentagem, largura_barra, altura_barra):
        if porcentagem < 0:
            porcentagem = 0
        
        fill = (porcentagem / 100) * largura_barra
        contorno_rect = pygame.Rect(x, y, largura_barra, altura_barra)
        fill_rect = pygame.Rect(x, y, fill, altura_barra)

        # Define a cor da barra com base na porcentagem de vida
        if porcentagem > 75:
            cor = (0, 255, 0)  # Verde
        elif porcentagem > 30:
            cor = (255, 255, 0)  # Amarelo
        else:
            cor = (255, 0, 0)  # Vermelho

        pygame.draw.rect(superficie, (40, 40, 40), contorno_rect)  # Fundo cinza escuro
        pygame.draw.rect(superficie, cor, fill_rect) # Barra de vida
    
    def spawnar_elementos_iniciais(self):
        # Posiciona os elementos no mundo de jogo
        # Os zumbis iniciais aparecem na primeira horda
    
        # Spawna 6 flores em posições aleatórias à frente (à direita) do jogador
        for j in range(6):
            # Gera uma posição X aleatória entre (X,Y) pixels à direita do jogador
            pos_x = self.player.rect.centerx + random.randint(400, 3500)
            # Gera uma posição Y aleatória na altura do mapa
            pos_y = random.randint(100, self.altura - 100)
            flor = Flor(pos_x, pos_y)
            self.obstaculos.add(flor)
            self.todos_sprites.add(flor)

        # Spawna 4 containers em posições aleatórias à frente (à direita) do jogador
        for k in range(4):
            # Gera uma posição X aleatória entre (X,Y) pixels à direita do jogador
            pos_x = self.player.rect.centerx + random.randint(300, 3500)
            # Gera uma posição Y aleatória na altura do mapa
            pos_y = random.randint(100, self.altura - 100)
            container = Container(pos_x, pos_y)
            self.obstaculos.add(container)
            self.todos_sprites.add(container)

    def spawn_zombie(self):
        # Spawna o zumbi em uma posição aleatória na tela
        pos_x = self.camera.x + random.randint(0, self.largura)
        pos_y = random.randint(100, self.altura - 100)

        # Decide aleatoriamente qual zumbi criar
        if random.random() < CHANCE_SPAWN_TANQUE:
            # Cria um Zumbi Tanque na posição
            novo_zumbi = ZombieTank(pos_x, pos_y)
        else:
            # Cria um Zumbi normal na posição
            novo_zumbi = Zombie(pos_x, pos_y)

        self.inimigos.add(novo_zumbi)
        self.todos_sprites.add(novo_zumbi)

        self.zumbis_spawnados += 1 # ate atingir 100, se tiver errado corrige pra += 5

    def spawn_horda(self, num_zombies):
        for i in range(num_zombies):
            if self.zumbis_spawnados < QTD_ZOMBIES:
                self.spawn_zombie()

    def gerenciar_tiros(self):
        keys = pygame.key.get_pressed()
        agora = pygame.time.get_ticks()

        # Verifica se a tecla de espaço está pressionada
        if keys[pygame.K_SPACE]:
            # Se a tecla está pressionada mas o som não está tocando, inicie o som em loop
            if not self.som_de_tiro_tocando and self.som_tiro:
                self.som_tiro.play(loops=-1)
                self.som_de_tiro_tocando = True

            # Lógica para criar o projétil com base na cadência de tiro
            if agora - self.ultimo_tiro > self.cadencia_tiro:
                self.ultimo_tiro = agora
                projetil = self.player.atirar(self.inimigos, self.obstaculos, self.coletaveis, self.todos_sprites, self.particulas, self)
                if projetil:
                    self.todos_sprites.add(projetil)
                    self.projeteis.add(projetil)
        else:
            # Se a tecla de espaço NÃO está pressionada e o som estava tocando, pare o som
            if self.som_de_tiro_tocando and self.som_tiro:
                self.som_tiro.stop()
                self.som_de_tiro_tocando = False
                      
    def gerenciar_uso_kit_medico(self):
        tempo_atual = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Só permite usar um kit a cada 300 ms
        if keys[pygame.K_e] and tempo_atual - self.cooldown_kitmed > 300:
            self.player.usar_kitmed()
            self.cooldown_kitmed = tempo_atual

    def gerenciar_coleta_itens(self):
        itens_coletados = pygame.sprite.spritecollide(self.player, self.coletaveis, True)
        for item in itens_coletados:
            self.player.coletar(item)
    
    def gerenciar_drops_inimigos(self):
        for inimigo in list(self.inimigos):
            if inimigo.vida <= 0:
                self.zumbis_mortos += 1
                coletavel = Moeda(inimigo.rect.centerx, inimigo.rect.centery)
                self.coletaveis.add(coletavel)
                self.todos_sprites.add(coletavel)
                inimigo.kill()

    def gerenciar_dano_sofrido_player(self):
        tempo_atual = pygame.time.get_ticks()
        # Verifica se o tempo de cooldown já passou
        if tempo_atual - self.ultimo_hit_player > COOLDOWN_DANO_JOGADOR:
            # Verifica colisão entre o jogador e os inimigos
            inimigos_colididos = pygame.sprite.spritecollide(self.player, self.inimigos, False)
            if inimigos_colididos:
                # Itera sobre todos os inimigos que colidiram
                for inimigo in inimigos_colididos:
                    # Aplica o dano no jogador
                    self.player.sofrer_dano(inimigo.dano)
                # Atualiza o tempo do último hit
                self.ultimo_hit_player = tempo_atual

    def update(self):
        # Se o jogo estiver em um estado final (VITORIA, DERROTA, etc.)
        if self.estado_jogo != 'JOGANDO':
            # Verificamos se já se passaram 3 segundos desde que o jogo acabou
            if pygame.time.get_ticks() - self.tempo_fim_jogo > 3000:
                return False  # Retorna False para encerrar o jogo
            return True  # Se não, mantém o jogo rodando na tela final
        
        if self.momento_pausa is not None: # Se tá pausado, não atualiza nada
            return True

        # --- LÓGICA DE JOGO ATIVO (só executa se self.estado_jogo == 'JOGANDO') ---
        tempo_atual = pygame.time.get_ticks()
        # Lógica para iniciar o timer da horda no primeiro frame
        if not self.jogo_comecou:
            self.ultimo_spawn_zombie = tempo_atual
            self.jogo_comecou = True

        # 1. VERIFICA CONDIÇÕES DE FIM DE JOGO E MUDA O ESTADO
        if self.zumbis_spawnados == QTD_ZOMBIES and self.zumbis_mortos == QTD_ZOMBIES:
            self.estado_jogo = 'VITORIA'
            self.tempo_fim_jogo = pygame.time.get_ticks() # Inicia o timer de 3 segundos

        elif self.player.vida <= 0:
            self.estado_jogo = 'DERROTA'
            self.tempo_fim_jogo = pygame.time.get_ticks() # Inicia o timer de 3 segundos
        
        else:
            # MODIFICADO: desconta o tempo que o jogo ficou pausado
            tempo_passado = (tempo_atual - self.tempo_inicial - self.tempo_pausado_total) / 1000
            tempo_restante = self.tempo_limite - tempo_passado
            if tempo_restante <= 0:
                self.estado_jogo = 'TEMPO_ESGOTADO'
                self.tempo_fim_jogo = pygame.time.get_ticks()
        
        # 2. ATUALIZA TODOS OS ELEMENTOS DO JOGO
        self.player.update(self.largura_mundo)
        self.coletaveis.update() 
        self.inimigos.update(self.player) #Atualiza os inimigos, passando a posição do jogador
        self.projeteis.update()
        self.particulas.update()

        #atualiza a câmera
        # A câmera segue o jogador, mantendo ele no centro da tela
        self.camera.center = self.player.rect.center
        # Garante que a câmera não saia dos limites do mundo
        if self.camera.left < 0:
            self.camera.left = 0
        if self.camera.right > self.largura_mundo:
            self.camera.right = self.largura_mundo
        if self.camera.top < 0:
            self.camera.top = 0
        if self.camera.bottom > self.altura_mundo:
            self.camera.bottom = self.altura_mundo

        self.gerenciar_tiros()
        self.gerenciar_coleta_itens()
        self.gerenciar_drops_inimigos()
        self.gerenciar_dano_sofrido_player()
        self.gerenciar_uso_kit_medico()

        # Lógica de hordas
        if not self.horda_em_andamento and tempo_atual - self.ultimo_spawn_zombie > INTERVALO_ENTRE_HORDAS and self.zumbis_spawnados < QTD_ZOMBIES:
            self.horda_em_andamento = True
            self.zumbis_para_spawnar_na_horda = ZOMBIES_POR_HORDA
            self.ultimo_spawn_zombie = tempo_atual

        if self.horda_em_andamento:
            if tempo_atual - self.ultimo_spawn_individual_zumbi > INTERVALO_SPAWN_ZUMBI_HORDA and self.zumbis_para_spawnar_na_horda > 0:
                self.spawn_zombie()
                self.zumbis_para_spawnar_na_horda -= 1
                self.ultimo_spawn_individual_zumbi = tempo_atual
            
            if self.zumbis_para_spawnar_na_horda == 0:
                self.horda_em_andamento = False

        return True # Se chegou até aqui, o jogo continua

    def draw(self, tela):
        # Se o jogo estiver acontecendo, desenha o jogo normalmente
        if self.estado_jogo == 'JOGANDO':
            # Desenha o fundo, deslocado pela câmera para criar o efeito de rolagem
            tela.blit(self.imagem_fundo, (0, 0), self.camera)
       
            # Desenha todos os outros sprites por cima do fundo, ajustando suas posições pela câmera
            for sprite in self.todos_sprites:
                tela.blit(sprite.imagem, sprite.rect.move(-self.camera.x, -self.camera.y))

                # Desenha a barra de vida para Zumbis e Obstáculos
                if isinstance(sprite, (Zombie, Obstaculo)):
                    porcentagem_vida = (sprite.vida / sprite.vida_maxima) * 100
                    bar_x = sprite.rect.centerx - 25 - self.camera.x
                    bar_y = sprite.rect.top - 15 - self.camera.y
                    self.draw_barra_vida(tela, bar_x, bar_y, porcentagem_vida, 50, 7) # Barra pequena (
                    
                # Desenha um retângulo vermelho ao redor de cada sprite
                #pygame.draw.rect(tela, (255, 0, 0), sprite.rect.move(-self.camera.x, -self.camera.y), 2)

           # Lógica do cronômetro
            tempo_atual = pygame.time.get_ticks()
            #!se o jogo está pausado, usamos o instante em que a pausa começou para congelar o cronômetro na tela
            if self.momento_pausa is not None:
                tempo_atual = self.momento_pausa
            #!desconta o tempo pausado do cálculo do tempo passado
            tempo_passado = (tempo_atual - self.tempo_inicial - self.tempo_pausado_total) / 1000
            tempo_restante = self.tempo_limite - tempo_passado

            # Garante que o cronômetro não fique negativo na tela
            if tempo_restante < 0:
                tempo_restante = 0
        
            # Exibir o cronômetro
            minutos = int(tempo_restante) // 60
            segundos = int(tempo_restante) % 60
            texto_tempo = f"{minutos:02}:{segundos:02}"
            
            texto_cronometro = self.fonte.render(texto_tempo, True, (255,255,255))
            tela.blit(texto_cronometro, (1100, 15))

            # Função auxiliar para desenhar cada item da UI
            def draw_ui_item(icon, text, x, y):
                tela.blit(icon, (x, y))
                superficie_texto = self.font.render(str(text), True, (255, 255, 255))
                texto_rect = superficie_texto.get_rect(center=(x + 30, y + 70))
                tela.blit(superficie_texto, texto_rect)
            
            # Desenha a barra de vida do jogador e outros itens
            porcentagem_vida_player = (self.player.vida / self.player.vida_maxima) * 100
            tela.blit(self.icone_vida, (20, 10))
            self.draw_barra_vida(tela, 70, 20, porcentagem_vida_player, 150, 25) # Barra grande (150x25)

            draw_ui_item(self.icone_municao, self.player.municao, 230, 10)
            draw_ui_item(self.icone_moeda, self.player.moedas, 290, 10)
            draw_ui_item(self.icone_medkit, self.player.kitmeds, 360, 10)
    
        # Se o jogo acabou, desenha a tela final correspondente
        elif self.estado_jogo == 'VITORIA':
            tela.fill((0, 0, 0))
            texto_vitoria = self.fonte.render("Você Venceu, Parabéns!", True, (0, 255, 50))
            texto_rect = texto_vitoria.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(texto_vitoria, texto_rect)

        elif self.estado_jogo == 'DERROTA':
            tela.fill((0, 0, 0))
            texto_derrota = self.fonte.render("Você Perdeu!", True, (255, 0, 0))
            texto_rect = texto_derrota.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(texto_derrota, texto_rect)

        elif self.estado_jogo == 'TEMPO_ESGOTADO':
            tela.fill((0, 0, 0))
            texto_derrota = self.fonte.render("Tempo Esgotado! Você Perdeu.", True, (255, 0, 0))
            texto_rect = texto_derrota.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(texto_derrota, texto_rect)