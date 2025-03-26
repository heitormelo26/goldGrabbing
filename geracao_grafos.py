#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx
import random
from plotagem import plot_graph

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

