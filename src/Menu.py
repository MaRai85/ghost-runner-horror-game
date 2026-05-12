import asyncio
import pygame
import sys
import os

#FUNÇÃO resource_path para PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

from .Constantes import width_max, height_max, BRANCO_SUAVE, AZUL, OPCAO_MENU

class Menu:
    def __init__(self, window):
        self.window = window
        self.opcao_atual = 0
        # FUNDO DO MENU
        self.surf = pygame.image.load(resource_path('assets/images/menu_v3.png')).convert()
        self.surf = pygame.transform.scale(self.surf, (width_max, height_max))
        self.rect = self.surf.get_rect(left=0, top=0)
        # SONS DO MENU
        self.som_click = pygame.mixer.Sound(resource_path("assets/sounds/menu_click.ogg"))
        self.som_click.set_volume(0.25)
        self.som_select = pygame.mixer.Sound(resource_path("assets/sounds/menu_select.ogg"))
        # FONTES
        self.fonte_titulo = pygame.font.Font(resource_path('assets/fonts/Nosifer-Regular.ttf'), 82)
        self.fonte_subtitulo = pygame.font.Font(resource_path('assets/fonts/Cinzel-Regular.ttf'), 45)
        self.fonte_menu = pygame.font.Font(resource_path('assets/fonts/FontdinerSwanky-Regular.ttf'), 24)
        self.fonte_info = pygame.font.SysFont("Arial", 18)

    def desenhar_texto(self, fonte, texto, cor, centro):
        sombra_cor = (10, 10, 10)
        # CONTORNO/SOMBRA PARA DAR PESO AO TEXTO
        for dx, dy in [(-3, 0), (3, 0),
            (0, -3), (0, 3),(-2, -2), (2, 2),(-2, 2), (2, -2)]:
            sombra = fonte.render(texto, True, sombra_cor)
            sombra_rect = sombra.get_rect(center=(centro[0] + dx, centro[1] + dy))
            self.window.blit(sombra, sombra_rect)
        # TEXTO PRINCIPAL
        surf = fonte.render(texto, True, cor)
        rect = surf.get_rect(center=centro)
        self.window.blit(surf, rect)

    def desenhar_botao_menu(self, texto, centro_y, ativo=False):
        # BOTÃO ATIVO FICA UM POUCO MAIOR PARA DAR PROFUNDIDADE
        if ativo:
            largura = 320
            altura = 46
        else:
            largura = 300
            altura = 42
        x = width_max // 2 - largura // 2
        y = centro_y - altura // 2

        # GLOW ATRÁS DO BOTÃO SELECIONADO
        if ativo:
            glow = pygame.Surface((largura + 35, altura + 22), pygame.SRCALPHA)
            pygame.draw.rect(
                glow,
                (80, 170, 255, 45),
                glow.get_rect(),
                border_radius=14
            )
            self.window.blit(glow, (x - 17, y - 11))

        # SOMBRA INFERIOR PARA DAR SENSAÇÃO DE ALTURA
        sombra = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(
            sombra,
            (0, 0, 0, 65),
            sombra.get_rect(),
            border_radius=8
        )
        self.window.blit(sombra, (x + 3, y + 6))

        # SUPERFÍCIE DO BOTÃO
        botao = pygame.Surface((largura, altura), pygame.SRCALPHA)
        if ativo:
            botao.fill((25, 80, 150, 135))
            borda = (120, 210, 255, 210)
            cor_texto = BRANCO_SUAVE
        else:
            botao.fill((0, 0, 0, 80))
            borda = (120, 210, 255, 70)
            cor_texto = (190, 190, 190)
        # BORDA DO BOTÃO
        pygame.draw.rect(
            botao,
            borda,
            botao.get_rect(),
            2,
            border_radius=8
        )
        self.window.blit(botao, (x, y))
        # TEXTO DO BOTÃO
        self.desenhar_texto(
            self.fonte_menu,
            texto,
            cor_texto,
            (width_max // 2, centro_y)
        )

    async def run(self):
        pygame.mixer.music.load(resource_path("assets/sounds/dark_intro.ogg"))
        pygame.mixer.music.play(-1)
        while True:
            # FUNDO
            self.window.blit(self.surf, self.rect)
            # ESCURECE LEVEMENTE A TELA PARA MELHORAR LEITURA
            overlay = pygame.Surface((width_max, height_max))
            overlay.set_alpha(65)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))
            # TÍTULO E SUBTÍTULO
            self.desenhar_texto(
                self.fonte_titulo,
                'A Ghost Story',
                AZUL,
                (width_max // 2, 120)
            )
            self.desenhar_texto(
                self.fonte_subtitulo,
                'The Death Race',
                (185, 220, 255),
                (width_max // 2, 210)
            )
            # BOTÕES DO MENU
            for i, opcao in enumerate(OPCAO_MENU):
                tamanho_y = 405 + (i * 55)
                ativo = i == self.opcao_atual
                self.desenhar_botao_menu(opcao, tamanho_y, ativo)

            # TEXTO DE AJUDA NO RODAPÉ
            texto_info = 'Use setas cima/baixo para mover   |   Enter para selecionar   |   Esc para sair'
            surf_info = self.fonte_info.render(texto_info, True, BRANCO_SUAVE)
            rect_info = surf_info.get_rect(bottomright=(width_max - 25, height_max - 25))
            self.window.blit(surf_info, rect_info)
            pygame.display.flip()

            # EVENTOS DO MENU
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'SAIR'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.opcao_atual = (self.opcao_atual - 1) % len(OPCAO_MENU)
                        self.som_click.play()
                    elif event.key == pygame.K_DOWN:
                        self.opcao_atual = (self.opcao_atual + 1) % len(OPCAO_MENU)
                        self.som_click.play()
                    elif event.key == pygame.K_RETURN:
                        self.som_select.play()
                        await asyncio.sleep(0.2)
                        return OPCAO_MENU[self.opcao_atual]
                    elif event.key == pygame.K_ESCAPE:
                        return 'SAIR'
            await asyncio.sleep(0)