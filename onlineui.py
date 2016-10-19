import connectfour
import userfunctions
import online

def user_move(game: connectfour.GameState, client: online.Client)-> connectfour.GameState:
    '''
    makes a move in the client-side game board and sends the move to the server
    '''
    move = userfunctions.get_move()
    col = userfunctions.int_input()
    if move == 0:
        game = userfunctions.catch_pop(game, col)
    elif move == 1:
        game = userfunctions.catch_drop(game, col)
    userfunctions.display_board(game)
    online.send_move(client, col + 1, move)#add 1 because int_input subtracts 1
    return game

def server_move(game: connectfour.GameState, client: online.Client)-> connectfour.GameState:
    '''
    Accepts a move from the server and updates it in the client side game board
    '''
    move = online.parse_msg(client)
    if move[1] >= 0:
        if move[0] < 10:
            col = move[0]
            game = userfunctions.catch_pop(game, col)
            userfunctions.display_board(game)
            return game
        elif move[0] >= 10:
            col = move[0] - 10
            game = userfunctions.catch_drop(game, col)
            userfunctions.display_board(game)
            return game
        elif move[0] == -1:
            userfunctions.display_board(game)
            return game


def main():
    client = online.input_host()
    if client == None:
        print('FATAL ERROR: Failed to connect')
        return
    try:
        online.ics_connect(client)
    except ValueError:
        print('FATAL ERROR: Connection closed')
        return
    game = userfunctions.start_game()
    while userfunctions.check_winner(game) is False:
        try:
            game = user_move(game, client)
            if userfunctions.check_winner(game) is True:
                break
            game = server_move(game, client)
        except ValueError:
            print('FATAL ERROR: Connection closed')
            break

    online.close_client(client)

if __name__ == '__main__':
    main()
