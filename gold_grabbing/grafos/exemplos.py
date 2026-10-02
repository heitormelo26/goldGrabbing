"""
Instâncias fixas e pequenas, usadas para testes manuais e como
contraexemplos para propriedades/estratégias.
"""

from typing import Iterable, Tuple

import networkx as nx

from gold_grabbing.jogo import Pesos
from gold_grabbing.visualizacao import plotar_grafo


def _grafo(arestas: Iterable[Tuple], pesos: Pesos) -> Tuple[nx.Graph, Pesos]:
    grafo = nx.Graph()
    grafo.add_edges_from(arestas)
    return grafo, pesos


# --------------------------------------------------------------------------
# Caminhos
# --------------------------------------------------------------------------

def caminho_p2() -> Tuple[nx.Graph, Pesos]:
    """P2: p0 - p1."""
    return _grafo([('p0', 'p1')], {'p0': 100, 'p1': 150})


def caminho_p3() -> Tuple[nx.Graph, Pesos]:
    """P3: a - b - c."""
    return _grafo([('a', 'b'), ('b', 'c')], {'a': 5, 'b': 4, 'c': 3})


def caminho_p4() -> Tuple[nx.Graph, Pesos]:
    """P4: a - b - c - d."""
    return _grafo([('a', 'b'), ('b', 'c'), ('c', 'd')],
                  {'a': 1, 'b': 3, 'c': 5, 'd': 1})


def caminho_p4_v() -> Tuple[nx.Graph, Pesos]:
    """P4: v1 - v2 - v3 - v4."""
    return _grafo([('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4')],
                  {'v1': 5, 'v2': 4, 'v3': 1, 'v4': 3})


def contraexemplo_preserva_vencedor_p5() -> Tuple[nx.Graph, Pesos]:
    """P5 usado como contraexemplo para a propriedade de preservação do vencedor."""
    return _grafo([('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')],
                  {'a': 1, 'b': 2, 'c': 3, 'd': 1, 'e': 2})


# --------------------------------------------------------------------------
# Ciclos, cliques e rodas
# --------------------------------------------------------------------------

def ciclo_c4() -> Tuple[nx.Graph, Pesos]:
    """C4: c0 - c1 - c2 - c3 - c0."""
    return _grafo([('c0', 'c1'), ('c1', 'c2'), ('c2', 'c3'), ('c0', 'c3')],
                  {'c0': 100, 'c1': 1, 'c2': 100, 'c3': 150})


def completo_k3() -> Tuple[nx.Graph, Pesos]:
    """Triângulo K3."""
    return _grafo([('a', 'b'), ('b', 'c'), ('a', 'c')], {'a': 3, 'b': 5, 'c': 1})


def roda_w3() -> Tuple[nx.Graph, Pesos]:
    """Roda W3 (isomorfa a K4)."""
    return _grafo([('a', 'b'), ('b', 'c'), ('a', 'c'), ('a', 'd'), ('b', 'd'), ('c', 'd')],
                  {'a': 3, 'b': 5, 'c': 1, 'd': 2})


def contraexemplo_roda_w5() -> Tuple[nx.Graph, Pesos]:
    """Roda W5: hub `h` ligado a todos os vértices do ciclo v1..v5."""
    arestas = [('h', f'v{i}') for i in range(1, 6)]
    arestas += [('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4'), ('v4', 'v5'), ('v5', 'v1')]
    return _grafo(arestas, {'h': 4, 'v1': 1, 'v2': 5, 'v3': 6, 'v4': 2, 'v5': 7})


# --------------------------------------------------------------------------
# Árvores
# --------------------------------------------------------------------------

def estrela() -> Tuple[nx.Graph, Pesos]:
    """Estrela com centro b e folhas a, c, d, e."""
    return _grafo([('a', 'b'), ('b', 'c'), ('b', 'd'), ('b', 'e')],
                  {'a': 4, 'b': 15, 'c': 7, 'd': 3, 'e': 6})


def arvore_aranha() -> Tuple[nx.Graph, Pesos]:
    """Árvore com 5 vértices: b - a - e, com e ligado às folhas f e g."""
    return _grafo([('b', 'a'), ('e', 'a'), ('e', 'g'), ('e', 'f')],
                  {'a': 10, 'e': 11, 'b': 9, 'f': 1, 'g': 1})


# --------------------------------------------------------------------------
# Contraexemplos e figuras de artigos
# --------------------------------------------------------------------------

def contraexemplo_guloso_barbell(plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """
    Barbell B(3) em que a estratégia gulosa falha: dois K3 unidos pela
    ponte a1-b1, com pesos que levam a gulosa a errar no turno 3.

    val(G) = 5, mas a gulosa produz diferença 1 (perda de 4).
    """
    arestas = [
        ('a1', 'a2'), ('a1', 'a3'), ('a2', 'a3'),  # K3 do lado A
        ('b1', 'b2'), ('b1', 'b3'), ('b2', 'b3'),  # K3 do lado B
        ('a1', 'b1'),                              # ponte
    ]
    grafo, pesos = _grafo(arestas, {'a1': 1, 'a2': 2, 'a3': 4, 'b1': 5, 'b2': 3, 'b3': 6})
    if plotar:
        plotar_grafo(grafo, pesos, "Contraexemplo guloso Barbell")
    return grafo, pesos


def figura3_egawa(plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """
    C6-tree da Figura 3 de Egawa et al.: ciclo C6 (v, c1, ..., c5) com
    caminhos pendentes de tamanhos 1, 2, 4, 2, 1 em c1..c5. Apenas c1, c5
    e d2 têm peso 1; os demais têm peso 0.
    """
    arestas = [('v', 'c1'), ('c1', 'c2'), ('c2', 'c3'), ('c3', 'c4'), ('c4', 'c5'), ('c5', 'v')]
    arestas += [('c1', 'a1')]                                              # P1 em c1
    arestas += [('c2', 'b1'), ('b1', 'b2')]                                # P2 em c2
    arestas += [('c3', 'd1'), ('d1', 'd2'), ('d2', 'd3'), ('d3', 'd4')]    # P4 em c3
    arestas += [('c4', 'e1'), ('e1', 'e2')]                                # P2 em c4
    arestas += [('c5', 'f1')]                                              # P1 em c5

    grafo = nx.Graph()
    grafo.add_edges_from(arestas)
    pesos = {v: 0 for v in grafo.nodes}
    pesos['c1'] = pesos['c5'] = pesos['d2'] = 1

    if plotar:
        plotar_grafo(grafo, pesos, "C6-tree Egawa")
    return grafo, pesos
