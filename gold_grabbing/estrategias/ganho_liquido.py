"""
Estratégia do Ganho Líquido (EGL).

Para cada vértice viável v, define-se:
    U(v)      = vértices viáveis depois da remoção de v
                (o que fica disponível para o adversário);
    Custo(v)  = maior peso em U(v);
    GL(v)     = w(v) - Custo(v).

A jogada escolhida é a de maior GL. Em caso de empate, prioriza-se o
vértice de maior grau (em grafos threshold, os vértices da clique).
"""

from typing import Hashable, List, Optional, Tuple

import networkx as nx

from gold_grabbing.estrategias.simulacao import ResultadoPartida, simular_partida
from gold_grabbing.jogo import Pesos, vertices_nao_corte


def avaliar_ganho_liquido(grafo: nx.Graph, pesos: Pesos) -> Tuple[Optional[Hashable], float, int, List[Hashable]]:
    """
    Avalia todas as jogadas viáveis pelo ganho líquido.

    Retorna:
        (melhor vértice, GL, custo, vértices viáveis para o adversário)
    """
    candidatos = vertices_nao_corte(grafo)
    if not candidatos:
        return None, 0, 0, []

    melhor_v = None
    melhor_gl = float('-inf')
    melhor_custo = 0
    melhor_liberados: List[Hashable] = []

    for v in candidatos:
        grafo_temp = grafo.copy()
        grafo_temp.remove_node(v)
        liberados = vertices_nao_corte(grafo_temp)

        custo = max((pesos[u] for u in liberados), default=0)
        gl = pesos[v] - custo

        desempate = gl == melhor_gl and grafo.degree(v) > grafo.degree(melhor_v)
        if gl > melhor_gl or desempate:
            melhor_v, melhor_gl, melhor_custo, melhor_liberados = v, gl, custo, liberados

    return melhor_v, melhor_gl, melhor_custo, melhor_liberados


def escolher_jogada_egl(grafo: nx.Graph, pesos: Pesos) -> Tuple[Optional[Hashable], str]:
    """Escolhe a jogada de maior ganho líquido."""
    escolha, gl, custo, liberados = avaliar_ganho_liquido(grafo, pesos)
    detalhes = f" | Custo: {custo} | GL: {gl}"
    if liberados:
        detalhes += f"\n  -> Viáveis para o adversário: {sorted(liberados)}"
    return escolha, detalhes


def jogar_egl(grafo: nx.Graph, pesos: Pesos, verbose: bool = True) -> ResultadoPartida:
    """
    Simula uma partida com ambos os jogadores usando a EGL.

    Retorna:
        (vertices_alice, ganho_alice, vertices_bob, ganho_bob)
    """
    return simular_partida(grafo, pesos, escolher_jogada_egl,
                           "Estratégia de Ganho Líquido (EGL)", verbose)
