from random import randint
from Player import Player

class RandomPlayer(Player):

    def name(self):
        return "Random"

    def bottomDiscExist(self, player_code, board, column):
        if board[5][column] == player_code:
            return True
        return False

    def isThereNoSpace(self, board, column): 
        if board[0][column] != 0:
            return True
        return False

    def move(self, player_code, board):
        x = randint(0,13)
        if x >= 7:
            p = x - 7
            if self.bottomDiscExist(player_code, board, p):
                #print(f'p{p}')
                return 'p', p
        
        x = randint(0,6)
        while self.isThereNoSpace(board, x):
            x = randint(0,6)
        #print(x)
        return None, x
