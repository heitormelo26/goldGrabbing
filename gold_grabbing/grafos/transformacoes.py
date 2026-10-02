"""
Transformações que constroem um novo grafo ponderado a partir de outro.
"""

import random
from typing import Hashable, List, Optional, Tuple

import networkx as nx

from gold_grabbing.jogo import Pesos
from gold_grabbing.visualizacao import plotar_grafo


def unir_por_ponte(grafo1: nx.Graph, pesos1: Pesos, grafo2: nx.Graph, pesos2: Pesos,
                   u: Optional[Hashable] = None, v: Optional[Hashable] = None,
                   plotar: bool = True) -> Tuple[nx.Graph, Pesos, Tuple[Hashable, Hashable]]:
    """
    Une dois grafos por uma única aresta (ponte) u-v.

    Se houver vértices com o mesmo nome nos dois grafos, os de `grafo2`
    recebem o sufixo `_g2`.

    Parâmetros:
        u: vértice de grafo1 na ponte (None = aleatório).
        v: vértice de grafo2 na ponte, pelo nome original (None = aleatório).

    Retorna:
        (grafo unido, pesos unidos, (u, v))
    """
    if set(grafo1.nodes()) & set(grafo2.nodes()):
        renomear = {no: f"{no}_g2" for no in grafo2.nodes()}
    else:
        renomear = {no: no for no in grafo2.nodes()}
    grafo2_renomeado = nx.relabel_nodes(grafo2, renomear)
    pesos2_renomeados = {renomear[k]: peso for k, peso in pesos2.items()}

    if u is None:
        u = random.choice(list(grafo1.nodes()))
    if v is None:
        v = renomear[random.choice(list(grafo2.nodes()))]
    else:
        v = renomear.get(v, v)

    grafo = nx.compose(grafo1, grafo2_renomeado)
    grafo.add_edge(u, v)
    pesos = {**pesos1, **pesos2_renomeados}

    if plotar:
        plotar_grafo(grafo, pesos, "União dos grafos")
    return grafo, pesos, (u, v)


def adicionar_pendentes_nulos(grafo: nx.Graph, pesos: Pesos) -> Tuple[nx.Graph, Pesos]:
    """
    Pendura em cada vértice v uma nova folha v' de peso 0.

    Exemplo: {a, b, c} passa a ter também {a', b', c'}, com a' ligado só a a.
    """
    novo_grafo = grafo.copy()
    novos_pesos = dict(pesos)
    for v in list(grafo.nodes()):
        pendente = f"{v}'"
        novo_grafo.add_edge(v, pendente)
        novos_pesos[pendente] = 0
    return novo_grafo, novos_pesos


def subdivisao_losango(grafo: nx.Graph, pesos: Pesos) -> Tuple[nx.Graph, Pesos]:
    """
    Substitui cada aresta (u, v) por um losango:

        u — uv1 — v
        u — uv2 — v

    Os novos vértices uv1 e uv2 recebem o menor peso entre u e v.
    """
    novo_grafo = nx.Graph()
    novos_pesos = dict(pesos)

    for u, v in grafo.edges():
        meio1, meio2 = f"{u}{v}1", f"{u}{v}2"
        novo_grafo.add_edges_from([(u, meio1), (meio1, v), (u, meio2), (meio2, v)])
        novos_pesos[meio1] = novos_pesos[meio2] = min(pesos[u], pesos[v])

    return novo_grafo, novos_pesos


def subdivisao_expansao(grafo: nx.Graph, pesos: Pesos, n: int) -> Tuple[nx.Graph, Pesos]:
    """
    Substitui cada aresta (u, v) por um caminho com `n` vértices
    intermediários de peso 0:

        n = 2:  u — u_v_1 — u_v_2 — v
        n = 3:  u — u_v_1 — u_v_2 — u_v_3 — v

    Com n = 0 o grafo permanece inalterado.
    """
    if n < 0:
        raise ValueError("O número de vértices intermediários deve ser >= 0.")

    novo_grafo = nx.Graph()
    novos_pesos = {v: pesos[v] for v in grafo.nodes()}

    for u, v in grafo.edges():
        intermediarios = [f"{u}_{v}_{i}" for i in range(1, n + 1)]
        caminho = [u] + intermediarios + [v]
        novo_grafo.add_edges_from(zip(caminho, caminho[1:]))
        for m in intermediarios:
            novos_pesos[m] = 0

    return novo_grafo, novos_pesos


def remover_gemeos(grafo: nx.Graph, pesos: Pesos, apenas_mesmo_peso: bool = True) -> Tuple[nx.Graph, Pesos]:
    """
    Reduz cada classe de gêmeos preservando a paridade: mantém 2
    representantes se a classe tiver tamanho par e 3 se for ímpar (ou
    seja, sempre remove um número par de vértices).

    Considera gêmeos verdadeiros e falsos ao mesmo tempo, pela relação
    N(u) \\ {v} == N(v) \\ {u}; assim funciona tanto em conjuntos
    independentes quanto em cliques.

    Parâmetros:
        apenas_mesmo_peso: True  -> só reduz classes em que todos os pesos são iguais.
                           False -> reduz qualquer classe, mantendo os de maior peso.
    """
    novo_grafo = grafo.copy()
    novos_pesos = dict(pesos)

    for classe in _classes_de_gemeos(grafo):
        tamanho = len(classe)
        if tamanho < 2:
            continue
        if apenas_mesmo_peso and len({pesos[v] for v in classe}) != 1:
            continue

        manter = 2 if tamanho % 2 == 0 else 3
        if manter >= tamanho:
            continue

        por_peso = sorted(classe, key=lambda v: pesos[v], reverse=True)
        for v in por_peso[manter:]:
            novo_grafo.remove_node(v)
            novos_pesos.pop(v, None)

    return novo_grafo, novos_pesos


def _classes_de_gemeos(grafo: nx.Graph) -> List[List[Hashable]]:
    """Particiona os vértices pela relação de gêmeos N(u) \\ {v} == N(v) \\ {u}."""
    nao_atribuidos = set(grafo.nodes())
    classes = []
    for v in grafo.nodes():
        if v not in nao_atribuidos:
            continue
        classe = [v]
        nao_atribuidos.discard(v)
        vizinhos_v = set(grafo.neighbors(v))
        for u in list(nao_atribuidos):
            if set(grafo.neighbors(u)) - {v} == vizinhos_v - {u}:
                classe.append(u)
                nao_atribuidos.discard(u)
        classes.append(classe)
    return classes
