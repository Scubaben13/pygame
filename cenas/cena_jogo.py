import pygame
import random
from entities.mao import Mao
from entities.carta import Carta
from entities.baralho import Baralho
from entities.mao_animada import MaoAnimada
from ui.hud import HUD
from config import LARGURA_TELA, ALTURA_TELA, COR_FUNDO, CONTROLES, SONS, DURACAO_EXIBICAO, PROBABILIDADE_FORCAR_ALVO
VALORES_CARTAS = ['A', '2', '3', '4', '5',
                  '6', '7', '8', '9', '10', 'J', 'Q', 'K']
NAIPES_CARTAS = ['espadas', 'copas', 'ouros', 'paus']

SFX = {}


def carregar_sons():
    """Carrega todos os sons após o mixer ser inicializado."""
    global SFX
    SFX = {nome: carregar_som(caminho) for nome, caminho in SONS.items()}


def carregar_som(caminho):
    try:
        return pygame.mixer.Sound(caminho)
    except Exception as e:
        print(f"[ERROR] Falha ao carregar {caminho}: {e}")
        return None


class CenaJogo:
    def __init__(self, gerenciador_jogo):
        self.gerenciador_jogo = gerenciador_jogo
        self.modo = gerenciador_jogo.modo_jogo or 'simples'
        self.fundo = COR_FUNDO
        self.baralho = Baralho()
        self.hud = HUD(self.modo)
        self.piscar_tempo = 0
        self.piscar_visivel = True
        self.inicio_turno = 0
        self.mao_animada = None
        self.congelar_sequencia = False
        self.inicio_congelamento = 0
        if self.modo == 'multi':
            self.mao_esquerda = Mao(lado='esquerda', tamanho=(100, 100))
            self.mao_direita = Mao(lado='direita', tamanho=(100, 100))
        else:
            self.mao = Mao(lado='direita', tamanho=(100, 100))
        if self.modo == 'multi':
            self.estado = 'selecionar_p1'
        else:
            self.estado = 'selecionar_alvo'
        self.alvo_carta = None
        self.objeto_alvo_carta = None
        self.alvo_carta_p1 = None
        self.alvo_carta_p2 = None
        self.objeto_alvo_carta_p1 = None
        self.objeto_alvo_carta_p2 = None
        self.carta_sequencia_atual = None
        self.cartas_selecionaveis = []
        self.ultimo_mudanca_tempo = 0
        self.duracao_exibicao = DURACAO_EXIBICAO
        self.pontuacao_p1 = 0
        self.pontuacao_p2 = 0
        self.turno = 'jogador1' if self.modo == 'multi' else 'simples'
        self.carta_selecionada = None
        self.inicio_turno = pygame.time.get_ticks()
        self.inicio_animacao_selecao = 0
        self._ultimo_hover = False
        print(f"[SFX] correto carregado: {SFX.get('correto') is not None}")
        print(f"[SFX] errado carregado: {SFX.get('errado') is not None}")
        print(f"[SFX] clique carregado: {SFX.get('clique') is not None}")
        self._gerar_cartas_selecionaveis()

    def _iniciar_novo_turno(self):
        self.inicio_turno = pygame.time.get_ticks()
        self._iniciar_nova_sequencia()

    def _gerar_cartas_selecionaveis(self):
        self.cartas_selecionaveis = []
        for i in range(5):
            valor = random.choice(VALORES_CARTAS)
            naipe = random.choice(NAIPES_CARTAS).strip()
            carta = Carta(valor, naipe, face_para_cima=False,
                          tamanho=(100, 150))
            carta.x = self.baralho.x + 40
            carta.y = self.baralho.y + 60
            if self.estado == 'selecionar_p1':
                x_final = 150 + i * 140
                y_final = ALTURA_TELA // 2 - 75
            elif self.estado == 'selecionar_p2':
                x_final = 150 + i * 140
                y_final = ALTURA_TELA // 2 + 50
            else:
                x_final = 150 + i * 140
                y_final = ALTURA_TELA // 2 - 75
            carta.x_final = x_final
            carta.y_final = y_final
            carta.progresso_animacao = 0.0
            carta.animacao_ativa = True
            self.cartas_selecionaveis.append((carta, (valor, naipe)))
        self.inicio_animacao_selecao = 0

    def _redefinir_antes_menu(self):
        self.gerenciador_jogo.modo_jogo = None
        self.hud.modo_edicao = False
        self.gerenciador_jogo.mudar_cena('menu')

    def tratar_evento(self, evento):
        if self.estado == 'jogando':
            print(
                f"[DEBUG] carta_sequencia_atual: {self.carta_sequencia_atual is not None}")
        if self.estado == 'jogando' and evento.type == pygame.KEYDOWN:
            print(
                f"[DEBUG] modo={self.modo}, turno={self.turno}, tecla={evento.key}")
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F1:
            self.hud.alternar_modo_edicao()
            return
        if not self.hud.modo_edicao and evento.type == pygame.MOUSEBUTTONDOWN:
            btn_x = self.hud.configuracao["global"]["btn_menu_x"]
            btn_y = self.hud.configuracao["global"]["btn_menu_y"]
            if pygame.Rect(btn_x, btn_y, 80, 30).collidepoint(evento.pos):
                self._redefinir_antes_menu()
                return
        if self.hud.modo_edicao:
            info_posicoes = {"btn_menu": [
                self.hud.configuracao["global"]["btn_menu_x"], self.hud.configuracao["global"]["btn_menu_y"]]}
            if self.modo == "simples" and self.estado == "jogando":
                info_posicoes.update({
                    "pontuacao": self.hud.configuracao["simples"]["pontuacao"],
                    "timer": self.hud.configuracao["simples"]["timer"],
                    "rotulo_alvo": self.hud.configuracao["simples"]["rotulo_alvo"],
                })
                if self.objeto_alvo_carta:
                    info_posicoes["carta_alvo"] = [
                        self.objeto_alvo_carta.x + 50, self.objeto_alvo_carta.y + 75]
                if self.carta_sequencia_atual:
                    info_posicoes["carta_sequencia"] = [
                        self.carta_sequencia_atual.x + 50, self.carta_sequencia_atual.y + 75]
            elif self.modo == "multi" and self.estado == "jogando":
                info_posicoes.update({
                    "rotulo_p1": self.hud.configuracao["multi"]["rotulo_p1"],
                    "pontuacao_p1": self.hud.configuracao["multi"]["pontuacao_p1"],
                    "timer_p1": self.hud.configuracao["multi"]["timer_p1"],
                    "rotulo_p2": self.hud.configuracao["multi"]["rotulo_p2"],
                    "pontuacao_p2": self.hud.configuracao["multi"]["pontuacao_p2"],
                    "timer_p2": self.hud.configuracao["multi"]["timer_p2"],
                })
                if self.objeto_alvo_carta_p1:
                    info_posicoes["carta_alvo_p1"] = [
                        self.objeto_alvo_carta_p1.x + 50, self.objeto_alvo_carta_p1.y + 75]
                if self.objeto_alvo_carta_p2:
                    info_posicoes["carta_alvo_p2"] = [
                        self.objeto_alvo_carta_p2.x + 50, self.objeto_alvo_carta_p2.y + 75]
                if self.carta_sequencia_atual:
                    info_posicoes["carta_sequencia"] = [
                        self.carta_sequencia_atual.x + 50, self.carta_sequencia_atual.y + 75]
            self.hud.tratar_evento(evento, info_posicoes)
            return
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self._redefinir_antes_menu()
            return
        if self.estado == 'jogando' and evento.type == pygame.KEYDOWN:
            tecla_valida = False
            if self.modo == 'simples':
                tecla_valida = (evento.key == CONTROLES['simples'])
            else:
                if self.turno == 'jogador1':
                    tecla_valida = (evento.key == CONTROLES['jogador1'])
                else:
                    tecla_valida = (evento.key == CONTROLES['jogador2'])
            if tecla_valida and self.carta_sequencia_atual:
                if self.modo == 'simples':
                    acertou = (self.carta_sequencia_atual.valor ==
                               self.alvo_carta[0] and self.carta_sequencia_atual.naipe == self.alvo_carta[1])
                else:
                    if self.turno == 'jogador1':
                        acertou = (self.carta_sequencia_atual.valor ==
                                   self.alvo_carta_p1[0] and self.carta_sequencia_atual.naipe == self.alvo_carta_p1[1])
                        print(
                            f"[DEBUG] J1 - sequencia=({self.carta_sequencia_atual.valor}, {self.carta_sequencia_atual.naipe}) vs alvo=({self.alvo_carta_p1[0]}, {self.alvo_carta_p1[1]})")
                    else:
                        acertou = (self.carta_sequencia_atual.valor ==
                                   self.alvo_carta_p2[0] and self.carta_sequencia_atual.naipe == self.alvo_carta_p2[1])
                        print(
                            f"[DEBUG] J2 - sequencia=({self.carta_sequencia_atual.valor}, {self.carta_sequencia_atual.naipe}) vs alvo=({self.alvo_carta_p2[0]}, {self.alvo_carta_p2[1]})")
                tempo_reacao = (pygame.time.get_ticks() -
                                self.inicio_turno) / 1000.0
                print(
                    f"[DEBUG] Acao valida! acertou={acertou}, tempo={tempo_reacao:.2f}s")
                self._processar_resultado(acertou, tempo_reacao)
            else:
                print(
                    f"[DEBUG] Tecla ignorada - valida: {tecla_valida}, carta existe: {self.carta_sequencia_atual is not None}")
        if self.modo == 'multi':
            if self.estado == 'selecionar_p1' and evento.type == pygame.MOUSEBUTTONDOWN:
                for carta, dados_carta in self.cartas_selecionaveis:
                    if carta.obter_retangulo().collidepoint(evento.pos) and not carta.esta_face_para_cima():
                        if SFX.get('clique'):
                            SFX['clique'].play()
                        x_alvo = 150
                        y_alvo = ALTURA_TELA - 200
                        carta.iniciar_virar_e_mover(x_alvo, y_alvo)
                        self.carta_selecionada = carta
                        self.alvo_carta_p1 = dados_carta
                        self.estado = 'movendo_alvo_p1'
                        break
            elif self.estado == 'selecionar_p2' and evento.type == pygame.MOUSEBUTTONDOWN:
                for carta, dados_carta in self.cartas_selecionaveis:
                    if carta.obter_retangulo().collidepoint(evento.pos) and not carta.esta_face_para_cima():
                        if SFX.get('clique'):
                            SFX['clique'].play()
                        x_alvo = LARGURA_TELA - 250
                        y_alvo = ALTURA_TELA - 200
                        carta.iniciar_virar_e_mover(x_alvo, y_alvo)
                        self.carta_selecionada = carta
                        self.alvo_carta_p2 = dados_carta
                        self.estado = 'movendo_alvo_p2'
                        break
        elif self.estado == 'selecionar_alvo' and evento.type == pygame.MOUSEBUTTONDOWN:
            for carta, dados_carta in self.cartas_selecionaveis:
                if carta.obter_retangulo().collidepoint(evento.pos) and not carta.esta_face_para_cima():
                    if SFX.get('clique'):
                        SFX['clique'].play()
                    x_alvo = LARGURA_TELA // 2 - 50
                    y_alvo = ALTURA_TELA - 200
                    carta.iniciar_virar_e_mover(x_alvo, y_alvo)
                    self.carta_selecionada = carta
                    self.alvo_carta = dados_carta
                    self.estado = 'movendo_alvo_simples'
                    break

    def _processar_resultado(self, acertou, tempo_reacao):
        if self.modo == 'simples':
            if acertou:
                self.pontuacao_p1 = max(0, self.pontuacao_p1 + 1)
                if SFX.get('correto'):
                    SFX['correto'].play()
                self._nova_carta_alvo_apos_pontuacao()
            else:
                self.pontuacao_p1 = max(0, self.pontuacao_p1 - 1)
                if SFX.get('errado'):
                    SFX['errado'].play()
            self.hud.atualizar_simples(
                self.pontuacao_p1, tempo_reacao if acertou else None)
            if self.carta_sequencia_atual:
                self.carta_sequencia_atual.disparar_salto(acertou)
                self.carta_sequencia_atual.congelada = True
                self.carta_sequencia_atual.inicio_congelamento = pygame.time.get_ticks()
                centro_sequencia = (
                    self.carta_sequencia_atual.x + 50, self.carta_sequencia_atual.y + 75)
                self.mao_animada = MaoAnimada('direita', centro_sequencia)
                self.mao_animada.iniciar_animacao(centro_sequencia)
                self.congelar_sequencia = True
                self.inicio_congelamento = pygame.time.get_ticks()
        else:
            if self.turno == 'jogador1':
                self.p1_correto = acertou
                self.p1_tempo = tempo_reacao if acertou else None
                if acertou:
                    if SFX.get('correto'):
                        SFX['correto'].play()
                else:
                    if SFX.get('errado'):
                        SFX['errado'].play()
                if self.carta_sequencia_atual:
                    self.carta_sequencia_atual.disparar_salto(acertou)
                    self.carta_sequencia_atual.congelada = True
                    self.carta_sequencia_atual.inicio_congelamento = pygame.time.get_ticks()
                    centro_sequencia = (
                        self.carta_sequencia_atual.x + 50, self.carta_sequencia_atual.y + 75)
                    self.mao_animada = MaoAnimada('esquerda', centro_sequencia)
                    self.mao_animada.iniciar_animacao(centro_sequencia)
                    self.congelar_sequencia = True
                    self.inicio_congelamento = pygame.time.get_ticks()
            else:
                self.p2_correto = acertou
                self.p2_tempo = tempo_reacao if acertou else None
                if acertou:
                    if SFX.get('correto'):
                        SFX['correto'].play()
                else:
                    if SFX.get('errado'):
                        SFX['errado'].play()
                if self.p1_correto and (not self.p2_correto or self.p1_tempo < self.p2_tempo):
                    self.pontuacao_p1 += 1
                elif self.p2_correto and (not self.p1_correto or self.p2_tempo < self.p1_tempo):
                    self.pontuacao_p2 += 1
                self.hud.atualizar_multi(
                    self.pontuacao_p1, self.pontuacao_p2, self.p1_tempo, self.p2_tempo)
                if self.carta_sequencia_atual:
                    self.carta_sequencia_atual.disparar_salto(acertou)
                    self.carta_sequencia_atual.congelada = True
                    self.carta_sequencia_atual.inicio_congelamento = pygame.time.get_ticks()
                    centro_sequencia = (
                        self.carta_sequencia_atual.x + 50, self.carta_sequencia_atual.y + 75)
                    self.mao_animada = MaoAnimada('direita', centro_sequencia)
                    self.mao_animada.iniciar_animacao(centro_sequencia)
                    self.congelar_sequencia = True
                    self.inicio_congelamento = pygame.time.get_ticks()
                    self._nova_carta_alvo_apos_pontuacao()

    def _iniciar_nova_sequencia(self):
        if self.modo == 'simples':
            if random.random() < PROBABILIDADE_FORCAR_ALVO:
                valor = self.alvo_carta[0]
                naipe = self.alvo_carta[1]
            else:
                valor = random.choice(VALORES_CARTAS)
                naipe = random.choice(NAIPES_CARTAS)
        else:
            if self.turno == 'jogador1':
                carta_alvo = self.alvo_carta_p1
            else:
                carta_alvo = self.alvo_carta_p2
            if random.random() < PROBABILIDADE_FORCAR_ALVO:
                valor = carta_alvo[0]
                naipe = carta_alvo[1]
            else:
                valor = random.choice(VALORES_CARTAS)
                naipe = random.choice(NAIPES_CARTAS)
        naipe = naipe.strip()
        largura_sequencia = self.hud.configuracao["global"]["largura_carta_sequencia"]
        altura_sequencia = self.hud.configuracao["global"]["altura_carta_sequencia"]
        self.carta_sequencia_atual = Carta(
            valor, naipe, tamanho=(largura_sequencia, altura_sequencia))
        if self.modo == "multi":
            x = self.hud.configuracao["multi"]["carta_sequencia_x"]
            y = self.hud.configuracao["multi"]["carta_sequencia_y"]
        else:
            x = self.hud.configuracao["simples"]["carta_sequencia_x"]
            y = self.hud.configuracao["simples"]["carta_sequencia_y"]
        self.carta_sequencia_atual.x = x
        self.carta_sequencia_atual.y = y
        self.ultimo_mudanca_tempo = pygame.time.get_ticks()
        self.inicio_turno = pygame.time.get_ticks()

    def _nova_carta_alvo_apos_pontuacao(self):
        if self.modo == 'simples':
            valor = random.choice(VALORES_CARTAS)
            naipe = random.choice(NAIPES_CARTAS).strip()
            self.alvo_carta = (valor, naipe)
            self.objeto_alvo_carta = Carta(valor, naipe, tamanho=(100, 150))
            self.objeto_alvo_carta.x = LARGURA_TELA // 2 - 50
            self.objeto_alvo_carta.y = ALTURA_TELA - 200
        else:
            valor1 = random.choice(VALORES_CARTAS)
            naipe1 = random.choice(NAIPES_CARTAS).strip()
            self.alvo_carta_p1 = (valor1, naipe1)
            self.objeto_alvo_carta_p1 = Carta(
                valor1, naipe1, tamanho=(100, 150))
            self.objeto_alvo_carta_p1.x = 150
            self.objeto_alvo_carta_p1.y = ALTURA_TELA - 200
            valor2 = random.choice(VALORES_CARTAS)
            naipe2 = random.choice(NAIPES_CARTAS).strip()
            self.alvo_carta_p2 = (valor2, naipe2)
            self.objeto_alvo_carta_p2 = Carta(
                valor2, naipe2, tamanho=(100, 150))
            self.objeto_alvo_carta_p2.x = LARGURA_TELA - 250
            self.objeto_alvo_carta_p2.y = ALTURA_TELA - 200

    def atualizar(self, dt):
        if self.estado in ('selecionar_alvo', 'selecionar_p1', 'selecionar_p2'):
            tempo_atual = pygame.time.get_ticks()
            if self.inicio_animacao_selecao == 0:
                self.inicio_animacao_selecao = tempo_atual
            for i, (carta, _) in enumerate(self.cartas_selecionaveis):
                if carta.animacao_ativa:
                    tempo_inicio_carta = self.inicio_animacao_selecao + \
                        (i * 100)
                    if tempo_atual >= tempo_inicio_carta:
                        decorrido = tempo_atual - tempo_inicio_carta
                        duracao = 300
                        if decorrido >= duracao:
                            carta.x = carta.x_final
                            carta.y = carta.y_final
                            carta.animacao_ativa = False
                        else:
                            t = decorrido / duracao
                            carta.x = self.baralho.x + 40 + \
                                (carta.x_final - (self.baralho.x + 40)) * t
                            carta.y = self.baralho.y + 60 + \
                                (carta.y_final - (self.baralho.y + 60)) * t
        if self.estado == 'movendo_alvo_simples' and self.carta_selecionada:
            self.carta_selecionada.atualizar()
            if self.carta_selecionada.animacao_concluida():
                self.objeto_alvo_carta = self.carta_selecionada
                self.estado = 'jogando'
                self.inicio_turno = pygame.time.get_ticks()
                self._iniciar_nova_sequencia()
        elif self.estado == 'movendo_alvo_p1' and self.carta_selecionada:
            self.carta_selecionada.atualizar()
            if self.carta_selecionada.animacao_concluida():
                self.objeto_alvo_carta_p1 = self.carta_selecionada
                self.estado = 'selecionar_p2'
                self._gerar_cartas_selecionaveis()
        elif self.estado == 'movendo_alvo_p2' and self.carta_selecionada:
            self.carta_selecionada.atualizar()
            if self.carta_selecionada.animacao_concluida():
                self.objeto_alvo_carta_p2 = self.carta_selecionada
                self.estado = 'jogando'
                self.inicio_turno = pygame.time.get_ticks()
                self._iniciar_nova_sequencia()
        if self.modo == 'multi':
            self.mao_esquerda.atualizar()
            self.mao_direita.atualizar()
        else:
            self.mao.atualizar()
        if self.estado == 'jogando':
            if self.modo == 'simples' and self.objeto_alvo_carta:
                self.objeto_alvo_carta.x = self.hud.configuracao["simples"]["carta_alvo_x"]
                self.objeto_alvo_carta.y = self.hud.configuracao["simples"]["carta_alvo_y"]
                self.objeto_alvo_carta.tamanho = (
                    self.hud.configuracao["global"]["largura_carta_alvo"], self.hud.configuracao["global"]["altura_carta_alvo"])
            elif self.modo == 'multi':
                if self.objeto_alvo_carta_p1:
                    self.objeto_alvo_carta_p1.x = self.hud.configuracao["multi"]["carta_alvo_p1_x"]
                    self.objeto_alvo_carta_p1.y = self.hud.configuracao["multi"]["carta_alvo_p1_y"]
                    self.objeto_alvo_carta_p1.tamanho = (
                        self.hud.configuracao["global"]["largura_carta_alvo"], self.hud.configuracao["global"]["altura_carta_alvo"])
                if self.objeto_alvo_carta_p2:
                    self.objeto_alvo_carta_p2.x = self.hud.configuracao["multi"]["carta_alvo_p2_x"]
                    self.objeto_alvo_carta_p2.y = self.hud.configuracao["multi"]["carta_alvo_p2_y"]
                    self.objeto_alvo_carta_p2.tamanho = (
                        self.hud.configuracao["global"]["largura_carta_alvo"], self.hud.configuracao["global"]["altura_carta_alvo"])
        if self.modo == 'multi' and self.estado == 'jogando':
            self.piscar_tempo += dt
            if self.piscar_tempo >= 0.5:
                self.piscar_tempo = 0
                self.piscar_visivel = not self.piscar_visivel
            self.hud.atualizar_turno(self.turno, self.piscar_visivel)
        if self.mao_animada:
            self.mao_animada.atualizar()
            if not self.mao_animada.esta_ativa():
                self.mao_animada = None
        if self.congelar_sequencia:
            if pygame.time.get_ticks() - self.inicio_congelamento > 2000:
                self.congelar_sequencia = False
                if self.modo == 'multi':
                    if self.turno == 'jogador1':
                        self.turno = 'jogador2'
                        self.inicio_turno = pygame.time.get_ticks()
                        self._iniciar_nova_sequencia()
                    elif self.turno == 'jogador2':
                        self.turno = 'jogador1'
                        self._nova_carta_alvo_apos_pontuacao()
                        self.inicio_turno = pygame.time.get_ticks()
                        self._iniciar_nova_sequencia()
        else:
            if self.estado == 'jogando':
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - self.ultimo_mudanca_tempo > self.duracao_exibicao:
                    self._iniciar_nova_sequencia()
                    self.inicio_turno = tempo_atual

    def desenhar(self, tela):
        tela.fill(self.fundo)
        self.baralho.desenhar(tela)
        if self.estado in ('selecionar_alvo', 'selecionar_p1', 'selecionar_p2'):
            if self.modo == 'multi':
                self.mao_esquerda.desenhar(tela)
                self.mao_direita.desenhar(tela)
            else:
                self.mao.desenhar(tela)
            fonte = pygame.font.SysFont(None, 48)
            if self.estado == 'selecionar_p1':
                titulo = fonte.render(
                    "Jogador 1: Escolha sua carta", True, (200, 200, 255))
            elif self.estado == 'selecionar_p2':
                titulo = fonte.render(
                    "Jogador 2: Escolha sua carta", True, (255, 200, 200))
            else:
                titulo = fonte.render(
                    "Escolha sua carta-alvo", True, (255, 255, 255))
            tela.blit(titulo, (LARGURA_TELA // 2 -
                      titulo.get_width() // 2, 80))
            pos_mouse = pygame.mouse.get_pos()
            hover_encontrado = False
            for carta, _ in self.cartas_selecionaveis:
                if carta.obter_retangulo().collidepoint(pos_mouse) and not carta.esta_face_para_cima():
                    hover_encontrado = True
                    break
            for carta, _ in self.cartas_selecionaveis:
                y_original = carta.y
                if hover_encontrado and carta.obter_retangulo().collidepoint(pos_mouse) and not carta.esta_face_para_cima():
                    carta.y -= 20
                carta.desenhar(tela)
                carta.y = y_original
            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND if hover_encontrado else pygame.SYSTEM_CURSOR_ARROW)
            novo_hover = False
            for carta, _ in self.cartas_selecionaveis:
                if carta.obter_retangulo().collidepoint(pos_mouse) and not carta.esta_face_para_cima():
                    novo_hover = True
                    break

            
            if novo_hover and not self._ultimo_hover:
                if SFX.get('hover_carta'):
                    SFX['hover_carta'].play()
            self._ultimo_hover = novo_hover
        elif self.estado in ('movendo_alvo_simples', 'movendo_alvo_p1', 'movendo_alvo_p2') and self.carta_selecionada:
            if self.modo == 'multi':
                self.mao_esquerda.desenhar(tela)
                self.mao_direita.desenhar(tela)
            else:
                self.mao.desenhar(tela)
            self.carta_selecionada.desenhar(tela)
        elif self.estado == 'jogando':
            if self.modo == 'simples' and self.objeto_alvo_carta:
                self.objeto_alvo_carta.desenhar(tela)
            elif self.modo == 'multi':
                if self.objeto_alvo_carta_p1:
                    self.objeto_alvo_carta_p1.desenhar(tela)
                if self.objeto_alvo_carta_p2:
                    self.objeto_alvo_carta_p2.desenhar(tela)
            if self.carta_sequencia_atual:
                self.carta_sequencia_atual.desenhar(tela)
        info_elementos = {}
        if self.modo == "simples" and self.estado == "jogando":
            if self.objeto_alvo_carta:
                info_elementos["carta_alvo"] = [
                    self.objeto_alvo_carta.x + 50, self.objeto_alvo_carta.y + 75]
            if self.carta_sequencia_atual:
                info_elementos["carta_sequencia"] = [
                    self.carta_sequencia_atual.x + 50, self.carta_sequencia_atual.y + 75]
        elif self.modo == "multi" and self.estado == "jogando":
            info_elementos = {}
        self.hud.desenhar(tela, info_elementos if info_elementos else None)
        if self.estado not in ('selecionar_alvo', 'selecionar_p1', 'selecionar_p2'):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self.mao_animada:
            self.mao_animada.desenhar(tela)
