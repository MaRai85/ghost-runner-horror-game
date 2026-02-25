import random
import asyncio
import pygame
import time
import sys
import os
from .Constantes import (height_max, EVENTO_INIMIGO, FPS, TEMPO_SHOW_INIMIGOS, TEMPO_LIMITE_NIVEL,
                         width_max, EVENTO_ORB, TEMPO_SHOW_ORBS, CUSTO_POWERUP, AZUL)
from .EntidadeFactory import EntidadeFactory
from .EntidadeMediadora import EntidadeMediadora
from .Jogador import Jogador
from .Inimigo import Inimigo
from .Orb import Orb
from .BancoScore import BancoScore
from .AdicaoNome import AdicaoNome
from .Constantes import DIFICULDADES

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

class Nivel:
    def __init__(self, window, nome, opcao_menu):
        self.window = window
        self.name = nome
        self.opcao_menu = opcao_menu
        self.timeout = TEMPO_LIMITE_NIVEL
        self.lista_entidade = []
        self.ultimo_clique_espaco = 0
        self.cliques_espaco = 0
        self.powerUp_ativo = False
        self.game_over = False
        self.vitoria = False
        self.velocidade_queda = 5
        # fontes a reutilizar
        self.fontes = {
            14: pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 14),
            18: pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 18),
            25: pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 25),
            30: pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 30),
            70: pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 60),
        }
        self.fonte_grande = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 60)
        self.fonte_media = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 30)
        self.fonte_pequena = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 25)
        self.texto_sair = 'Pressione ESC para sair'
        # fim fontes a reutilizar
        self.lista_entidade.extend(EntidadeFactory.get_entity("demoModeBg"))
        self.lista_entidade.extend(EntidadeFactory.get_entity("Jogador"))

        self.SOUND_DIR = resource_path("assets/sounds")

        self.fonte = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 14)
        self.som_orb_s = pygame.mixer.Sound(os.path.join(self.SOUND_DIR, "orb_s.ogg"))
        self.som_orb_s.set_volume(0.4)
        self.som_orb_xl = pygame.mixer.Sound(os.path.join(self.SOUND_DIR, "orb_xl.ogg"))
        self.som_orb_xl.set_volume(0.4)

        self.banco_score = BancoScore()
        self.score_salvo = False

        self.som_vitoria = pygame.mixer.Sound(os.path.join(self.SOUND_DIR, "vitoria_nivel.ogg"))
        self.som_vitoria.set_volume(0.7)
        self.vitoria_tocada = False

        self.som_game_over = pygame.mixer.Sound(os.path.join(self.SOUND_DIR, "game_over_som.ogg"))
        self.som_game_over.set_volume(0.7)

        self.som_powerup = pygame.mixer.Sound(os.path.join(self.SOUND_DIR, "power_up.ogg"))
        self.som_powerup.set_volume(0.6)
        self.powerup_tocado = False

        self.som_grilos = pygame.mixer.Sound(os.path.join(self.SOUND_DIR, "grilos.ogg"))
        self.ultimo_input = pygame.time.get_ticks()
        self.idle_tocado = False

        self.cancelado = False
        self.dificuldade = "NORMAL"

        # TIMER MANUAL PARA SUBSTITUIR pygame.time.set_timer()
        self.ultimo_spawn_inimigo = 0
        self.ultimo_spawn_orb = 0

    async def pedir_nome_jogador(self):
        tela_nome = AdicaoNome(self.window)
        nome_digitado, dificuldade = await tela_nome.run()
        if nome_digitado == "CANCELAR":
            self.nome_jogador = "NOME"
            self.dificuldade = "NORMAL"
            self.cancelado = True
            return
        self.cancelado = False
        self.dificuldade = dificuldade
        if nome_digitado and nome_digitado.strip():
            self.nome_jogador = nome_digitado.strip()

    def desenhar_texto(self, texto, pos, tamanho=18):
        fonte = self.fontes[tamanho]
        surf = fonte.render(texto, True, AZUL)
        self.window.blit(surf, pos)

    def desenhar_caixa_hud(self, x, y, largura, altura):
        caixa = pygame.Surface((largura, altura), pygame.SRCALPHA)
        caixa.fill((0, 7, 14, 160))
        pygame.draw.rect(
            caixa,
            (110, 190, 255, 110),
            caixa.get_rect(),
            2,
            border_radius=14
        )
        self.window.blit(caixa, (x, y))

    def ordena_por_layer(self):
        return sorted(self.lista_entidade, key=self.get_layer)

    def get_layer(self, entidade):
        return entidade.layer

    def obter_jogador(self):
        for ent in self.lista_entidade:
            if isinstance(ent, Jogador):
                return ent
        return None

    def confirma_colisao(self):
        jogador = self.obter_jogador()
        if jogador is None:
            return
        for ent in self.lista_entidade[:]:
            if isinstance(ent, Inimigo):
                hitbox_jogador = jogador.Rect.inflate(-30, -30)
                hitbox_inimigo = ent.Rect.inflate(-35, -35)
                if hitbox_jogador.colliderect(hitbox_inimigo):
                    offset = (
                        ent.Rect.left - jogador.Rect.left,
                        ent.Rect.top - jogador.Rect.top
                    )
                    if jogador.mask.overlap(ent.mask, offset):
                        resultado = jogador.regras.processar_colisao_inimigo(ent)
                        if resultado['inimigo_destruido']:
                            ent.saude = 0
                        if not jogador.stats.esta_vivo:
                            jogador.estado = 'morto'
                            jogador.atualizar_sprites()
                            pygame.mixer.music.stop()
                            self.som_grilos.stop()
                            self.idle_tocado = False
                            self.game_over = True
                            self.som_game_over.play()
                            self.salvar_score_partida()
                            return

    def coleta_orbs(self):
        jogador = self.obter_jogador()
        if jogador is None:
            return

        for ent in self.lista_entidade[:]:
            if isinstance(ent, Orb):
                if jogador.Rect.colliderect(ent.Rect):
                    resultado = jogador.regras.processar_coleta_orb(ent.name)

                    if ent.name == 'energy_orb_S':
                        self.som_orb_s.play()
                    elif ent.name == 'energy_orb_XL':
                        self.som_orb_xl.play()
                    ent.saude = 0

    def verificar_vitoria(self):
        jogador = self.obter_jogador()
        if jogador is None:
            return

        if jogador.regras.verificar_condicao_vitoria():
            self.salvar_score_partida()
            self.vitoria = True
            pygame.mixer.music.stop()
            self.som_vitoria.play()

    def animar_derrota(self):
        for ent in self.lista_entidade:
            if isinstance(ent, Jogador):
                if ent.Rect.y < height_max - 150:
                    ent.Rect.y += self.velocidade_queda
                ent.atualizar_sprites()

    def animar_vitoria(self):
        for ent in self.lista_entidade:
            if isinstance(ent, Jogador):
                ent.atualizar_sprites()

    def spawn_inimigos(self, config):
        for _ in range(config["inimigos_por_spawn"]):
            escolha = random.choice(['inimigo01', 'inimigo02', 'inimigo03'])
            self.lista_entidade.extend(EntidadeFactory.get_entity(escolha))

    def spawn_orbs(self, config):
        sorteio = random.random()
        if sorteio <= config["chance_orb_xl"]:
            escolha = "energy_orb_XL"
        elif sorteio <= config["chance_orb_s"]:
            escolha = "energy_orb_S"
        else:
            escolha = None
        if escolha:
            self.lista_entidade.extend(EntidadeFactory.get_entity(escolha))

    async def run(self):
        await self.pedir_nome_jogador()
        if self.cancelado:
            return self.opcao_menu
        config = DIFICULDADES[self.dificuldade]

        self.ultimo_spawn_inimigo = pygame.time.get_ticks()
        self.ultimo_spawn_orb = pygame.time.get_ticks()

        pygame.mixer.music.load(os.path.join(self.SOUND_DIR, "som_nivel.ogg"))
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()
        tempo_inicio_nivel = pygame.time.get_ticks()
        running = True

        while running:
            jogo_ativo = not self.game_over and not self.vitoria
            tempo_atual = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.ultimo_input = pygame.time.get_ticks()
                    if self.idle_tocado:
                        self.som_grilos.stop()
                        self.idle_tocado = False
                    if event.key == pygame.K_SPACE:
                        now = pygame.time.get_ticks()
                        if now - self.ultimo_clique_espaco < 1000:
                            self.cliques_espaco += 1
                        else:
                            self.cliques_espaco = 1
                        self.ultimo_clique_espaco = now

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    self.som_vitoria.stop()
                    self.som_game_over.stop()
                    self.som_grilos.stop()
                    running = False

            if jogo_ativo:
                if tempo_atual - self.ultimo_spawn_inimigo >= config["tempo_inimigo"]:
                    self.spawn_inimigos(config)
                    self.ultimo_spawn_inimigo = tempo_atual

            if jogo_ativo:
                if tempo_atual - self.ultimo_spawn_orb >= config["tempo_orb"]:
                    self.spawn_orbs(config)
                    self.ultimo_spawn_orb = tempo_atual

            if not self.game_over and not self.vitoria:
                if tempo_atual - self.ultimo_input > 5000:
                    if not self.idle_tocado:
                        self.som_grilos.play(-1)
                        self.idle_tocado = True

            if not self.game_over and not self.vitoria:
                for ent in self.lista_entidade:
                    ent.move()
                self.confirma_colisao()
                self.coleta_orbs()
                tempo_decorrido = tempo_atual - tempo_inicio_nivel
                if tempo_decorrido >= TEMPO_LIMITE_NIVEL:
                    self.salvar_score_partida()
                    self.vitoria = True
                    pygame.mixer.music.stop()
                    self.som_vitoria.play()
                config = DIFICULDADES[self.dificuldade]
                if config["vitoria_por_pontos"]:
                    self.verificar_vitoria()
            elif self.game_over:
                self.animar_derrota()
            elif self.vitoria:
                self.animar_vitoria()

            if not self.game_over and not self.vitoria:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE]:
                    if self.cliques_espaco >= 2:
                        for ent in self.lista_entidade:
                            if isinstance(ent, Jogador) and ent.stats.esta_vivo:
                                ativou = ent.regras.tentar_ativar_powerup()
                                if ativou:
                                    self.som_powerup.play()
                                    self.cliques_espaco = 0

            self.window.fill((0, 0, 0))

            for ent in self.ordena_por_layer():
                self.window.blit(ent.Surf, ent.Rect)

            jogador_hud = self.obter_jogador()

            if jogador_hud:
                status = jogador_hud.regras.get_status_hud()
                powerup_pronto = jogador_hud.stats.energia_atual >= CUSTO_POWERUP
                if powerup_pronto:
                    texto_power = 'PowerUp: PRONTO!'
                else:
                    texto_power = f'PowerUp: {jogador_hud.stats.energia_atual}/{CUSTO_POWERUP}'

                largura_caixa = 300
                altura_caixa = 105
                margem = 20
                x_esquerda = margem
                x_direita = width_max - largura_caixa - margem
                y_hud = height_max - altura_caixa - 20

                self.desenhar_caixa_hud(x_esquerda, y_hud, largura_caixa, altura_caixa)
                self.desenhar_caixa_hud(x_direita, y_hud, largura_caixa, altura_caixa)

                self.desenhar_texto(
                    f'Orbes Energia: {status["orbs_energia"]}',
                    (x_esquerda + 25, y_hud + 15)
                )
                self.desenhar_texto(
                    f'Orbes Vida: {status["orbs_vida"]}',
                    (x_esquerda + 25, y_hud + 45)
                )
                self.desenhar_texto(
                    f'Estado: {status["estado"]}',
                    (x_esquerda + 25, y_hud + 75)
                )

                self.desenhar_texto(
                    f'Pontos: {status["pontuacao"]}',
                    (x_direita + 25, y_hud + 15)
                )
                if powerup_pronto:
                    fonte_power = self.fontes[25]
                    texto_power_surf = fonte_power.render(texto_power, True, (80, 255, 120))
                    self.window.blit(texto_power_surf, (x_direita + 25, y_hud + 38))
                else:
                    self.desenhar_texto(
                        texto_power,
                        (x_direita + 25, y_hud + 45)
                    )
                self.desenhar_texto(
                    f'Vida: {status["saude"]}',
                    (x_direita + 25, y_hud + 75)
                )

            if self.game_over:
                texto_game_over = self.fonte_grande.render("FIM DA CORRIDA", True, (255, 0, 0))
                texto_sub = self.fonte_pequena.render(self.texto_sair, True, (255, 255, 255))

                rect_game_over = texto_game_over.get_rect(center=(width_max // 2, height_max // 2 - 30))
                rect_sub = texto_sub.get_rect(center=(width_max // 2, height_max // 2 + 30))

                self.window.blit(texto_game_over, rect_game_over)
                self.window.blit(texto_sub, rect_sub)

            if self.vitoria:
                texto_vitoria = self.fonte_grande.render("VOCÊ VENCEU!", True, (0, 255, 0))
                texto_sub = self.fonte_media.render(self.texto_sair, True, (255, 255, 255))

                rect_vitoria = texto_vitoria.get_rect(center=(width_max // 2, height_max // 2 - 30))
                rect_sub = texto_sub.get_rect(center=(width_max // 2, height_max // 2 + 30))

                self.window.blit(texto_vitoria, rect_vitoria)
                self.window.blit(texto_sub, rect_sub)

            pygame.display.flip()
            clock.tick(FPS)

            await asyncio.sleep(0)

            if not self.game_over and not self.vitoria:
                EntidadeMediadora.verificar_colisoes(lista_entidades=self.lista_entidade)
                EntidadeMediadora.verificar_saude(lista_entidades=self.lista_entidade)

        return self.opcao_menu

    def salvar_score_partida(self):
        if self.score_salvo:
            return
        jogador = self.obter_jogador()
        if jogador is None:
            return
        pontuacao_final = jogador.regras.pontuacao
        if not self.banco_score.entra_no_top10(pontuacao_final):
            self.score_salvo = True
            return
        data_partida = time.strftime('%d/%m/%Y %H:%M:%S')
        self.banco_score.salvar_score(
            nome_jogador=self.nome_jogador,
            pontuacao=pontuacao_final,
            orbes_energia=jogador.stats.orbs_energia,
            orbes_vida=jogador.stats.orbs_vida,
            dificuldade=self.dificuldade,
            data_partida=data_partida
        )
        self.score_salvo = True