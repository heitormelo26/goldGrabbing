"""
Estratégias para o Gold Grabbing Game.

Exatas (calculam val(G) e uma sequência ótima de jogadas):
    otima                  Busca exaustiva (minimax) e redução por classes.
    programacao_dinamica   Versões memorizadas, incluindo otimizações para
                           K(m, n) e caminhos.

Heurísticas (simulam uma partida com os dois jogadores usando a regra):
    gulosa                 Remove sempre o vértice viável de maior peso.
    ganho_liquido          Estratégia do Ganho Líquido (EGL).
    simulacao              Laço de partida compartilhado pelas heurísticas.
    casos_especiais        Estratégias por bicoloração para caminhos e ciclos.
"""
