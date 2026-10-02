"""
Estratégia gulosa: a cada turno, remove o vértice viável de maior peso.

Essa mesma regra cobre os casos particulares estudados anteriormente:
  * árvores: os vértices viáveis são exatamente as folhas;
  * grafos completos: todos os vértices são viáveis, então a partida
    equivale a ordenar os pesos e alterná-los entre os jogadores;
  * bipartidos completos K(m, n).

A gulosa não é ótima em geral (ver `exemplos.contraexemplo_guloso_barbell`).
"""

from typing import Hashable, Optional, Tuple

import networkx as nx

from gold_grabbing.estrategias.simulacao import ResultadoPartida, simular_partida
from gold_grabbing.jogo import Pesos, vertices_nao_corte


def escolher_jogada_gulosa(grafo: nx.Graph, pesos: Pesos) -> Tuple[Optional[Hashable], str]:
    """Escolhe o vértice viável de maior peso."""
    candidatos = vertices_nao_corte(grafo)
    if not candidatos:
        return None, ''
    return max(candidatos, key=lambda v: pesos[v]), ''


def jogar_guloso(grafo: nx.Graph, pesos: Pesos, verbose: bool = True) -> ResultadoPartida:
    """
    Simula uma partida com ambos os jogadores usando a estratégia gulosa.

    Retorna:
        (vertices_alice, ganho_alice, vertices_bob, ganho_bob)
    """
    return simular_partida(grafo, pesos, escolher_jogada_gulosa, "Estratégia Gulosa", verbose)
