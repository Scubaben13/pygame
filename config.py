import pygame
import os

# Diretórios
DIRETORIO_RAIZ = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_ASSETS = os.path.join(DIRETORIO_RAIZ, 'assets')
CAMINHO_CONFIGURACAO_HUD = os.path.join(
    DIRETORIO_RAIZ, 'config', 'hud_config.json')

# Tela
LARGURA_TELA = 1024
ALTURA_TELA = 768

# Cores
COR_FUNDO = (34, 100, 34)
COR_BRANCA = (255, 255, 255)
COR_PRETA = (0, 0, 0)
COR_CINZA = (200, 200, 200)
COR_VERDE_CLARO = (100, 200, 100)
COR_VERMELHA = (200, 50, 50)
COR_AZUL = (255, 200, 200)
COR_VERMELHO_CLARO = (200, 200, 255)

# Textos
TITULO_JANELA= "Jogatina — Jogo de Atenção"
TITULO_JOGO = "JOGATINA"
OPCOES_MENU = ["Jogo Simples", "Jogo Duplo", "Instruções"]
TEXTO_INSTRUCOES = [
    "COMO JOGAR:",
    "",
    "• Uma carta-alvo será mostrada.",
    "• Observe a sequência de cartas na tela.",
    "• Pressione a tecla correta EXATAMENTE quando sua carta-alvo aparecer.",
    "",
    "MODO SIMPLES:",
    "   - Pressione ENTER para confirmar.",
    "",
    "MODO DUPLA:",
    "   - Jogador 1 (esquerda): pressione ESPAÇO",
    "   - Jogador 2 (direita): pressione ENTER",
    "   - Turnos alternados. Quem for mais rápido e acertar ganha o ponto!",
    "",
    "Dicas:",
    "   - Não há penalidade por não agir.",
    "   - O jogo espera sua ação (até 3 minutos).",
    "",
    "Pressione qualquer SETA para pular esta tela."
]

# Controles
CONTROLES = {
    'simples': pygame.K_RETURN,
    'jogador1': pygame.K_SPACE,
    'jogador2': pygame.K_RETURN
}

# Tempos
TEMPO_BASE_EXIBICAO = 2000  # ms
DECREMENTO_TEMPO = 250      # ms
TEMPO_MINIMO_EXIBICAO = 4   # ms
DURACAO_EXIBICAO = 800      # ms
DURACAO_MAXIMA_INSTRUCOES = 15000  # 15 segundos
TEMPO_CONGELAMENTO = 2000   # 2 segundos
TEMPO_ESPERA_MAXIMA = 180   # 3 minutos em segundos

# Probabilidades
PROBABILIDADE_FORCAR_ALVO = 0.1  # 10%

# Símbolos de naipes
SIMBOLOS_NAIPE = {
    'espadas': '♠',
    'copas': '♥',
    'ouros': '♦',
    'paus': '♣'
}

# Sons
SONS = {
    'virar_carta': 'assets/sons/virar_carta.wav',
    'hover_carta': 'assets/sons/virar_carta.wav',
    'correto': 'assets/sons/correto.wav',
    'errado': 'assets/sons/errado.wav',
    'clique': 'assets/sons/clique.wav'
}

# Música
MUSIC = 'assets/sons/bg_music.mp3'

# UI (Modo Edição)
MODO_EDICAO_ATIVADO = True
