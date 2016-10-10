import connectfour

def player_drop(game: connectfour.GameState) -> connectfour.GameState: #better implementation using catch_drop, but not catching exceptions
    col = _int_input()
    game = _catch_drop(game, col)
    display_board(game)
    return game

def _catch_drop(game: connectfour.GameState, col: int)->connectfour.GameState:
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

def player_pop(game: connectfour.GameState) -> connectfour.GameState:
    col = _int_input()
    game = _catch_pop(game, col)
    display_board(game)
    return game

def _catch_pop(game:connectfour.GameState, col: int) -> connectfour.GameState:
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

def _int_input()->int:
    result = int()
    try:
        result = int(input('Select a column (1-7): '))
    except (TypeError, ValueError):
        print('ERROR: Invalid Input')
        return _int_input()
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
