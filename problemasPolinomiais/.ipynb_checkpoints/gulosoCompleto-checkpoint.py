import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import datetime

def estrategia_gulosa_completo(grafo, pesos):
    vertices = sorted(pesos.keys(), key=lambda v: pesos[v], reverse=True)  # Ordena pelos maiores pesos
    ganho_ana, ganho_bob = 0, 0
    vertices_ana, vertices_bob = [], []
    
    for i, vertice in enumerate(vertices):
        if i % 2 == 0:
            ganho_ana += pesos[vertice]
            vertices_ana.append(vertice)
        else:
            ganho_bob += pesos[vertice]
            vertices_bob.append(vertice)
    
    print("\nEstratégia Gulosa:")
    print("Vértices escolhidos por Ana:", vertices_ana)
    print("Ganho de Ana:", ganho_ana)
    print("Vértices escolhidos por Bob:", vertices_bob)
    print("Ganho de Bob:", ganho_bob)



def mainGulosoCompleto(grafo,pesos):
    inicio_tempo = time.time()
    print("\n ======== GULOSO EM COMPLETO: ==========\n")
    estrategia_gulosa_completo(grafo,pesos)
    fim_tempo = time.time()
    print("Tempo de execução:", fim_tempo - inicio_tempo, "segundos")