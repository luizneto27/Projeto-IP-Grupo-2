# scripts/game.py
import pygame
import random
from scripts.soldados import Soldado
from scripts.boss import Boss
from scripts.monstrinhos import Monstrinho
from scripts.carta import Carta
from scripts.coletaveis import Vida 

class Game:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.todos_sprites = pygame.sprite.Group()
        self.humanos_grupo = pygame.sprite.Group()
        self.enemies_grupo = pygame.sprite.Group()
        self.coletaveis_grupo = pygame.sprite.Group()

        self.recurso_sangue = 0
        self.game_over = False
        self.vitoria = False
        self.carta_selecionada = None
        self.soldado_fantasma_surf = None 
        
        self.posicoes_linhas = [300, 450, 600]
        self.largura_casa = 120
        self.x_inicial_grade = 50

        self.imagem_fundo = pygame.image.load(r'Imagens/fundodojogo.webp').convert()
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (self.largura_tela, self.altura_tela))
        
        boss_pos_x = self.largura_tela - 150
        boss_pos_y = self.posicoes_linhas[1] 
        self.boss = Boss(vida_total=2000, pos_x=boss_pos_x, pos_y=boss_pos_y, dano=20)
        self.todos_sprites.add(self.boss)
        
        self.cartas = []
        caminho_img_soldado_comum = 'Imagens/soldado_comum_parado.png'
        self.cartas.append(Carta(caminho_img_soldado_comum, 50, self.altura_tela - 90, 'comum', custo=300, cost_type='time', imagem_soldado_path=caminho_img_soldado_comum))
        
        caminho_img_soldado_buff = 'Imagens/soldado_upgrade_parado.png'
        self.cartas.append(Carta(caminho_img_soldado_buff, 150, self.altura_tela - 90, 'buffado', custo=100, cost_type='blood', imagem_soldado_path=caminho_img_soldado_buff))

        self.spawn_inimigo_timer_max = 180 
        self.spawn_inimigo_timer = self.spawn_inimigo_timer_max
        
        self.spawn_vida_timer_max = 600
        self.spawn_vida_timer = self.spawn_vida_timer_max

    def handle_event(self, event):
        if self.game_over or self.vitoria: return

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if event.button == 3: 
                if self.carta_selecionada:
                    self.carta_selecionada = None
                    self.soldado_fantasma_surf = None
                    return
            
            if self.carta_selecionada:
                if pos[1] < self.altura_tela - 100 and pos[0] < self.boss.rect.left:
                    casa_rect = self.get_grid_rect(pos)
                    if casa_rect:
                        self.spawn_humano(self.carta_selecionada.tipo_soldado, casa_rect)
                        
                        if self.carta_selecionada.cost_type == 'blood':
                            self.recurso_sangue -= self.carta_selecionada.custo
                        
                        self.carta_selecionada.usar()
                        self.carta_selecionada = None
                        self.soldado_fantasma_surf = None
            
            else:
                for carta in self.cartas:
                    if carta.clicou_em_cima(pos) and carta.pode_usar(self.recurso_sangue):
                        self.carta_selecionada = carta
                        self.soldado_fantasma_surf = pygame.image.load(carta.imagem_soldado_path).convert_alpha()
                        self.soldado_fantasma_surf = pygame.transform.scale(self.soldado_fantasma_surf, (100,100))
                        self.soldado_fantasma_surf.set_alpha(150)
                        break 
    
    def get_grid_rect(self, pos_mouse):
        linha_idx = min(range(len(self.posicoes_linhas)), key=lambda i: abs(self.posicoes_linhas[i] - pos_mouse[1]))
        pos_y_linha = self.posicoes_linhas[linha_idx]

        coluna_idx = (pos_mouse[0] - self.x_inicial_grade) // self.largura_casa
        pos_x_casa = self.x_inicial_grade + (coluna_idx * self.largura_casa)

        return pygame.Rect(pos_x_casa, pos_y_linha - 50, self.largura_casa, 100)

    def spawn_humano(self, tipo, casa_rect):
        pos_x, pos_y = casa_rect.center
        
        if tipo == 'comum':
            novo_soldado = Soldado(vida_total=100, pos_x=pos_x, pos_y=pos_y, dano=10)
        elif tipo == 'buffado':
            novo_soldado = Soldado(vida_total=200, pos_x=pos_x, pos_y=pos_y, dano=25)
        
        self.humanos_grupo.add(novo_soldado)
        self.todos_sprites.add(novo_soldado)

    # ESTA FUNÇÃO GARANTE QUE OS MONSTROS APAREÇAM NAS FILEIRAS
    def spawn_enemy(self):
        # 1. Sorteia a fileira de onde o monstro vai sair
        linha_idx = random.randint(0, 2)
        pos_y_spawn = self.posicoes_linhas[linha_idx]
        
        # 2. A posição X de spawn agora é a frente do Boss
        pos_x_spawn = self.boss.rect.left 
        
        # 3. Cria o monstrinho na posição calculada
        novo_monstro = Monstrinho(vida_total=50, pos_x=pos_x_spawn, pos_y=pos_y_spawn, dano=1, velocidade=1)
        self.enemies_grupo.add(novo_monstro)
        self.todos_sprites.add(novo_monstro)
    
    def spawn_vida(self):
        pos_x = random.randint(50, self.largura_tela - 50)
        pos_y = -50 
        nova_vida = Vida(pos_x, pos_y, self.altura_tela)
        self.coletaveis_grupo.add(nova_vida)
        self.todos_sprites.add(nova_vida)

    def update(self):
        if self.game_over or self.vitoria: return

        for carta in self.cartas:
            carta.update()
            
        self.spawn_inimigo_timer -= 1
        if self.spawn_inimigo_timer <= 0:
            self.spawn_enemy()
            self.spawn_inimigo_timer = self.spawn_inimigo_timer_max
        
        self.spawn_vida_timer -= 1
        if self.spawn_vida_timer <= 0:
            self.spawn_vida()
            self.spawn_vida_timer = self.spawn_vida_timer_max

        for soldado in self.humanos_grupo:
            inimigos_na_frente = [e for e in self.enemies_grupo if abs(e.rect.centery - soldado.rect.centery) < 40]
            alvos = inimigos_na_frente if inimigos_na_frente else [self.boss]
            
            if soldado.atacar(alvos, self.coletaveis_grupo, self.todos_sprites):
                self.recurso_sangue += 10

        for monstro in self.enemies_grupo:
            soldados_na_frente = [s for s in self.humanos_grupo if abs(s.rect.centery - monstro.rect.centery) < 40]
            monstro.update(soldados_na_frente)
            if monstro.rect.right < 0:
                monstro.kill()
                self.game_over = True

        self.coletaveis_grupo.update()
        for coletavel in pygame.sprite.groupcollide(self.humanos_grupo, self.coletaveis_grupo, False, True).keys():
            pass

        if not self.boss.esta_vivo():
            self.vitoria = True
            print("VITÓRIA!")
    
    def draw(self, tela):
        tela.blit(self.imagem_fundo, (0,0))
        
        linha_surf = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        for y in self.posicoes_linhas:
            pygame.draw.line(linha_surf, (70, 100, 80, 120), (0, y), (self.largura_tela, y), 5)
        tela.blit(linha_surf, (0,0))
        
        # self.todos_sprites.draw(tela) # Desabilitado para usar o draw customizado de cada sprite
        for sprite in self.todos_sprites:
            if hasattr(sprite, 'image'): # Desenha o sprite principal
                 tela.blit(sprite.image, sprite.rect)
            if hasattr(sprite, 'draw'): # Chama o draw customizado (para barras de vida, etc)
                sprite.draw(tela)

        for carta in self.cartas:
            carta.draw(tela, self.recurso_sangue)
            
        if self.carta_selecionada and self.soldado_fantasma_surf:
            pos_mouse = pygame.mouse.get_pos()
            casa_rect = self.get_grid_rect(pos_mouse)
            if casa_rect:
                rect_fantasma = self.soldado_fantasma_surf.get_rect(center=casa_rect.center)
                tela.blit(self.soldado_fantasma_surf, rect_fantasma)
            
        fonte = pygame.font.SysFont('Arial', 30)
        texto_sangue = fonte.render(f"Sangue: {self.recurso_sangue}", True, (255, 255, 0))
        tela.blit(texto_sangue, (self.largura_tela - 200, self.altura_tela - 50))
        
        if self.vitoria:
            fonte_final = pygame.font.SysFont('Impact', 100)
            texto_vitoria = fonte_final.render("VITÓRIA!", True, (0, 255, 0))
            pos_x = (self.largura_tela - texto_vitoria.get_width()) / 2
            pos_y = (self.altura_tela - texto_vitoria.get_height()) / 2
            tela.blit(texto_vitoria, (pos_x, pos_y))

        if self.game_over:
            fonte_final = pygame.font.SysFont('Impact', 100)
            texto_derrota = fonte_final.render("FIM DE JOGO", True, (255, 0, 0))
            pos_x = (self.largura_tela - texto_derrota.get_width()) / 2
            pos_y = (self.altura_tela - texto_derrota.get_height()) / 2
            tela.blit(texto_derrota, (pos_x, pos_y))
        
        # para ver as caixas de colisão
        #for sprite in self.todos_sprites:
            #pygame.draw.rect(tela, (255, 0, 0), sprite.rect, 2) # Desenha um retângulo vermelho em volta de cada sprite