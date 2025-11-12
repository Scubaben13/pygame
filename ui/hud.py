import pygame
import json
import os
from config import LARGURA_TELA, ALTURA_TELA, COR_BRANCA, COR_VERDE_CLARO, COR_VERMELHA, CAMINHO_CONFIGURACAO_HUD


class HUD:
    def __init__(self, modo):
        self.modo = modo
        self.modo_edicao = False
        self.arrastando = None
        self.elemento_selecionado = None
        self.turno_atual = None
        self.piscar_visivel = True
        self.pontuacao_simples = 0
        self.tempo_reacao = None
        self.pontuacao_p1 = 0
        self.pontuacao_p2 = 0
        self.tempo_p1 = None
        self.tempo_p2 = None
        self.configuracao = self._carregar_configuracao()

    def _carregar_configuracao(self):
        configuracao_padrao = {
            "global": {
                "tamanho_fonte_pontuacao": 48,
                "tamanho_fonte_timer": 36,
                "tamanho_fonte_rotulo": 32,
                "largura_carta_alvo": 100,
                "altura_carta_alvo": 150,
                "largura_carta_sequencia": 100,
                "altura_carta_sequencia": 150,
                "btn_menu_x": LARGURA_TELA - 100,
                "btn_menu_y": 20
            },
            "simples": {
                "pontuacao": [20, 20],
                "timer": [20, 80],
                "rotulo_alvo": [LARGURA_TELA // 2, ALTURA_TELA - 240],
                "carta_alvo_x": LARGURA_TELA // 2 - 50,
                "carta_alvo_y": ALTURA_TELA - 200,
                "carta_sequencia_x": LARGURA_TELA // 2 - 50,
                "carta_sequencia_y": ALTURA_TELA // 2 - 75
            },
            "multi": {
                "rotulo_p1": [150, ALTURA_TELA - 240],
                "pontuacao_p1": [50, 50],
                "timer_p1": [50, 140],
                "carta_alvo_p1_x": 150,
                "carta_alvo_p1_y": ALTURA_TELA - 200,
                "rotulo_p2": [LARGURA_TELA - 250, ALTURA_TELA - 240],
                "pontuacao_p2": [LARGURA_TELA - 200, 50],
                "timer_p2": [LARGURA_TELA - 200, 140],
                "carta_alvo_p2_x": LARGURA_TELA - 250,
                "carta_alvo_p2_y": ALTURA_TELA - 200,
                "carta_sequencia_x": LARGURA_TELA // 2 - 50,
                "carta_sequencia_y": ALTURA_TELA // 2 - 75
            }
        }
        configuracao_carregada = {}
        try:
            if os.path.exists(CAMINHO_CONFIGURACAO_HUD):
                with open(CAMINHO_CONFIGURACAO_HUD, 'r', encoding='utf-8') as f:
                    configuracao_carregada = json.load(f)
        except Exception as e:
            print(f"[HUD] Erro ao carregar configuracao: {e}")

        def mesclar_profundo(padrao, carregado):
            if not isinstance(carregado, dict):
                return padrao
            resultado = padrao.copy()
            for chave, valor in carregado.items():
                if chave in resultado and isinstance(resultado[chave], dict) and isinstance(valor, dict):
                    resultado[chave] = mesclar_profundo(
                        resultado[chave], valor)
                else:
                    resultado[chave] = valor
            return resultado
        return mesclar_profundo(configuracao_padrao, configuracao_carregada)

    def salvar_configuracao(self):
        os.makedirs(os.path.dirname(CAMINHO_CONFIGURACAO_HUD), exist_ok=True)
        with open(CAMINHO_CONFIGURACAO_HUD, 'w', encoding='utf-8') as f:
            json.dump(self.configuracao, f, indent=2)
        print("[HUD] Configuracao salva!")

    def tratar_evento(self, evento, info_posicoes=None):
        if not self.modo_edicao:
            return
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
            self.salvar_configuracao()
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_PLUS, pygame.K_EQUALS):
                self._ajustar_tamanho(+5)
            elif evento.key == pygame.K_MINUS:
                self._ajustar_tamanho(-5)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            self.elemento_selecionado = None
            self.arrastando = None
            if not info_posicoes:
                return
            if "btn_menu" in info_posicoes and info_posicoes["btn_menu"]:
                if self._esta_perto(x, y, info_posicoes["btn_menu"]):
                    self.elemento_selecionado = "btn_menu"
                    self.arrastando = "btn_menu"
                    return
            if self.modo == "simples":
                for chave in ["pontuacao", "timer", "rotulo_alvo", "carta_alvo", "carta_sequencia"]:
                    if chave in info_posicoes and info_posicoes[chave]:
                        if self._esta_perto(x, y, info_posicoes[chave]):
                            self.elemento_selecionado = chave
                            self.arrastando = chave
                            return
            elif self.modo == "multi":
                for chave in ["rotulo_p1", "pontuacao_p1", "timer_p1", "rotulo_p2", "pontuacao_p2", "timer_p2", "carta_alvo_p1", "carta_alvo_p2", "carta_sequencia"]:
                    if chave in info_posicoes and info_posicoes[chave]:
                        if self._esta_perto(x, y, info_posicoes[chave]):
                            self.elemento_selecionado = chave
                            self.arrastando = chave
                            return
        if evento.type == pygame.MOUSEBUTTONUP:
            self.arrastando = None
        if evento.type == pygame.MOUSEMOTION and self.arrastando:
            x, y = evento.pos
            g = self.configuracao["global"]
            if self.arrastando == "btn_menu":
                self.configuracao["global"]["btn_menu_x"] = x
                self.configuracao["global"]["btn_menu_y"] = y
            elif self.modo == "simples":
                if self.arrastando in self.configuracao["simples"]:
                    self.configuracao["simples"][self.arrastando] = [x, y]
                elif self.arrastando == "carta_alvo":
                    self.configuracao["simples"]["carta_alvo_x"] = x - \
                        g["largura_carta_alvo"] // 2
                    self.configuracao["simples"]["carta_alvo_y"] = y - \
                        g["altura_carta_alvo"] // 2
                elif self.arrastando == "carta_sequencia":
                    self.configuracao["simples"]["carta_sequencia_x"] = x - \
                        g["largura_carta_sequencia"] // 2
                    self.configuracao["simples"]["carta_sequencia_y"] = y - \
                        g["altura_carta_sequencia"] // 2
            elif self.modo == "multi":
                if self.arrastando in self.configuracao["multi"]:
                    self.configuracao["multi"][self.arrastando] = [x, y]
                elif self.arrastando == "carta_alvo_p1":
                    self.configuracao["multi"]["carta_alvo_p1_x"] = x - \
                        g["largura_carta_alvo"] // 2
                    self.configuracao["multi"]["carta_alvo_p1_y"] = y - \
                        g["altura_carta_alvo"] // 2
                elif self.arrastando == "carta_alvo_p2":
                    self.configuracao["multi"]["carta_alvo_p2_x"] = x - \
                        g["largura_carta_alvo"] // 2
                    self.configuracao["multi"]["carta_alvo_p2_y"] = y - \
                        g["altura_carta_alvo"] // 2
                elif self.arrastando == "carta_sequencia":
                    self.configuracao["multi"]["carta_sequencia_x"] = x - \
                        g["largura_carta_sequencia"] // 2
                    self.configuracao["multi"]["carta_sequencia_y"] = y - \
                        g["altura_carta_sequencia"] // 2

    def _ajustar_tamanho(self, delta):
        if not self.elemento_selecionado:
            return
        g = self.configuracao["global"]
        if "carta_alvo" in self.elemento_selecionado:
            g["largura_carta_alvo"] = max(50, g["largura_carta_alvo"] + delta)
            g["altura_carta_alvo"] = max(
                75, g["altura_carta_alvo"] + int(delta * 1.5))
        elif "carta_sequencia" in self.elemento_selecionado:
            g["largura_carta_sequencia"] = max(
                50, g["largura_carta_sequencia"] + delta)
            g["altura_carta_sequencia"] = max(
                75, g["altura_carta_sequencia"] + int(delta * 1.5))
        elif "rotulo" in self.elemento_selecionado:
            g["tamanho_fonte_rotulo"] = max(
                16, g["tamanho_fonte_rotulo"] + delta)
        elif "pontuacao" in self.elemento_selecionado:
            g["tamanho_fonte_pontuacao"] = max(
                20, g["tamanho_fonte_pontuacao"] + delta)
        elif "timer" in self.elemento_selecionado:
            g["tamanho_fonte_timer"] = max(
                16, g["tamanho_fonte_timer"] + delta)

    def _esta_perto(self, x, y, pos, limite=60):
        if not pos:
            return False
        if isinstance(pos, (list, tuple)):
            px, py = pos
        else:
            return False
        return abs(x - px) < limite and abs(y - py) < limite

    def alternar_modo_edicao(self):
        self.modo_edicao = not self.modo_edicao
        if self.modo_edicao:
            print("[HUD] Modo de edicao ativado")
        else:
            print("[HUD] Modo de edicao desativado")

    def obter_fontes(self):
        g = self.configuracao["global"]
        return {
            "pontuacao": pygame.font.SysFont(None, g["tamanho_fonte_pontuacao"]),
            "timer": pygame.font.SysFont(None, g["tamanho_fonte_timer"]),
            "rotulo": pygame.font.SysFont(None, g["tamanho_fonte_rotulo"])
        }

    def desenhar(self, tela, info_elementos=None):
        fontes = self.obter_fontes()
        if self.modo == "simples":
            texto_pontuacao = fontes["pontuacao"].render(
                f"Pontos: {self.pontuacao_simples}", True, COR_BRANCA)
            tela.blit(texto_pontuacao,
                      self.configuracao["simples"]["pontuacao"])
            if self.tempo_reacao is not None:
                cor = COR_VERDE_CLARO if self.tempo_reacao < 0.5 else (
                    COR_VERMELHA if self.tempo_reacao > 2.0 else COR_BRANCA)
                texto_timer = fontes["timer"].render(
                    f"Reacao: {self.tempo_reacao:.2f}s", True, cor)
                tela.blit(texto_timer, self.configuracao["simples"]["timer"])
            pos_rotulo = self.configuracao["simples"]["rotulo_alvo"]
            texto_rotulo = fontes["rotulo"].render(
                "Sua carta:", True, COR_BRANCA)
            tela.blit(
                texto_rotulo, (pos_rotulo[0] - texto_rotulo.get_width() // 2, pos_rotulo[1]))
        elif self.modo == "multi":
            cor_p1 = COR_BRANCA if (
                self.piscar_visivel and self.turno_atual == 'jogador1') else (200, 200, 255)
            rotulo_p1 = fontes["rotulo"].render("Jogador 1", True, cor_p1)
            tela.blit(rotulo_p1, self.configuracao["multi"]["rotulo_p1"])
            pontuacao_p1 = fontes["pontuacao"].render(
                str(self.pontuacao_p1), True, COR_BRANCA)
            tela.blit(pontuacao_p1, self.configuracao["multi"]["pontuacao_p1"])
            if self.tempo_p1 is not None:
                timer_p1 = fontes["timer"].render(
                    f"{self.tempo_p1:.2f}s", True, COR_BRANCA)
                tela.blit(timer_p1, self.configuracao["multi"]["timer_p1"])
            cor_p2 = COR_BRANCA if (
                self.piscar_visivel and self.turno_atual == 'jogador2') else (255, 200, 200)
            rotulo_p2 = fontes["rotulo"].render("Jogador 2", True, cor_p2)
            tela.blit(rotulo_p2, self.configuracao["multi"]["rotulo_p2"])
            pontuacao_p2 = fontes["pontuacao"].render(
                str(self.pontuacao_p2), True, COR_BRANCA)
            tela.blit(pontuacao_p2, self.configuracao["multi"]["pontuacao_p2"])
            if self.tempo_p2 is not None:
                timer_p2 = fontes["timer"].render(
                    f"{self.tempo_p2:.2f}s", True, COR_BRANCA)
                tela.blit(timer_p2, self.configuracao["multi"]["timer_p2"])
        g = self.configuracao["global"]
        btn_x = g["btn_menu_x"]
        btn_y = g["btn_menu_y"]
        rect_btn = pygame.Rect(btn_x, btn_y, 80, 30)
        pygame.draw.rect(tela, (80, 80, 120), rect_btn)
        pygame.draw.rect(tela, (200, 200, 255), rect_btn, 2)
        fonte_menu = pygame.font.SysFont(None, 24)
        texto_btn = fonte_menu.render("Menu", True, COR_BRANCA)
        tela.blit(texto_btn, (btn_x + 40 - texto_btn.get_width() //
                  2, btn_y + 15 - texto_btn.get_height() // 2))
        if self.modo_edicao:
            fonte_debug = pygame.font.SysFont(None, 18)
            todas_posicoes = {}
            if self.modo == "simples":
                todas_posicoes = {
                    "pontuacao": self.configuracao["simples"]["pontuacao"],
                    "timer": self.configuracao["simples"]["timer"],
                    "rotulo_alvo": self.configuracao["simples"]["rotulo_alvo"],
                    "carta_alvo": [self.configuracao["simples"]["carta_alvo_x"] + 50, self.configuracao["simples"]["carta_alvo_y"] + 75],
                    "carta_sequencia": [self.configuracao["simples"]["carta_sequencia_x"] + 50, self.configuracao["simples"]["carta_sequencia_y"] + 75],
                }
            elif self.modo == "multi":
                todas_posicoes = {
                    "rotulo_p1": self.configuracao["multi"]["rotulo_p1"],
                    "pontuacao_p1": self.configuracao["multi"]["pontuacao_p1"],
                    "timer_p1": self.configuracao["multi"]["timer_p1"],
                    "carta_alvo_p1": [self.configuracao["multi"]["carta_alvo_p1_x"] + 50, self.configuracao["multi"]["carta_alvo_p1_y"] + 75],
                    "rotulo_p2": self.configuracao["multi"]["rotulo_p2"],
                    "pontuacao_p2": self.configuracao["multi"]["pontuacao_p2"],
                    "timer_p2": self.configuracao["multi"]["timer_p2"],
                    "carta_alvo_p2": [self.configuracao["multi"]["carta_alvo_p2_x"] + 50, self.configuracao["multi"]["carta_alvo_p2_y"] + 75],
                    "carta_sequencia": [self.configuracao["multi"]["carta_sequencia_x"] + 50, self.configuracao["multi"]["carta_sequencia_y"] + 75],
                }
            todas_posicoes["btn_menu"] = [self.configuracao["global"]
                                          ["btn_menu_x"], self.configuracao["global"]["btn_menu_y"]]
            for nome, pos in todas_posicoes.items():
                if pos:
                    pygame.draw.circle(tela, (255, 0, 0),
                                       (int(pos[0]), int(pos[1])), 4)
                    txt = fonte_debug.render(nome, True, (255, 255, 0))
                    tela.blit(txt, (pos[0] + 5, pos[1] + 5))

    def atualizar_simples(self, pontuacao, tempo_reacao):
        self.pontuacao_simples = pontuacao
        self.tempo_reacao = tempo_reacao

    def atualizar_multi(self, pontuacao_p1, pontuacao_p2, tempo_p1, tempo_p2):
        self.pontuacao_p1 = pontuacao_p1
        self.pontuacao_p2 = pontuacao_p2
        self.tempo_p1 = tempo_p1
        self.tempo_p2 = tempo_p2

    def atualizar_turno(self, turno, piscar_visivel):
        self.turno_atual = turno
        self.piscar_visivel = piscar_visivel
