import asyncio
import pygame
import sys
import os

def resource_path(relative_path):
    """Retorna caminho absoluto que funciona tanto no desenvolvimento quanto no executável PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # Dentro do executável PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Desenvolvimento normal
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

# PRE_INIT do mixer
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
pygame.init()
pygame.mixer.init()

from src.Jogo import Jogo

async def main():
    jogo = Jogo()
    await jogo.run()

if __name__ == "__main__":
    asyncio.run(main())