"""
Instrumentação das execuções de programação dinâmica (PD).

Durante a busca, as funções de PD registram aqui:
  * quais estados da tabela foram reutilizados e por qual caminho de jogadas;
  * a evolução, ao longo do tempo, do tamanho da tabela em bytes e em
    quantidade de estados (usada nos gráficos de `visualizacao`).

Há duas séries de evolução: a "padrão" (PD sem otimização) e a
"otimizada" (PD com descarte de estados, ex.: Kmn e caminho), para que
as duas possam ser plotadas lado a lado.
"""

import time
from typing import Dict, Hashable, List, Tuple

import networkx as nx
from pympler import asizeof

from gold_grabbing.jogo import eh_viavel

Estado = Tuple[Hashable, ...]


class EstatisticasPD:
    """Acumula as métricas coletadas pelas funções de programação dinâmica."""

    def __init__(self) -> None:
        self.reusos: List[Estado] = []
        self.estados_reusados: Dict[Estado, dict] = {}
        self.estados_na_tabela: set = set()

        # Séries (tempo, valor) da PD padrão.
        self.bytes_padrao: List[Tuple[float, int]] = []
        self.qtd_estados_padrao: List[Tuple[float, int]] = []

        # Séries (tempo, valor, estado) da PD otimizada.
        self.bytes_otimizada: List[Tuple[float, int, object]] = []
        self.qtd_estados_otimizada: List[Tuple[float, int, object]] = []

    def reiniciar(self) -> None:
        """Limpa as métricas de reuso (as séries de evolução são mantidas)."""
        self.reusos.clear()
        self.estados_reusados.clear()
        self.estados_na_tabela.clear()

    def registrar_reuso(self, estado: Estado, historico: Tuple) -> None:
        """Registra que `estado` foi lido da tabela após a sequência `historico`."""
        self.reusos.append(estado)
        info = self.estados_reusados.setdefault(estado, {'count': 0, 'historico': []})
        info['count'] += 1
        info['historico'].append(historico)

    def registrar_tabela_padrao(self, memo: dict, inicio: float) -> None:
        """Registra o tamanho atual (bytes e estados) da tabela da PD padrão."""
        decorrido = time.time() - inicio
        self.bytes_padrao.append((decorrido, asizeof.asizeof(memo)))
        self.qtd_estados_padrao.append((decorrido, len(memo)))

    def registrar_tabela_otimizada(self, memo: dict, inicio: float, estado: object = 'padrão') -> None:
        """Registra o tamanho atual (bytes e estados) da tabela da PD otimizada."""
        decorrido = time.time() - inicio
        self.bytes_otimizada.append((decorrido, asizeof.asizeof(memo), estado))
        self.qtd_estados_otimizada.append((decorrido, len(memo), estado))


# Instância compartilhada usada pelas funções de PD e pelos relatórios.
estatisticas = EstatisticasPD()


def contar_estados(grafo: nx.Graph) -> int:
    """
    Conta quantos estados distintos (subgrafos conexos alcançáveis com
    mais de um vértice) o jogo pode gerar a partir de `grafo`.
    """
    estados_gerados = set()

    def explorar(subgrafo: nx.Graph) -> None:
        estado = tuple(subgrafo.nodes)
        if len(estado) > 1 and estado not in estados_gerados:
            estados_gerados.add(estado)
            for v in list(subgrafo.nodes):
                if eh_viavel(subgrafo, v):
                    proximo = subgrafo.copy()
                    proximo.remove_node(v)
                    explorar(proximo)

    explorar(grafo)
    return len(estados_gerados)


def imprimir_estados_reusados() -> None:
    """Imprime cada estado reutilizado, quantas vezes e por quais caminhos."""
    print("\nEstados Reutilizados:")
    if not estatisticas.estados_reusados:
        print("Nenhum estado foi reutilizado.")
        return

    for estado, info in estatisticas.estados_reusados.items():
        print(f"{estado} → reutilizado {info['count']} vezes")
        print("  Caminhos que levaram ao reuso:")
        for historico in info['historico']:
            print(f"    {historico}")


def imprimir_estados_nao_reutilizados(memo: dict) -> None:
    """Imprime os estados da tabela que nunca foram reutilizados."""
    print("\nEstados NÃO reutilizados:")
    nao_reutilizados = [e for e in memo if e not in estatisticas.estados_reusados]
    for estado in nao_reutilizados:
        print(f"Estado: {estado}")
        print("-------------------------")
    print(f"\nTotal de estados que nunca foram reutilizados: {len(nao_reutilizados)}")


def imprimir_tabela_pd(memo: dict) -> None:
    """Imprime toda a tabela de PD, com informações de reuso de cada estado."""
    print("\nTabela de Programação Dinâmica:")
    for estado, entrada in memo.items():
        melhor_valor, melhor_sequencia = entrada[0], entrada[1]
        print(f"Estado: {estado}")
        print(f"  Melhor valor: {melhor_valor}")
        print(f"  Melhor sequência: {melhor_sequencia}")

        info = estatisticas.estados_reusados.get(estado)
        if info:
            print(f"  Reutilizado {info['count']} vezes")
            print(f"  Caminhos que levaram ao reuso: {info['historico']}")
        else:
            print("  Nunca reutilizado")
        print("-------------------------")
