import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import datetime

def bicoloracaoCaminho(grafo,pesos):
    n = len(grafo)  # Número de vértices no grafo
    colors = [-1] * n  # -1 significa que o nó ainda não foi colorido
    verticesPares = []
    verticesImpares = []
    somaPar = 0
    somaImpar = 0
    for i, v in enumerate(grafo.nodes):
        if i % 2 == 0:
            verticesPares.append(v)
            somaPar += pesos[v]
        else:
            verticesImpares.append(v)
            somaImpar += pesos[v]

    print(f"Pares: {verticesPares}")
    print(f"Impares: {verticesImpares}")
    if somaPar >= somaImpar:
        return verticesPares,somaPar
    else:
        return verticesImpares,somaImpar

def mainBicoloracaoCaminho(grafo,pesos):
    inicio_tempo = time.time()
    caminhoEscolhido,ganho = bicoloracaoCaminho(grafo,pesos)
    fim_tempo = time.time()
    print("\n ======== Bicoloração em Caminho: ==========\n")
    print(f"Sequencia vencedora da Ana: {caminhoEscolhido} : Peso = {ganho} ")
    print("Tempo de execução:", fim_tempo - inicio_tempo, "segundos")