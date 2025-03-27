from utils import *
from valG import *
from funcoesDP import *
from plotagem import *
import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import datetime

from typing import Dict, Tuple



def main_caminho_otimiziado_pd(grafo, pesos):
    primeirosVerticesViaveis = verticesViaveis(grafo)
    print(primeirosVerticesViaveis)
    print(grafo.nodes - primeirosVerticesViaveis)
    primeirosVerticesNaoViaveis = grafo.nodes - primeirosVerticesViaveis
    inicio_tempo = time.time()
    memo = {}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Mantém milissegundos
  # Captura o instante de reutilização
    print(f"Iniciou às {timestamp}")
    melhor_valor_dp, arvore_decisao_dp, melhor_caminho_dp = valor_dp_otimizado_caminho(grafo, pesos, primeirosVerticesNaoViaveis,memo)
    fim_tempo = time.time()
    print("\nCom Programação Dinâmica Otimiziada Para CAMINHO:")
    print("Melhor caminho:", melhor_caminho_dp)
    print("Tempo de execução:", fim_tempo - inicio_tempo, "segundos")
    quantidade_estados = contar_estados(grafo)
    print("Quantidade de estados  a serem gerados:", quantidade_estados)
    print("Número de entradas na tabela dinâmica:", len(memo))
    print("Número de reusos:", len(contagem_reuso_dp))
    print("Número de estados distintos usados: ",len(estados_reusados))
    calcular_ganhos(melhor_caminho_dp, pesos)
    #imprime_estados_reusados()
    #imprime_estados_nao_reutilizados()
    imprime_tabela_dp(memo)
    imprimirArvoreDecisao(arvore_decisao_dp)
