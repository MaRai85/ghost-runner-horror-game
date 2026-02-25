import pygame
# !!!!!!!!!!!!!!!!!!!!!!CONDIÇÕES DE VITÓRIA!!!!!!!!!!!!!!!!!!!!!!!!!!
META_PONTOS_VITORIA = 2000

# CORES
AZUL =(115,190,245)
AZUL_GELO = (175, 214, 238)
AZUL_BRILHO = (80, 170, 255)
BRANCO_SUAVE = (228, 216, 198)
BRANCO = BRANCO_SUAVE
BEGE_TEXTO = (220, 205, 188)
BEGE_FRACO = (200, 188, 170)
CINZA = (60, 60, 60)
VERMELHO = (140, 30, 35)
LARANJA = AZUL_GELO
FUNDO_ESCURO = (2, 7, 12)
PAINEL_ESCURO = (4, 14, 22)
COR_BOTAO_ATIVO = (45, 85, 120, 170)
COR_BORDA_ATIVA = (110, 190, 255)
COR_GLOW = (80, 170, 255)
BORDA_AZUL = COR_BORDA_ATIVA
COR_DIFICULDADE = AZUL_GELO

# EVENTOS
try:
    EVENTO_INIMIGO = pygame.USEREVENT + 1
    EVENTO_ORB = pygame.USEREVENT + 2
except AttributeError:
    # Fallback para WebAssembly
    EVENTO_INIMIGO = 24
    EVENTO_ORB = 25

# FPS
FPS = 60 # Pode mudar para 30, 45, 120 ...

# MENU
OPCAO_MENU = ('NOVO JOGO',
              "INSTRUÇÕES",
              'PONTUAÇÃO',
              'SAIR')

# ORBS / ENERGIA
CURA_ORB_XL = 100 # valor quanto cura cada bola orbe XL
ENERGIA_ORB_S= 50

CHANCE_ORB_XL = 0.10   # 10% chances de aparecer
CHANCE_ORB_S = 0.70    # 70% chances de aparecer
TEMPO_SHOW_ORBS = 3000

# PONTUAÇÃO
PONTOS_POR_INIMIGO = 50
PONTOS_ORB_S = 25
PONTOS_ORB_XL = 50

#POWERUP
ENERGIA_MAXIMA_JOGADOR = 1000
CUSTO_POWERUP = 200
DURACAO_POWERUP = 5000


# TAMANHOS
width_max: int = 1200
height_max: int = 700

#TEMPOS
TEMPO_SHOW_INIMIGOS = 2000 #ESTE VALOR ALTERA VELOCIDADE DE APARECIMENTO DE INIMIGOS
TEMPO_LIMITE_NIVEL = 300000  # 5 minutos em ms

# VELOCIDADE DAS ENTIDADES:
VELOCIDA_DE_ENTIDADE = {
    'demoModeBg0': 0,
    'demoModeBg1': 1,
    'demoModeBg2': 2,
    'demoModeBg3': 3,
    'demoModeBg4': 4,
    'demoModeBg5': 5,
    'ghost_frente': 8,
    'ghost_morto': 0,
    'ghost_speed': 18,
    'ghost_tras': 5,
    'ghost_assustado': 3,
    'inimigo01': 4,
    'inimigo02': 5,
    'inimigo03': 6,
    'energy_orb_S': 3,
    'energy_orb_XL': 2,
}

#VIDA DAS ENTIDADES
SAUDE_ENTIDADE = {
    'Jogador': 300,
    'ghost_frente': 300,
    'inimigo01': 500,
    'inimigo02': 500,
    'inimigo03': 500,
    'demoModeBg0': float('inf'),
    'demoModeBg1': float('inf'),
    'demoModeBg2': float('inf'),
    'demoModeBg3': float('inf'),
    'demoModeBg4': float('inf'),
    'demoModeBg5': float('inf'),
    'energy_orb_S': 1,
    'energy_orb_XL': 1,
}
# VIDA DO JOGADOR AO NÍVEL DE JOGABILIDADE (saúde do fantasma)
VIDA_INICIAL_JOGADOR = 100
VIDA_MAXIMA_JOGADOR = 300
DANO_COLISAO_INIMIGO = 100

# LEVELS
DIFICULDADES = {
    "NORMAL": {
        "tempo_inimigo": 2300,
        "tempo_orb": 3000,
        "velocidade_extra_inimigo": -1,
        "chance_orb_xl": 0.20,
        "chance_orb_s": 0.70,
        "inimigos_por_spawn": 1,
        "vitoria_por_pontos": True
    },
    "DIFICIL": {
        "tempo_inimigo": 1900,
        "tempo_orb": 4000,
        "velocidade_extra_inimigo": 0,
        "chance_orb_xl": 0.05,
        "chance_orb_s": 0.50,
        "inimigos_por_spawn": 1,
        "vitoria_por_pontos": True
    },
    "PESADELO": {
        "tempo_inimigo": 1500,
        "tempo_orb": 4000,
        "velocidade_extra_inimigo": 1,
        "chance_orb_xl": 0.05,
        "chance_orb_s": 0,
        "inimigos_por_spawn": 1,
        "vitoria_por_pontos": False
    }
}