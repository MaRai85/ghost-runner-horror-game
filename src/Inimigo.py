import math
import random
from .Entidade import Entidade
from .Constantes import width_max, VELOCIDA_DE_ENTIDADE,height_max

class Inimigo(Entidade):
    def __init__(self, nome_inimigo: str, posicao_inimigo: tuple):
        super().__init__(nome_inimigo, posicao_inimigo, layer= 8) ##definido Layer dos inimigos
        self.speed = VELOCIDA_DE_ENTIDADE.get(nome_inimigo,3)
        self.tempo=0
        self.base_y = self.Rect.y
        self.direcao_y = random.choice([-1,1])
        #regras para amplitude de movimentos padrões, colocados mais abaixo
        self.amplitude = random.randint(15, 35)
        self.frequencia = random.uniform(1.5, 3.0)
        self.velocidade_vertical = random.randint(2, 5)
        self.tipo_movimento = random.choice(['reto', 'onda','zigzag','sobe_desce'])

    def move(self, ):
        self.Rect.centerx -= self.speed
        self.tempo += 0.12
        self.Rect.y += self.direcao_y * self.velocidade_vertical

        if self.tipo_movimento == 'reto':
            pass
        elif self.tipo_movimento == 'onda':
            self.Rect.y = self.base_y + int(25 * math.sin(self.tempo * 2))
        elif self.tipo_movimento == 'zigzag':
            self.Rect.y += self.direcao_y * 4
            if self.Rect.top <= 40 or self.Rect.bottom >= height_max - 40:
                self.direcao_y *= -1
        elif self.tipo_movimento == 'sobe_desce':
            self.Rect.y += self.direcao_y * 2
            if random.randint(1, 25) == 1:
                self.direcao_y *= -1
            if self.Rect.top <= 40:
                self.direcao_y = 1
            elif self.Rect.bottom >= height_max - 40:
                self.direcao_y = -1