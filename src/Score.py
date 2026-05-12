import asyncio
import pygame
import sys
import os
from .BancoScore import BancoScore
from .Constantes import width_max, height_max, BRANCO_SUAVE, LARANJA, AZUL

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

class Score:
    def __init__(self, window):
        self.window = window
        self.banco = BancoScore()
        self.fundo = pygame.image.load(resource_path("assets/images/menu_v3.png")).convert()
        self.fundo = pygame.transform.scale(self.fundo, (width_max, height_max))
        self.fonte_titulo = pygame.font.Font(resource_path('assets/fonts/Nosifer-Regular.ttf'), 40)
        self.fonte_texto = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 16)

        self.col_x = {
            "pos": 120,
            "nome": 260,
            "pontos": 410,
            "energia": 540,
            "vida": 660,
            "dificuldade": 805,
            "data": 990
        }

    def desenhar_texto_centro(self, texto, fonte, cor, x, y):
        surf = fonte.render(str(texto), True, cor)
        rect = surf.get_rect(center=(x, y))
        self.window.blit(surf, rect)

    def desenhar_fundo_blur(self):
        fundo_blur = pygame.transform.smoothscale(
            self.fundo,
            (width_max // 8, height_max // 8)
        )
        fundo_blur = pygame.transform.smoothscale(
            fundo_blur,
            (width_max, height_max)
        )
        self.window.blit(fundo_blur, (0, 0))

    def desenhar_caixa(self):
        caixa_rect = pygame.Rect(90, 80, width_max - 180, 500)
        caixa = pygame.Surface((caixa_rect.width, caixa_rect.height), pygame.SRCALPHA)
        caixa.fill((0, 7, 14, 132))
        pygame.draw.rect(
            caixa,
            (110, 190, 255, 92),
            caixa.get_rect(),
            2,
            border_radius=12
        )
        self.window.blit(caixa, caixa_rect)

    def desenhar_botao_voltar(self):
        botao_rect = pygame.Rect(width_max // 2 - 155, 610, 310, 45)
        botao = pygame.Surface((botao_rect.width, botao_rect.height), pygame.SRCALPHA)
        botao.fill((45, 85, 120, 170))
        pygame.draw.rect(
            botao,
            (110, 190, 255, 190),
            botao.get_rect(),
            2,
            border_radius=8
        )
        self.window.blit(botao, botao_rect)
        texto_back = self.fonte_texto.render("VOLTAR = ESC", True, BRANCO_SUAVE)
        texto_rect = texto_back.get_rect(center=botao_rect.center)
        self.window.blit(texto_back, texto_rect)

    async def run(self):
        running = True
        while running:
            scores = self.banco.listar_top10()
            self.desenhar_fundo_blur()
            self.desenhar_caixa()
            titulo = self.fonte_titulo.render("PONTUAÇÃO", True, BRANCO_SUAVE)
            self.window.blit(titulo, titulo.get_rect(center=(width_max // 2, 135)))

            cabecalho_y = 205
            self.desenhar_texto_centro("#", self.fonte_texto, AZUL, self.col_x["pos"], cabecalho_y)
            self.desenhar_texto_centro("NOME", self.fonte_texto, AZUL, self.col_x["nome"], cabecalho_y)
            self.desenhar_texto_centro("PONTOS", self.fonte_texto, AZUL, self.col_x["pontos"], cabecalho_y)
            self.desenhar_texto_centro("ORB E", self.fonte_texto, AZUL, self.col_x["energia"], cabecalho_y)
            self.desenhar_texto_centro("ORB V", self.fonte_texto, AZUL, self.col_x["vida"], cabecalho_y)
            self.desenhar_texto_centro("MODO", self.fonte_texto, AZUL, self.col_x["dificuldade"], cabecalho_y)
            self.desenhar_texto_centro("DATA", self.fonte_texto, AZUL, self.col_x["data"], cabecalho_y)
            y = 230

            if scores:
                for i, score in enumerate(scores, start=1):
                    nome, pontuacao, orbes_energia, orbes_vida, dificuldade, data_partida = score
                    self.desenhar_texto_centro(f"{i}", self.fonte_texto, BRANCO_SUAVE, self.col_x["pos"], y)
                    self.desenhar_texto_centro(nome, self.fonte_texto, BRANCO_SUAVE, self.col_x["nome"], y)
                    self.desenhar_texto_centro(pontuacao, self.fonte_texto, BRANCO_SUAVE, self.col_x["pontos"], y)
                    self.desenhar_texto_centro(orbes_energia, self.fonte_texto, BRANCO_SUAVE, self.col_x["energia"], y)
                    self.desenhar_texto_centro(orbes_vida, self.fonte_texto, BRANCO_SUAVE, self.col_x["vida"], y)
                    self.desenhar_texto_centro(dificuldade, self.fonte_texto, BRANCO_SUAVE, self.col_x["dificuldade"], y)
                    self.desenhar_texto_centro(data_partida, self.fonte_texto, BRANCO_SUAVE, self.col_x["data"], y)
                    y += 32
            else:
                self.desenhar_texto_centro(
                    "Ainda não há pontuação salva.",
                    self.fonte_texto,
                    BRANCO_SUAVE,
                    width_max // 2,
                    height_max // 2
                )
            self.desenhar_botao_voltar()

            pygame.display.flip()
            await asyncio.sleep(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return