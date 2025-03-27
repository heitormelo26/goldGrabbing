#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx
import random
from plotagem import *

def gerar_grafo_caminho(n):
    G = nx.path_graph(n)
    nos = list(G.nodes())
    random.shuffle(nos)
    pesos = {v: random.randint(1, n) for v in nos}
    plot_graph(G, pesos, "Grafo Caminho Ponderado")
    return G, pesos

def gerar_grafo_ciclo(n):
    G = nx.cycle_graph(n)
    nos = list(G.nodes())
    random.shuffle(nos)
    pesos = {v: random.randint(1, n) for v in nos}
    plot_graph(G, pesos, "Grafo Ciclo Ponderado")
    return G, pesos

def gerar_grafo_completo(n):
    G = nx.complete_graph(n)
    nos = list(G.nodes())
    random.shuffle(nos)
    pesos = {v: random.randint(1, n) for v in nos}
    plot_graph(G, pesos, "Grafo Completo Ponderado")
    return G, pesos

def criar_grafo_bipartido(m, n):
    """Cria um grafo bipartido com dois conjuntos de vértices de tamanhos m e n."""
    G = nx.Graph()
    conjunto_x = [f"X{i}" for i in range(m)]  # Conjunto X
    conjunto_y = [f"Y{i}" for i in range(n)]  # Conjunto Y
    
    G.add_nodes_from(conjunto_x, bipartite=0)
    G.add_nodes_from(conjunto_y, bipartite=1)
    
    # Adiciona arestas aleatórias entre os conjuntos
    for x in conjunto_x:
        for y in conjunto_y:
            if random.random() > 0.5:  # Probabilidade de conexão
                G.add_edge(x, y)
    
    # Atribui pesos aleatórios aos nós
    pesos = {node: random.randint(1, 10) for node in G.nodes()}
    plotar_grafo_bipartido(G, conjunto_x, conjunto_y,pesos)
    return G, pesos, conjunto_x, conjunto_y


def criar_grafo_bipartido_completo(m, n):
    """Cria um grafo bipartido completo K(m, n) com dois conjuntos de vértices de tamanhos m e n."""
    G = nx.complete_bipartite_graph(m, n)
    
    conjunto_x = [f"X{i}" for i in range(m)]  # Conjunto X
    conjunto_y = [f"Y{i}" for i in range(n)]  # Conjunto Y
    
    mapping = {i: conjunto_x[i] for i in range(m)}
    mapping.update({i + m: conjunto_y[i] for i in range(n)})
    G = nx.relabel_nodes(G, mapping)
    
    # Atribui pesos aleatórios aos nós
    pesos = {node: random.randint(1, 10) for node in G.nodes()}
    plotar_grafo_bipartido(G, conjunto_x, conjunto_y,pesos)

    return G, pesos, conjunto_x, conjunto_y



def grafoSimples():
    G = nx.Graph()
    edges = [('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4')]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'v1': 5, 'v2': 4, 'v3': 1, 'v4': 3}

    return G,weights


def arvoreCompleta(h: int):
    """Gera uma árvore completa de altura h."""
    G = nx.Graph()
    
    if h < 0:
        raise ValueError("A altura da árvore deve ser um número inteiro não negativo.")
    
    def adicionar_nos(G, parent, nivel_atual, max_nivel, contador):
        if nivel_atual > max_nivel:
            return contador
        
        filhos = [f'v{contador + i}' for i in range(2)]  # Cada nó tem dois filhos (árvore binária)
        for filho in filhos:
            G.add_edge(parent, filho)
        
        novo_contador = contador + 2
        for filho in filhos:
            novo_contador = adicionar_nos(G, filho, nivel_atual + 1, max_nivel, novo_contador)
        
        return novo_contador
    
    G.add_node("v0")  # Raiz da árvore
    adicionar_nos(G, "v0", 1, h, 1)
    
    pesos = {node: random.randint(1, 10) for node in G.nodes()}

    imprimirArvoreCompleta(G,pesos)
    return G, pesos