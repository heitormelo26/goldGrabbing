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
    
def book(n, wa=None, wb=None):
    """
    Gera um grafo Book com n vértices.

    Parâmetros:
        n: número total de vértices (n >= 3)
        wa: peso do centro a (None = aleatório 1-10)
        wb: peso do centro b (None = aleatório 1-10)

    Retorna:
        G: grafo networkx
        weights: dicionário de pesos
    """
    k = n - 2
    G = nx.Graph()
    G.add_edge('a', 'b')
    for i in range(k):
        G.add_edge('a', f'p{i}')
        G.add_edge('b', f'p{i}')
    weights = {v: random.randint(1, 10) for v in G.nodes}
    if wa is not None:
        weights['a'] = wa
    if wb is not None:
        weights['b'] = wb
    plot_graph(G, weights, "Grafo Book")
    return G, weights

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
def gerar_contraexemplo_barbell():
    """
    Gera o contraexemplo B(3) onde a gulosa falha:
    duas K_3 unidas por ponte a1-b1, com pesos que fazem
    a gulosa escolher subotimamente no turno 3.

    val(G) = 5, mas gulosa produz diff = 1 (perda de 4).
    """
    G = nx.Graph()
    edges = [
        ('a1', 'a2'), ('a1', 'a3'), ('a2', 'a3'),  # K_3 do lado A
        ('b1', 'b2'), ('b1', 'b3'), ('b2', 'b3'),  # K_3 do lado B
        ('a1', 'b1')                                # ponte
    ]
    G.add_edges_from(edges)
    pesos = {'a1': 1, 'a2': 2, 'a3': 4, 'b1': 5, 'b2': 3, 'b3': 6}
    plot_graph(G, pesos, "Contraexemplo guloso Barbell")

    return G, pesos

def gerar_grafo_barbell(n1, n2):
    """
    Gera um grafo barbell com duas cliques de tamanhos n1 e n2 unidas por uma aresta-ponte.
    Cliques: a1..a_{n1} e b1..b_{n2}. Ponte: a1-b1.
    """
    G = nx.Graph()
    A = [f"a{i}" for i in range(1, n1 + 1)]
    B = [f"b{i}" for i in range(1, n2 + 1)]

    # K_{n1} sobre A
    for i in range(n1):
        for j in range(i + 1, n1):
            G.add_edge(A[i], A[j])

    # K_{n2} sobre B
    for i in range(n2):
        for j in range(i + 1, n2):
            G.add_edge(B[i], B[j])

    # Garante que vértices isolados (caso n=1) sejam adicionados
    for v in A + B:
        G.add_node(v)

    # Ponte
    G.add_edge(A[0], B[0])

    nos = list(G.nodes())
    random.shuffle(nos)
    pesos = {v: random.randint(1, n1 + n2) for v in nos}
    plot_graph(G, pesos, f"Grafo Barbell ({n1}, {n2}) Ponderado")
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


def p2():
    G = nx.Graph()
    edges = [('p0', 'p1') ]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'p0': 100, 'p1': 150}

    return G,weights

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
    edges = [('c0', 'c1'), ('c1', 'c2'),('c2', 'c3'), ('c0','c3') ]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'c0': 100, 'c1': 1, 'c2': 100,'c3': 150}

    return G,weights

def teste():
    G = nx.Graph()
    edges = [('b', 'a'), ('e', 'a'),('e', 'g'),('e', 'f') ]
    #edges = [('v4', 'v3'), ('v3', 'v2'), ('v2', 'v1')]

    G.add_edges_from(edges)
    weights = {'a': 10, 'e': 11, 'b': 9,'f':1, 'g':1}

    return G,weights

def w5_contraexemplo():
    G = nx.Graph()
    edges = [
        # Hub conectado a todos os vértices do ciclo
        ('h', 'v1'), ('h', 'v2'), ('h', 'v3'), ('h', 'v4'), ('h', 'v5'),
        # Ciclo v1-v2-v3-v4-v5-v1
        ('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4'), ('v4', 'v5'), ('v5', 'v1')
    ]
    G.add_edges_from(edges)
    weights = {'h': 4, 'v1': 1, 'v2': 5, 'v3': 6, 'v4': 2, 'v5': 7}
    return G, weights

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




def fig3_egawa():
    G = nx.Graph()
    # Ciclo C6: v(B) - c1(W) - c2(B) - c3(W) - c4(B) - c5(W)
    edges = [
        ('v', 'c1'), ('c1', 'c2'), ('c2', 'c3'),
        ('c3', 'c4'), ('c4', 'c5'), ('c5', 'v')
    ]
    # c1: P1 (1 pendente)
    edges.append(('c1', 'a1'))
    # c2: P2 (2 pendentes)
    edges += [('c2', 'b1'), ('b1', 'b2')]
    # c3: P4 (4 pendentes — caminho longo no topo)
    edges += [('c3', 'd1'), ('d1', 'd2'), ('d2', 'd3'), ('d3', 'd4')]
    # c4: P2 (2 pendentes)
    edges += [('c4', 'e1'), ('e1', 'e2')]
    # c5: P1 (1 pendente)
    edges.append(('c5', 'f1'))

    G.add_edges_from(edges)
    weights = {v: 0 for v in G.nodes}
    weights['c1'] = 1   # branco peso 1 (esquerda do ciclo)
    weights['c5'] = 1   # branco peso 1 (direita do ciclo)
    weights['d2'] = 1   # branco peso 1 (topo, meio do P4)
    plot_graph(G, weights, "C6-tree Egwa")

    return G, weights


def unir_por_ponte(G1, weights1, G2, weights2, u=None, v=None):
    """
    Une dois grafos G1 e G2 por uma única aresta (ponte).

    Parâmetros:
        G1, G2: grafos networkx
        weights1, weights2: dicionários de pesos {vértice: peso}
        u: vértice de G1 para a ponte (None = aleatório)
        v: vértice de G2 para a ponte (None = aleatório)

    Retorna:
        G3: grafo unido
        weights3: pesos do grafo unido
        (u, v): vértices usados na ponte
    """

    # Verifica se há conflito de nomes
    intersecao = set(G1.nodes()) & set(G2.nodes())

    print(intersecao)
    if intersecao:
        # Só renomeia se houver conflito
        mapping = {node: f"{node}_g2" for node in G2.nodes()}
        G2_renamed = nx.relabel_nodes(G2, mapping)
        weights2_renamed = {mapping[k]: val for k, val in weights2.items()}
    else:
        # Mantém como está
        mapping = {node: node for node in G2.nodes()}
        G2_renamed = G2
        weights2_renamed = weights2.copy()
        
    # Escolher vértices da ponte
    if u is None:
        u = random.choice(list(G1.nodes()))

    if v is None:
        v_original = random.choice(list(G2.nodes()))
        v = mapping[v_original]
    else:
        v = mapping.get(v, v)

    # Construir grafo unido
    G3 = nx.compose(G1, G2_renamed)
    G3.add_edge(u, v)

    # Combinar pesos
    weights3 = {}
    weights3.update(weights1)
    weights3.update(weights2_renamed)
    print(weights1)
    print(weights2_renamed)
    plot_graph(G3, weights3, "Uniao dos grafos")

    return G3, weights3, (u, v)