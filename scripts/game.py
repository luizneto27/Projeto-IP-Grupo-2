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

        self.recurso_sangue = 100
        self.game_over = False
        self.vitoria = False
        # NOVO: Variável para gerenciar o estado de posicionamento
        self.carta_selecionada = None
        self.soldado_fantasma_surf = None # Superfície para a imagem fantasma
    
        self.posicoes_linhas = [300, 450, 600] # ALTERADO: Posições ajustadas para tela maior
        
        self.imagem_fundo = pygame.image.load('Imagens/ideiainicialtela.png').convert()
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (self.largura_tela, self.altura_tela))
        
        self.boss = Boss(vida_total=2000, pos_x=self.largura_tela - 280, pos_y=self.posicoes_linhas[1] - 100, dano=20)
        self.todos_sprites.add(self.boss)
        
        self.cartas = []
        # ALTERADO: Passar o caminho da imagem do soldado para a carta
        caminho_img_soldado = 'Imagens/imagem-soldado-comum.gif'
        self.cartas.append(Carta(caminho_img_soldado, 50, self.altura_tela - 90, 'comum', custo=50, imagem_soldado_path=caminho_img_soldado))

        # --- CORRIGIDO: Inicialização dos Timers ---
        self.spawn_inimigo_timer_max = 180 # 3 segundos a 60 FPS
        self.spawn_inimigo_timer = self.spawn_inimigo_timer_max
        
        # NOVO: Timer para spawn de coletável de vida
        self.spawn_vida_timer_max = 600 # A cada 10 segundos
        self.spawn_vida_timer = self.spawn_vida_timer_max

    def handle_event(self, event):
        if self.game_over or self.vitoria: return

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # NOVO: Lógica para cancelar seleção com o botão direito
            if event.button == 3: # 3 é o botão direito do mouse
                if self.carta_selecionada:
                    self.carta_selecionada = None
                    self.soldado_fantasma_surf = None
                    return
            
            # --- Lógica de posicionamento (se uma carta já foi selecionada) ---
            if self.carta_selecionada:
                # Verifica se o clique foi na área de jogo (não nas cartas)
                if pos[1] < self.altura_tela - 100:
                    linha_escolhida = self.escolher_linha_por_pos(pos)
                    pos_x_clique = pos[0] # Pega a posição X do clique
                    
                    self.spawn_humano(linha_escolhida, pos_x_clique) # Passa a posição X
                    
                    # Consome os recursos e reinicia o estado
                    self.recurso_sangue -= self.carta_selecionada.custo
                    self.carta_selecionada.usar()
                    self.carta_selecionada = None
                    self.soldado_fantasma_surf = None
            
             # --- Lógica de seleção de carta (se nenhuma carta estiver selecionada) ---
            else:
                 for carta in self.cartas:
                    if carta.clicou_em_cima(pos) and carta.pode_usar() and self.recurso_sangue >= carta.custo:
                        self.carta_selecionada = carta
                        # Prepara a imagem "fantasma" para o cursor
                        self.soldado_fantasma_surf = pygame.image.load(carta.imagem_soldado_path).convert_alpha()
                        self.soldado_fantasma_surf = pygame.transform.scale(self.soldado_fantasma_surf, (100,100)) # Tamanho do soldado
                        self.soldado_fantasma_surf.set_alpha(150) # Deixa semitransparente
                        break # Para de checar outras cartas          
    
    # NOVO: Função para escolher a linha com base no clique do mouse
    def escolher_linha_por_pos(self, pos_mouse):
        # Retorna o índice da linha mais próxima da altura do clique
        return min(range(len(self.posicoes_linhas)), key=lambda i: abs(self.posicoes_linhas[i] - pos_mouse[1]))

    def spawn_humano(self, linha, pos_x):
        pos_y = self.posicoes_linhas[linha]
        novo_soldado = Soldado(vida_total=100, pos_x=pos_x, pos_y=pos_y, dano=10)
        self.humanos_grupo.add(novo_soldado)
        self.todos_sprites.add(novo_soldado)

    def spawn_enemy(self): # ALTERADO: Removido parâmetro 'linha' que não era usado
        linha = random.randint(0, 2)
        pos_x = self.largura_tela + 50
        pos_y = self.posicoes_linhas[linha]
        novo_monstro = Monstrinho(vida_total=50, pos_x=pos_x, pos_y=pos_y, dano=1, velocidade=1)
        self.enemies_grupo.add(novo_monstro)
        self.todos_sprites.add(novo_monstro)
    
    # NOVO: Função para spawnar o coletável de vida
    def spawn_vida(self):
        pos_x = random.randint(50, self.largura_tela - 50)
        pos_y = -50 # Começa acima da tela
        nova_vida = Vida(pos_x, pos_y, self.altura_tela)
        self.coletaveis_grupo.add(nova_vida)
        self.todos_sprites.add(nova_vida)

    def update(self):
        if self.game_over or self.vitoria: return

        for carta in self.cartas:
            carta.update()
            
        # --- Lógica de Spawn ---
        self.spawn_inimigo_timer -= 1
        if self.spawn_inimigo_timer <= 0:
            self.spawn_enemy()
            self.spawn_inimigo_timer = self.spawn_inimigo_timer_max
        
        # NOVO: Lógica de spawn de vida
        self.spawn_vida_timer -= 1
        if self.spawn_vida_timer <= 0:
            self.spawn_vida()
            self.spawn_vida_timer = self.spawn_vida_timer_max

        # --- Lógica de Combate ---
        for soldado in self.humanos_grupo:
            inimigos_na_frente = [e for e in self.enemies_grupo if abs(e.rect.centery - soldado.rect.centery) < 40]
            alvos = inimigos_na_frente if inimigos_na_frente else [self.boss]
            # ALTERADO: Passa os grupos necessários para o método atacar
            soldado.atacar(alvos, self.coletaveis_grupo, self.todos_sprites)

        # --- Lógica de Ataque dos Inimigos ---
        for monstro in self.enemies_grupo:
            soldados_na_frente = [s for s in self.humanos_grupo if abs(s.rect.centery - monstro.rect.centery) < 40]
            monstro.update(soldados_na_frente)
            if monstro.rect.right < 0:
                monstro.kill()
                self.game_over = True

        # --- Lógica de Coletáveis ---
        self.coletaveis_grupo.update()
        for coletavel in self.coletaveis_grupo:
            if coletavel.tipo == 'sangue':
                if coletavel.rect.collidepoint(pygame.mouse.get_pos()):
                    self.recurso_sangue += 25
                    coletavel.kill()
            elif coletavel.tipo == 'arma':
                for soldado in self.humanos_grupo:
                    if soldado.rect.colliderect(coletavel.rect):
                        soldado.upgrade()
                        coletavel.kill()
                        break
            # NOVO: Lógica para o coletável de vida
            elif coletavel.tipo == 'vida':
                if self.humanos_grupo: # Só cura se houver soldados
                    soldado_a_curar = None
                    menor_vida_perc = 1
                    # Encontra o soldado com a menor % de vida
                    for s in self.humanos_grupo:
                        vida_perc = s.vida_atual / s.vida_total
                        if vida_perc < menor_vida_perc:
                            menor_vida_perc = vida_perc
                            soldado_a_curar = s
                    
                    if soldado_a_curar and soldado_a_curar.rect.colliderect(coletavel.rect):
                        soldado_a_curar.curar(coletavel.valor_cura)
                        coletavel.kill()

        # --- Checagem de Drops de Monstros ---
        for monstro in self.enemies_grupo:
            if not monstro.esta_vivo():
                drop = monstro.levar_dano(0)
                if drop:
                    self.coletaveis_grupo.add(drop)
                    self.todos_sprites.add(drop)
                monstro.kill()
        
        if not self.boss.esta_vivo():
            self.vitoria = True
            print("VITÓRIA!")
    
    def draw(self, tela):
        tela.blit(self.imagem_fundo, (0,0))
        
        linha_surf = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        for y in self.posicoes_linhas:
            pygame.draw.line(linha_surf, (70, 100, 80, 120), (0, y), (self.largura_tela, y), 5)
        tela.blit(linha_surf, (0,0))
        
        self.todos_sprites.draw(tela)
        for carta in self.cartas:
            carta.draw(tela)
            
        # NOVO: Desenha o soldado "fantasma" seguindo o mouse
        if self.carta_selecionada and self.soldado_fantasma_surf:
            pos_mouse = pygame.mouse.get_pos()
            # Centraliza a imagem fantasma no cursor
            rect_fantasma = self.soldado_fantasma_surf.get_rect(center=pos_mouse)
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