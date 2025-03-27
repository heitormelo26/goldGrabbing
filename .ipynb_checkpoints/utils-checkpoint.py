import networkx as nx
import itertools




def calcular_ganhos(melhor_caminho, pesos):
    ganho_ana = 0
    ganho_bob = 0
    vertices_ana = []
    vertices_bob = []

    for i, vertice in enumerate(melhor_caminho):
        if i % 2 == 0:
            ganho_ana += pesos[vertice]
            vertices_ana.append(vertice)
        else:
            ganho_bob += pesos[vertice]
            vertices_bob.append(vertice)

    print("\nVértices escolhidos por Ana:", vertices_ana)
    print("Ganho de Ana:", ganho_ana)
    
    print("\nVértices escolhidos por Bob:", vertices_bob)
    print("Ganho de Bob:", ganho_bob)

def eh_viavel(grafo: nx.Graph, v: int) -> bool:
    if len(grafo.nodes) == 1:
        return True

    grafo_copia = grafo.copy()
    grafo_copia.remove_node(v)
    return nx.is_connected(grafo_copia) if grafo_copia.nodes else True

def verticesViaveis(grafo: nx.Graph): 
    verticesViaveis = []
    for v in grafo.nodes:
        grafo_copia = grafo.copy()
        grafo_copia.remove_node(v)
        if nx.is_connected(grafo_copia):
            verticesViaveis.append(v)
    
    return verticesViaveis


## O(n²)
def gerar_subconjuntos_maior_que_1(nos):
    """
    Gera todos os subconjuntos de um conjunto de nós com tamanho maior que 1.
    """
    subconjuntos = []
    
    for tamanho in range(2, len(nos) + 1):
        subconjuntos.extend(itertools.combinations(nos, tamanho))
    
    return subconjuntos

## O(n)
def eh_caminho(G, conjunto):
    """
    Verifica se um conjunto de vértices forma um caminho válido no grafo G.
    """
    caminho = list(conjunto)
    
    for i in range(len(caminho) - 1):
        if not G.has_edge(caminho[i], caminho[i + 1]):
            return False
    return True


def eh_subconjunto(conjuntoPai, conjuntoFilho):
    count = 0
    for sub in conjuntoFilho:
        if sub in conjuntoPai:
            count +=1
    if(count == len(conjuntoFilho)): return True
    return False

def eh_subconjunto_caminho(G, conjunto, conjuntoPai):
    """
    Verifica se um conjunto de vértices contém algum subconjunto que forma um caminho válido no grafo G.
    """

    if len(conjunto) < 2:
        return False  # Um caminho precisa de pelo menos dois nós

    # Gerar todos os subconjuntos de tamanho maior que 1 do conjunto dado
    #subconjuntos = gerar_subconjuntos(conjunto)

    if(eh_subconjunto(conjuntoPai,conjunto)):
        if eh_caminho(G, conjunto):
            return True

    return False
