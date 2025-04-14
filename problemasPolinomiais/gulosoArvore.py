import time
import networkx as nx

def guloso_arvore(grafo, pesos):
    grafo_copia = grafo.copy()
    visitados_ana = []
    visitados_bob = []
    ganho_ana = 0
    ganho_bob = 0

    jogadores = ["Ana", "Bob"]
    turno = 0  # Ana começa

    while grafo_copia.number_of_nodes() > 0:
        folhas = [v for v in grafo_copia.nodes if grafo_copia.degree[v] == 1 or grafo_copia.degree[v] == 0]

        if not folhas:
            # Se não há folhas, não pode continuar (caso especial)
            print("Não há folhas restantes. Encerrando.")
            break

        # Escolhe a folha com maior peso
        melhor_folha = max(folhas, key=lambda v: pesos[v])

        # Remove do grafo e adiciona ao jogador atual
        grafo_copia.remove_node(melhor_folha)
        if jogadores[turno] == "Ana":
            visitados_ana.append(melhor_folha)
            ganho_ana += pesos[melhor_folha]
        else:
            visitados_bob.append(melhor_folha)
            ganho_bob += pesos[melhor_folha]

        turno = 1 - turno  # Alterna jogador

    return visitados_ana, ganho_ana, visitados_bob, ganho_bob


def mainGulosoArvore(grafo, pesos):
    inicio_tempo = time.time()
    caminho_ana, ganho_ana, caminho_bob, ganho_bob = guloso_arvore(grafo, pesos)
    fim_tempo = time.time()

    print("\n ======== Estratégia Gulosa para Árvores ==========\n")
    print(f"Ana escolheu: {caminho_ana} -> Ganho total: {ganho_ana}")
    print(f"Bob escolheu: {caminho_bob} -> Ganho total: {ganho_bob}")
    print("Tempo de execução:", fim_tempo - inicio_tempo, "segundos")
