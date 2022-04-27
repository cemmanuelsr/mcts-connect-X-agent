from kaggle_environments import evaluate, make, utils
import numpy as np

from MCTSPlayer import MCTSPlayer

env = make("connectx", debug=True)
env.render()
mcts = MCTSPlayer()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def my_agent(observation, configuration):
    player_code = observation.mark
    board = np.reshape(observation.board, (configuration.rows, configuration.columns))
    _, column = mcts.move(player_code, board, popout=False)
    return column

def test_agent(agent1, name_agent1, agent2, name_agent2, n_rounds=100):
    print(f"{bcolors.HEADER}Simulation outcomes for {n_rounds} played games between {name_agent1} x {name_agent2}{bcolors.ENDC}")

    config = {'rows': 6, 'columns': 7, 'inarow': 4, 'actTimeout': 10}

    # Agent 1 goes first (roughly) half the time          
    outcomes = evaluate("connectx", [agent1, agent2], config, [], n_rounds//2)

    # Agent 2 goes first (roughly) half the time      
    outcomes += [[b,a] for [a,b] in evaluate("connectx", [agent2, agent1], config, [], n_rounds-n_rounds//2)]

    agent1_win_pct = outcomes.count([1,-1])/len(outcomes)
    agent2_win_pct = outcomes.count([-1,1])/len(outcomes)
    draw_pct = 1 - agent1_win_pct - agent2_win_pct

    print(f"{bcolors.OKGREEN}{name_agent1} win rate: {np.round(agent1_win_pct, 2)}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{name_agent1} loss rate: {np.round(agent2_win_pct, 2)}{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Draw rate: {np.round(draw_pct, 2)}{bcolors.ENDC}")
    print(f"{bcolors.FAIL}Number of Invalid Plays by {name_agent1}: {outcomes.count([None, 0])}{bcolors.ENDC}")
    print(f"{bcolors.FAIL}Number of Invalid Plays by {name_agent2}: {outcomes.count([0, None])}\n{bcolors.ENDC}")

test_agent(my_agent, mcts.name(), "random", "Random")
test_agent(my_agent, mcts.name(), "negamax", "Negamax")

