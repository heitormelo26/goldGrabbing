import time
import networkx as nx

def guloso_kmn(grafo, pesos):
    grafo_copia = grafo.copy()
    visitados_ana = []
    visitados_bob = []
    ganho_ana = 0
    ganho_bob = 0

    jogadores = ["Ana", "Bob"]
    turno = 0  # Ana começa

    while grafo_copia.number_of_nodes() > 0:
        candidatos = sorted(
            grafo_copia.nodes,
            key=lambda v: pesos[v],
            reverse=True
        )

        movimento_feito = False  # Flag para indicar se alguém jogou

        for v in candidatos:
            grafo_temp = grafo_copia.copy()
            grafo_temp.remove_node(v)

            if len(grafo_temp.nodes) == 0 or nx.is_connected(grafo_temp):
                grafo_copia.remove_node(v)
                if jogadores[turno] == "Ana":
                    visitados_ana.append(v)
                    ganho_ana += pesos[v]
                else:
                    visitados_bob.append(v)
                    ganho_bob += pesos[v]
                movimento_feito = True
                break

        if not movimento_feito:
            # Nenhum movimento possível, encerra para evitar loop infinito
            print("Nenhum movimento possível neste turno. Encerrando.")
            break

        turno = 1 - turno  # Alterna entre Ana e Bob

    return visitados_ana, ganho_ana, visitados_bob, ganho_bob


def mainGulosoKmn(grafo, pesos):
    inicio_tempo = time.time()
    caminho_ana, ganho_ana, caminho_bob, ganho_bob = guloso_kmn(grafo, pesos)
    fim_tempo = time.time()

    print("\n ======== Estratégia Gulosa Kmn ==========\n")
    print(f"Ana escolheu: {caminho_ana} -> Ganho total: {ganho_ana}")
    print(f"Bob escolheu: {caminho_bob} -> Ganho total: {ganho_bob}")
    print("Tempo de execução:", fim_tempo - inicio_tempo, "segundos")