import math
import random
from .Entidade import Entidade
from .Constantes import VELOCIDA_DE_ENTIDADE

class Orb(Entidade):
    def __init__(self, nome_orb: str, posicao_orb: tuple):
        super().__init__(nome_orb, posicao_orb, layer=7)
        self.speed = VELOCIDA_DE_ENTIDADE.get(nome_orb, 3)
        self.base_y = self.Rect.y
        self.tempo = 0

    def move(self):
        self.Rect.x -= self.speed
        #movimento vertical suave adicionado abaixo para dar mais vida
        self.tempo += 0.1
        movimento_suavizado = int(15* math.sin(self.tempo)) #usando função SIN (seno) para movimento mais harmônico
        self.Rect.y = self.base_y+movimento_suavizado
