import pygame
import os
from config import LARGURA_TELA, ALTURA_TELA, DIRETORIO_ASSETS

CAMINHO_ASSETS = os.path.join(DIRETORIO_ASSETS, 'imagens')


class Mao:
    def __init__(self, lado='direita', posicao=None, tamanho=(100, 100)):
        self.lado = lado
        self.estado = 'ocioso'
        self.x_alvo = None
        self.y_alvo = None
        self.x_atual = None
        self.y_atual = None
        self.velocidade = 5
        self.tamanho = tamanho
        self.carta_segurada = None
        caminho_imagem = os.path.join(
            CAMINHO_ASSETS, 'maos', f'mao_{lado}.png')
        try:
            self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem, tamanho)
        except:
            self.imagem = pygame.Surface((100, 100), pygame.SRCALPHA)
            cor = (255, 200, 200) if lado == 'direita' else (200, 200, 255)
            pygame.draw.circle(self.imagem, cor, (50, 50), 45)
            pygame.draw.circle(self.imagem, (0, 0, 0), (50, 50), 45, 2)
        if posicao:
            self.x_atual, self.y_atual = posicao
        else:
            if lado == 'esquerda':
                self.x_atual = 200
                self.y_atual = ALTURA_TELA - 150
            else:
                self.x_atual = LARGURA_TELA - 320
                self.y_atual = ALTURA_TELA - 150
        self.x_ocioso = self.x_atual
        self.y_ocioso = self.y_atual

    def mover_para_baralho(self, posicao_baralho):
        self.estado = 'alcancando'
        self.x_alvo, self.y_alvo = posicao_baralho

    def retornar_para_ocioso(self):
        self.estado = 'retornando'
        self.x_alvo = self.x_ocioso
        self.y_alvo = self.y_ocioso

    def segurar_carta(self, carta):
        self.carta_segurada = carta
        self.estado = 'segurando'

    def atualizar(self):
        if self.estado in ('alcancando', 'retornando') and self.x_alvo is not None:
            dx = self.x_alvo - self.x_atual
            dy = self.y_alvo - self.y_atual
            distancia = (dx**2 + dy**2)**0.5
            if distancia < self.velocidade:
                self.x_atual = self.x_alvo
                self.y_atual = self.y_alvo
                if self.estado == 'alcancando':
                    self.estado = 'segurando'
                elif self.estado == 'retornando':
                    self.estado = 'ocioso'
            else:
                self.x_atual += dx * self.velocidade / distancia
                self.y_atual += dy * self.velocidade / distancia

    def desenhar(self, tela):
        tela.blit(self.imagem, (int(self.x_atual), int(self.y_atual)))
