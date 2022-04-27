# Monte Carlo Tree Search - Connect X - Agent

Este projeto consiste de um agente autônomo capaz de jogar partidas do jogo [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) com a variante PopOut para a eletiva de [Agentes Autônomos e Reinforcement Learning](http://fbarth.net.br/agents/).

----

## Setup do ambiente para execução do agente

Configure um ambiente virtual:

```
python3 -m virtualenv venv
source venv/bin/activate
```

Instalando dependências:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Execute o FourInRow.py e você deve conseguir jogar contra o agente.

## Lógica do Agente

O agente desenvolvido utiliza um algoritmo de busca em uma árvore construída a partir do algoritmo de Monte Carlo, chamado Monte Carlo Tree Search (MCTS), que ganhou notoriedade depois de ter sido implementado no modelo AlphaGo Zero da Google que derrotou o então campeão mundial de Go em 2016 e um artigo para entender como isso foi feito pode ser lido [aqui](https://jonathan-hui.medium.com/monte-carlo-tree-search-mcts-in-alphago-zero-8a403588276a).
