# Gold Grabbing Game

Estudo do *Gold Grabbing Game* em grafos. Dois jogadores, **Alice** (que começa) e **Bob**,
se alternam removendo vértices de um grafo conexo com pesos nos vértices. Cada vértice
removido rende ao jogador o seu peso em ouro. A única regra é que **o grafo restante deve
continuar conexo** após cada remoção, ou seja, só podem ser removidos vértices que não são
de corte (chamados aqui de *viáveis*). Vence quem acumular mais ouro.

O valor do jogo para o jogador da vez é

```
val(G) = max { w(v) - val(G - v) : v viável em G }
```

isto é, a maior diferença de ouro que ele consegue garantir sobre o adversário.

## Estrutura

```
main.ipynb                      Notebook principal: escolhe um grafo e executa as estratégias.
gold_grabbing/
├── jogo.py                     Regras: vértices viáveis, divisão das jogadas e placar.
├── metricas.py                 Métricas das execuções de PD (reusos, tamanho da tabela).
├── visualizacao.py             Plot de grafos, árvores de decisão e evolução da tabela de PD.
├── relatorios.py               executar_*: roda uma estratégia, mede o tempo e imprime o resultado.
├── grafos/
│   ├── geradores.py            Famílias: caminho, ciclo, completo, book, barbell, threshold,
│   │                           bipartido, bipartido completo e árvores.
│   ├── exemplos.py             Instâncias fixas (P3, P4, C4, K3, W3, W5, estrela, ...) e contraexemplos.
│   └── transformacoes.py       União por ponte, pendentes nulos, subdivisões (losango e
│                               expansão) e remoção de gêmeos.
└── estrategias/
    ├── otima.py                val(G) por busca exaustiva e por classes de vizinhança.
    ├── programacao_dinamica.py val(G) com PD (padrão, por classes, K(m,n) e caminhos).
    ├── gulosa.py               Heurística gulosa: maior peso entre os vértices viáveis.
    ├── ganho_liquido.py        Estratégia do Ganho Líquido (EGL).
    ├── casos_especiais.py      Estratégias por bicoloração para caminhos e ciclos.
    └── simulacao.py            Laço de partida usado pelas heurísticas.
figuras/                        Figuras geradas (evolução da tabela de PD, árvores de decisão).
legado/                         Notebook original autocontido e os arquivos que ele produziu.
```

## Estratégias

| Estratégia | Função | Tipo |
| --- | --- | --- |
| Busca exaustiva (minimax) | `otima.valor` | exata |
| Busca por classes de vizinhança | `otima.valor_classes` | exata |
| Programação dinâmica | `programacao_dinamica.valor_dp` | exata |
| PD + classes de vizinhança | `programacao_dinamica.valor_dp_classes` | exata |
| PD otimizada para K(m, n) | `programacao_dinamica.valor_dp_bipartido` | exata, menos memória |
| PD otimizada para caminhos | `programacao_dinamica.valor_dp_caminho` | exata, menos memória |
| Gulosa | `gulosa.jogar_guloso` | heurística |
| Ganho Líquido (EGL) | `ganho_liquido.jogar_egl` | heurística |
| Bicoloração em caminho | `casos_especiais.bicoloracao_caminho` | heurística |
| Primeira jogada + bicoloração em ciclo | `casos_especiais.melhor_jogada_ciclo` | heurística |

As estratégias exatas retornam `(val(G), sequência de jogadas)`, em que as posições pares
da sequência são de Alice e as ímpares de Bob. As heurísticas retornam
`(vertices_alice, ganho_alice, vertices_bob, ganho_bob)`.

## Uso

Dependências: `networkx`, `matplotlib`, `pympler` (e `openpyxl` para o notebook legado).

```bash
pip install networkx matplotlib pympler
jupyter notebook main.ipynb
```

Ou diretamente em Python, a partir da raiz do projeto:

```python
from gold_grabbing.grafos.exemplos import contraexemplo_guloso_barbell
from gold_grabbing.relatorios import executar_pd, executar_guloso

grafo, pesos = contraexemplo_guloso_barbell()
executar_pd(grafo, pesos)      # val(G) = 5
executar_guloso(grafo, pesos)  # a gulosa obtém diferença 1
```
