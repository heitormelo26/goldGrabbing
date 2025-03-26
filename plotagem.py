{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fc6965b6-17f3-4b42-8824-80510d6e112b",
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import networkx as nx\n",
    "\n",
    "def plot_graph(G, pesos, title):\n",
    "    plt.figure(figsize=(8, 6))\n",
    "    pos = nx.spring_layout(G)\n",
    "    nx.draw(G, pos, with_labels=True, node_color=\"lightblue\", node_size=1000, font_size=10, edge_color=\"gray\")\n",
    "\n",
    "    labels = {node: f\"\\n\\n({pesos[node]})\" for node in G.nodes()}\n",
    "    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color=\"black\")\n",
    "\n",
    "    plt.title(title)\n",
    "    plt.show()\n",
    "\n",
    "def plotarArvoreDeDecisao(tree, comDp = True,parent_name='G', graph=None, pos=None, level=0, x=0, width=1, counter=None):\n",
    "    \"\"\"Gera uma árvore de decisão organizada hierarquicamente, com identificadores únicos para nós repetidos.\"\"\"\n",
    "    if graph is None:\n",
    "        graph = nx.DiGraph()\n",
    "        pos = {parent_name: (0, 0)}  # Posição inicial da raiz\n",
    "    if counter is None:\n",
    "        counter = 0  # Inicializa um contador para garantir nós únicos\n",
    "    \n",
    "    if parent_name == 'G':\n",
    "        level = 1  # Faz com que o vértice G seja a raiz\n",
    "    \n",
    "    num_children = len(tree)\n",
    "    if num_children == 0:\n",
    "        return graph, pos, counter\n",
    "    \n",
    "    spacing = width / max(num_children, 1)\n",
    "    x_offset = x - (width / 2) + (spacing / 2)\n",
    "    \n",
    "    for i, (choice, value, subtree) in enumerate(tree):\n",
    "        # Criando um identificador único para cada nó\n",
    "        if comDp:\n",
    "            node_name = f'{choice}({value})'\n",
    "        else:\n",
    "            node_name = f'{choice}_{counter} ({value})'\n",
    "        counter += 1\n",
    "        \n",
    "        graph.add_edge(parent_name, node_name)\n",
    "        pos[node_name] = (x_offset + i * spacing, -level)\n",
    "        \n",
    "        # Recursão para os subgrafos\n",
    "        graph, pos, counter = plotarArvoreDeDecisao(subtree,comDp, node_name, graph, pos, level + 1, x_offset + i * spacing, spacing, counter)\n",
    "    \n",
    "    return graph, pos, counter\n",
    "\n",
    "\n",
    "def imprimirArvoreDecisao(arvore_decisao, comDP=True):\n",
    "    arvore_plotada, pos, counter = plotarArvoreDeDecisao(arvore_decisao,comDP)\n",
    "    plt.figure(figsize=(16, 12))\n",
    "    nx.draw(arvore_plotada, pos, with_labels=True, node_color=\"lightblue\", width=2, font_size=10)\n",
    "    plt.title(\"Árvore de Decisão Final com Caminhos Hierárquicos\")\n",
    "    plt.show()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
