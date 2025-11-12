import pygame
import os
from config import LARGURA_TELA, ALTURA_TELA, DIRETORIO_ASSETS

CAMINHO_ASSETS = os.path.join(DIRETORIO_ASSETS, 'imagens')


class Baralho:
    def __init__(self, posicao=None):
        if posicao is None:
            self.x = LARGURA_TELA - 150
            self.y = ALTURA_TELA - 300
        else:
            self.x, self.y = posicao
        caminho_verso = os.path.join(CAMINHO_ASSETS, 'cartas', 'Fundo.png')
        self.imagem = None
        try:
            self.imagem = pygame.image.load(caminho_verso).convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem, (80, 120))
        except:
            self.imagem = pygame.Surface((80, 120), pygame.SRCALPHA)
            pygame.draw.rect(self.imagem, (50, 50, 150), (0, 0, 80, 120))
            pygame.draw.rect(self.imagem, (0, 0, 0), (0, 0, 80, 120), 2)
            fonte = pygame.font.SysFont(None, 24)
            texto = fonte.render("BARALHO", True, (255, 255, 255))
            self.imagem.blit(texto, (40 - texto.get_width() //
                             2, 60 - texto.get_height()//2))

    def obter_posicao(self):
        return (self.x + 40, self.y + 60)

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))
