import datetime
import networkx as nx
from typing import Dict, Tuple
from utils import *


contagem_reuso_dp = []
estados_reusados = {}
estados_na_tabela = set()
estados_timestamps = {}

def limparVariaveisGlobais():
    global contagem_reuso_dp, estados_reusados, estados_na_tabela, estados_timestamps
    contagem_reuso_dp = []
    estados_reusados = {}
    estados_na_tabela = set()
    estados_timestamps = {}


def valor(grafo: nx.Graph, pesos: Dict[int, int], profundidade=0) -> Tuple[int, list, list]:
    if not grafo.nodes:
        return 0, [], []
    melhor_valor = float('-inf')
    melhor_escolha = None
    arvore_decisao = []
    melhor_caminho = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            valor_subgrafo, sub_arvore_decisao, sub_melhor_caminho = valor(grafo_copia, pesos, profundidade + 1)
            valor_atual = pesos[v] - valor_subgrafo
            arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_escolha = v
                melhor_caminho = [v] + sub_melhor_caminho

    return melhor_valor, arvore_decisao, melhor_caminho


def valor_dp(grafo: nx.Graph, pesos: dict, memo=None, profundidade=0, history=()):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        contagem_reuso_dp.append(estado)

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0, 'timestamps': []}

        estados_reusados[estado]['count'] += 1
        estados_reusados[estado]['timestamps'].append(timestamp)

        return memo[estado]

    if not grafo.nodes:
        return 0, [], []

    melhor_valor = float('-inf')
    melhor_caminho = []
    arvore_decisao = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            novo_history = history + (v,)
            valor_subgrafo, sub_arvore_decisao, sub_melhor_caminho = valor_dp(grafo_copia, pesos, memo, profundidade + 1, novo_history)
            valor_atual = pesos[v] - valor_subgrafo

            arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_caminho = [v] + sub_melhor_caminho

            if len(grafo.nodes) > 1:
                memo[estado] = (melhor_valor, arvore_decisao, melhor_caminho)
                estados_na_tabela.add(estado)

    return melhor_valor, arvore_decisao, melhor_caminho







def valor_dp_otimizado_caminho(grafo: nx.Graph, pesos: dict, primeirosVerticesNaoViaveis, memo=None, profundidade=0, history=()):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        contagem_reuso_dp.append(estado)

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0, 'timestamps': []}

        estados_reusados[estado]['count'] += 1
        estados_reusados[estado]['timestamps'].append(timestamp)

        return memo[estado]

    if not grafo.nodes:
        return 0, [], []

    melhor_valor = float('-inf')
    melhor_caminho = []
    arvore_decisao = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            novo_history = history + (v,)
            valor_subgrafo, sub_arvore_decisao, sub_melhor_caminho = valor_dp_otimizado_caminho(grafo_copia, pesos, primeirosVerticesNaoViaveis,memo, profundidade + 1, novo_history)
            valor_atual = pesos[v] - valor_subgrafo

            arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_caminho = [v] + sub_melhor_caminho

            if len(grafo.nodes) > 1:
                eh_sc = eh_subconjunto_caminho(grafo,grafo.nodes,primeirosVerticesNaoViaveis)
                if eh_sc:
                    memo[estado] = (melhor_valor, arvore_decisao, melhor_caminho)
                    estados_na_tabela.add(estado)

    return melhor_valor, arvore_decisao, melhor_caminho






