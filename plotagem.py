#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import networkx as nx

def plot_graph(G, pesos, title):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1000, font_size=10, edge_color="gray")

    labels = {node: f"\n\n({pesos[node]})" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black")

    plt.title(title)
    plt.show()

def plotarArvoreDeDecisao(tree, comDp = True,parent_name='G', graph=None, pos=None, level=0, x=0, width=1, counter=None):
    """Gera uma árvore de decisão organizada hierarquicamente, com identificadores únicos para nós repetidos."""
    if graph is None:
        graph = nx.DiGraph()
        pos = {parent_name: (0, 0)}  # Posição inicial da raiz
    if counter is None:
        counter = 0  # Inicializa um contador para garantir nós únicos
    
    if parent_name == 'G':
        level = 1  # Faz com que o vértice G seja a raiz
    
    num_children = len(tree)
    if num_children == 0:
        return graph, pos, counter
    
    spacing = width / max(num_children, 1)
    x_offset = x - (width / 2) + (spacing / 2)
    
    for i, (choice, value, subtree) in enumerate(tree):
        # Criando um identificador único para cada nó
        if comDp:
            node_name = f'{choice}({value})'
        else:
            node_name = f'{choice}_{counter} ({value})'
        counter += 1
        
        graph.add_edge(parent_name, node_name)
        pos[node_name] = (x_offset + i * spacing, -level)
        
        # Recursão para os subgrafos
        graph, pos, counter = plotarArvoreDeDecisao(subtree,comDp, node_name, graph, pos, level + 1, x_offset + i * spacing, spacing, counter)
    
    return graph, pos, counter


def imprimirArvoreDecisao(arvore_decisao, comDP=True):
    arvore_plotada, pos, counter = plotarArvoreDeDecisao(arvore_decisao,comDP)
    plt.figure(figsize=(16, 12))
    nx.draw(arvore_plotada, pos, with_labels=True, node_color="lightblue", width=2, font_size=10)
    plt.title("Árvore de Decisão Final com Caminhos Hierárquicos")
    plt.show()

