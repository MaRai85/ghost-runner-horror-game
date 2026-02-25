import pygame
from pathlib import Path
from .Entidade import Entidade
from .JogadorStats import JogadorStats
from .RegrasJogador import RegrasJogador
from .Constantes import VELOCIDA_DE_ENTIDADE, width_max, height_max

class Jogador(Entidade):
    def __init__(self, posicao_ghost):
        super().__init__('ghost_frente', posicao_ghost, layer=10)

        self.stats = JogadorStats()
        self.regras = RegrasJogador(self.stats)
        self.stats.on_dano_recebido = self._on_dano
        self.speed = VELOCIDA_DE_ENTIDADE['ghost_frente']

        BASE_DIR = Path(__file__).resolve().parent.parent
        IMG_DIR = BASE_DIR / "assets" / "images"

        self.imagens = {
            'normal': pygame.image.load(str(IMG_DIR / "ghost_frente.png")).convert_alpha(),
            'morto': pygame.image.load(str(IMG_DIR / "ghost_morto.png")).convert_alpha(),
            'esquerda': pygame.image.load(str(IMG_DIR / "ghost_esquerda.png")).convert_alpha(),
            'direita': pygame.image.load(str(IMG_DIR / "ghost_frente.png")).convert_alpha(),
            'powerUp': pygame.image.load(str(IMG_DIR / "ghost_powerup.png")).convert_alpha(),
            'assustado': pygame.image.load(str(IMG_DIR / "ghost_assustado.png")).convert_alpha(),
            'invencivel': pygame.image.load(str(IMG_DIR / "ghost_invencivel.png")).convert_alpha(),
        }
        # temporizador para atualização de estado
        self.tempo_acumulado = 0

    def _on_dano(self):
        print("Fantasma recebeu dano!")

    @property
    def estado(self):
        return self.stats.estado_atual

    @estado.setter
    def estado(self, valor):
        self.stats.mudar_estado(valor)

    def atualizar_sprites(self):
        sprite_estado = self.stats.estado_atual
        if sprite_estado not in self.imagens:
            sprite_estado = 'normal'
        self.Surf = self.imagens[sprite_estado]
        self.mask = pygame.mask.from_surface(self.Surf) #OTIMO para colisões pixel a pixel

    def move(self):
        keys = pygame.key.get_pressed()
        self.stats.atualizar_estado()  # Atualiza estado dos temporizadores

        velocidade_atual = self.speed
        if self.stats.powerup_ativo:
            velocidade_atual = self.speed + 3

        if not self.stats.esta_vivo:  # só vai mexer se estiver vivo
            self.atualizar_sprites()
            return

        pode_mover = self.stats.estado_atual not in ['morto']
        if pode_mover:
            if keys[pygame.K_UP]:
                self.Rect.y -= velocidade_atual
            if keys[pygame.K_DOWN]:
                self.Rect.y += velocidade_atual
            if keys[pygame.K_LEFT]:
                self.Rect.x -= velocidade_atual
                if self.stats.estado_atual == 'normal':
                    self.stats.mudar_estado('esquerda')
            if keys[pygame.K_RIGHT]:
                self.Rect.x += velocidade_atual
                if self.stats.estado_atual == 'esquerda':
                    self.stats.mudar_estado('normal')

        # LIMITES DA TELA, PERMITINDO SAÍR ATÉ METADE DO PERSONAGEM FORA
        meia_largura = self.Rect.width // 2
        meia_altura = self.Rect.height // 2
        self.Rect.left = max(-meia_largura, min(self.Rect.left, width_max - meia_largura))
        self.Rect.top = max(-meia_altura, min(self.Rect.top, height_max - meia_altura))

        # importantíssimo para atualizar os estados
        self.atualizar_sprites()