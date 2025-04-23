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



def plotar_grafo_bipartido(G, conjunto_x, conjunto_y, pesos, title="Grafo Bipartido com Pesos Aleatórios"):
    """Plota um grafo bipartido organizado, com X à esquerda e Y à direita, e exibe os pesos nos vértices."""
    plt.figure(figsize=(8, 6))
    
    pos = {}
    x_offset = -1  # X fica na esquerda
    y_offset = 1   # Y fica na direita
    
    for i, node in enumerate(conjunto_x):
        pos[node] = (x_offset, i - len(conjunto_x) / 2)  # Alinhar verticalmente

    for i, node in enumerate(conjunto_y):
        pos[node] = (y_offset, i - len(conjunto_y) / 2)  # Alinhar verticalmente

    nx.draw(G, pos, node_color="lightblue", node_size=1000, font_size=12)
    
    labels = {node: f"{node}\n({pesos[node]})" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black")

    plt.title(title)
    plt.show()



    
def imprimirArvoreEnraizada(G,pesos):
    """Plota a árvore gerada com hierarquia de altura."""
    pos = {}
    nivel_map = {}  # Dicionário para armazenar a posição dos nós em cada nível

    def definir_posicoes(nodo, x, y, delta_x, nivel_atual):
        if nivel_atual not in nivel_map:
            nivel_map[nivel_atual] = []
        nivel_map[nivel_atual].append(x)
        
        pos[nodo] = (x, -y)
        filhos = list(G.neighbors(nodo))
        
        # Remover o pai da lista de vizinhos (para evitar recursão infinita)
        if nivel_atual > 0:
            filhos = [f for f in filhos if f not in pos]

        num_filhos = len(filhos)
        if num_filhos > 0:
            espacamento = delta_x / num_filhos
            for i, filho in enumerate(filhos):
                definir_posicoes(filho, x + (i - num_filhos // 2) * espacamento, y + 1, delta_x / 2, nivel_atual + 1)

    definir_posicoes("v0", 0, 0, 4, 0)
    labels = {node: f"{node} ({pesos[node]})" for node in G.nodes()}

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True,labels=labels, node_color="lightblue", node_size=1000, font_size=10, edge_color="gray")
    plt.title("Árvore Completa com Hierarquia de Altura")
    plt.show()

def plotar_evolucao_memo(logs_memo, logs_memoKmn):
    """
    Plota a evolução do tamanho do memo ao longo do tempo para dois conjuntos de logs.
    """
    if not logs_memo and not logs_memoKmn:
        print("Nenhum log de memória foi registrado.")
        return

    plt.figure(figsize=(10, 6))

    if logs_memo:
        tempos1, tamanhos1 = zip(*logs_memo)
        plt.plot(tempos1, tamanhos1, marker='o', linestyle='-', label='Memo Padrão', color='blue')
        pico1 = max(logs_memo, key=lambda x: x[1])
        plt.annotate(f'Pico: {pico1[1]} bytes\n({pico1[0]:.2f}s)',
                     xy=pico1, xytext=(pico1[0], pico1[1]*1.1),
                     arrowprops=dict(facecolor='blue', shrink=0.05))

    if logs_memoKmn:
        tempos2, tamanhos2 = zip(*logs_memoKmn)
        plt.plot(tempos2, tamanhos2, marker='s', linestyle='--', label='Memo Otimizado', color='green')
        pico2 = max(logs_memoKmn, key=lambda x: x[1])
        plt.annotate(f'Pico: {pico2[1]} bytes\n({pico2[0]:.2f}s)',
                     xy=pico2, xytext=(pico2[0], pico2[1]*1.1),
                     arrowprops=dict(facecolor='green', shrink=0.05))

    plt.xlabel('Tempo decorrido (s)')
    plt.ylabel('Tamanho do memo (bytes)')
    plt.title('Evolução do uso de memória do memo')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plotar_evolucaoQtdEstados_memo(logs_memo, logs_memoKmn):
    """
    Plota a evolução da quantidade de estados do memo ao longo do tempo para dois conjuntos de logs.
    """
    if not logs_memo and not logs_memoKmn:
        print("Nenhum log de memória foi registrado.")
        return

    plt.figure(figsize=(10, 6))

    if logs_memo:
        tempos1, tamanhos1 = zip(*logs_memo)
        plt.plot(tempos1, tamanhos1, marker='o', linestyle='-', label='Memo Padrão', color='blue')
        pico1 = max(logs_memo, key=lambda x: x[1])
        plt.annotate(f'Pico: {pico1[1]} estados\n({pico1[0]:.2f}s)',
                     xy=pico1, xytext=(pico1[0], pico1[1]*1.1),
                     arrowprops=dict(facecolor='blue', shrink=0.05))

    if logs_memoKmn:
        tempos2, tamanhos2 = zip(*logs_memoKmn)
        plt.plot(tempos2, tamanhos2, marker='s', linestyle='--', label='Memo Otimizado', color='green')
        pico2 = max(logs_memoKmn, key=lambda x: x[1])
        plt.annotate(f'Pico: {pico2[1]} estados\n({pico2[0]:.2f}s)',
                     xy=pico2, xytext=(pico2[0], pico2[1]*1.1),
                     arrowprops=dict(facecolor='green', shrink=0.05))

    plt.xlabel('Tempo decorrido (s)')
    plt.ylabel('Tamanho do memo (un.)')
    plt.title('Evolução do tamanho do memo')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def imprimirArvoreDecisao(arvore_decisao, comDP=True, nome_arquivo="arvore_decisao.png"):
    arvore_plotada, pos, counter = plotarArvoreDeDecisao(arvore_decisao, comDP)
    plt.figure(figsize=(54, 36))  # Tamanho grande, ajuste se necessário
    nx.draw(
        arvore_plotada,
        pos,
        with_labels=True,
        node_color="lightblue",
        width=2,
        font_size=10
    )
    plt.title("Árvore de Decisão Final com Caminhos Hierárquicos")
    
    # Salvar como imagem PNG
    plt.savefig(nome_arquivo, format="png", dpi=300, bbox_inches="tight")
    
    # Opcional: exibe a imagem
    plt.show()
