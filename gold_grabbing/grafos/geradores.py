"""
Geradores de famílias de grafos ponderados.

Por padrão, cada gerador plota o grafo gerado; use `plotar=False`
para desativar.
"""

import random
from typing import List, Optional, Sequence, Tuple

import networkx as nx

from gold_grabbing.jogo import Pesos
from gold_grabbing.visualizacao import plotar_arvore_enraizada, plotar_grafo, plotar_grafo_bipartido


def _pesos_aleatorios(grafo: nx.Graph, maximo: int) -> Pesos:
    nos = list(grafo.nodes())
    random.shuffle(nos)
    return {v: random.randint(1, maximo) for v in nos}


def gerar_caminho(n: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """Caminho P_n com pesos aleatórios em [1, n]."""
    grafo = nx.path_graph(n)
    pesos = _pesos_aleatorios(grafo, n)
    if plotar:
        plotar_grafo(grafo, pesos, "Grafo Caminho Ponderado")
    return grafo, pesos


def gerar_ciclo(n: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """Ciclo C_n com pesos aleatórios em [1, n]."""
    grafo = nx.cycle_graph(n)
    pesos = _pesos_aleatorios(grafo, n)
    if plotar:
        plotar_grafo(grafo, pesos, "Grafo Ciclo Ponderado")
    return grafo, pesos


def gerar_completo(n: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """Grafo completo K_n com pesos aleatórios em [1, n]."""
    grafo = nx.complete_graph(n)
    pesos = _pesos_aleatorios(grafo, n)
    if plotar:
        plotar_grafo(grafo, pesos, "Grafo Completo Ponderado")
    return grafo, pesos


def gerar_book(n: int, peso_a: Optional[int] = None, peso_b: Optional[int] = None,
               plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """
    Grafo Book com n vértices: dois centros adjacentes `a` e `b` e
    n - 2 páginas `p0, p1, ...`, cada uma ligada aos dois centros.

    Parâmetros:
        n: número total de vértices (n >= 3).
        peso_a, peso_b: pesos dos centros (None = aleatório em [1, 10]).
    """
    grafo = nx.Graph()
    grafo.add_edge('a', 'b')
    for i in range(n - 2):
        grafo.add_edge('a', f'p{i}')
        grafo.add_edge('b', f'p{i}')

    pesos = {v: random.randint(1, 10) for v in grafo.nodes}
    if peso_a is not None:
        pesos['a'] = peso_a
    if peso_b is not None:
        pesos['b'] = peso_b

    if plotar:
        plotar_grafo(grafo, pesos, "Grafo Book")
    return grafo, pesos


def gerar_barbell(n1: int, n2: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """
    Barbell: cliques K_{n1} (a1..a_{n1}) e K_{n2} (b1..b_{n2}) unidas
    pela ponte a1-b1. Pesos aleatórios em [1, n1 + n2].
    """
    grafo = nx.Graph()
    lado_a = [f"a{i}" for i in range(1, n1 + 1)]
    lado_b = [f"b{i}" for i in range(1, n2 + 1)]

    for lado in (lado_a, lado_b):
        for i in range(len(lado)):
            for j in range(i + 1, len(lado)):
                grafo.add_edge(lado[i], lado[j])

    # Garante a presença de cliques com um único vértice.
    grafo.add_nodes_from(lado_a + lado_b)
    grafo.add_edge(lado_a[0], lado_b[0])

    pesos = _pesos_aleatorios(grafo, n1 + n2)
    if plotar:
        plotar_grafo(grafo, pesos, f"Grafo Barbell ({n1}, {n2}) Ponderado")
    return grafo, pesos


def gerar_threshold(papeis: Sequence[str], pesos_sequencia: Sequence[int],
                    plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """
    Grafo threshold construído vértice a vértice.

    Parâmetros:
        papeis: sequência de 'i' (isolado: entra sem arestas) e
                'u' (universal: liga-se a todos os vértices já existentes).
                Exemplo: 'iuui'.
        pesos_sequencia: peso de cada vértice, na mesma ordem.

    Os vértices são nomeados i1, i2, ... e u1, u2, ... conforme o papel.
    """
    if len(papeis) != len(pesos_sequencia):
        raise ValueError("A sequência de papéis e a lista de pesos devem ter o mesmo tamanho.")

    grafo = nx.Graph()
    pesos: Pesos = {}
    contadores = {'i': 1, 'u': 1}

    for papel, peso in zip(papeis, pesos_sequencia):
        papel = papel.lower()
        if papel not in contadores:
            raise ValueError(f"Papel desconhecido '{papel}'. Use apenas 'i' (isolado) ou 'u' (universal).")

        vertice = f"{papel}{contadores[papel]}"
        contadores[papel] += 1

        existentes = list(grafo.nodes())
        grafo.add_node(vertice)
        pesos[vertice] = peso
        if papel == 'u':
            grafo.add_edges_from((vertice, v) for v in existentes)

    if plotar:
        plotar_grafo(grafo, pesos, f"Grafo Threshold ({papeis})")
    return grafo, pesos


def gerar_bipartido(m: int, n: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos, List[str], List[str]]:
    """
    Bipartido conexo aleatório com partes X (m vértices) e Y (n vértices).

    Primeiro garante a conectividade ligando cada vértice a algum vértice
    do outro lado; depois adiciona cada aresta restante com probabilidade 1/2.

    Retorna:
        (grafo, pesos, conjunto_x, conjunto_y)
    """
    grafo = nx.Graph()
    conjunto_x = [f"X{i}" for i in range(m)]
    conjunto_y = [f"Y{i}" for i in range(n)]
    grafo.add_nodes_from(conjunto_x, bipartite=0)
    grafo.add_nodes_from(conjunto_y, bipartite=1)

    grafo.add_edge(random.choice(conjunto_x), random.choice(conjunto_y))
    for x in conjunto_x[1:]:
        grafo.add_edge(x, random.choice(conjunto_y))
    for y in conjunto_y[1:]:
        grafo.add_edge(random.choice(conjunto_x), y)

    for x in conjunto_x:
        for y in conjunto_y:
            if random.random() > 0.5 and not grafo.has_edge(x, y):
                grafo.add_edge(x, y)

    pesos = {v: random.randint(1, 10) for v in grafo.nodes()}
    if plotar:
        plotar_grafo_bipartido(grafo, conjunto_x, conjunto_y, pesos)
    return grafo, pesos, conjunto_x, conjunto_y


def gerar_bipartido_completo(m: int, n: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos, List[str], List[str]]:
    """
    Bipartido completo K(m, n) com vértices X0..X{m-1} e Y0..Y{n-1} e
    pesos aleatórios em [1, 10].

    Retorna:
        (grafo, pesos, conjunto_x, conjunto_y)
    """
    conjunto_x = [f"X{i}" for i in range(m)]
    conjunto_y = [f"Y{i}" for i in range(n)]
    nomes = {i: nome for i, nome in enumerate(conjunto_x + conjunto_y)}
    grafo = nx.relabel_nodes(nx.complete_bipartite_graph(m, n), nomes)

    pesos = {v: random.randint(1, 10) for v in grafo.nodes()}
    if plotar:
        plotar_grafo_bipartido(grafo, conjunto_x, conjunto_y, pesos)
    return grafo, pesos, conjunto_x, conjunto_y


def gerar_arvore_aleatoria(n: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """
    Árvore aleatória com n vértices (n par, n >= 2), enraizada em v0:
    cada novo vértice se liga a um vértice já existente escolhido ao acaso.
    """
    if n % 2 != 0 or n < 2:
        raise ValueError("O número de vértices deve ser um inteiro par >= 2.")

    grafo = nx.Graph()
    grafo.add_node("v0")
    existentes = ["v0"]
    for i in range(1, n):
        novo = f"v{i}"
        grafo.add_edge(novo, random.choice(existentes))
        existentes.append(novo)

    pesos = {v: random.randint(1, 10) for v in grafo.nodes()}
    if plotar:
        plotar_arvore_enraizada(grafo, pesos)
    return grafo, pesos


def gerar_arvore_binaria_completa(altura: int, plotar: bool = True) -> Tuple[nx.Graph, Pesos]:
    """Árvore binária completa de altura `altura`, com raiz v0 e pesos em [1, 10]."""
    if altura < 0:
        raise ValueError("A altura da árvore deve ser um número inteiro não negativo.")

    grafo = nx.Graph()
    grafo.add_node("v0")

    def adicionar_filhos(pai: str, nivel: int, contador: int) -> int:
        if nivel > altura:
            return contador
        filhos = [f'v{contador}', f'v{contador + 1}']
        for filho in filhos:
            grafo.add_edge(pai, filho)
        contador += 2
        for filho in filhos:
            contador = adicionar_filhos(filho, nivel + 1, contador)
        return contador

    adicionar_filhos("v0", 1, 1)

    pesos = {v: random.randint(1, 10) for v in grafo.nodes()}
    if plotar:
        plotar_arvore_enraizada(grafo, pesos)
    return grafo, pesos
