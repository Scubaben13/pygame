import pygame
from config import LARGURA_TELA, ALTURA_TELA, COR_FUNDO, COR_BRANCA, DURACAO_MAXIMA_INSTRUCOES, TEXTO_INSTRUCOES


class CenaInstrucoes:
    def __init__(self, gerenciador_jogo):
        self.gerenciador_jogo = gerenciador_jogo
        self.fonte = pygame.font.SysFont(None, 36)
        self.fonte_pequena = pygame.font.SysFont(None, 28)
        self.inicio_tempo = pygame.time.get_ticks()
        self.duracao_maxima = DURACAO_MAXIMA_INSTRUCOES
        self.linhas = TEXTO_INSTRUCOES

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                self._iniciar_jogo()

    def atualizar(self, dt):
        if pygame.time.get_ticks() - self.inicio_tempo > self.duracao_maxima:
            self._iniciar_jogo()

    def _iniciar_jogo(self):
        if self.gerenciador_jogo.modo_jogo is None:
            self.gerenciador_jogo.mudar_cena('menu')
        else:
            self.gerenciador_jogo.mudar_cena('jogo')

    def desenhar(self, tela):
        tela.fill(COR_FUNDO)
        titulo = self.fonte.render("INSTRUÇÕES", True, COR_BRANCA)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 50))
        y_offset = 120
        for linha in self.linhas:
            texto = self.fonte_pequena.render(linha, True, COR_BRANCA)
            tela.blit(texto, (100, y_offset))
            y_offset += 32
        decorrido = (pygame.time.get_ticks() - self.inicio_tempo) // 1000
        restante = max(0, 15 - decorrido)
        temporizador = self.fonte_pequena.render(
            f"Tempo restante: {restante}s (ou pressione uma seta para pular)", True, (220, 220, 100))
        tela.blit(temporizador, (LARGURA_TELA // 2 -
                  temporizador.get_width() // 2, ALTURA_TELA - 50))
