import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import datetime
from problemasPolinomiais.bicoloracaoCaminho import *

def estrategia_gulosa_ciclo(grafo, pesos):
    melhor_escolha = None
    melhor_pontuacao = float('-inf')
    melhor_caminho = []
    
    for v in grafo.nodes:
        grafo_reduzido = grafo.copy()
        grafo_reduzido.remove_node(v)
        caminho = list(nx.dfs_preorder_nodes(grafo_reduzido))  # Transformando em caminho
        
        bob_caminho, bob_pontuacao = bicoloracaoCaminho(grafo_reduzido, pesos)
        ana_pontuacao = pesos[v]  # Ana pega apenas este vértice
        
        if ana_pontuacao > melhor_pontuacao:
            melhor_pontuacao = ana_pontuacao
            melhor_escolha = v
            melhor_caminho = bob_caminho
    
    # Ana faz a escolha ótima
    grafo_final = grafo.copy()
    grafo_final.remove_node(melhor_escolha)
    caminhoEscolhido, ganho = bicoloracaoCaminho(grafo_final, pesos)
    ganho += pesos[melhor_escolha]  # Somamos o peso do primeiro vértice escolhido por Ana
    caminhoEscolhido.insert(0, melhor_escolha)  # Ana começa com esse vértice
    
    return caminhoEscolhido, ganho


def mainGulosoBicoloridoCiclo(grafo,pesos):
    inicio_tempo = time.time()
    caminhoEscolhido, ganho = estrategia_gulosa_ciclo(grafo, pesos)
    fim_tempo = time.time()
    print("\n ======== Bicoloração em Caminho: ==========\n")
    print(f"Sequencia vencedora da Ana: {caminhoEscolhido} : Peso = {ganho} ")
    print("Tempo de execução:", fim_tempo - inicio_tempo, "segundos")
