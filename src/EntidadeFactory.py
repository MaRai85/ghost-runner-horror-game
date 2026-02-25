from .Constantes import width_max, height_max
from .Fundo import Fundo
from .Jogador import Jogador
from .Inimigo import Inimigo
from .Orb import Orb
import random
class EntidadeFactory:

    @staticmethod
    def get_entity(nome_entidade: str):  # BACKGROUND DO MODO DEMO
        if nome_entidade == 'demoModeBg':
            lista = []
            for i in range(6):  # carrega somente até 05 imagens para load em background
                lista.append(Fundo(f"demoModeBg{i}", (0, 0), layer=i))
                lista.append(Fundo(f"demoModeBg{i}", (width_max, 0), layer=i))
            return lista
        #JOGADOR
        elif nome_entidade == 'Jogador':
            return [Jogador((10, height_max / 3))]
        #INIMIGOS
        elif nome_entidade == 'inimigo01':
            return [Inimigo('inimigo01', (width_max + 10, random.randint(50, height_max - -140)))]
        elif nome_entidade == 'inimigo02':
            return[Inimigo('inimigo02', (width_max + 10, random.randint(50, height_max - 140)))]
        elif nome_entidade == 'inimigo03':
            return[Inimigo('inimigo03', (width_max + 10, random.randint(50, height_max -140)))]
        #ORBES DE ENERGIA
        elif nome_entidade == 'energy_orb_S':
            return [Orb('energy_orb_S', (width_max + 10, random.randint(50, height_max - 50)))]
        elif nome_entidade == 'energy_orb_XL':
            return [Orb('energy_orb_XL', (width_max + 10, random.randint(50, height_max - 50)))]
        else:
            raise ValueError(f'Entidade desconhecida: {nome_entidade}')
