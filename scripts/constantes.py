#constantes.py
#dimensões da tela
LARGURA_TELA = 1240
ALTURA_TELA = 768

#player
VELOCIDADE_PLAYER = 3
VIDA_PLAYER = 200
MUNICAO_INICIAL_PLAYER = 50
MOEDAS_INICIAIS_PLAYER = 0
KITMEDS_INICIAIS_PLAYER = 0
# Cooldown
COOLDOWN_DANO_JOGADOR = 1000 # 1 segundo de invencibilidade após ser atingido

# Projéteis
VELOCIDADE_PROJETIL = 20
DANO_PROJETIL = 25
VIDA_UTIL_PROJETIL = 2500  # pixels

# Zumbis
VIDA_ZOMBIE = 50
VELOCIDADE_ZOMBIE = 1
DANO_ZOMBIE = 10  # Dano que o zumbi causa
QTD_ZOMBIES = 40

#Zumbi Tanque
VIDA_ZUMBI_TANQUE = 200
VELOCIDADE_ZUMBI_TANQUE = 0.5
DANO_ZUMBI_TANQUE = 25
CHANCE_SPAWN_TANQUE = 0.5 # chance de um zumbi da horda ser tanque


# Obstáculos
VIDA_FLOR = 30
VIDA_CONTAINER = 75

# Cadência de tiro (ms)
CADENCIA_TIRO = 250

# Respawn
INTERVALO_RESPAWN_ZOMBIE = 2500  # em ms
ZOMBIES_POR_HORDA = 10 # Zumbis por horda
INTERVALO_ENTRE_HORDAS = 10000 # Intervalo entre hordas em ms
INTERVALO_SPAWN_ZUMBI_HORDA = 600 # intervalo entre cada zumbi da horda