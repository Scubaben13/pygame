import pygame
from config import LARGURA_TELA, COR_FUNDO, COR_BRANCA, COR_CINZA, OPCOES_MENU, TITULO_JOGO


class CenaMenu:
    def __init__(self, gerenciador_jogo):
        self.gerenciador_jogo = gerenciador_jogo
        self.fonte_titulo = pygame.font.SysFont(None, 72)
        self.fonte_opcao = pygame.font.SysFont(None, 48)
        self.selecionado = 0

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.selecionado = (self.selecionado - 1) % 3
            elif evento.key == pygame.K_DOWN:
                self.selecionado = (self.selecionado + 1) % 3
            elif evento.key == pygame.K_RETURN:
                if self.selecionado == 0:
                    self.gerenciador_jogo.mudar_cena(
                        'instrucoes', modo='simples')
                elif self.selecionado == 1:
                    self.gerenciador_jogo.mudar_cena(
                        'instrucoes', modo='multi')
                elif self.selecionado == 2:
                    self.gerenciador_jogo.mudar_cena('instrucoes', modo=None)

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        tela.fill(COR_FUNDO)
        titulo = self.fonte_titulo.render(TITULO_JOGO, True, COR_BRANCA)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 150))
        for i, opcao in enumerate(OPCOES_MENU):
            cor = COR_BRANCA if i == self.selecionado else COR_CINZA
            texto = self.fonte_opcao.render(opcao, True, cor)
            tela.blit(texto, (LARGURA_TELA // 2 -
                      texto.get_width() // 2, 300 + i * 70))
