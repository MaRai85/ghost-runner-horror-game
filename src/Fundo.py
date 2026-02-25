from .Entidade import Entidade
from .Constantes import VELOCIDA_DE_ENTIDADE, width_max

class Fundo(Entidade):
    def __init__(self, nome: str, posicao: tuple, layer: int = 0):
        super().__init__(nome, posicao, layer)

    def move(self, ):
        velocidade = VELOCIDA_DE_ENTIDADE.get(self.name, self.layer + 1)
        self.Rect.centerx -= velocidade

        if self.Rect.right <= 0:
            self.Rect.left = width_max