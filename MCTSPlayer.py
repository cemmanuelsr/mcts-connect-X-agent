from time import time
from random import randint

from Player import Player
from MCTNode import State
from constants import *

class MCTSPlayer(Player):

    def __init__(self, timeout=TIMEOUT, cp=CP):
        self.timeout = timeout
        self.cp = cp

    def bottomDiscExist(self, player_code, board, column):
        if board[5][column] == player_code:
            return True
        return False

    def isThereNoSpace(self, board, column): 
        if board[0][column] != 0:
            return True
        return False

    def move(self, player_code, board, popout=True):
        
        try:
            start = time()
            state = State(board, player_code, rows=ROWS, columns=COLUMNS, condition=CONNECT_X-1, parent=None, final=False, final_score=None, action=None, column=None, popout=popout, cp=self.cp)

            while time() - start <= self.timeout:
                state.run_tree()

            state = state.playable_child()
            if state.action == 'put':
                return None, state.column
            else:
                return 'p', state.column
        except:
            # caso nada possa ser feito ou bateu o timeout, movimento aleatório
            if not(popout):
                return randint(0,6)
            x = randint(0,13)
            if x >= 7:
                p = x - 7
                if self.bottomDiscExist(player_code, board, p):
                    return 'p', p
            
            x = randint(0,6)
            while self.isThereNoSpace(board, x):
                x = randint(0,6)
            return None, x
    
    def name(self):

        return f"Carlos Monteiro"
