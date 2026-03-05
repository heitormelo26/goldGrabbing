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
    """Cria um grafo bipartido com dois conjuntos de vértices de tamanhos m e n, garantindo que o grafo seja conexo."""
    G = nx.Graph()
    conjunto_x = [f"X{i}" for i in range(m)]  # Conjunto X
    conjunto_y = [f"Y{i}" for i in range(n)]  # Conjunto Y
    
    G.add_nodes_from(conjunto_x, bipartite=0)
    G.add_nodes_from(conjunto_y, bipartite=1)
    
    # Garantir conectividade: Conectando todos os vértices de X e Y
    # Passo 1: Conectando aleatoriamente um vértice de X com um vértice de Y
    x_random = random.choice(conjunto_x)
    y_random = random.choice(conjunto_y)
    G.add_edge(x_random, y_random)
    
    # Passo 2: Criando uma árvore para garantir que todos os vértices sejam alcançáveis
    for i in range(1, m):
        x = conjunto_x[i]
        y = random.choice(conjunto_y)  # Conectar a um vértice de Y aleatoriamente
        G.add_edge(x, y)
    
    for i in range(1, n):
        y = conjunto_y[i]
        x = random.choice(conjunto_x)  # Conectar a um vértice de X aleatoriamente
        G.add_edge(x, y)
    
    # Passo 3: Adicionando arestas aleatórias entre os conjuntos para aumentar a complexidade
    for x in conjunto_x:
        for y in conjunto_y:
            if random.random() > 0.5 and not G.has_edge(x, y):  # Evita arestas duplicadas
                G.add_edge(x, y)
    
    # Atribui pesos aleatórios aos nós
    pesos = {node: random.randint(1, 10) for node in G.nodes()}
    
    # Função para visualizar o grafo (ajuste conforme sua necessidade)
    plotar_grafo_bipartido(G, conjunto_x, conjunto_y, pesos)
    
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
    #edges = [('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4'),('v4', 'v5'),('v5', 'v6')]
    edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'v1': 5, 'v2':4, 'v3': 1, 'v4': 3}

    return G,weights

def gerar_arvore_par(n):
    """Gera uma árvore aleatória com n vértices (n deve ser par)."""
    if n % 2 != 0 or n < 2:
        raise ValueError("O número de vértices deve ser um inteiro par >= 2.")
    
    G = nx.Graph()
    G.add_node("v0")
    nos_existentes = ["v0"]

    for i in range(1, n):
        novo_no = f"v{i}"
        no_conectado = random.choice(nos_existentes)
        G.add_edge(novo_no, no_conectado)
        nos_existentes.append(novo_no)

    pesos = {node: random.randint(1, 10) for node in G.nodes()}
    imprimirArvoreEnraizada(G, pesos)
    return G, pesos


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

    imprimirArvoreEnraizada(G,pesos)
    return G, pesos



def grafoSimples():
    G = nx.Graph()
    edges = [('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4')]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'v1': 5, 'v2': 4, 'v3': 1, 'v4': 3}

    return G,weights

def p4():
    G = nx.Graph()
    edges = [('a', 'b'), ('b', 'c'),('c', 'd')]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 1, 'b': 3, 'c': 5, 'd':1}

    return G,weights

def p5_Contraexemplo_PreservaVencedor():
    G = nx.Graph()
    edges = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]
    G.add_edges_from(edges)
    weights = {'a': 1, 'b': 2, 'c': 3, 'd': 1, 'e': 2}
    return G, weights

def p3():
    G = nx.Graph()
    edges = [('a', 'b'), ('b', 'c')]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 5, 'b': 4, 'c': 3}

    return G,weights

def estrela():
    G = nx.Graph()
    edges = [('a', 'b'), ('b', 'c'), ('b', 'd'), ('b', 'e')]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 4, 'b': 15, 'c': 7,'d': 3,'e':6}

    return G,weights

def c4():
    G = nx.Graph()
    edges = [('a', 'b'), ('b', 'c'),('c', 'd'), ('a','d') ]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 3, 'b': 5, 'c': 1,'d': 4}

    return G,weights

def teste():
    G = nx.Graph()
    edges = [('b', 'a'), ('e', 'a'),('e', 'g'),('e', 'f') ]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 10, 'e': 11, 'b': 9,'f':1, 'g':1}

    return G,weights

def w3():
    G = nx.Graph()
    edges = [('a', 'b'), ('b', 'c'),('a', 'c'),('a', 'd'), ('b', 'd'),('c', 'd') ]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 3, 'b': 5, 'c': 1,'d':2}

    return G,weights

def k3():
    G = nx.Graph()
    edges = [('a', 'b'), ('b', 'c'),('a', 'c') ]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 3, 'b': 5, 'c': 1}

    return G,weights


def adicionar_pendentes_nulos(G, weights):
    """
    Dado um grafo G, retorna um novo grafo G' onde cada vértice original
    recebe um vértice pendente (folha) adicional com peso 0.

    Exemplo: se G tem vértices {a, b, c}, G' terá os vértices originais
    mais {a', b', c'}, cada um conectado apenas ao seu vértice original.
    """
    G_novo = G.copy()
    novos_pesos = dict(weights)

    for v in list(G.nodes()):
        pendente = f"{v}'"
        G_novo.add_edge(v, pendente)
        novos_pesos[pendente] = 0

    return G_novo, novos_pesos