import connectfour

def start_game()->connectfour.GameState:
    game = connectfour.new_game()
    display_board(game)
    return game



def catch_drop(game: connectfour.GameState, col: int)->connectfour.GameState:
    try:
        game = connectfour.drop(game, col)
    except ValueError:
        print('ERROR: Invalid Column')
    except connectfour.InvalidMoveError:
        print('ERROR: Invalid Move')
    except connectfour.GameOverError:
        print('Game Over')
    finally:
        return game


def catch_pop(game:connectfour.GameState, col: int) -> connectfour.GameState:
    try:
        game = connectfour.pop(game, col)
    except ValueError:
        print('ERROR: Invalid Column')
    except connectfour.InvalidMoveError:
        print('ERROR: Invalid Move')
    except connectfour.GameOverError:
        print('Game Over')
    finally:
        return game

def int_input()->int:
    result = int()
    try:
        result = int(input('Select a column (1-7): '))
    except (TypeError, ValueError):
        print('ERROR: Invalid Input')
        return int_input()
    else:
        return result - 1

def display_board(g: connectfour.GameState):
    '''Displays current board when called'''
    col_array = g.board
    for n in range(1, connectfour.BOARD_COLUMNS+1): #display col #s
        print(n, end=' ')
    print()
    for i in range(0, connectfour.BOARD_ROWS): #displays board
        for col in col_array:
            if col[i] == 0:
                print('.', end=' ')
            elif col[i] == 1:
                print('R', end=' ')
            elif col[i] == 2:
                print('Y', end=' ')
        print()

def get_move()->int:
    move = input('Pop or Drop? (P/D)')
    if move == 'P':
        return 0
    elif move == 'D':
        return 1
    else:
        print('ERROR: Invalid Input')
        return get_move()

def check_winner(game: connectfour.GameState)->bool:
    try:
        connectfour.drop(game,0)
        return False
    except connectfour.GameOverError:
        winner = connectfour.winner(game)
        print('Game Over')
        if winner == 1:
            print('Red Wins')
        elif winner == 2:
            print('Yellow Wins')
        return True
