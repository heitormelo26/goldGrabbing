"""
Cálculo de val(G) com programação dinâmica (memorização).

O estado da tabela é a tupla dos vértices restantes. Como os subgrafos
são sempre obtidos removendo vértices do grafo original, a ordem dos
vértices na tupla é estável e o mesmo conjunto gera a mesma chave.

Variações:
    valor_dp            PD padrão: guarda todos os estados.
    valor_dp_classes    PD padrão ramificando só por classes de vizinhança.
    valor_dp_bipartido  PD para K(m, n) que descarta estados após o
                        número máximo de reusos esperado.
    valor_dp_caminho    PD que só guarda estados formados por vértices
                        inicialmente inviáveis que formam um caminho, e
                        descarta cada estado após o primeiro reuso.

Parâmetro comum `inicio_tempo`: quando informado (ex.: `time.time()`),
a evolução do tamanho da tabela é registrada em
`metricas.estatisticas` para gerar os gráficos. Quando é `None`, essa
medição (custosa) é omitida.
"""

from typing import Dict, Hashable, Iterable, List, Optional, Tuple

import networkx as nx

from gold_grabbing.estrategias.otima import candidatos_por_classe
from gold_grabbing.jogo import Pesos, eh_viavel
from gold_grabbing.metricas import estatisticas

Resultado = Tuple[int, List[Hashable]]


def valor_dp(grafo: nx.Graph, pesos: Pesos, memo: Optional[dict] = None,
             inicio_tempo: Optional[float] = None, historico: Tuple = ()) -> Resultado:
    """
    PD padrão: considera todas as jogadas viáveis e memoriza todo estado
    com mais de um vértice.

    Retorna:
        (val(G), sequência ótima de jogadas)
    """
    return _valor_dp_generico(grafo, pesos, memo, inicio_tempo, historico,
                              _jogadas_viaveis)


def valor_dp_classes(grafo: nx.Graph, pesos: Pesos, memo: Optional[dict] = None,
                     inicio_tempo: Optional[float] = None, historico: Tuple = ()) -> Resultado:
    """
    PD padrão, mas ramificando apenas no melhor representante de cada
    classe de vizinhança (ver `otima.candidatos_por_classe`).
    """
    return _valor_dp_generico(grafo, pesos, memo, inicio_tempo, historico,
                              candidatos_por_classe)


def _jogadas_viaveis(grafo: nx.Graph, pesos: Pesos) -> List[Hashable]:
    return [v for v in grafo.nodes if eh_viavel(grafo, v)]


def _valor_dp_generico(grafo, pesos, memo, inicio_tempo, historico, gerar_jogadas) -> Resultado:
    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        if inicio_tempo is not None:
            estatisticas.registrar_tabela_padrao(memo, inicio_tempo)
        estatisticas.registrar_reuso(estado, historico)
        return memo[estado]

    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_sequencia: List[Hashable] = []

    for v in gerar_jogadas(grafo, pesos):
        grafo_copia = grafo.copy()
        grafo_copia.remove_node(v)
        valor_subgrafo, sub_sequencia = _valor_dp_generico(
            grafo_copia, pesos, memo, inicio_tempo, historico + (v,), gerar_jogadas
        )
        valor_atual = pesos[v] - valor_subgrafo

        if inicio_tempo is not None:
            estatisticas.registrar_tabela_padrao(memo, inicio_tempo)

        if valor_atual > melhor_valor:
            melhor_valor = valor_atual
            melhor_sequencia = [v] + sub_sequencia

    if len(grafo.nodes) > 1:
        memo[estado] = (melhor_valor, melhor_sequencia)
        estatisticas.estados_na_tabela.add(estado)

    return melhor_valor, melhor_sequencia


# --------------------------------------------------------------------------
# PD otimizada para bipartidos completos K(m, n)
# --------------------------------------------------------------------------

def reusos_por_tamanho_kmn(m: int, n: int) -> Dict[int, int]:
    """
    Número máximo de vezes que um estado de cada tamanho é reutilizado
    na PD sobre K(m, n): um estado com i vértices é reutilizado
    m + n - 1 - i vezes (para 2 <= i <= m + n - 2).
    """
    return {i: m + n - 1 - i for i in range(2, m + n - 1)}


def valor_dp_bipartido(grafo: nx.Graph, pesos: Pesos, m: int, n: int,
                       memo: Optional[dict] = None, inicio_tempo: Optional[float] = None,
                       historico: Tuple = (), reusos_por_tamanho: Optional[Dict[int, int]] = None,
                       verbose: bool = False) -> Resultado:
    """
    PD para K(m, n) que economiza memória: cada entrada da tabela guarda
    quantos reusos ainda restam e é apagada quando esse número chega a zero.

    Parâmetros:
        m, n: tamanhos das partes do bipartido.
        verbose: imprime cada estado descartado da tabela.
    """
    if memo is None:
        memo = {}
    if reusos_por_tamanho is None:
        reusos_por_tamanho = reusos_por_tamanho_kmn(m, n)

    estado = tuple(grafo.nodes)

    if estado in memo:
        if inicio_tempo is not None:
            estatisticas.registrar_tabela_otimizada(memo, inicio_tempo, estado)
        estatisticas.registrar_reuso(estado, historico)

        valor_salvo, sequencia_salva, reusos = memo[estado]
        reusos_restantes = reusos - 1
        memo[estado] = (valor_salvo, sequencia_salva, reusos_restantes)
        if reusos_restantes == 0:
            if verbose:
                print("Estado deletado: ", estado)
            del memo[estado]

        return valor_salvo, sequencia_salva

    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_sequencia: List[Hashable] = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            valor_subgrafo, sub_sequencia = valor_dp_bipartido(
                grafo_copia, pesos, m, n, memo, inicio_tempo, historico + (v,),
                reusos_por_tamanho, verbose
            )
            valor_atual = pesos[v] - valor_subgrafo

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_sequencia = [v] + sub_sequencia

            if inicio_tempo is not None:
                estatisticas.registrar_tabela_otimizada(memo, inicio_tempo, estado)

    # Estados com 1 vértice e o estado inicial (e seus filhos diretos)
    # nunca são reutilizados, então não são guardados.
    if 1 < len(grafo.nodes) < m + n - 1:
        memo[estado] = (melhor_valor, melhor_sequencia, reusos_por_tamanho[len(grafo.nodes)])
        estatisticas.estados_na_tabela.add(estado)

    return melhor_valor, melhor_sequencia


# --------------------------------------------------------------------------
# PD otimizada para caminhos
# --------------------------------------------------------------------------

def forma_caminho_inviavel(grafo: nx.Graph, vertices: Iterable[Hashable],
                           inviaveis_iniciais: Iterable[Hashable]) -> bool:
    """
    Indica se `vertices` (com pelo menos 2 elementos) estão todos entre os
    vértices inicialmente inviáveis e, na ordem dada, formam um caminho em
    `grafo` (cada vértice adjacente ao seguinte).
    """
    sequencia = list(vertices)
    if len(sequencia) < 2:
        return False

    inviaveis = set(inviaveis_iniciais)
    if not all(v in inviaveis for v in sequencia):
        return False

    return all(grafo.has_edge(a, b) for a, b in zip(sequencia, sequencia[1:]))


def valor_dp_caminho(grafo: nx.Graph, pesos: Pesos, inviaveis_iniciais: Iterable[Hashable],
                     memo: Optional[dict] = None, inicio_tempo: Optional[float] = None,
                     historico: Tuple = ()) -> Resultado:
    """
    PD para caminhos P_n que guarda apenas estados formados por vértices
    internos do caminho original (inicialmente inviáveis) e apaga cada
    estado da tabela logo após seu primeiro reuso.

    Parâmetros:
        inviaveis_iniciais: vértices que não podiam ser removidos no grafo
                            inicial (para P_n, os vértices internos).
    """
    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        if inicio_tempo is not None:
            estatisticas.registrar_tabela_otimizada(memo, inicio_tempo)
        estatisticas.registrar_reuso(estado, historico)
        return memo.pop(estado)

    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_sequencia: List[Hashable] = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            valor_subgrafo, sub_sequencia = valor_dp_caminho(
                grafo_copia, pesos, inviaveis_iniciais, memo, inicio_tempo, historico + (v,)
            )
            valor_atual = pesos[v] - valor_subgrafo

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_sequencia = [v] + sub_sequencia

            if inicio_tempo is not None:
                estatisticas.registrar_tabela_otimizada(memo, inicio_tempo)

    if len(grafo.nodes) > 1 and forma_caminho_inviavel(grafo, grafo.nodes, inviaveis_iniciais):
        memo[estado] = (melhor_valor, melhor_sequencia)
        estatisticas.estados_na_tabela.add(estado)

    return melhor_valor, melhor_sequencia
