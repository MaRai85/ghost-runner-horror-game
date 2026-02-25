import asyncio
import pygame
import sys
import os
from .Constantes import width_max, height_max, BRANCO_SUAVE, LARANJA, AZUL, COR_DIFICULDADE

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

class AdicaoNome:
    def __init__(self, window):
        self.window = window
        self.fundo = pygame.image.load(resource_path("assets/images/menu_v3.png")).convert()
        self.fundo = pygame.transform.scale(self.fundo, (width_max, height_max))
        self.menu_select = pygame.mixer.Sound(resource_path("assets/sounds/risada_fantasmagorica.ogg"))
        self.fonte_setas = pygame.font.SysFont("Arial", 20, bold=True)
        self.fonte_titulo = pygame.font.Font(resource_path('assets/fonts/Nosifer-Regular.ttf'), 40)
        self.fonte_texto = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 19)
        self.fonte_input = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 38)
        self.fonte_dificuldade = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 30)

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
        caixa_rect = pygame.Rect(170, 80, width_max - 340, 520)
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

    def texto_centralizado(self, texto, y, cor=BRANCO_SUAVE, fonte=None):
        if fonte is None:
            fonte = self.fonte_texto
        surf = fonte.render(texto, True, cor)
        rect = surf.get_rect(center=(width_max // 2, y))
        self.window.blit(surf, rect)

    async def run(self):
        nome = ""
        erro_nome = False
        dificuldades = ["NORMAL", "DIFICIL", "PESADELO"]
        dificuldade_atual = 0
        texto_completo = "Digite seu nome para selar seu destino..."
        inicio_animacao = pygame.time.get_ticks()
        velocidade_letra = 100

        while True:
            self.desenhar_fundo_blur()
            self.desenhar_caixa()
            tempo_passado = pygame.time.get_ticks() - inicio_animacao
            letras_visiveis = min(len(texto_completo), tempo_passado // velocidade_letra)
            texto_animado = texto_completo[:letras_visiveis]

            if letras_visiveis < len(texto_completo):
                texto_animado += "|"
            dificuldade = dificuldades[dificuldade_atual]
            self.texto_centralizado("NOME DO JOGADOR", 135, BRANCO_SUAVE, self.fonte_titulo)
            self.texto_centralizado(texto_animado, 220, BRANCO_SUAVE, self.fonte_texto)
            input_rect = pygame.Rect(width_max // 2 - 210, 265, 420, 55)
            input_box = pygame.Surface((input_rect.width, input_rect.height), pygame.SRCALPHA)
            input_box.fill((0, 0, 0, 72))

            pygame.draw.rect(
                input_box,
                (110, 190, 255, 150),
                input_box.get_rect(),
                2,
                border_radius=8
            )
            self.window.blit(input_box, input_rect)
            texto_nome = self.fonte_input.render(nome, True, BRANCO_SUAVE)
            self.window.blit(
                texto_nome,
                texto_nome.get_rect(center=input_rect.center)
            )
            self.texto_centralizado(
                f"DIFICULDADE: {dificuldade}",
                390,
                COR_DIFICULDADE,
                self.fonte_dificuldade
            )
            self.texto_centralizado(
                "←  →  para escolher dificuldade",
                435,
                AZUL,
                self.fonte_setas
            )
            self.texto_centralizado("ENTER para confirmar", 520, AZUL, self.fonte_texto)
            self.texto_centralizado("BACKSPACE para apagar", 560, AZUL, self.fonte_texto)
            if erro_nome:
                self.texto_centralizado(
                    "O nome deve conter pelo menos 3 caracteres",
                    635,
                    (255, 90, 90),
                    self.fonte_texto
                )
            pygame.display.flip()
            await asyncio.sleep(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(nome.strip()) >= 3:
                            return nome.strip(), dificuldade
                        erro_nome = True
                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return "CANCELAR", "NORMAL"
                    elif event.key == pygame.K_LEFT:
                        self.menu_select.play()
                        dificuldade_atual = (dificuldade_atual - 1) % len(dificuldades)
                    elif event.key == pygame.K_RIGHT:
                        self.menu_select.play()
                        dificuldade_atual = (dificuldade_atual + 1) % len(dificuldades)
                    else:
                        if len(nome) < 12 and event.unicode.isprintable():
                            nome += event.unicode
                            erro_nome = False
                        else:
                            erro_nome = True