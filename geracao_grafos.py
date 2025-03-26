{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b1ed9e49-2457-4292-800e-aa0ce3bf3161",
   "metadata": {},
   "outputs": [],
   "source": [
    "import networkx as nx\n",
    "import random\n",
    "from plotagens import plot_graph\n",
    "\n",
    "def gerar_grafo_caminho(n):\n",
    "    G = nx.path_graph(n)\n",
    "    nos = list(G.nodes())\n",
    "    random.shuffle(nos)\n",
    "    pesos = {v: random.randint(1, n) for v in nos}\n",
    "    plot_graph(G, pesos, \"Grafo Caminho Ponderado\")\n",
    "    return G, pesos\n",
    "\n",
    "def gerar_grafo_ciclo(n):\n",
    "    G = nx.cycle_graph(n)\n",
    "    nos = list(G.nodes())\n",
    "    random.shuffle(nos)\n",
    "    pesos = {v: random.randint(1, n) for v in nos}\n",
    "    plot_graph(G, pesos, \"Grafo Ciclo Ponderado\")\n",
    "    return G, pesos\n",
    "\n",
    "def gerar_grafo_completo(n):\n",
    "    G = nx.complete_graph(n)\n",
    "    nos = list(G.nodes())\n",
    "    random.shuffle(nos)\n",
    "    pesos = {v: random.randint(1, n) for v in nos}\n",
    "    plot_graph(G, pesos, \"Grafo Completo Ponderado\")\n",
    "    return G, pesos\n"
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
