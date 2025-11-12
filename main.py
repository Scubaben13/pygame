import pygame
import sys
from core.gerenciador_jogo import GerenciadorJogo
from config import LARGURA_TELA, ALTURA_TELA, MUSIC, TITULO_JANELA


def main():
    pygame.init()
    pygame.display.set_caption(TITULO_JANELA)
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    gerenciador_jogo = GerenciadorJogo(tela)
    pygame.mixer.init()
    from cenas.cena_jogo import carregar_sons
    carregar_sons()
    if pygame.mixer.get_init() is None:
        print("[ERROR] Mixer não inicializou corretamente!")
    try:
        pygame.mixer.music.load(MUSIC)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except:
        print("Música de fundo não encontrada.")
    try:
        gerenciador_jogo.executar()
    except Exception as e:
        print(f"Erro durante a execucao: {e}")
        pygame.quit()
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
