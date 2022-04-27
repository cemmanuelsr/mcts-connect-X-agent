from kaggle_environments import evaluate, make, utils
from time import time
import numpy as np

from MCTSPlayer import MCTSPlayer


env = make("connectx", debug=True)
env.render()
mcts = MCTSPlayer()

def my_agent(observation, configuration):
    player_code = observation.mark
    board = np.reshape(observation.board, (configuration.rows, configuration.columns))
    _, column = mcts.move(player_code, board, popout=False)
    return column

trainer = env.train([None, "negamax"])

observation = trainer.reset()

start = time()
while not env.done:
    my_action = my_agent(observation, env.configuration)
    end = time()
    print(f'Tempo: {end - start}')
    print("My Action", my_action)
    observation, reward, done, info = trainer.step(my_action)
    start = end
    # env.render(mode="ipython", width=100, height=90, header=False, controls=False)
env.render()
