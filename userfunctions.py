import connectfour

def start_game()->connectfour.GameState:
    '''
    creates new game and displays a blank board
    '''
    game = connectfour.new_game()
    display_board(game)
    return game



def catch_drop(game: connectfour.GameState, col: int)->connectfour.GameState:
    '''
    Drops a piece in a given column and returns any possible errors
    '''
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
    '''
    pops a piece from a given column and returns any possible errors
    '''
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
    '''
    Asks for a valid input for a column
    '''
    result = int()
    valid = False
    while not valid:
        try:
            result = int(input('Select a column (1-7): '))
            #if result not in range(1,8):
            #    print('ERROR: Invalid Column')
            #else:
            valid = True
        except (TypeError, ValueError):
            print('ERROR: Invalid Input')

    return result - 1#connect four library functions are 0-indexed

def display_board(game: connectfour.GameState):

    '''Displays current board when called'''
    col_array = game.board
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
    '''
    Asks user for choice of move
    '''
    move = input('Pop or Drop? (P/D)').upper()
    if move == 'P':
        return 0
    elif move == 'D':
        return 1
    else:
        print('ERROR: Invalid Input')
        return get_move()

def check_winner(game: connectfour.GameState)->bool:
    '''
    Checks for a winner in the current gamestate by trying to drop in a column
    '''
    try:
        for i in range(0,7):
            try:
                connectfour.drop(game, i)
            except connectfour.InvalidMoveError:
                pass
        return False
    except connectfour.GameOverError:
        winner = connectfour.winner(game)
        print('Game Over')
        if winner == 1:
            print('Red Wins')
        elif winner == 2:
            print('Yellow Wins')
        return True
