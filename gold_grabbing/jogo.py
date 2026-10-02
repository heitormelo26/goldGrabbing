"""
Regras básicas do Gold Grabbing Game.

Um vértice é *viável* (pode ser removido) quando sua remoção mantém o
grafo conexo, ou seja, quando ele não é um vértice de corte
(ponto de articulação).
"""

from typing import Dict, Hashable, List, Sequence, Tuple

import networkx as nx

Pesos = Dict[Hashable, int]


def eh_viavel(grafo: nx.Graph, v: Hashable) -> bool:
    """Indica se `v` pode ser removido sem desconectar o grafo."""
    if len(grafo.nodes) == 1:
        return True

    grafo_copia = grafo.copy()
    grafo_copia.remove_node(v)
    return nx.is_connected(grafo_copia) if grafo_copia.nodes else True


def vertices_viaveis(grafo: nx.Graph) -> List[Hashable]:
    """Lista os vértices cuja remoção mantém o grafo conexo."""
    viaveis = []
    for v in grafo.nodes:
        grafo_copia = grafo.copy()
        grafo_copia.remove_node(v)
        if nx.is_connected(grafo_copia):
            viaveis.append(v)
    return viaveis


def vertices_nao_corte(grafo: nx.Graph) -> List[Hashable]:
    """
    Lista os vértices viáveis usando pontos de articulação (O(n + m)).

    É equivalente a `vertices_viaveis`, porém mais eficiente, pois não
    precisa testar a conectividade para cada vértice separadamente.
    """
    if grafo.number_of_nodes() == 0:
        return []
    corte = set(nx.articulation_points(grafo))
    return [v for v in grafo.nodes() if v not in corte]


def dividir_jogadas(sequencia: Sequence[Hashable], pesos: Pesos) -> Tuple[List, int, List, int]:
    """
    Separa uma sequência de jogadas entre os jogadores.

    As posições pares pertencem a Alice (primeira a jogar) e as ímpares a Bob.

    Retorna:
        (vertices_alice, ganho_alice, vertices_bob, ganho_bob)
    """
    vertices_alice = list(sequencia[0::2])
    vertices_bob = list(sequencia[1::2])
    ganho_alice = sum(pesos[v] for v in vertices_alice)
    ganho_bob = sum(pesos[v] for v in vertices_bob)
    return vertices_alice, ganho_alice, vertices_bob, ganho_bob


def imprimir_ganhos(sequencia: Sequence[Hashable], pesos: Pesos) -> None:
    """Imprime os vértices escolhidos e o ouro acumulado por cada jogador."""
    vertices_alice, ganho_alice, vertices_bob, ganho_bob = dividir_jogadas(sequencia, pesos)

    print("\nVértices escolhidos por Alice:", vertices_alice)
    print("Ganho de Alice:", ganho_alice)

    print("\nVértices escolhidos por Bob:", vertices_bob)
    print("Ganho de Bob:", ganho_bob)
