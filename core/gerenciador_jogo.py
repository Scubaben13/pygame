import pygame
from cenas import CenaMenu, CenaInstrucoes, CenaJogo


class GerenciadorJogo:
    def __init__(self, tela):
        self.tela = tela
        self.executando = True
        self.relogio = pygame.time.Clock()
        self.modo_jogo = None
        self.cenas = {
            'menu': CenaMenu(self),
            'instrucoes': CenaInstrucoes(self)
        }
        self.cena_atual = 'menu'

    def mudar_cena(self, nome_cena: str, modo=None):
        if modo is not None:
            self.modo_jogo = modo
        if nome_cena == 'instrucoes':
            self.cenas['instrucoes'] = CenaInstrucoes(self)
        if nome_cena == 'jogo':
            self.cenas['jogo'] = CenaJogo(self)
        self.cena_atual = nome_cena

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False
            else:
                self.cenas[self.cena_atual].tratar_evento(evento)

    def atualizar(self, dt):
        self.cenas[self.cena_atual].atualizar(dt)

    def desenhar(self, tela):
        self.cenas[self.cena_atual].desenhar(tela)

    def executar(self):
        while self.executando:
            dt = self.relogio.tick(60) / 1000.0
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar(self.tela)
            pygame.display.flip()
