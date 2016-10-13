import socket
import connectfour
import console
import userfunctions
import online

def start_client():#Run after connecting to server & receiving 'READY'
    game = userfunctions.start_game()

def user_move(game: connectfour.GameState, c: socket.socket)-> connectfour.GameState:
    move = userfunctions.get_move()
    col = userfunctions.int_input()
    if move == 0:
        game = userfunctions.catch_pop(game, col)
    elif move == 1:
        game = userfunctions.catch_drop(game, col)
    userfunctions.display_board(game)
    online.send_move(c, col, move)
    return game

def server_move(game: connectfour.GameState, c: socket.socket)-> connectfour.GameState:
    move = online.recv_move(c)
    if move < 10 and move >= 0:
        col = move
        game = userfunctions.catch_pop(game, col)
        userfunctions.display_board(game)
        return game
    elif move > 10:
        col = move - 10
        game = userfunctions.catch_drop(game, col)
        userfunctions.display_board(game)
        return game
    elif move == -1: #invalid move
        userfunctions.display_board(game)
        return game
    elif move == -2: #game over
        return game

def main():
    user = online.input_username()
    c = online.input_host()
    if c == None:
        print('FATAL ERROR: Failed to connect')
        return
    online.ics_connect(c,user)
    game = userfunctions.start_game()
    while userfunctions.check_winner(game) is False:
        game = user_move(game, c)
        if userfunctions.check_winner(game) is True:
            break
        game = server_move(game, c)


if __name__ == '__main__':
    main()
