import pygame
from .Constantes import VIDA_INICIAL_JOGADOR, VIDA_MAXIMA_JOGADOR, ENERGIA_MAXIMA_JOGADOR

class JogadorStats:
    def __init__(self):
        self.saude_maxima = VIDA_MAXIMA_JOGADOR
        self.saude_atual = VIDA_INICIAL_JOGADOR
        self.energia_maxima = ENERGIA_MAXIMA_JOGADOR
        self.energia_atual = 0
        self.energia_espiritual = 0
        self.orbs_energia = 0
        self.orbs_vida = 0
        self.estado_atual = "normal"
        self.esta_vivo = True
        self.invencivel = False
        self.powerup_ativo = False
        self.tempo_assustado = 0
        self.tempo_invencivel = 0
        self.tempo_powerup = 0
        self.duracao_assustado = 1500
        self.duracao_invencivel = 3000
        self.duracao_powerup = 8000
        self.on_dano_recebido = None

    def mudar_estado(self, novo_estado):
        if self.esta_vivo:
            self.estado_atual = novo_estado


    def atualizar_estado(self):
        agora = pygame.time.get_ticks()

        if self.estado_atual == "assustado":
            if agora - self.tempo_assustado >= self.duracao_assustado:
                self.estado_atual = "invencivel"
                self.invencivel = True
                self.tempo_invencivel = agora

        elif self.estado_atual == "invencivel":
            if agora - self.tempo_invencivel >= self.duracao_invencivel:
                self.invencivel = False
                self.estado_atual = "normal"

        if self.powerup_ativo:
            if agora - self.tempo_powerup >= self.duracao_powerup:
                self.powerup_ativo = False
                if self.esta_vivo:
                    self.estado_atual = "normal"

    def curar(self, valor=100):
        self.saude_atual = min(self.saude_maxima, self.saude_atual + valor)
        self.orbs_vida += 1

    def adicionar_energia(self, valor):
        self.energia_atual = min(self.energia_maxima, self.energia_atual + valor)
        self.energia_espiritual += valor
        self.orbs_energia += 1

    def consumir_energia(self, valor):
        if self.energia_atual >= valor:
            self.energia_atual -= valor
            return True
        return False

    def ativar_powerup(self):
        if not self.esta_vivo:
            return

        self.powerup_ativo = True
        self.invencivel = False
        self.estado_atual = "powerUp"
        self.tempo_powerup = pygame.time.get_ticks()

    def receber_dano(self, dano=100):
        if (
                self.invencivel
                or self.powerup_ativo
                or self.estado_atual == "assustado"
                or not self.esta_vivo
        ):
            return False

        self.saude_atual -= dano
        self.estado_atual = "assustado"
        self.tempo_assustado = pygame.time.get_ticks()
        if self.on_dano_recebido:
            self.on_dano_recebido()
        if self.saude_atual <= 0:
            self.saude_atual = 0
            self.esta_vivo = False
            self.estado_atual = "morto"
            return True

        return False