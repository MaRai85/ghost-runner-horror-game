from .JogadorStats import JogadorStats
from .Inimigo import Inimigo
from .Constantes import (
    DANO_COLISAO_INIMIGO,
    CURA_ORB_XL,
    ENERGIA_ORB_S,
    PONTOS_ORB_S,
    PONTOS_ORB_XL,
    PONTOS_POR_INIMIGO,
    CUSTO_POWERUP,
    META_PONTOS_VITORIA,
)

class RegrasJogador:
    def __init__(self, stats: JogadorStats):
        self.stats = stats
        self.pontuacao = 0
        self.combo = 0
        self.ultimo_inimigo_derrotado = 0

    def processar_colisao_inimigo(self, inimigo: Inimigo) -> dict:
        resultado = {
            'dano_recebido': 0,
            'inimigo_destruido': False,
            'mensagem': ''
        }
        # POWERUP: atropela/destrói inimigo
        if self.stats.powerup_ativo:
            resultado['inimigo_destruido'] = True
            resultado['mensagem'] = '+50 pontos! Inimigo atropelado usando PowerUp de coragem devastadora!'
            self.pontuacao += PONTOS_POR_INIMIGO
            return resultado
        # INVENCIBILIDADE CURTA APÓS DANO: não perde vida de novo
        if self.stats.invencivel:
            resultado['mensagem'] = 'Fantasma está temporariamente invencível devido a um boost de coragem.'
            return resultado
        # DANO NORMAL
        morreu = self.stats.receber_dano(DANO_COLISAO_INIMIGO)
        resultado['dano_recebido'] = DANO_COLISAO_INIMIGO
        if morreu:
            resultado['mensagem'] = 'GAME OVER'
        else:
            resultado['mensagem'] = 'Ai! Estou muuuuuuito assustado!'
        return resultado

    def processar_coleta_orb(self, tipo_orb: str) -> dict:
        resultado = {'cura': 0, 'energia': 0, 'pontos': 0, 'mensagem': ''}

        if tipo_orb == 'energy_orb_S':
            resultado['energia'] = ENERGIA_ORB_S
            resultado['pontos'] = PONTOS_ORB_S
            resultado['mensagem'] = 'Orbe de energia coletado!'

            self.stats.adicionar_energia(ENERGIA_ORB_S)

        elif tipo_orb == 'energy_orb_XL':
            resultado['cura'] = CURA_ORB_XL
            resultado['pontos'] = PONTOS_ORB_XL
            resultado['mensagem'] = 'Orbe de vida coletado!'

            self.stats.curar(CURA_ORB_XL)

        self.pontuacao += resultado['pontos']
        return resultado

    def tentar_ativar_powerup(self) -> bool:
        if self.stats.consumir_energia(CUSTO_POWERUP):
            self.stats.ativar_powerup()
            return True
        return False

    def verificar_condicao_vitoria(self) -> bool:
        return self.pontuacao >= META_PONTOS_VITORIA

    def get_status_hud(self) -> dict:
        return {
            'saude': f"{self.stats.saude_atual}/{self.stats.saude_maxima}",
            'energia': f"{self.stats.energia_atual}/{self.stats.energia_maxima}",
            'energia_espiritual': self.stats.energia_espiritual,
            'orbs_energia': self.stats.orbs_energia,
            'orbs_vida': self.stats.orbs_vida,
            'estado': self.stats.estado_atual.upper(),
            'pontuacao': self.pontuacao
        }
