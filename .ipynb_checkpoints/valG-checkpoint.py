import datetime
import networkx as nx
from typing import Dict, Tuple
from utils import *
import time
from pympler import asizeof

contagem_reuso_dp = []
estados_reusados = {}
estados_na_tabela = set()
estados_timestamps = {}
relacao = {}
logs_memoKmn = []
logs_memo = []
qtd_estados_plot = []
qtd_estados_plotKmn = []

def gerar_reuso_estados(m, n):
    global relacao
    max_tamanho_estado = m + n - 2
    max_reuso = m + n - 3
    numero_reuso = max_reuso + 1
    resultado = {}
    for i in range(2, max_tamanho_estado +1 ):
        tamanho_estado = i 
        numero_reuso = numero_reuso - 1
        resultado[tamanho_estado] = numero_reuso 

    print("Relação estado reuso: ")
    print(resultado)
    relacao = resultado

def registrar_qtdEstados_memoKmn(memo, inicio,estado='padrão'):
    """
    Registra o tempo decorrido e a quantidade real do memo.
    """
    tempo_decorrido = time.time() - inicio
    tamanho = len(memo)
    qtd_estados_plotKmn.append((tempo_decorrido, tamanho,estado))
    # Opcional: imprimir no log

def registrar_qtdEstados(memo, inicio):
    """
    Registra o tempo decorrido e a quantidade real do memo.
    """
    tempo_decorrido = time.time() - inicio
    tamanho = len(memo)
    qtd_estados_plot.append((tempo_decorrido, tamanho))
    # Opcional: imprimir no log

def registrar_tamanho_memoKmn(memo, inicio,estado='padrão'):
    """
    Registra o tempo decorrido e o tamanho real do memo.
    """
    tempo_decorrido = time.time() - inicio
    tamanho = asizeof.asizeof(memo)
    logs_memoKmn.append((tempo_decorrido, tamanho,estado))
    # Opcional: imprimir no log

def registrar_tamanho_memo(memo, inicio):
    """
    Registra o tempo decorrido e o tamanho real do memo.
    """
    tempo_decorrido = time.time() - inicio
    tamanho = asizeof.asizeof(memo)
    logs_memo.append((tempo_decorrido, tamanho))
    # Opcional: imprimir no log

def limparVariaveisGlobais():
    global contagem_reuso_dp, estados_reusados, estados_na_tabela, estados_timestamps
    contagem_reuso_dp = []
    estados_reusados = {}
    estados_na_tabela = set()
    estados_timestamps = {}

#===============================================================================================================================#

def valor(grafo: nx.Graph, pesos: Dict[int, int]) -> Tuple[int, list, list]:
    if not grafo.nodes:
        return 0, []
    melhor_valor = float('-inf')
    melhor_escolha = None
    melhor_caminho = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            valor_subgrafo, sub_melhor_caminho = valor(grafo_copia, pesos)
            valor_atual = pesos[v] - valor_subgrafo

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_escolha = v
                melhor_caminho = [v] + sub_melhor_caminho

    return melhor_valor, melhor_caminho

#===============================================================================================================================#

def valor_dp(grafo: nx.Graph, pesos: dict, memo=None, inicio_tempo= 0,profundidade=0, history=()):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)
    #print("aaaa")
    if estado in memo:
        registrar_tamanho_memo(memo, inicio_tempo)
        registrar_qtdEstados(memo, inicio_tempo)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        contagem_reuso_dp.append(estado)

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0, 'timestamps': [],'historico': []}

        estados_reusados[estado]['count'] += 1
        estados_reusados[estado]['timestamps'].append(history)
        estados_reusados[estado]['historico'].append(history)

        return memo[estado]

    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_caminho = [[]]
    arvore_decisao = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            novo_history = history + (v,)
            valor_subgrafo, sub_melhor_caminho = valor_dp(grafo_copia, pesos, memo, inicio_tempo,profundidade + 1, novo_history)
            valor_atual = pesos[v] - valor_subgrafo

            #arvore_decisao.append((v, valor_atual, sub_arvore_decisao))
            registrar_tamanho_memo(memo, inicio_tempo)
            registrar_qtdEstados(memo, inicio_tempo)
            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_caminho = [v] + sub_melhor_caminho
            
            if len(grafo.nodes) > 1:
                memo[estado] = (melhor_valor, melhor_caminho)
                estados_na_tabela.add(estado)

    return melhor_valor, melhor_caminho



# def valor_dp(grafo: nx.Graph, pesos: dict, memo=None):
#     global contagem_reuso_dp, estados_reusados, estados_na_tabela

#     if memo is None:
#         memo = {}

#     estado = tuple(grafo.nodes)

#     if estado in memo:    
#         return memo[estado]

#     if not grafo.nodes:
#         return 0, []

#     melhor_valor = float('-inf')
#     melhor_caminho = []

#     for v in list(grafo.nodes):
#         if eh_viavel(grafo, v):
#             grafo_copia = grafo.copy()
#             grafo_copia.remove_node(v)
#             valor_subgrafo, sub_melhor_caminho = valor_dp(grafo_copia, pesos, memo)
#             valor_atual = pesos[v] - valor_subgrafo

#             if valor_atual > melhor_valor:
#                 melhor_valor = valor_atual
#                 melhor_caminho = [v] + sub_melhor_caminho

#             if len(grafo.nodes) > 1:
#                 memo[estado] = (melhor_valor, melhor_caminho)
#                 estados_na_tabela.add(estado)

#     return melhor_valor, melhor_caminho


#===============================================================================================================================#

def valor_dp_bipartido(grafo: nx.Graph, pesos: dict, memo=None,m =0 ,n = 0,inicio_tempo = 0, profundidade=0, history=()):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela,relacao

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        registrar_tamanho_memoKmn(memo, inicio_tempo,estado)
        registrar_qtdEstados_memoKmn(memo, inicio_tempo,estado)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        contagem_reuso_dp.append(estado)
        reusosRestantes = memo[estado][2] - 1 
        #memo[estado][2] = reusosRestantes
        valor, caminho, _ = memo[estado]
        memo[estado] = (valor, caminho, reusosRestantes)  

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0, 'timestamps': [],'historico': []}

        estados_reusados[estado]['count'] += 1
        estados_reusados[estado]['timestamps'].append(history)
        estados_reusados[estado]['historico'].append(history)

        estadoCopia = memo[estado]

        if reusosRestantes == 0:
            print("Estado deletado: ",estado)
            del memo[estado]

        return estadoCopia[0],estadoCopia[1]

    
    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_caminho = []
    #arvore_decisao = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            novo_history = history + (v,)
            valor_subgrafo , sub_melhor_caminho = valor_dp_bipartido(grafo_copia, pesos, memo,m,n,inicio_tempo, profundidade + 1, novo_history)
            valor_atual = pesos[v] - valor_subgrafo

            #arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_caminho = [v] + sub_melhor_caminho
            registrar_tamanho_memoKmn(memo, inicio_tempo,estado)
            registrar_qtdEstados_memoKmn(memo, inicio_tempo,estado)
            if len(grafo.nodes) > 1 and len(grafo.nodes) < (m+n-1):
                n_reusos_max = relacao.get(len(grafo.nodes))
                if estado in memo:
                
                    valorAux = memo[estado][0]
                    if valorAux < melhor_valor:
                        memo[estado] = (melhor_valor, melhor_caminho, n_reusos_max)
                        estados_na_tabela.add(estado)
                else:
                    memo[estado] = (melhor_valor, melhor_caminho, n_reusos_max)
                    estados_na_tabela.add(estado)
                    
                #print(f"Adiconou o estado: {estado}")
               

    return melhor_valor, melhor_caminho




def valor_dp_bipartido_LIMPO(grafo: nx.Graph, pesos: dict, memo=None,m =0 ,n = 0):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela,relacao

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        #registrar_tamanho_memoKmn(memo, inicio_tempo)
        #registrar_qtdEstados_memoKmn(memo, inicio_tempo)
        #timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        #contagem_reuso_dp.append(estado)
        reusosRestantes = memo[estado][2] - 1 
        memo[estado][2] = reusosRestantes
        valor, caminho, _ = memo[estado]
        memo[estado] = (valor, caminho, reusosRestantes)  

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0}

        estados_reusados[estado]['count'] += 1
        #estados_reusados[estado]['timestamps'].append(history)
        #estados_reusados[estado]['historico'].append(history)

        estadoCopia = memo[estado]

        if reusosRestantes == 0:
            #print("Estado deletado: ",estado)
            del memo[estado]

        return estadoCopia[0],estadoCopia[1]

    
    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_caminho = []
    #arvore_decisao = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            #novo_history = history + (v,)
            valor_subgrafo , sub_melhor_caminho = valor_dp_bipartido(grafo_copia, pesos, memo,m,n)
            valor_atual = pesos[v] - valor_subgrafo

            #arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_caminho = [v] + sub_melhor_caminho
            #registrar_tamanho_memoKmn(memo, inicio_tempo)
            #registrar_qtdEstados_memoKmn(memo, inicio_tempo)
            if len(grafo.nodes) > 1 and len(grafo.nodes) < (m+n-1):
                n_reusos_max = relacao.get(len(grafo.nodes))
                if estado in memo:
                
                    valorAux = memo[estado][0]
                    if valorAux < melhor_valor:
                        memo[estado] = (melhor_valor, melhor_caminho, n_reusos_max)
                        estados_na_tabela.add(estado)
                else:
                    memo[estado] = (melhor_valor, melhor_caminho, n_reusos_max)
                    estados_na_tabela.add(estado)
                    
                #print(f"Adiconou o estado: {estado}")
               

    return melhor_valor, melhor_caminho

#===============================================================================================================================#


#===============================================================================================================================#

def valor_dp_caminho(grafo: nx.Graph, pesos: dict, primeirosVerticesNaoViaveis,memo=None,inicio_tempo = 0, profundidade=0, history=()):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela,relacao

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        registrar_tamanho_memoKmn(memo, inicio_tempo)
        registrar_qtdEstados_memoKmn(memo, inicio_tempo)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        contagem_reuso_dp.append(estado)

        valor, caminho = memo[estado]
        memo[estado] = (valor, caminho)  

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0, 'timestamps': [],'historico': []}

        estados_reusados[estado]['count'] += 1
        estados_reusados[estado]['timestamps'].append(history)
        estados_reusados[estado]['historico'].append(history)

        estadoCopia = memo[estado]

        print("Estado deletado: ",estado)
        del memo[estado]


        return estadoCopia[0],estadoCopia[1]

    
    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_caminho = []
    #arvore_decisao = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            novo_history = history + (v,)
            valor_subgrafo , sub_melhor_caminho = valor_dp_caminho(grafo_copia, pesos, primeirosVerticesNaoViaveis,memo,inicio_tempo, profundidade + 1, novo_history)
            valor_atual = pesos[v] - valor_subgrafo

            #arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_caminho = [v] + sub_melhor_caminho
            registrar_tamanho_memoKmn(memo, inicio_tempo)
            registrar_qtdEstados_memoKmn(memo, inicio_tempo)

            if len(grafo.nodes) > 1:
               eh_sc = eh_subconjunto_caminho(grafo,grafo.nodes,primeirosVerticesNaoViaveis)
               if eh_sc:
                 memo[estado] = (melhor_valor, melhor_caminho)
                 estados_na_tabela.add(estado)    
            
            # if len(grafo.nodes) > 1:
            #     if estado in memo:
            #         valorAux = memo[estado][0]
            #         if valorAux < melhor_valor:
            #             memo[estado] = (melhor_valor, melhor_caminho)
            #             estados_na_tabela.add(estado)
            #     else:
            #         memo[estado] = (melhor_valor, melhor_caminho)
            #         estados_na_tabela.add(estado)
                    
                #print(f"Adiconou o estado: {estado}")
               

    return melhor_valor, melhor_caminho


def valor_dp_caminho_LIMPO(grafo: nx.Graph, pesos: dict, primeirosVerticesNaoViaveis,memo=None,inicio_tempo = 0, profundidade=0, history=()):
    global contagem_reuso_dp, estados_reusados, estados_na_tabela,relacao

    if memo is None:
        memo = {}

    estado = tuple(grafo.nodes)

    if estado in memo:
        #registrar_tamanho_memoKmn(memo, inicio_tempo)
        #registrar_qtdEstados_memoKmn(memo, inicio_tempo)
        #timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        contagem_reuso_dp.append(estado)

        valor, caminho = memo[estado]
        memo[estado] = (valor, caminho)  

        if estado not in estados_reusados:
            estados_reusados[estado] = {'count': 0}

        #estados_reusados[estado]['count'] += 1
        #estados_reusados[estado]['timestamps'].append(history)
        #estados_reusados[estado]['historico'].append(history)

        estadoCopia = memo[estado]

        #print("Estado deletado: ",estado)
        del memo[estado]


        return estadoCopia[0],estadoCopia[1]

    
    if not grafo.nodes:
        return 0, []

    melhor_valor = float('-inf')
    melhor_caminho = []
    #arvore_decisao = []

    for v in list(grafo.nodes):
        if eh_viavel(grafo, v):
            grafo_copia = grafo.copy()
            grafo_copia.remove_node(v)
            #novo_history = history + (v,)
            valor_subgrafo , sub_melhor_caminho = valor_dp_caminho(grafo_copia, pesos, primeirosVerticesNaoViaveis,memo)
            valor_atual = pesos[v] - valor_subgrafo

            #arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_caminho = [v] + sub_melhor_caminho
            #registrar_tamanho_memoKmn(memo, inicio_tempo)
            #registrar_qtdEstados_memoKmn(memo, inicio_tempo)

            if len(grafo.nodes) > 1:
               eh_sc = eh_subconjunto_caminho(grafo,grafo.nodes,primeirosVerticesNaoViaveis)
               if eh_sc:
                 memo[estado] = (melhor_valor, melhor_caminho)
                 estados_na_tabela.add(estado)    
            
            # if len(grafo.nodes) > 1:
            #     if estado in memo:
            #         valorAux = memo[estado][0]
            #         if valorAux < melhor_valor:
            #             memo[estado] = (melhor_valor, melhor_caminho)
            #             estados_na_tabela.add(estado)
            #     else:
            #         memo[estado] = (melhor_valor, melhor_caminho)
            #         estados_na_tabela.add(estado)
                    
                #print(f"Adiconou o estado: {estado}")
               

    return melhor_valor, melhor_caminho

#===============================================================================================================================#

# def valor_dp_otimizado_caminho(grafo: nx.Graph, pesos: dict, primeirosVerticesNaoViaveis, memo=None, profundidade=0, history=()):
#     global contagem_reuso_dp, estados_reusados, estados_na_tabela

#     if memo is None:
#         memo = {}

#     estado = tuple(grafo.nodes)

#     if estado in memo:
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
#         contagem_reuso_dp.append(estado)

#         if estado not in estados_reusados:
#             estados_reusados[estado] = {'count': 0, 'timestamps': []}

#         estados_reusados[estado]['count'] += 1
#         estados_reusados[estado]['timestamps'].append(timestamp)

#         return memo[estado]

#     if not grafo.nodes:
#         return 0, [], []

#     melhor_valor = float('-inf')
#     melhor_caminho = []
#     arvore_decisao = []

#     for v in list(grafo.nodes):
#         if eh_viavel(grafo, v):
#             grafo_copia = grafo.copy()
#             grafo_copia.remove_node(v)
#             novo_history = history + (v,)
#             valor_subgrafo, sub_arvore_decisao, sub_melhor_caminho = valor_dp_otimizado_caminho(grafo_copia, pesos, primeirosVerticesNaoViaveis,memo, profundidade + 1, novo_history)
#             valor_atual = pesos[v] - valor_subgrafo

#             arvore_decisao.append((v, valor_atual, sub_arvore_decisao))

#             if valor_atual > melhor_valor:
#                 melhor_valor = valor_atual
#                 melhor_caminho = [v] + sub_melhor_caminho

#             if len(grafo.nodes) > 1:
#                 eh_sc = eh_subconjunto_caminho(grafo,grafo.nodes,primeirosVerticesNaoViaveis)
#                 if eh_sc:
#                     memo[estado] = (melhor_valor, arvore_decisao, melhor_caminho)
#                     estados_na_tabela.add(estado)

#     return melhor_valor, arvore_decisao, melhor_caminho






