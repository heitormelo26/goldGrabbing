import networkx as nx


def find_non_cut_vertices(G):
    """Retorna os vértices que NÃO são de corte."""
    if G.number_of_nodes() == 0:
        return []
    cut = set(nx.articulation_points(G))
    non_cut = [v for v in G.nodes() if v not in cut]
    # Se todos são de corte (ex: árvore com >2 vértices), 
    # as folhas nunca são de corte — mas por segurança:
    if not non_cut:
        # Caso especial: grafo com 1 ou 2 vértices
        if G.number_of_nodes() <= 2:
            return list(G.nodes())
        # Em árvores, folhas não são de corte
        non_cut = [v for v in G.nodes() if G.degree(v) == 1]
    return non_cut


def greedy_move(G, weights):
    """Escolhe o vértice não-corte de maior peso."""
    candidates = find_non_cut_vertices(G)
    if not candidates:
        return None
    return max(candidates, key=lambda v: weights[v])


def abordagemGulosa(G, weights, verbose=True):
    """Simula o jogo com ambos os jogadores usando estratégia gulosa."""
    G = G.copy()
    scores = {1: 0, 2: 0}
    moves = {1: [], 2: []}
    turn = 1  # Jogador 1 começa

    if verbose:
        print("=" * 50)
        print("Estratégia Gulosa")
        print("=" * 50)
        print(f"Grafo inicial: {sorted(G.nodes())}")
        print(f"Pesos: {weights}")
        print()

    while G.number_of_nodes() > 0:
        choice = greedy_move(G, weights)
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
            print(f"  Corte: {sorted(cut) if cut else 'nenhum'}")
            print(f"  Candidatos (não-corte): {sorted(non_cut)}")
            print(f"  -> Escolhe '{choice}' (peso {w})")
            print(f"  Placar: J1={scores[1]}  J2={scores[2]}")
            print()

        G.remove_node(choice)
        turn = 3 - turn  # Alterna entre 1 e 2

    if verbose:
        print("=" * 50)
        print("RESULTADO FINAL")
        print("=" * 50)
        print(f"  J1: {scores[1]}  jogadas: {moves[1]}")
        print(f"  J2: {scores[2]}  jogadas: {moves[2]}")
        if scores[1] > scores[2]:
            print("  >>> JOGADOR 1 VENCE <<<")
        elif scores[2] > scores[1]:
            print("  >>> JOGADOR 2 VENCE <<<")
        else:
            print("  >>> EMPATE <<<")
        print()

    return scores, moves