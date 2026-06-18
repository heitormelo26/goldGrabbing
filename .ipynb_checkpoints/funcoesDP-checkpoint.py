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

def classes_vizinhanca(grafo: nx.Graph):
    """Agrupa vértices por vizinhança aberta N(v) idêntica.
       Cada classe é um conjunto de falsos gêmeos."""
    grupos = {}
    for v in grafo.nodes:
        chave = frozenset(grafo.neighbors(v))
        grupos.setdefault(chave, []).append(v)
    return list(grupos.values())


def candidatos_por_classe(grafo: nx.Graph, pesos: dict):
    """Retorna 1 representante por classe: o vértice VIÁVEL de maior peso.
       Por Teorema A, se a classe tem algum viável, todos são viáveis;
       por Teorema D, basta o de maior peso."""
    candidatos = []
    for classe in classes_vizinhanca(grafo):
        viaveis = [v for v in classe if eh_viavel(grafo, v)]
        if viaveis:
            # vértice de peso máximo da classe (um representante)
            melhor = max(viaveis, key=lambda v: pesos[v])
            candidatos.append(melhor)
    return candidatos


def valor_classes(grafo: nx.Graph, pesos: Dict[int, int]) -> Tuple[int, list]:
    """val(G) pela estratégia de classes de vizinhança.
       Análogo a 'valor', mas ramifica só nos candidatos de cada classe.
       Garantidamente igual a valor(grafo, pesos)."""
    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_caminho = []

    for v in candidatos_por_classe(grafo, pesos):   # <-- só candidatos por classe
        grafo_copia = grafo.copy()
        grafo_copia.remove_node(v)
        valor_subgrafo, sub_melhor_caminho = valor_classes(grafo_copia, pesos)
        valor_atual = pesos[v] - valor_subgrafo

        if valor_atual > melhor_valor:
            melhor_valor = valor_atual
            melhor_escolha = v
            melhor_caminho = [v] + sub_melhor_caminho

    return melhor_valor, melhor_caminho

def valor_dp_classes(grafo: nx.Graph, pesos: dict, memo=None, inicio_tempo=0, profundidade=0, history=()):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        registrar_tamanho_memo(memo, inicio_tempo)
        registrar_qtdEstados(memo, inicio_tempo)
        contagem_reuso_dp.append(estado)

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0, 'timestamps': [], 'historico': []}

        estados_reusados[estado]['count'] += 1
        estados_reusados[estado]['timestamps'].append(history)
        estados_reusados[estado]['historico'].append(history)

        return memo[estado]

    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_caminho = []

    # >>> ÚNICA MUDANÇA vs valor_dp: candidatos por classe em vez de todos os viáveis <
    for v in candidatos_por_classe(grafo, pesos):
        grafo_copia = grafo.copy()
        grafo_copia.remove_node(v)
        novo_history = history + (v,)
        valor_subgrafo, sub_melhor_caminho = valor_dp_classes(
            grafo_copia, pesos, memo, inicio_tempo, profundidade + 1, novo_history
        )
        valor_atual = pesos[v] - valor_subgrafo

        registrar_tamanho_memo(memo, inicio_tempo)
        registrar_qtdEstados(memo, inicio_tempo)

        if valor_atual > melhor_valor:
            melhor_valor = valor_atual
            melhor_caminho = [v] + sub_melhor_caminho

        if len(grafo.nodes) > 1:
            memo[estado] = (melhor_valor, melhor_caminho)
            estados_na_tabela.add(estado)

    return melhor_valor, melhor_caminho

        
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