# Documentação Técnica - Jogatina

## Estrutura do Projeto

```
jogatina/
├── config.py                 # Configurações centralizadas
├── main.py                   # Ponto de entrada
├── core/                     # Lógica central do jogo
├── entities/                 # Objetos do jogo (cartas, mãos, etc.)
├── scenes/                   # Telas/cenas do jogo
├── ui/                       # Interface do usuário
├── utils/                    # Funções auxiliares
└── assets/                   # Recursos (imagens, sons)
```

---

## Arquivos Principais

### **config.py**
**Descrição**: Arquivo de configuração centralizado com todos os parâmetros personalizáveis.

**Seções**:
- **Diretórios**: Caminhos dos assets e configurações
- **Tela**: Dimensões da janela
- **Cores**: Paleta de cores do jogo
- **Textos**: Títulos e mensagens (facilmente traduzíveis)
- **Controles**: Mapeamento de teclas
- **Tempos**: Durações de animações e timeouts
- **Probabilidades**: Configurações de gameplay
- **Sons e Música**: Caminhos dos arquivos de áudio
- **UI**: Configurações do modo de edição

---

### **main.py**
**Descrição**: Ponto de entrada da aplicação.

**Funções**:
- `main()`: Inicializa Pygame, carrega música e inicia o gerenciador de jogo

---

## Pasta `core`

### **core/gerenciador_jogo.py**
**Classe**: `GerenciadorJogo`

**Descrição**: Gerencia o fluxo entre cenas e o loop principal do jogo.

**Métodos**:
- `__init__(self, tela)`: Inicializa o gerenciador
- `mudar_cena(self, nome_cena, modo=None)`: Troca entre cenas
- `tratar_eventos(self)`: Processa eventos do Pygame
- `atualizar(self, dt)`: Atualiza lógica da cena atual
- `desenhar(self, tela)`: Renderiza a cena atual
- `executar(self)`: Loop principal do jogo

---

### **core/dificuldade.py**
**Funções**:
- `obter_tempo_exibicao(pontuacao)`: Calcula tempo de exibição baseado na pontuação

---

## Pasta `entities`

### **entities/carta.py**
**Classe**: `Carta`

**Descrição**: Representa uma carta de jogo com animações de virar, mover e feedback.

**Métodos**:
- `__init__(self, valor, naipe, face_para_cima, tamanho)`: Inicializa a carta
- `iniciar_virar_e_mover(self, x_alvo, y_alvo)`: Inicia animação de virar e mover
- `animacao_concluida(self)`: Verifica se animações terminaram
- `atualizar(self)`: Atualiza lógica de animações
- `desenhar(self, tela)`: Renderiza a carta
- `disparar_salto(self, sucesso)`: Ativa efeito de feedback visual

---

### **entities/mao.py**
**Classe**: `Mao`

**Descrição**: Representa as mãos que aparecem nas laterais da tela.

**Métodos**:
- `__init__(self, lado, posicao, tamanho)`: Inicializa a mão
- `mover_para_baralho(self, posicao_baralho)`: Anima movimento até o baralho
- `atualizar(self)`: Atualiza posição da mão
- `desenhar(self, tela)`: Renderiza a mão

---

### **entities/mao_animada.py**
**Classe**: `MaoAnimada`

**Descrição**: Representa a mão que aponta para a carta durante o feedback.

**Métodos**:
- `__init__(self, lado, posicao_alvo)`: Inicializa a mão animada
- `iniciar_animacao(self, posicao_alvo)`: Começa a animação
- `atualizar(self)`: Atualiza lógica da animação
- `desenhar(self, tela)`: Renderiza a mão animada

---

### **entities/baralho.py**
**Classe**: `Baralho`

**Descrição**: Representa o baralho no canto superior direito.

**Métodos**:
- `__init__(self, posicao)`: Inicializa o baralho
- `obter_posicao(self)`: Retorna posição central do baralho
- `desenhar(self, tela)`: Renderiza o baralho

---

## Pasta `scenes`

### **scenes/cena_jogo.py**
**Classe**: `CenaJogo`

**Descrição**: Cena principal do jogo com toda a lógica de gameplay.

**Métodos**:
- `__init__(self, gerenciador_jogo)`: Inicializa a cena
- `tratar_evento(self, evento)`: Processa entradas do jogador
- `_processar_resultado(self, acertou, tempo_reacao)`: Lida com resultados
- `atualizar(self, dt)`: Atualiza lógica da cena
- `desenhar(self, tela)`: Renderiza todos os elementos

---

### **scenes/cena_menu.py**
**Classe**: `CenaMenu`

**Descrição**: Tela inicial com opções de jogo.

**Métodos**:
- `tratar_evento(self, evento)`: Navegação por teclado
- `desenhar(self, tela)`: Renderiza o menu

---

### **scenes/cena_instrucoes.py**
**Classe**: `CenaInstrucoes`

**Descrição**: Tela de instruções com contagem regressiva.

**Métodos**:
- `tratar_evento(self, evento)`: Permite pular com teclas de seta
- `atualizar(self, dt)`: Verifica tempo limite
- `desenhar(self, tela)`: Renderiza instruções

---

## Pasta `ui`

### **ui/hud.py**
**Classe**: `HUD`

**Descrição**: Interface do usuário com pontuação, timer e modo de edição.

**Métodos**:
- `__init__(self, modo)`: Inicializa o HUD
- `tratar_evento(self, evento, info_posicoes)`: Lida com modo de edição
- `desenhar(self, tela, info_elementos)`: Renderiza todos os elementos da UI
- `salvar_configuracao(self)`: Salva posições personalizadas

---

## Pasta `utils`

### **utils/funcoes_auxiliares.py**
**Funções**:
- `carregar_imagem(caminho, tamanho, cor_fallback)`: Carrega imagens com fallback
- `centralizar_retangulo(superficie, x, y)`: Calcula posição centralizada

---

## Fluxo do Jogo

1. **Menu** (`CenaMenu`) → Seleção de modo
2. **Instruções** (`CenaInstrucoes`) → Exibição de regras
3. **Jogo** (`CenaJogo`) → 
   - Seleção de carta-alvo com animação do baralho
   - Sequência de cartas com probabilidade ajustada
   - Feedback visual com mão animada e congelamento
   - Sistema de pontuação e turnos (multiplayer)

---

## Personalização

Todo o jogo pode ser personalizado editando apenas **`config.py`**:

- **Textos**: Títulos, instruções, mensagens
- **Tempos**: Duração de animações, timeouts, congelamento
- **Probabilidades**: Frequência da carta-alvo na sequência
- **Controles**: Teclas para cada ação
- **Cores**: Paleta completa do jogo
- **Modo de Edição**: Ativar/desativar no arquivo de configuração

O modo de edição (F1) permite ajustar **posições e tamanhos** de todos os elementos visuais, com configurações salvas automaticamente em `config/hud_config.json`.