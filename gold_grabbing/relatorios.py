"""
Funções que executam uma estratégia sobre um grafo, medem o tempo e
imprimem um relatório do resultado. São o ponto de entrada usado no
notebook `main.ipynb`.

As execuções de PD reiniciam `metricas.estatisticas` no início, e as
séries de evolução da tabela ficam disponíveis nele depois da execução.
"""

import datetime
import time
from typing import Callable, Hashable, List, Tuple

import networkx as nx
from pympler import asizeof

from gold_grabbing.estrategias.casos_especiais import bicoloracao_caminho, melhor_jogada_ciclo
from gold_grabbing.estrategias.ganho_liquido import jogar_egl
from gold_grabbing.estrategias.gulosa import jogar_guloso
from gold_grabbing.estrategias.otima import valor, valor_classes
from gold_grabbing.estrategias.programacao_dinamica import (valor_dp, valor_dp_bipartido,
                                                            valor_dp_caminho, valor_dp_classes)
from gold_grabbing.jogo import Pesos, imprimir_ganhos, vertices_viaveis
from gold_grabbing.metricas import (contar_estados, estatisticas, imprimir_estados_nao_reutilizados,
                                    imprimir_estados_reusados)


def _agora() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def _cronometrar(funcao: Callable, *args, **kwargs):
    inicio = time.time()
    resultado = funcao(*args, **kwargs)
    return resultado, time.time() - inicio


# --------------------------------------------------------------------------
# Estratégia ótima sem memorização
# --------------------------------------------------------------------------

def executar_busca_exaustiva(grafo: nx.Graph, pesos: Pesos) -> Tuple[int, List[Hashable]]:
    """Calcula val(G) por força bruta (sem PD) e imprime o resultado."""
    (melhor_valor, sequencia), tempo = _cronometrar(valor, grafo, pesos)
    print("Busca exaustiva (sem Programação Dinâmica):")
    print("Melhor valor:", melhor_valor)
    print("Melhor sequência:", sequencia)
    print("Tempo de execução:", tempo, "segundos")
    imprimir_ganhos(sequencia, pesos)
    return melhor_valor, sequencia


def executar_busca_por_classes(grafo: nx.Graph, pesos: Pesos) -> Tuple[int, List[Hashable]]:
    """Calcula val(G) ramificando por classes de vizinhança (sem PD)."""
    (melhor_valor, sequencia), tempo = _cronometrar(valor_classes, grafo, pesos)
    print("\nAbordagem por Classes de Vizinhança:")
    print("Melhor valor:", melhor_valor)
    print("Melhor sequência:", sequencia)
    print("Tempo de execução:", tempo, "segundos")
    imprimir_ganhos(sequencia, pesos)
    return melhor_valor, sequencia


# --------------------------------------------------------------------------
# Programação dinâmica
# --------------------------------------------------------------------------

def _relatorio_pd(titulo: str, grafo: nx.Graph, pesos: Pesos, memo: dict,
                  melhor_valor: int, sequencia: List[Hashable], tempo: float) -> None:
    print(f"\n{titulo}:")
    print("Melhor valor:", melhor_valor)
    print("Melhor sequência:", sequencia)
    print("Tempo de execução:", tempo, "segundos")
    print("Quantidade de estados a serem gerados:", contar_estados(grafo))
    print("Número de entradas na tabela dinâmica:", len(memo))
    print("Tamanho total do memo (real):", asizeof.asizeof(memo), "bytes")
    print("Número de reusos:", len(estatisticas.reusos))
    print("Número de estados distintos reutilizados:", len(estatisticas.estados_reusados))
    imprimir_ganhos(sequencia, pesos)


def executar_pd(grafo: nx.Graph, pesos: Pesos) -> Tuple[int, List[Hashable]]:
    """Calcula val(G) com a PD padrão e imprime o relatório."""
    estatisticas.reiniciar()
    memo = {}
    print("PROGRAMAÇÃO DINÂMICA:")
    print(f"Iniciou às {_agora()}")
    inicio = time.time()
    melhor_valor, sequencia = valor_dp(grafo, pesos, memo, inicio)
    _relatorio_pd("Com Programação Dinâmica", grafo, pesos, memo,
                  melhor_valor, sequencia, time.time() - inicio)
    return melhor_valor, sequencia


def executar_pd_classes(grafo: nx.Graph, pesos: Pesos) -> Tuple[int, List[Hashable]]:
    """Calcula val(G) com PD + classes de vizinhança e imprime o relatório."""
    estatisticas.reiniciar()
    memo = {}
    print(f"Iniciou às {_agora()}")
    inicio = time.time()
    melhor_valor, sequencia = valor_dp_classes(grafo, pesos, memo, inicio)
    _relatorio_pd("Com PD + Classes de Vizinhança", grafo, pesos, memo,
                  melhor_valor, sequencia, time.time() - inicio)
    return melhor_valor, sequencia


def executar_pd_bipartido(grafo: nx.Graph, pesos: Pesos, m: int, n: int) -> Tuple[int, List[Hashable]]:
    """Calcula val(K(m, n)) com a PD otimizada para bipartidos completos."""
    estatisticas.reiniciar()
    memo = {}
    print(f"Iniciou às {_agora()}")
    inicio = time.time()
    melhor_valor, sequencia = valor_dp_bipartido(grafo, pesos, m, n, memo, inicio)
    _relatorio_pd("Com Programação Dinâmica Kmn Otimizada", grafo, pesos, memo,
                  melhor_valor, sequencia, time.time() - inicio)
    return melhor_valor, sequencia


def executar_pd_caminho(grafo: nx.Graph, pesos: Pesos) -> Tuple[int, List[Hashable]]:
    """Calcula val(P_n) com a PD otimizada para caminhos."""
    estatisticas.reiniciar()
    inviaveis_iniciais = set(grafo.nodes) - set(vertices_viaveis(grafo))
    memo = {}
    print(f"Iniciou às {_agora()}")
    inicio = time.time()
    melhor_valor, sequencia = valor_dp_caminho(grafo, pesos, inviaveis_iniciais, memo, inicio)
    _relatorio_pd("Com Programação Dinâmica Pn Otimizada", grafo, pesos, memo,
                  melhor_valor, sequencia, time.time() - inicio)
    imprimir_estados_reusados()
    imprimir_estados_nao_reutilizados(memo)
    return melhor_valor, sequencia


# --------------------------------------------------------------------------
# Heurísticas
# --------------------------------------------------------------------------

def executar_guloso(grafo: nx.Graph, pesos: Pesos, verbose: bool = True):
    """Simula a partida com a estratégia gulosa para os dois jogadores."""
    print(f"Iniciou às {_agora()}")
    resultado, tempo = _cronometrar(jogar_guloso, grafo, pesos, verbose)
    print("Tempo de execução:", tempo, "segundos")
    return resultado


def executar_egl(grafo: nx.Graph, pesos: Pesos, verbose: bool = True):
    """Simula a partida com a Estratégia de Ganho Líquido para os dois jogadores."""
    print(f"Iniciou EGL às {_agora()}")
    resultado, tempo = _cronometrar(jogar_egl, grafo, pesos, verbose)
    print("Tempo de execução EGL:", tempo, "segundos\n")
    return resultado


# --------------------------------------------------------------------------
# Caminhos e ciclos (bicoloração)
# --------------------------------------------------------------------------

def executar_bicoloracao_caminho(grafo: nx.Graph, pesos: Pesos):
    """Resolve um caminho pela bicoloração e imprime as sequências de cada jogador."""
    resultado, tempo = _cronometrar(bicoloracao_caminho, grafo, pesos)
    vertices_alice, ganho_alice, vertices_bob, ganho_bob = resultado
    print("\n ======== Bicoloração em Caminho ==========\n")
    print(f"Alice: {vertices_alice} : Peso = {ganho_alice}")
    print(f"Bob: {vertices_bob} : Peso = {ganho_bob}")
    print("Tempo de execução:", tempo, "segundos")
    return resultado


def executar_ciclo(grafo: nx.Graph, pesos: Pesos):
    """Resolve um ciclo escolhendo a melhor primeira jogada e bicolorindo o resto."""
    resultado, tempo = _cronometrar(melhor_jogada_ciclo, grafo, pesos)
    vertices_alice, ganho_alice = resultado
    print("\n ======== Ciclo (primeira jogada + bicoloração) ==========\n")
    print(f"Alice: {vertices_alice} : Peso = {ganho_alice}")
    print("Tempo de execução:", tempo, "segundos")
    return resultado
