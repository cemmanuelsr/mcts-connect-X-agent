import random
import math
import numpy as np

from constants import *


def column_is_full(board, column, rows=ROWS):
    return sum([1 for row in range(rows) if board[row, column] != 0]) == rows

def put_in(board, column, player_code, rows=ROWS):
    if not(column_is_full(board, column, rows)):
        row = max([i for i in range(rows) if board[:, column][i] == 0])
        board[row, column] = player_code

        return 'put'

def pop_out(board, column, player_code, rows=ROWS):
    if board[-1, column] == player_code:
        for i in range(rows-1, 0, -1):
            board[i, column] = board[i - 1, column]
        board[0, column] = 0

        return 'pop'

def random_put_in(board, columns=COLUMNS):
    # função para adicionar aleatoriedade na simulação de Monte Carlo
    return random.choice([column for column in range(columns) if not(column_is_full(board, column))])

def random_pop_out(board, player_code, columns=COLUMNS):
    return random.choice([column for column in range(columns) if board[-1, column] == player_code])

def check_winner(board, column, player_code, rows=ROWS, columns=COLUMNS, condition=CONNECT_X - 1):
    try:
        row = min([i for i in range(rows) if board[:, column][i] == player_code])

        # trecho adaptado do ambiente Kaggle
        def count(offset_row, offset_column):
            for i in range(1, condition + 1):
                r = row + offset_row * i
                c = column + offset_column * i
                if (r < 0 or r >= rows or c < 0 or c >= columns or board[r, c] != player_code):
                    return i - 1
            return condition

        return (
                count(1, 0) >= condition  # vertical.
                or (count(0, 1) + count(0, -1)) >= condition  # horizontal.
                or (count(-1, -1) + count(1, 1)) >= condition  # top left diagonal.
                or (count(-1, 1) + count(1, -1)) >= condition  # top right diagonal.
        )
    except:
        return False

def check_tie(board):
    return (0 in board)

def check_final_and_get_score(board, column, player_code, rows=ROWS, columns=COLUMNS, condition=CONNECT_X - 1, popout=True):

    if not(popout):
        if check_tie(board):
            return True, 0.5

    if check_winner(board, column, player_code, rows, columns, condition):
        return True, 1
    return False, None

def opponent_code(player_code):
    return 2 if player_code == 1 else 1

def opponent_score(player_score):
    # ja que eh um jogo de soma 1
    return 1 - player_score;

def UCT(total_score, total_visits, parent_total_visits, cp=CP):
    if total_visits == 0:
        return math.inf

    uct = total_score / total_visits + cp * math.sqrt(2 * math.log(parent_total_visits) / total_visits)
    return uct

def random_move(board, player_code, drop, rows=ROWS, columns=COLUMNS):
    if drop:
        try:
            column = random_put_in(board, columns)
            action = put_in(board, column, player_code, rows)
        except:
            column = random_pop_out(board, player_code, columns)
            action = pop_out(board, column, player_code, rows)
    else:
        try:
            column = random_pop_out(board, player_code, columns)
            action = pop_out(board, column, player_code, rows)
        except:
            column = random_put_in(board, columns)
            action = put_in(board, column, player_code, rows)

    return action, column

def random_move_without_popout(board, player_code, rows=ROWS, columns=COLUMNS):
    column = random_put_in(board, columns)
    action = put_in(board, column, player_code, rows)

    return action, column


def rule_for_simulation(board, player_code, rows=ROWS, columns=COLUMNS, condition=CONNECT_X - 1, popout=True):
    # simula um jogo aleatorio
    initial_player_code = player_code
    board = board.copy()
    if popout:
        _, column = random_move(board, player_code, drop=1, rows=rows, columns=columns)
    else:
        _, column = random_move_without_popout(board, player_code, rows=rows, columns=columns)
    final, score = check_final_and_get_score(board, column, player_code, rows, columns, condition, popout)

    while not final:
        player_code = opponent_code(player_code)
        if popout:
            _, column = random_move(board, player_code, drop=random.randint(0,1), rows=rows, columns=columns)
        else:
            _, column = random_move_without_popout(board, player_code, rows=rows, columns=columns)
        final, score = check_final_and_get_score(board, column, player_code, rows, columns, condition, popout)

    if initial_player_code == player_code:
        return score

    return opponent_score(score)

def get_opponent_action(after_board, before_board, rows=ROWS, columns=COLUMNS):
    for i in range(rows*columns):
        if(after_board.item(i) != before_board.item(i)):
            column = i % columns
            if np.any((after_board[1:, :] == before_board[:-1, :]) == False):
                return 'put', column
            else:
                return 'pop', column

    return None, -1
