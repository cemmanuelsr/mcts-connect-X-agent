from Player import Player

class ManualPlayer(Player):

    def name(self):
        return "Manual"

    def move(self, player_code, board):
        g = input("You can add a piece in a column (0..6) or remove (p0..p6) a piece from the bottom: ")
        if g[0] == 'p':
            return 'p', int(g[1])
        return None, int(g)
