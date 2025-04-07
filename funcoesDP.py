import networkx as nx
from valG import *

def imprime_estados_reusados():
    print("\nEstados Reutilizados:")
    
    if not estados_reusados:
        print("Nenhum estado foi reutilizado.")
        return
    
    for estado, info in estados_reusados.items():
        print(f"{estado} → reutilizado {info['count']} vezes")
        print(f"Caminho percorrido: {info['historico']}")
        print("  Momentos de reutilização:")
        for  historico in info['historico']:
            print(f" Historico:  {historico}")
        print("  Instantes de reutilização:")
        # for timestamp in info['timestamps']:
        #     print(f"    - {timestamp}")


        
# def imprimirTabelaPd(soTamanho =  True):
#     """Imprime a tabela de programação dinâmica para análise da complexidade."""
#     len(tabela_dp)
#     qtdDeLinhas = 0 
#     print("\n Tabela de Programação Dinâmica:")
#     for estado, (resultados, _) in tabela_dp.items():
#         if(soTamanho == False):
#             print(f"Estado: {estado}")
#         for caminho, ganho_alice, ganho_bob in resultados:
#             qtdDeLinhas = qtdDeLinhas + 1
#             if(soTamanho == False):
#                 print(f"  Caminho: {caminho} → Alice: {ganho_alice}, Bob: {ganho_bob}")

#     print(f"\nTAMANHO DA TABELA: {qtdDeLinhas}" )

def imprime_estados_nao_reutilizados(memo):
    print("\nEstados NÃO reutilizados:")
    estados_nao_reutilizados = []
    
    for estado in memo.keys():
        if estado not in estados_reusados:
            estados_nao_reutilizados.append(estado)
            melhor_valor, melhor_caminho = memo[estado]
            print(f"Estado: {estado}")
            print("-------------------------")
    
    print(f"\nTotal de estados que nunca foram reutilizados: {len(estados_nao_reutilizados)}")



def contar_estados(grafo: nx.Graph) -> int:
    estados_gerados = set()

    def explorar_estados(subgrafo: nx.Graph):
        estado = tuple(subgrafo.nodes)
        if len(estado) > 1 and estado not in estados_gerados:
            estados_gerados.add(estado)

            for v in list(subgrafo.nodes):
                if eh_viavel(subgrafo, v):  # Só remove se for viável
                    novo_grafo = subgrafo.copy()
                    novo_grafo.remove_node(v)
                    explorar_estados(novo_grafo)  # Chamada recursiva para explorar mais estados

    explorar_estados(grafo)
    return len(estados_gerados)



def imprime_tabela_dp(memo):
    print("\nTabela de Programação Dinâmica:")
    for estado, (melhor_valor, melhor_caminho) in memo.items():
        print(f"Estado: {estado}")
        print(f"  Melhor valor: {melhor_valor}")
        print(f"  Melhor caminho: {melhor_caminho}")

        if estado in estados_reusados:
            print(f"  Reutilizado {estados_reusados[estado]['count']} vezes")
            print(f"Caminho percorrido: {estados_reusados[estado]['historico']}")
            print(f"  Instantes de reutilização: {estados_reusados[estado]['timestamps']}")
        else:
            print("  Nunca reutilizado")
        print("-------------------------")