"""
Estratégia ótima por busca exaustiva (minimax), sem memorização.

O valor de um grafo G para o jogador da vez é

    val(G) = max_{v viável} ( w(v) - val(G - v) ),

ou seja, a maior diferença de ouro que o jogador da vez consegue
garantir sobre o adversário quando ambos jogam de forma ótima.
"""

from typing import Hashable, List, Tuple

import networkx as nx

from gold_grabbing.jogo import Pesos, eh_viavel


def valor(grafo: nx.Graph, pesos: Pesos) -> Tuple[int, List[Hashable]]:
    """
    Calcula val(G) testando todas as jogadas viáveis recursivamente.

    Retorna:
        (val(G), sequência ótima de jogadas alternando Alice e Bob)
    """
    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_sequencia: List[Hashable] = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            valor_subgrafo, sub_sequencia = valor(grafo_copia, pesos)
            valor_atual = pesos[v] - valor_subgrafo

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_sequencia = [v] + sub_sequencia

    return melhor_valor, melhor_sequencia


# --------------------------------------------------------------------------
# Redução por classes de vizinhança (falsos gêmeos)
# --------------------------------------------------------------------------

def classes_vizinhanca(grafo: nx.Graph) -> List[List[Hashable]]:
    """
    Agrupa os vértices com vizinhança aberta N(v) idêntica.

    Cada classe é um conjunto de falsos gêmeos.
    """
    grupos = {}
    for v in grafo.nodes:
        chave = frozenset(grafo.neighbors(v))
        grupos.setdefault(chave, []).append(v)
    return list(grupos.values())


def candidatos_por_classe(grafo: nx.Graph, pesos: Pesos) -> List[Hashable]:
    """
    Retorna um representante por classe de vizinhança: o vértice viável
    de maior peso.

    Se algum vértice da classe é viável, todos são (Teorema A); e, entre
    eles, basta considerar o de maior peso (Teorema D).
    """
    candidatos = []
    for classe in classes_vizinhanca(grafo):
        viaveis = [v for v in classe if eh_viavel(grafo, v)]
        if viaveis:
            candidatos.append(max(viaveis, key=lambda v: pesos[v]))
    return candidatos


def valor_classes(grafo: nx.Graph, pesos: Pesos) -> Tuple[int, List[Hashable]]:
    """
    Calcula val(G) como `valor`, mas ramificando apenas nos candidatos
    de cada classe de vizinhança. O resultado é igual ao de `valor`.
    """
    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_sequencia: List[Hashable] = []

    for v in candidatos_por_classe(grafo, pesos):
        grafo_copia = grafo.copy()
        grafo_copia.remove_node(v)
        valor_subgrafo, sub_sequencia = valor_classes(grafo_copia, pesos)
        valor_atual = pesos[v] - valor_subgrafo

        if valor_atual > melhor_valor:
            melhor_valor = valor_atual
            melhor_sequencia = [v] + sub_sequencia

    return melhor_valor, melhor_sequencia
