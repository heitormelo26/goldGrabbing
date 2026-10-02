"""
Simulação de uma partida em que os dois jogadores usam a mesma
estratégia de escolha de jogada (heurística).

Uma estratégia é uma função `escolher(grafo, pesos)` que devolve
`(vertice, detalhes)`, em que `detalhes` é um texto opcional exibido no
modo verboso (ou `(None, '')` se não houver jogada possível).
"""

from typing import Callable, Hashable, List, Optional, Tuple

import networkx as nx

from gold_grabbing.jogo import Pesos, vertices_nao_corte

Estrategia = Callable[[nx.Graph, Pesos], Tuple[Optional[Hashable], str]]
ResultadoPartida = Tuple[List[Hashable], int, List[Hashable], int]

JOGADORES = ("Alice", "Bob")


def simular_partida(grafo: nx.Graph, pesos: Pesos, escolher: Estrategia,
                    titulo: str = "Partida", verbose: bool = True) -> ResultadoPartida:
    """
    Joga uma partida completa com ambos os jogadores usando `escolher`.

    Retorna:
        (vertices_alice, ganho_alice, vertices_bob, ganho_bob)
    """
    grafo = grafo.copy()
    vertices = ([], [])
    ganhos = [0, 0]
    turno = 0  # Alice começa

    if verbose:
        print("=" * 60)
        print(titulo)
        print("=" * 60)
        print(f"Grafo inicial: {sorted(grafo.nodes())}")
        print(f"Pesos: {pesos}\n")

    while grafo.number_of_nodes() > 0:
        escolha, detalhes = escolher(grafo, pesos)
        if escolha is None:
            break

        ganhos[turno] += pesos[escolha]
        vertices[turno].append(escolha)

        if verbose:
            viaveis = vertices_nao_corte(grafo)
            corte = set(grafo.nodes()) - set(viaveis)
            print(f"Turno de {JOGADORES[turno]}:")
            print(f"  Vértices restantes: {sorted(grafo.nodes())}")
            print(f"  Corte (inviáveis):  {sorted(corte) if corte else 'nenhum'}")
            print(f"  Viáveis atuais:     {sorted(viaveis)}")
            print(f"  -> Escolhe '{escolha}' (peso {pesos[escolha]}){detalhes}")
            print(f"  Placar: Alice = {ganhos[0]} | Bob = {ganhos[1]}\n")

        grafo.remove_node(escolha)
        turno = 1 - turno

    if verbose:
        _imprimir_resultado(titulo, vertices, ganhos, pesos)

    return vertices[0], ganhos[0], vertices[1], ganhos[1]


def _imprimir_resultado(titulo, vertices, ganhos, pesos) -> None:
    print("=" * 60)
    print(f"RESULTADO FINAL ({titulo})")
    print("=" * 60)
    for i, nome in enumerate(JOGADORES):
        jogadas = [(v, pesos[v]) for v in vertices[i]]
        print(f"  {nome}: {ganhos[i]}  jogadas: {jogadas}")
    if ganhos[0] > ganhos[1]:
        print("  >>> ALICE VENCE <<<")
    elif ganhos[1] > ganhos[0]:
        print("  >>> BOB VENCE <<<")
    else:
        print("  >>> EMPATE <<<")
    print("=" * 60 + "\n")
