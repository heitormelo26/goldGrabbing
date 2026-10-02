"""
Funções de plotagem: grafos ponderados, árvores de decisão do jogo e
gráficos da evolução da tabela de programação dinâmica.
"""

import os
from typing import Hashable, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import networkx as nx

PASTA_FIGURAS = "figuras"


def _caminho_figura(nome_arquivo: str) -> str:
    os.makedirs(PASTA_FIGURAS, exist_ok=True)
    return os.path.join(PASTA_FIGURAS, nome_arquivo)


# --------------------------------------------------------------------------
# Grafos
# --------------------------------------------------------------------------

def plotar_grafo(grafo: nx.Graph, pesos: dict, titulo: str) -> None:
    """Desenha o grafo com o nome de cada vértice e, logo abaixo, seu peso."""
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_color="lightblue", node_size=1000,
            font_size=10, edge_color="gray")

    rotulos = {v: f"\n\n({pesos[v]})" for v in grafo.nodes()}
    nx.draw_networkx_labels(grafo, pos, rotulos, font_size=10, font_color="black")

    plt.title(titulo)
    plt.show()


def plotar_grafo_bipartido(grafo: nx.Graph, conjunto_x: Sequence, conjunto_y: Sequence,
                           pesos: dict, titulo: str = "Grafo Bipartido com Pesos Aleatórios") -> None:
    """Desenha um bipartido com a parte X à esquerda e a parte Y à direita."""
    plt.figure(figsize=(8, 6))

    pos = {}
    for i, v in enumerate(conjunto_x):
        pos[v] = (-1, i - len(conjunto_x) / 2)
    for i, v in enumerate(conjunto_y):
        pos[v] = (1, i - len(conjunto_y) / 2)

    nx.draw(grafo, pos, node_color="lightblue", node_size=1000, font_size=12)
    rotulos = {v: f"{v}\n({pesos[v]})" for v in grafo.nodes()}
    nx.draw_networkx_labels(grafo, pos, rotulos, font_size=10, font_color="black")

    plt.title(titulo)
    plt.show()


def plotar_arvore_enraizada(grafo: nx.Graph, pesos: dict, raiz: Hashable = "v0") -> None:
    """Desenha uma árvore em níveis, a partir de `raiz`."""
    pos = {}

    def posicionar(vertice, x, y, largura, nivel):
        pos[vertice] = (x, -y)
        filhos = list(grafo.neighbors(vertice))
        if nivel > 0:
            filhos = [f for f in filhos if f not in pos]  # ignora o pai

        if filhos:
            espacamento = largura / len(filhos)
            for i, filho in enumerate(filhos):
                posicionar(filho, x + (i - len(filhos) // 2) * espacamento, y + 1, largura / 2, nivel + 1)

    posicionar(raiz, 0, 0, 4, 0)
    rotulos = {v: f"{v} ({pesos[v]})" for v in grafo.nodes()}

    plt.figure(figsize=(8, 6))
    nx.draw(grafo, pos, with_labels=True, labels=rotulos, node_color="lightblue",
            node_size=1000, font_size=10, edge_color="gray")
    plt.title("Árvore com Hierarquia de Altura")
    plt.show()


# --------------------------------------------------------------------------
# Árvore de decisão do jogo
# --------------------------------------------------------------------------

def montar_arvore_decisao(arvore: List[Tuple], com_dp: bool = True, pai: str = 'G',
                          grafo: Optional[nx.DiGraph] = None, pos: Optional[dict] = None,
                          nivel: int = 0, x: float = 0, largura: float = 1,
                          contador: int = 0) -> Tuple[nx.DiGraph, dict, int]:
    """
    Converte uma árvore de decisão em um DiGraph com posições hierárquicas.

    Parâmetros:
        arvore: lista de tuplas (vertice_escolhido, valor, subarvore), em que
                `subarvore` tem o mesmo formato.
        com_dp: se False, acrescenta um contador ao nome de cada nó para que
                estados repetidos apareçam como nós distintos.

    Retorna:
        (digrafo, posições, contador)
    """
    if grafo is None:
        grafo = nx.DiGraph()
        pos = {pai: (0, 0)}
    if pai == 'G':
        nivel = 1  # a raiz G fica no topo

    if not arvore:
        return grafo, pos, contador

    espacamento = largura / len(arvore)
    x_inicial = x - (largura / 2) + (espacamento / 2)

    for i, (escolha, valor, subarvore) in enumerate(arvore):
        nome = f'{escolha}({valor})' if com_dp else f'{escolha}_{contador} ({valor})'
        contador += 1

        x_filho = x_inicial + i * espacamento
        grafo.add_edge(pai, nome)
        pos[nome] = (x_filho, -nivel)
        grafo, pos, contador = montar_arvore_decisao(subarvore, com_dp, nome, grafo, pos,
                                                     nivel + 1, x_filho, espacamento, contador)

    return grafo, pos, contador


def plotar_arvore_decisao(arvore: List[Tuple], com_dp: bool = True,
                          nome_arquivo: str = "arvore_decisao.png") -> None:
    """Desenha a árvore de decisão (ver `montar_arvore_decisao`) e salva em `figuras/`."""
    digrafo, pos, _ = montar_arvore_decisao(arvore, com_dp)
    plt.figure(figsize=(54, 36))
    nx.draw(digrafo, pos, with_labels=True, node_color="lightblue", width=2, font_size=10)
    plt.title("Árvore de Decisão Final com Caminhos Hierárquicos")
    plt.savefig(_caminho_figura(nome_arquivo), format="png", dpi=300, bbox_inches="tight")
    plt.show()


# --------------------------------------------------------------------------
# Evolução da tabela de programação dinâmica
# --------------------------------------------------------------------------

def plotar_evolucao_bytes(serie_padrao: list, serie_otimizada: list,
                          nome_arquivo: str = "evolucao-tabela-pd-bytes.png") -> None:
    """
    Compara o tamanho em bytes da tabela de PD ao longo do tempo, para a
    PD padrão e a otimizada, e salva a figura em `figuras/`.

    As séries vêm de `metricas.estatisticas.bytes_padrao` e `.bytes_otimizada`.
    """
    if not serie_padrao and not serie_otimizada:
        print("Nenhum log de memória foi registrado.")
        return

    plt.figure(figsize=(12, 8))
    for serie, rotulo, cor in ((serie_padrao, 'PD padrão', 'blue'),
                               (serie_otimizada, 'PD otimizado', 'green')):
        if not serie:
            continue
        tempos, tamanhos = [p[0] for p in serie], [p[1] for p in serie]
        plt.plot(tempos, tamanhos, linestyle='-', label=rotulo, color=cor)
        pico = max(serie, key=lambda p: p[1])
        plt.annotate(f'Pico: {pico[1]} bytes\n({pico[0]:.2f}s)',
                     xy=pico[:2], xytext=(pico[0], pico[1] * 1.1),
                     arrowprops=dict(facecolor=cor, shrink=0.05))

    plt.xlabel('Tempo decorrido (s)')
    plt.ylabel('Tamanho do memo (bytes)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.title("Evolução da Ocupação da Tabela PD (Bytes)")
    plt.savefig(_caminho_figura(nome_arquivo), format="png", dpi=300, bbox_inches="tight")
    plt.show()


def plotar_evolucao_qtd_estados(serie_padrao: list, serie_otimizada: list) -> None:
    """
    Compara a quantidade de estados na tabela de PD ao longo do tempo,
    para a PD padrão e a otimizada.

    As séries vêm de `metricas.estatisticas.qtd_estados_padrao` e
    `.qtd_estados_otimizada`.
    """
    if not serie_padrao and not serie_otimizada:
        print("Nenhum log de memória foi registrado.")
        return

    fig, ax = plt.subplots(figsize=(14, 10))
    for serie, rotulo, cor in ((serie_padrao, 'PD Padrão', 'blue'),
                               (serie_otimizada, 'PD Otimizado', 'green')):
        if not serie:
            continue
        tempos, tamanhos = [p[0] for p in serie], [p[1] for p in serie]
        ax.plot(tempos, tamanhos, linestyle='-', label=rotulo, color=cor)
        pico = max(serie, key=lambda p: p[1])
        texto = f'Pico: {pico[1]} estados\n({pico[0]:.4f}s)'
        if len(pico) > 2:
            texto += f' Estado {pico[2]}'
        ax.annotate(texto, xy=pico[:2], xytext=(pico[0], pico[1] + 5),
                    arrowprops=dict(facecolor=cor, shrink=0.05),
                    fontsize=18, ha='center', va='bottom')

    ax.set_xlabel('Tempo decorrido (s)', fontsize=20)
    ax.set_ylabel('Tamanho tabela PD (un.)', fontsize=20)
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(True)
    ax.legend(fontsize=14)
    plt.tight_layout()
    plt.show()
