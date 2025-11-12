from config import TEMPO_BASE_EXIBICAO, DECREMENTO_TEMPO, TEMPO_MINIMO_EXIBICAO


def obter_tempo_exibicao(pontuacao: int) -> int:
    if pontuacao < 2:
        return TEMPO_BASE_EXIBICAO
    elif pontuacao < 4:
        return TEMPO_BASE_EXIBICAO - 500
    elif pontuacao < 6:
        return TEMPO_BASE_EXIBICAO - 750
    else:
        reducao = 750 + ((pontuacao - 6) // 2) * DECREMENTO_TEMPO
        return max(TEMPO_MINIMO_EXIBICAO, TEMPO_BASE_EXIBICAO - reducao)
