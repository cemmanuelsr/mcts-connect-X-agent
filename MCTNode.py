import random

from constants import *
from utils import *


class State:
    # Estado do nó da árvore de busca de Monte Carlo
    
    def __init__(self, board, player_code, rows=ROWS, columns=COLUMNS, condition=CONNECT_X-1, parent=None, final=False, final_score=None, action=None, column=None, popout=True, cp=CP):
        self.board = board.copy()
        self.player_code = player_code
        self.rows = rows
        self.columns = columns
        self.condition = condition
        self.parent = parent
        self.children = []
        self.total_score = 0
        self.total_visits = 0
        self.possible_put = [('put', column) for column in range(columns) if not(column_is_full(board, column))]
        self.possible_pop = [('pop', column) for column in range(columns) if board[-1, column] == player_code]
        self.possible_moves = self.possible_put + self.possible_pop
        self.moves_after_expand = self.possible_moves.copy()
        self.final = final
        self.final_score = final_score
        self.action = action
        self.column = column
        self.popout = popout
        self.cp = cp

    def check_expand(self):
        # função para checar se podemos continuar em um caminho da árvore
        return (not self.final) and (len(self.moves_after_expand) > 0)

    def simulate(self):
        if self.final:
            return self.final_score
        return opponent_score(rule_for_simulation(self.board, self.player_code, self.rows, self.columns, self.condition, self.popout))

    def backpropagate(self, simulation_score):
        self.total_score += simulation_score
        self.total_visits += 1
        
        if self.parent is not None:
            self.parent.backpropagate(opponent_score(simulation_score))

    def expand_and_simulate(self):
        # parte de expandir simulação do algoritmo clássico de Monte Carlo
        choice = random.choice(self.moves_after_expand)
        action, column = choice
        child_board = self.board.copy()
        if action == 'put':
            put_in(child_board, column, self.player_code, self.rows)
        if action == 'pop':
            pop_out(child_board, column, self.player_code, self.rows)

        final, score = check_final_and_get_score(child_board, column, self.player_code, self.rows, self.columns, self.condition)
        self.children.append(State(child_board, 
                                   opponent_code(self.player_code), 
                                   self.rows, self.columns, self.condition, 
                                   parent=self, final=final, final_score=score, 
                                   action=action, column=column, popout=self.popout
                                   ))

        simulation_score = self.children[-1].simulate()
        self.children[-1].backpropagate(simulation_score)
        self.moves_after_expand.remove(choice)

    def best_child(self):
        children_uct_scores = [UCT(child.total_score, child.total_visits, self.total_visits, self.cp) for child in self.children]
        max_child_uct_score = max(children_uct_scores)

        best_child = children_uct_scores.index(max_child_uct_score)
        return self.children[best_child]

    def playable_child(self):
        children_scores = [child.total_score for child in self.children]
        max_score = max(children_scores)

        playable_child = children_scores.index(max_score)
        return self.children[playable_child]

    def choose_child_by_action(self, action, column):
        for child in self.children:
            if (child.action == action) and (child.column == column):
                return child

        return None

    def run_tree(self):
        if self.final:
            self.backpropagate(self.final_score)
            return
        if self.check_expand():
            self.expand_and_simulate()
            return
        self.best_child().run_tree()
