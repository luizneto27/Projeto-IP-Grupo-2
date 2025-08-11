# game.py
import pygame
import random
from scripts.player import Player
from scripts.zombie import Zombie
from scripts.obstaculos import Flor, Container, Obstacle
from scripts.coletaveis import KitMedico, Moeda, Municao
from scripts.projeteis import Projetil
from scripts.constantes import CADENCIA_TIRO, INTERVALO_RESPAWN_ZOMBIE, COOLDOWN_DANO_JOGADOR, QTD_ZOMBIES, LARGURA_TELA, ALTURA_TELA

# configura a tela e o titulo da janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Bem vindo ao jogo!')

class Game:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        #CÂMERA E MUNDO
        # Define o tamanho total
        self.largura_mundo = largura * 2
        self.altura_mundo = altura

        #imagem de fundo
        self.imagem_fundo = pygame.image.load('Imagens/fundodojogo.webp').convert()
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (self.largura_mundo, altura))

        #Grupo de Sprites
        self.player = Player(largura // 2, altura // 2)
        self.inimigos = pygame.sprite.Group()
        self.obstaculos = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()
        self.projeteis = pygame.sprite.Group()
        self.todos_sprites = pygame.sprite.Group(self.player)
        
        # A câmera é um retângulo que representa a área visível da tela
        self.camera = pygame.Rect(0, 0, self.largura, self.altura)

        # tempo de jogo
        self.tempo_limite = 120 # seg
        self.tempo_inicial = pygame.time.get_ticks()
        self.fonte = pygame.font.Font(None, 74)

        self.zumbis_spawnados = 0 # contador de zumbis
        self.zumbis_mortos = 0 # o proprio nome ja diz

        #CARREGAR ÍCONES 
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.icone_vida = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de coração/vida
        self.icone_municao = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de munição
        self.icone_moeda = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de moeda
        self.icone_medkit = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de kit médico
        
        self.spawn_initial_elements()
        self.ultimo_tiro = 0 # Controle para cadência de tiro
        self.ultimo_spawn_zombie = pygame.time.get_ticks()
        # Guarda o tempo do último hit no jogador para o cooldown
        self.ultimo_hit_player = 0

    def draw_health_bar(self, superficie, x, y, porcentagem, largura_barra, altura_barra):
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
    
    def spawn_initial_elements(self):
        # Posiciona os elementos no mundo de jogo
        for i in range(5):
            self.spawn_zombie()

        # Spawna 3 flores em posições aleatórias à frente (à direita) do jogador
        for j in range(6):
            # Gera uma posição X aleatória entre 200 e 1000 pixels à direita do jogador
            pos_x = self.player.rect.centerx + random.randint(200, 1000)
            # Gera uma posição Y aleatória na altura do mapa
            pos_y = random.randint(100, self.altura - 100)
            flor = Flor(pos_x, pos_y)
            self.obstaculos.add(flor)
            self.todos_sprites.add(flor)

        # Spawna 2 containers em posições aleatórias à frente (à direita) do jogador
        for k in range(4):
            # Gera uma posição X aleatória entre 300 e 1500 pixels à direita do jogador
            pos_x = self.player.rect.centerx + random.randint(300, 1500)
            # Gera uma posição Y aleatória na altura do mapa
            pos_y = random.randint(100, self.altura - 100)
            container = Container(pos_x, pos_y)
            self.obstaculos.add(container)
            self.todos_sprites.add(container)

    def spawn_zombie(self):
        # Spawna o zumbi em uma altura aleatória, à direita do mundo visível
        pos_y = random.randint(100, self.altura - 100)
        pos_x = self.camera.right + random.randint(50, 200)
        zombie = Zombie(pos_x, pos_y)
        self.inimigos.add(zombie)
        self.todos_sprites.add(zombie)

        self.zumbis_spawnados += 1 # ate atingir 100, se tiver errado corrige pra += 5

    def handle_shooting(self):
        #lógica de tiro
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.ultimo_tiro > CADENCIA_TIRO:
                self.ultimo_tiro = tempo_atual
                projetil = self.player.shoot(self.inimigos, self.obstaculos, self.coletaveis, self.todos_sprites)
                if projetil:
                    self.projeteis.add(projetil)
                    self.todos_sprites.add(projetil)
       
    def handle_collecting_items(self):
        itens_coletados = pygame.sprite.spritecollide(self.player, self.coletaveis, True)
        for item in itens_coletados:
            self.player.collect(item)
    
    def handle_enemy_drops(self):
        for inimigo in list(self.inimigos):
            if inimigo.vida <= 0:
                self.zumbis_mortos += 1
                coletavel = Moeda(inimigo.rect.centerx, inimigo.rect.centery)
                self.coletaveis.add(coletavel)
                self.todos_sprites.add(coletavel)
                inimigo.kill()

    def handle_player_damage(self):
        tempo_atual = pygame.time.get_ticks()
        # Verifica se o tempo de cooldown já passou
        if tempo_atual - self.ultimo_hit_player > COOLDOWN_DANO_JOGADOR:
            # Verifica colisão entre o jogador e os inimigos
            inimigos_colididos = pygame.sprite.spritecollide(self.player, self.inimigos, False)
            if inimigos_colididos:
                # Pega o primeiro inimigo da lista de colisão
                inimigo = inimigos_colididos[0]
                # Aplica o dano no jogador
                self.player.take_damage(inimigo.dano)
                # Atualiza o tempo do último hit
                self.ultimo_hit_player = tempo_atual

    def update(self):
        # 1. Atualiza o jogador (e outros sprites que não precisam de argumentos)
        self.player.update()
        self.coletaveis.update() # Atualiza os coletáveis (ex: animações, movimento)
        # 2. Atualiza os inimigos, passando a posição do jogador
        self.inimigos.update(self.player)
        self.projeteis.update()

        #ATUALIZAR A CÂMERA
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

        self.handle_shooting()
        self.handle_collecting_items()
        self.handle_enemy_drops()
        self.handle_player_damage()

        # Lógica de vitória: verifica se todos os zumbis foram eliminados
        if self.zumbis_spawnados >= QTD_ZOMBIES and self.zumbis_mortos == QTD_ZOMBIES:
            tela.fill((0,0,0))
            texto_vitoria = self.fonte.render("Você Venceu, Parabéns!", True, (0,255,50))
            texto_rect = texto_vitoria.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(texto_vitoria, texto_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
            pygame.quit()
            # Depois, você deve encerrar o jogo ou voltar ao menu
            return

        # Lógica de derrota por morte do jogador
        if self.player.vida <= 0:
            tela.fill((0,0,0))
            texto_derrota = self.fonte.render("Você Perdeu!", True, (255,0,0))
            texto_rect = texto_derrota.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(texto_derrota, texto_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
            pygame.quit()
            return

        # Lógica de derrota por tempo esgotado
        tempo_decorrido = (pygame.time.get_ticks() - self.tempo_inicial) / 1000
        if tempo_decorrido >= self.tempo_limite:
            return

        # Respawn dinâmico
        tempo_atual = pygame.time.get_ticks()
        # Verifica se o tempo de respawn já passou E se ainda faltam zumbis para spawnar
        if tempo_atual - self.ultimo_spawn_zombie > INTERVALO_RESPAWN_ZOMBIE and self.zumbis_spawnados < QTD_ZOMBIES:
            self.spawn_zombie()
            self.ultimo_spawn_zombie = tempo_atual

    def draw(self, tela):
        # Desenha o fundo, deslocado pela câmera para criar o efeito de rolagem
        tela.blit(self.imagem_fundo, (0, 0), self.camera)
        # Desenha todos os outros sprites por cima do fundo
        # Desenha todos os sprites, ajustando suas posições pela câmera
        for sprite in self.todos_sprites:
            tela.blit(sprite.imagem, sprite.rect.move(-self.camera.x, -self.camera.y))

            # Desenha a barra de vida para Zumbis e Obstáculos
            if isinstance(sprite, (Zombie, Obstacle)):
                porcentagem_vida = (sprite.vida / sprite.vida_maxima) * 100
                bar_x = sprite.rect.centerx - 25 - self.camera.x
                bar_y = sprite.rect.top - 15 - self.camera.y
                self.draw_health_bar(tela, bar_x, bar_y, porcentagem_vida, 50, 7) # Barra pequena (50x7)
                
            # Desenha um retângulo vermelho ao redor de cada sprite
            pygame.draw.rect(tela, (255, 0, 0), sprite.rect.move(-self.camera.x, -self.camera.y), 2)

        # Fundo da UI
        ui_bg = pygame.Surface((self.largura, 80), pygame.SRCALPHA)
        ui_bg.fill((0, 0, 0, 150))
        tela.blit(ui_bg, (0, 0))

        # Lógica do cronômetro
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = (tempo_atual - self.tempo_inicial) / 1000  # Converte para segundos
        tempo_restante = self.tempo_limite - tempo_passado

        # lógica de vitória e derrota
        if tempo_restante <= 0:
            tela.fill((0,0,0))
            texto_derrota = self.fonte.render("Tempo Esgotado! Você Perdeu.", True, (255,0,0))
            texto_rect = texto_derrota.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            tela.blit(texto_derrota, texto_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
            pygame.quit()

        # Exibir o cronômetro
        minutos = int(tempo_restante) // 60
        segundos = int(tempo_restante) % 60
        texto_tempo = f"{minutos:02}:{segundos:02}"
            
        texto_cronometro = self.fonte.render(texto_tempo, True, (255,0,0))
        tela.blit(texto_cronometro, (1100, 15))

        # Função auxiliar para desenhar cada item da UI
        def draw_ui_item(icon, text, x, y):
            tela.blit(icon, (x, y))
            superficie_texto = self.font.render(str(text), True, (255, 0, 0))
            texto_rect = superficie_texto.get_rect(center=(x + 20, y + 60))
            tela.blit(superficie_texto, texto_rect)
        
        # Desenha a barra de vida do jogador
        porcentagem_vida_player = (self.player.vida / self.player.vida_maxima) * 100
        tela.blit(self.icone_vida, (20, 10))
        self.draw_health_bar(tela, 70, 20, porcentagem_vida_player, 150, 25) # Barra grande (150x25)

        draw_ui_item(self.icone_municao, self.player.municao, 230, 10)
        draw_ui_item(self.icone_moeda, self.player.moedas, 290, 10)
        draw_ui_item(self.icone_medkit, self.player.kitmeds, 360, 10)