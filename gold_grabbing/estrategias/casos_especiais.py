"""
Estratégias polinomiais baseadas em bicoloração, para caminhos e ciclos.

Caminhos (P_n): os vértices são bicoloridos alternadamente ao longo do
caminho; o primeiro jogador fica com a classe de cor de maior peso.

Ciclos (C_n): o primeiro jogador testa cada vértice como jogada inicial;
o que sobra é um caminho, no qual o adversário passa a ser o primeiro a
jogar e fica com a melhor classe de cor.

Observação: estas estratégias não coincidem sempre com o valor ótimo
calculado por `otima.valor` (principalmente em caminhos com número
ímpar de vértices); compare com a PD para confirmar em cada instância.
"""

from typing import Hashable, List, Tuple

import networkx as nx

from gold_grabbing.jogo import Pesos


def ordenar_caminho(grafo: nx.Graph) -> List[Hashable]:
    """
    Devolve os vértices de um grafo caminho na ordem em que aparecem,
    começando por uma das extremidades.
    """
    if grafo.number_of_nodes() <= 1:
        return list(grafo.nodes)
    extremidade = next(v for v in grafo.nodes if grafo.degree(v) <= 1)
    return list(nx.dfs_preorder_nodes(grafo, extremidade))


def bicoloracao_caminho(grafo: nx.Graph, pesos: Pesos) -> Tuple[List, int, List, int]:
    """
    Divide os vértices de um caminho em duas classes alternadas (posições
    pares e ímpares) e atribui ao primeiro jogador a de maior peso.

    Retorna:
        (vertices_primeiro, ganho_primeiro, vertices_segundo, ganho_segundo)
    """
    ordem = ordenar_caminho(grafo)
    pares, impares = ordem[0::2], ordem[1::2]
    soma_pares = sum(pesos[v] for v in pares)
    soma_impares = sum(pesos[v] for v in impares)

    if soma_pares >= soma_impares:
        return pares, soma_pares, impares, soma_impares
    return impares, soma_impares, pares, soma_pares


def melhor_jogada_ciclo(grafo: nx.Graph, pesos: Pesos) -> Tuple[List[Hashable], int]:
    """
    Escolhe a primeira jogada em um ciclo testando todos os vértices.

    Após remover v, o restante é um caminho em que o adversário joga
    primeiro e pega a classe de cor mais pesada; o primeiro jogador fica
    com v mais a outra classe.

    Retorna:
        (vértices do primeiro jogador começando pela jogada inicial, ganho)
    """
    melhor_escolha = None
    melhor_pontuacao = float('-inf')
    melhores_vertices: List[Hashable] = []

    for v in grafo.nodes:
        caminho = grafo.copy()
        caminho.remove_node(v)
        _, _, vertices_restantes, pontos_restantes = bicoloracao_caminho(caminho, pesos)

        pontuacao = pesos[v] + pontos_restantes
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_escolha = v
            melhores_vertices = vertices_restantes

    return [melhor_escolha] + melhores_vertices, melhor_pontuacao
