import networkx as nx
import time
import datetime

def find_non_cut_vertices(G):
    """Retorna os vértices que NÃO são de corte (Viáveis)."""
    if G.number_of_nodes() == 0:
        return []
    cut = set(nx.articulation_points(G))
    non_cut = [v for v in G.nodes() if v not in cut]
    
    if not non_cut:
        # Caso especial: grafo com 1 ou 2 vértices
        if G.number_of_nodes() <= 2:
            return list(G.nodes())
        # Em árvores, folhas não são de corte
        non_cut = [v for v in G.nodes() if G.degree(v) == 1]
    return non_cut


def net_gain_move(G, weights):
    """
    Escolhe o vértice usando a Estratégia do Ganho Líquido (EGL).
    Calcula U(v) e Custo(v) para cada candidato.
    """
    candidates = find_non_cut_vertices(G)
    if not candidates:
        return None, 0, 0, []

    current_valid = set(candidates)
    
    best_v = None
    max_gl = float('-inf')
    best_cost = 0
    best_unlocked = []

    for v in candidates:
        # 1. Simula a remoção de v
        G_temp = G.copy()
        G_temp.remove_node(v)
        
        # 2. Encontra os vértices viáveis APÓS a remoção
        next_valid = set(find_non_cut_vertices(G_temp))
        
        # 3. Conjunto de Desbloqueio U(v): quem é viável agora, mas não era antes?
        #unlocked = next_valid - current_valid
        #Agora ve todos os que são viáveis não apenas os que se tornaram
        #unlocked = current_valid
        unlocked = next_valid
        
        # 4. Custo(v): o maior peso entre os vértices vivaveis
        if unlocked:
            cost = max(weights[u] for u in unlocked)
        else:
            cost = 0
            
        # 5. Ganho Líquido: GL(v) = w(v) - Custo(v)
        gl = weights[v] - cost
        
        # 6. Regra de Decisão e Desempate
        if gl > max_gl:
            max_gl = gl
            best_v = v
            best_cost = cost
            best_unlocked = list(unlocked)
        elif gl == max_gl:
            # Em caso de empate no GL, a teoria manda priorizar vértices da Clique.
            # Como a clique se conecta a muitos vértices, desempatamos pelo MAIOR GRAU.
            if best_v is None or G.degree(v) > G.degree(best_v):
                max_gl = gl
                best_v = v
                best_cost = cost
                best_unlocked = list(unlocked)

    return best_v, max_gl, best_cost, best_unlocked


def abordagemEGL(G, weights, verbose=True):
    """Simula o jogo com ambos os jogadores usando a Estratégia EGL."""
    G = G.copy()
    scores = {1: 0, 2: 0}
    moves = {1: [], 2: []}
    turn = 1  # Jogador 1 começa

    if verbose:
        print("=" * 60)
        print("JOGO: Estratégia de Ganho Líquido (EGL)")
        print("=" * 60)
        print(f"Grafo inicial: {sorted(G.nodes())}")
        print(f"Pesos: {weights}\n")

    while G.number_of_nodes() > 0:
        choice, gl, cost, unlocked = net_gain_move(G, weights)
        
        if choice is None:
            break

        w = weights[choice]
        scores[turn] += w
        moves[turn].append((choice, w))

        if verbose:
            non_cut = find_non_cut_vertices(G)
            cut = set(G.nodes()) - set(non_cut)
            print(f"Turno J{turn}:")
            print(f"  Vértices restantes: {sorted(G.nodes())}")
            print(f"  Corte (Inviáveis):  {sorted(cut) if cut else 'nenhum'}")
            print(f"  Viáveis atuais:     {sorted(non_cut)}")
            print(f"  -> Joga '{choice}' | Peso: {w} | Custo: {cost} | GL: {gl}")
            if unlocked:
                print(f"  -> Desbloqueou para o adversário: {sorted(unlocked)}")
            print(f"  Placar: J1 = {scores[1]} | J2 = {scores[2]}\n")

        G.remove_node(choice)
        turn = 3 - turn  # Alterna entre 1 e 2

    if verbose:
        print("=" * 60)
        print("RESULTADO FINAL (EGL)")
        print("=" * 60)
        print(f"  J1: {scores[1]}  jogadas: {moves[1]}")
        print(f"  J2: {scores[2]}  jogadas: {moves[2]}")
        if scores[1] > scores[2]:
            print("  >>> JOGADOR 1 VENCE <<<")
        elif scores[2] > scores[1]:
            print("  >>> JOGADOR 2 VENCE <<<")
        else:
            print("  >>> EMPATE <<<")
        print("=" * 60 + "\n")

    return scores, moves


def mainEGL(grafo, pesos):
    """Função main acionadora para a abordagem EGL, mantendo o padrão do seu main.py"""
    inicio_tempo = time.time()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    print(f"Iniciou EGL às {timestamp}")
    scores, moves = abordagemEGL(grafo, pesos, verbose=True)
    
    fim_tempo = time.time()
    print("Tempo de execução EGL:", fim_tempo - inicio_tempo, "segundos\n")