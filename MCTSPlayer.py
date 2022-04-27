from time import time

from Player import Player
from MCTNode import State
from constants import *

class MCTSPlayer(Player):

    def move(self, player_code, board, popout=True):
        
        start = time()
        state = State(board, player_code, rows=ROWS, columns=COLUMNS, condition=CONNECT_X-1, parent=None, final=False, final_score=None, action=None, column=None, popout=popout)

        while time() - start <= TIMEOUT:
            state.run_tree()

        state = state.playable_child()
        if state.action == 'put':
            return None, state.column
        else:
            return 'p', state.column
    
    def name(self):

        return "Carlos Monteiro"
