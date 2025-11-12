import pygame
import os
from config import LARGURA_TELA, ALTURA_TELA, DIRETORIO_ASSETS

CAMINHO_ASSETS = os.path.join(DIRETORIO_ASSETS, 'imagens')


class MaoAnimada:
    def __init__(self, lado='direita', posicao_alvo=None):
        self.lado = lado
        self.posicao_alvo = posicao_alvo
        self.estado = 'ocioso'
        self.progresso = 0.0
        self.inicio_apontar = 0
        if lado == 'esquerda':
            self.x = -100
            self.y = ALTURA_TELA
            self.x_inicio, self.y_inicio = -100, ALTURA_TELA
        else:
            self.x = LARGURA_TELA + 100
            self.y = ALTURA_TELA
            self.x_inicio, self.y_inicio = LARGURA_TELA + 100, ALTURA_TELA
        self.imagem_mao = None
        self.carregar_imagem_mao()

    def carregar_imagem_mao(self):
        caminho_imagem = os.path.join(
            CAMINHO_ASSETS, 'maos', f'mao_{self.lado}.png')
        try:
            self.imagem_mao = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem_mao = pygame.transform.scale(
                self.imagem_mao, (100, 100))
        except:
            self.imagem_mao = None

    def iniciar_animacao(self, posicao_alvo):
        self.posicao_alvo = posicao_alvo
        self.estado = 'movendo'
        self.progresso = 0.0
        if self.lado == 'esquerda':
            self.x, self.y = -100, ALTURA_TELA
        else:
            self.x, self.y = LARGURA_TELA + 100, ALTURA_TELA

    def atualizar(self):
        if self.estado == 'movendo':
            self.progresso += 0.05
            if self.progresso >= 1.0:
                self.progresso = 1.0
                self.estado = 'apontando'
                self.inicio_apontar = pygame.time.get_ticks()
            else:
                t = self.progresso
                self.x = (1-t)**2 * self.x_inicio + 2*(1-t)*t * \
                    (self.x_inicio + 200) + t**2 * self.posicao_alvo[0]
                self.y = (1-t)**2 * self.y_inicio + 2*(1-t)*t * \
                    (self.y_inicio - 300) + t**2 * self.posicao_alvo[1]
        elif self.estado == 'apontando':
            if pygame.time.get_ticks() - self.inicio_apontar > 500:
                self.estado = 'retornando'
                self.progresso = 0.0
        elif self.estado == 'retornando':
            self.progresso += 0.1
            if self.progresso >= 1.0:
                self.estado = 'ocioso'
            else:
                self.x = self.posicao_alvo[0] + \
                    (self.x_inicio - self.posicao_alvo[0]) * self.progresso
                self.y = self.posicao_alvo[1] + \
                    (self.y_inicio - self.posicao_alvo[1]) * self.progresso

    def esta_ativa(self):
        return self.estado != 'ocioso'

    def desenhar(self, tela):
        if self.estado == 'ocioso' or self.posicao_alvo is None:
            return
        if self.imagem_mao:
            tela.blit(self.imagem_mao, (int(self.x) - 50, int(self.y) - 50))
        else:
            x_visivel = max(50, min(LARGURA_TELA - 50, int(self.x)))
            y_visivel = max(50, min(ALTURA_TELA - 50, int(self.y)))
            pygame.draw.circle(tela, (255, 220, 180),
                               (x_visivel, y_visivel), 30)
            pygame.draw.ellipse(
                tela, (0, 0, 0), (x_visivel - 40, y_visivel - 20, 80, 40))
            if self.posicao_alvo:
                pygame.draw.line(tela, (255, 100, 100),
                                 (x_visivel, y_visivel), self.posicao_alvo, 3)
