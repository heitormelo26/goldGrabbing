"""
Gold Grabbing Game
==================

Jogo de dois jogadores sobre um grafo conexo com pesos nos vértices.
Os jogadores (Alice, que começa, e Bob) se alternam removendo um vértice
por vez e acumulando o peso dele como ouro. A única restrição é que o
grafo restante deve continuar conexo após cada remoção. O objetivo de
cada jogador é terminar com o máximo de ouro possível.

Organização do pacote:

    jogo             Regras básicas: vértices viáveis, placar.
    metricas         Instrumentação das execuções de programação dinâmica.
    visualizacao     Funções de plotagem de grafos e gráficos de análise.
    relatorios       Funções que executam uma estratégia e imprimem o resultado.
    grafos/          Geração, exemplos fixos e transformações de grafos.
    estrategias/     Estratégias de jogo (ótima, PD, gulosa, EGL, casos especiais).
"""
