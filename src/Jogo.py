import asyncio
import pygame
from .Constantes import width_max, height_max
from .Nivel import Nivel
from .Instrucoes import Instrucoes
from .Score import Score
from .Menu import Menu
from .IntroSplash import IntroSplash

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((width_max, height_max))
        pygame.display.set_caption("Jogo Fantasma")
        self.running = True

    async def run(self):
        #corre a intro
        splash = IntroSplash(self.window)
        await splash.run()
        #corre o jogo
        while self.running:
            menu = Menu(self.window)
            escolha = await menu.run()

            if escolha == "NOVO JOGO":
                pygame.mixer.music.stop()
                nivel = Nivel(self.window, "Nível 1", escolha)
                await nivel.run()

            elif escolha == "INSTRUÇÕES":
                instrucoes = Instrucoes(self.window)
                await instrucoes.run()

            elif escolha == "PONTUAÇÃO":
                score = Score(self.window)
                await score.run()

            elif escolha == "SAIR":
                self.running = False

            await asyncio.sleep(0)
        pygame.quit()