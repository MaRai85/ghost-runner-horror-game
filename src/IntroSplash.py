import pygame
import asyncio
import sys
import os
from .Constantes import width_max, height_max, BRANCO_SUAVE, LARANJA, AZUL

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # No desenvolvimento, base é a pasta do arquivo atual
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Sobe um nível (de src/ para a raiz do projeto)
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

class IntroSplash:
    def __init__(self, window):
        self.window = window
        self.fonte = pygame.font.Font(
            resource_path("assets/fonts/FontdinerSwanky-Regular.ttf"),
            40
        )
        self.mensagens = [
            "Criado por Marcos Raimundo",
            "Engine: PYGAME 2.6",
            "Versão 5.0 - Demo"
        ]

    async def run(self):
        for mensagem in self.mensagens:
            # FADE IN
            for alpha in range(0, 256, 8):
                self.window.fill((0, 0, 0))
                texto = self.fonte.render(
                    mensagem,
                    True,
                    (255, 255, 255)
                )
                texto.set_alpha(alpha)
                rect = texto.get_rect(
                    center=(width_max // 2, height_max // 2)
                )
                self.window.blit(texto, rect)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                await asyncio.sleep(0.02)

            # TEXTO FIXO (2 segundos)
            inicio = pygame.time.get_ticks()
            while pygame.time.get_ticks() - inicio < 2000:
                self.window.fill((0, 0, 0))
                texto = self.fonte.render(
                    mensagem,
                    True,
                    (255, 255, 255)
                )
                rect = texto.get_rect(
                    center=(width_max // 2, height_max // 2)
                )
                self.window.blit(texto, rect)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                await asyncio.sleep(0)

            # FADE OUT
            for alpha in range(255, -1, -8):
                self.window.fill((0, 0, 0))
                texto = self.fonte.render(
                    mensagem,
                    True,
                    (255, 255, 255)
                )
                texto.set_alpha(alpha)
                rect = texto.get_rect(
                    center=(width_max // 2, height_max // 2)
                )
                self.window.blit(texto, rect)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                await asyncio.sleep(0.02)