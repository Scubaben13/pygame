import pygame
import os
from config import SIMBOLOS_NAIPE, DIRETORIO_ASSETS

CAMINHO_ASSETS = os.path.join(DIRETORIO_ASSETS, 'imagens')


class Carta:
    def __init__(self, valor, naipe=None, face_para_cima=True, tamanho=(100, 150)):
        self.valor = valor
        self.naipe = naipe
        self.face_para_cima = face_para_cima
        self._tamanho = tamanho
        self.x = 0
        self.y = 0
        self.x_alvo = None
        self.y_alvo = None
        self.movendo = False
        self.progresso_virar = 1.0 if face_para_cima else 0.0
        self.virando = False
        self.salto_offset = 0
        self.direcao_salto = 0
        self.cor_salto = (255, 255, 255)
        self.congelada = False
        self.inicio_congelamento = 0
        self.x_final = 0
        self.y_final = 0
        self.progresso_animacao = 0.0
        self.animacao_ativa = False
        self._carregar_imagens()

    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, valor):
        if self._tamanho != valor:
            self._tamanho = valor
            self._carregar_imagens()

    def iniciar_virar_e_mover(self, x_alvo, y_alvo):
        self.virando = True
        self.progresso_virar = 0.0
        self.x_alvo = x_alvo
        self.y_alvo = y_alvo
        self.movendo = True

    def animacao_concluida(self):
        return not self.virando and not self.movendo

    def _carregar_imagens(self):
        caminho_verso = os.path.join(CAMINHO_ASSETS, 'cartas', 'Fundo.png')
        self.imagem_verso = None
        try:
            self.imagem_verso = pygame.image.load(
                caminho_verso).convert_alpha()
            self.imagem_verso = pygame.transform.scale(
                self.imagem_verso, self.tamanho)
        except:
            self.imagem_verso = self._criar_placeholder("?", (80, 80, 120))
        if self.valor.startswith(('RedJoker', 'BlackJoker')):
            nome_arquivo = f"{self.valor}.png"
        else:
            simbolo = SIMBOLOS_NAIPE.get(self.naipe, '')
            nome_arquivo = f"{self.valor}{simbolo}.png"
        caminho_frente = os.path.join(CAMINHO_ASSETS, 'cartas', nome_arquivo)
        self.imagem_frente = None
        try:
            self.imagem_frente = pygame.image.load(
                caminho_frente).convert_alpha()
            self.imagem_frente = pygame.transform.scale(
                self.imagem_frente, self.tamanho)
        except:
            rotulo = f"{self.valor}{SIMBOLOS_NAIPE.get(self.naipe, '')}" if self.naipe else self.valor
            self.imagem_frente = self._criar_placeholder(rotulo)

    def _criar_placeholder(self, texto, cor=(255, 255, 255)):
        superficie = pygame.Surface(self.tamanho, pygame.SRCALPHA)
        pygame.draw.rect(superficie, cor, (0, 0, *self._tamanho))
        pygame.draw.rect(superficie, (0, 0, 0), (0, 0, *self._tamanho), 2)
        fonte = pygame.font.SysFont(None, 36)
        texto_renderizado = fonte.render(str(texto), True, (0, 0, 0))
        superficie.blit(texto_renderizado, (self.tamanho[0]//2 - texto_renderizado.get_width(
        )//2, self.tamanho[1]//2 - texto_renderizado.get_height()//2))
        return superficie

    def atualizar(self):
        if self.virando:
            self.progresso_virar += 0.1
            if self.progresso_virar >= 1.0:
                self.progresso_virar = 1.0
                self.face_para_cima = True
                self.virando = False
                from cenas.cena_jogo import SFX
                if SFX.get('virar_carta'):
                    SFX['virar_carta'].play()
        if self.movendo and self.x_alvo is not None:
            dx = self.x_alvo - self.x
            dy = self.y_alvo - self.y
            if abs(dx) < 1 and abs(dy) < 1:
                self.x = self.x_alvo
                self.y = self.y_alvo
                self.movendo = False
            else:
                self.x += dx * 0.1
                self.y += dy * 0.1
        if self.direcao_salto != 0:
            self.salto_offset += self.direcao_salto * 8
            if self.salto_offset >= 25:
                self.direcao_salto = -1
            elif self.salto_offset <= 0:
                self.salto_offset = 0
                self.direcao_salto = 0
                self.congelada = True
                self.inicio_congelamento = pygame.time.get_ticks()
        if self.congelada:
            if pygame.time.get_ticks() - self.inicio_congelamento > 2000:
                self.congelada = False

    def desenhar(self, tela):
        x_desenho = self.x
        y_desenho = self.y - self.salto_offset
        largura_atual, altura_atual = self._tamanho
        progresso = self.progresso_virar
        if progresso < 0.5:
            escala = 1 - (progresso / 0.5)
            imagem = self.imagem_verso
        else:
            escala = (progresso - 0.5) / 0.5
            imagem = self.imagem_frente
        if imagem and escala > 0:
            w = int(largura_atual * escala)
            h = int(altura_atual * escala)
            if w > 0 and h > 0:
                escalada = pygame.transform.scale(imagem, (w, h))
                tela.blit(escalada, (x_desenho + (largura_atual - w) //
                          2, y_desenho + (altura_atual - h) // 2))
        if self.direcao_salto != 0 or self.congelada:
            sombra = pygame.Surface(
                (largura_atual, altura_atual), pygame.SRCALPHA)
            cor = self.cor_salto if self.direcao_salto != 0 else (
                255, 255, 255)
            sombra.fill((*cor, 128))
            tela.blit(sombra, (x_desenho, y_desenho + 8))

    def obter_retangulo(self):
        return pygame.Rect(self.x, self.y, *self._tamanho)

    def esta_face_para_cima(self):
        return self.face_para_cima

    def disparar_salto(self, sucesso=True):
        self.salto_offset = 0
        self.direcao_salto = 1
        self.cor_salto = (100, 255, 100) if sucesso else (255, 100, 100)
