from abc import ABC, abstractmethod
import pygame
import sys
import os
from pathlib import Path
from .Constantes import SAUDE_ENTIDADE

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

class Entidade(ABC):
    def __init__(self, nome: str, posicao: tuple, layer: int = 0, imagem=None):
        self.layer = int(layer)
        self.name: str = nome

        if imagem is not None:
            self.Surf = imagem
        else:
            #AMINHO com resource_path
            image_path = resource_path(f"assets/images/{nome}.png")
            self.Surf = pygame.image.load(image_path).convert_alpha()

        self.Rect = self.Surf.get_rect(left=posicao[0], top=posicao[1])
        self.mask = pygame.mask.from_surface(self.Surf)
        self.speed = 0
        self.saude = SAUDE_ENTIDADE.get(self.name, 0)

    @abstractmethod
    def move(self):
        pass