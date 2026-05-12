import asyncio
import pygame
import sys
import os


#FUNÇÃO resource_path para PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)


from .Constantes import width_max, height_max, LARANJA, BRANCO_SUAVE, AZUL
from .EntidadeFactory import EntidadeFactory


class Instrucoes:
    def __init__(self, window):
        self.window = window

        #FONTES com resource_path
        self.fonte_titulo = pygame.font.Font(
            resource_path('assets/fonts/Nosifer-Regular.ttf'), 46
        )
        self.fonte_texto = pygame.font.Font(
            resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 21
        )

        # MAGEM com resource_path
        self.fundo = pygame.image.load(
            resource_path("assets/images/menu_v3.png")
        ).convert()

    def texto_centralizado(self, texto, y, cor=BRANCO_SUAVE, fonte=None):
        if fonte is None:
            fonte = self.fonte_texto
        surf = fonte.render(texto, True, cor)
        rect = surf.get_rect(center=(width_max // 2, y))
        self.window.blit(surf, rect)

    def desenhar_caixa(self):
        caixa_rect = pygame.Rect(180, 80, width_max - 360, 525)
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
        botao_rect = pygame.Rect(width_max // 2 - 125, 625, 250, 42)
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
            #MOVIDO: asyncio.sleep(0) no INÍCIO do loop
            await asyncio.sleep(0)

            fundo_blur = pygame.transform.smoothscale(
                self.fundo,
                (width_max // 8, height_max // 8))
            fundo_blur = pygame.transform.smoothscale(
                fundo_blur,
                (width_max, height_max))

            self.window.blit(fundo_blur, (0, 0))
            self.desenhar_caixa()
            self.desenhar_botao_voltar()
            self.texto_centralizado("INSTRUÇÕES", 160, BRANCO_SUAVE, self.fonte_titulo)
            self.texto_centralizado("Use as setas do teclado para vagar pelo além", 230)
            self.texto_centralizado("Desvie dos inimigos antes que eles drenem sua essência", 280)
            self.texto_centralizado("Orbes S aumentam sua energia espiritual", 335, AZUL)
            self.texto_centralizado("Orbes XL recuperam sua vida durante a corrida", 385, AZUL)
            self.texto_centralizado("Use o PowerUp quando sua energia estiver pronta", 445)
            self.texto_centralizado("Alcance 2000 pontos ou sobreviva por 5 minutos", 495)
            self.texto_centralizado("No PESADELO, vencer é resistir ao terror até o fim", 545, AZUL)

            pygame.display.flip()

            #MOVIDO: Eventos DEPOIS do flip
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #SUBSTITUÍDO: pygame.quit() + exit() por return
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return