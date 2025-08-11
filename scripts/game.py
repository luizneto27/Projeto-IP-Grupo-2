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
    def __init__(self, width, height):
        self.width = width
        self.height = height

        #CÂMERA E MUNDO
        # Define o tamanho total
        self.world_width = width * 2
        self.world_height = height

        #imagem de fundo
        self.background_image = pygame.image.load('Imagens/fundodojogo.webp').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.world_width, height))

        #Grupo de Sprites
        self.player = Player(width // 2, height // 2)
        self.enemies = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        
        # A câmera é um retângulo que representa a área visível da tela
        self.camera = pygame.Rect(0, 0, self.width, self.height)

        # tempo de jogo
        self.tempo_limite = 120 # seg
        self.tempo_inicial = pygame.time.get_ticks()
        self.fonte = pygame.font.Font(None, 74)

        self.zumbis_spawnados = 0 # contador de zumbis
        self.zumbis_mortos = 0 # o proprio nome ja diz

        #CARREGAR ÍCONES 
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.health_icon = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de coração/vida
        self.ammo_icon = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de munição
        self.coin_icon = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de moeda
        self.medkit_icon = pygame.transform.scale(pygame.image.load('Imagens/imagem-soldado-comum.gif').convert_alpha(),(40,40)) # Substitua pela imagem de kit médico
        
        self.spawn_initial_elements()
        self.last_shot_time = 0 # Controle para cadência de tiro
        self.last_zombie_spawn = pygame.time.get_ticks()
        # Guarda o tempo do último hit no jogador para o cooldown
        self.last_player_hit = 0

    def draw_health_bar(self, surf, x, y, pct, bar_length, bar_height):
        if pct < 0:
            pct = 0
        
        fill = (pct / 100) * bar_length
        outline_rect = pygame.Rect(x, y, bar_length, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)

        # Define a cor da barra com base na porcentagem de vida
        if pct > 75:
            color = (0, 255, 0)  # Verde
        elif pct > 30:
            color = (255, 255, 0)  # Amarelo
        else:
            color = (255, 0, 0)  # Vermelho

        pygame.draw.rect(surf, (40, 40, 40), outline_rect)  # Fundo cinza escuro
        pygame.draw.rect(surf, color, fill_rect)         # Barra de vida
    
    def spawn_initial_elements(self):
        # Posiciona os elementos no mundo de jogo
        for i in range(5):
            self.spawn_zombie()

        # Spawna 3 flores em posições aleatórias à frente (à direita) do jogador
        for j in range(6):
            # Gera uma posição X aleatória entre 200 e 1000 pixels à direita do jogador
            pos_x = self.player.rect.centerx + random.randint(200, 1000)
            # Gera uma posição Y aleatória na altura do mapa
            pos_y = random.randint(100, self.height - 100)
            flor = Flor(pos_x, pos_y)
            self.obstacles.add(flor)
            self.all_sprites.add(flor)

        # Spawna 2 containers em posições aleatórias à frente (à direita) do jogador
        for k in range(4):
            # Gera uma posição X aleatória entre 300 e 1500 pixels à direita do jogador
            pos_x = self.player.rect.centerx + random.randint(300, 1500)
            # Gera uma posição Y aleatória na altura do mapa
            pos_y = random.randint(100, self.height - 100)
            container = Container(pos_x, pos_y)
            self.obstacles.add(container)
            self.all_sprites.add(container)

    def spawn_zombie(self):
        # Spawna o zumbi em uma altura aleatória, à direita do mundo visível
        pos_y = random.randint(100, self.height - 100)
        pos_x = self.camera.right + random.randint(50, 200)
        zombie = Zombie(pos_x, pos_y)
        self.enemies.add(zombie)
        self.all_sprites.add(zombie)

        self.zumbis_spawnados += 1 # ate atingir 100, se tiver errado corrige pra += 5

    def handle_shooting(self):
        #lógica de tiro
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > CADENCIA_TIRO:
                self.last_shot_time = current_time
                projectile = self.player.shoot(self.enemies, self.obstacles, self.collectibles, self.all_sprites)
                if projectile:
                    self.projectiles.add(projectile)
                    self.all_sprites.add(projectile)
       
    def handle_collecting_items(self):
        collected_items = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for item in collected_items:
            self.player.collect(item)
    
    def handle_enemy_drops(self):
        for enemy in list(self.enemies):
            if enemy.health <= 0:
                self.zumbis_mortos += 1
                collectible = Moeda(enemy.rect.centerx, enemy.rect.centery)
                self.collectibles.add(collectible)
                self.all_sprites.add(collectible)
                enemy.kill()

    def handle_player_damage(self):
        current_time = pygame.time.get_ticks()
        # Verifica se o tempo de cooldown já passou
        if current_time - self.last_player_hit > COOLDOWN_DANO_JOGADOR:
            # Verifica colisão entre o jogador e os inimigos
            collided_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if collided_enemies:
                # Pega o primeiro inimigo da lista de colisão
                enemy = collided_enemies[0]
                # Aplica o dano no jogador
                self.player.take_damage(enemy.damage)
                # Atualiza o tempo do último hit
                self.last_player_hit = current_time

    def update(self):
        # 1. Atualiza o jogador (e outros sprites que não precisam de argumentos)
        self.player.update()
        self.collectibles.update() # Atualiza os coletáveis (ex: animações, movimento)
        # 2. Atualiza os inimigos, passando a posição do jogador
        self.enemies.update(self.player)
        self.projectiles.update()

        #ATUALIZAR A CÂMERA
        # A câmera segue o jogador, mantendo ele no centro da tela
        self.camera.center = self.player.rect.center
          # Garante que a câmera não saia dos limites do mundo
        if self.camera.left < 0:
            self.camera.left = 0
        if self.camera.right > self.world_width:
            self.camera.right = self.world_width
        if self.camera.top < 0:
            self.camera.top = 0
        if self.camera.bottom > self.world_height:
            self.camera.bottom = self.world_height

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
        current_time = pygame.time.get_ticks()
        # Verifica se o tempo de respawn já passou E se ainda faltam zumbis para spawnar
        if current_time - self.last_zombie_spawn > INTERVALO_RESPAWN_ZOMBIE and self.zumbis_spawnados < QTD_ZOMBIES:
            self.spawn_zombie()
            self.last_zombie_spawn = current_time

    def draw(self, screen):
        # Desenha o fundo, deslocado pela câmera para criar o efeito de rolagem
        screen.blit(self.background_image, (0, 0), self.camera)
        # Desenha todos os outros sprites por cima do fundo
        # Desenha todos os sprites, ajustando suas posições pela câmera
        for sprite in self.all_sprites:
            screen.blit(sprite.image, sprite.rect.move(-self.camera.x, -self.camera.y))

            # Desenha a barra de vida para Zumbis e Obstáculos
            if isinstance(sprite, (Zombie, Obstacle)):
                health_pct = (sprite.vida / sprite.vida_maxima) * 100
                bar_x = sprite.rect.centerx - 25 - self.camera.x
                bar_y = sprite.rect.top - 15 - self.camera.y
                self.draw_health_bar(screen, bar_x, bar_y, health_pct, 50, 7) # Barra pequena (50x7)
                
            # Desenha um retângulo vermelho ao redor de cada sprite
            pygame.draw.rect(screen, (255, 0, 0), sprite.rect.move(-self.camera.x, -self.camera.y), 2)

        # Fundo da UI
        ui_bg = pygame.Surface((self.width, 80), pygame.SRCALPHA)
        ui_bg.fill((0, 0, 0, 150))
        screen.blit(ui_bg, (0, 0))

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
            screen.blit(icon, (x, y))
            text_surface = self.font.render(str(text), True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(x + 20, y + 60))
            screen.blit(text_surface, text_rect)
        
        # Desenha a barra de vida do jogador
        player_health_pct = (self.player.vida / self.player.vida_maxima) * 100
        screen.blit(self.health_icon, (20, 10))
        self.draw_health_bar(screen, 70, 20, player_health_pct, 150, 25) # Barra grande (150x25)

        draw_ui_item(self.ammo_icon, self.player.municao, 230, 10)
        draw_ui_item(self.coin_icon, self.player.moedas, 290, 10)
        draw_ui_item(self.medkit_icon, self.player.kitmeds, 360, 10)