import pygame


def carregar_imagem(caminho, tamanho=None, cor_fallback=None):
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        if tamanho:
            imagem = pygame.transform.scale(imagem, tamanho)
        return imagem
    except (pygame.error, FileNotFoundError):
        w, h = tamanho if tamanho else (100, 100)
        placeholder = pygame.Surface((w, h), pygame.SRCALPHA)
        if cor_fallback:
            placeholder.fill(cor_fallback)
        else:
            placeholder.fill((100, 100, 100))
        pygame.draw.rect(placeholder, (0, 0, 0), (0, 0, w, h), 2)
        return placeholder


def centralizar_retangulo(superficie, x=None, y=None):
    retangulo_tela = pygame.display.get_surface().get_rect()
    retangulo = superficie.get_rect()
    if x is None:
        x = retangulo_tela.centerx - retangulo.width // 2
    if y is None:
        y = retangulo_tela.centery - retangulo.height // 2
    return (x, y)
