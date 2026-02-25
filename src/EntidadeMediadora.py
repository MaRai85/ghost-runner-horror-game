from .Entidade import Entidade
from .Inimigo import Inimigo
from .Orb import Orb
class EntidadeMediadora:

    @staticmethod
    def __verificar_janela_colisao(ent: Entidade):
        if isinstance(ent,(Inimigo, Orb)): #SO verifica entidade Inimigo e Orbs, excluindo player e background
            if ent.Rect.right <0:
                ent.saude = 0

    @staticmethod
    def verificar_colisoes(lista_entidades: list[Entidade]):
        for ent in lista_entidades:
            EntidadeMediadora.__verificar_janela_colisao(ent)

    @staticmethod #se vid = 0  remove
    def verificar_saude(lista_entidades: list[Entidade]): #só remove entidades com saude abaixo ou igual zero
        for ent in lista_entidades[:]:
            if isinstance(ent, (Inimigo, Orb)) and ent.saude <= 0:
                lista_entidades.remove(ent)
