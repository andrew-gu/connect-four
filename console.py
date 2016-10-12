import connectfour
import userfunctions



def get_move()->int:
    move = input('Pop or Drop? (P/D)')
    if move == 'P':
        return 0
    elif move == 'D':
        return 1
    else:
        print('ERROR: Invalid Input')
        return get_move()

def main():
    game = userfunctions.start_game()
    while True:
        move = get_move()
        if move == 0:
            game = userfunctions.player_pop(game)
        elif move == 1:
            game = userfunctions.player_drop(game)
        try:
            connectfour.drop(game,0)
        except connectfour.GameOverError:
            winner = connectfour.winner(game)
            print('Game Over')
            if winner == 1:
                print('Red Wins')
            elif winner == 2:
                print('Yellow Wins')
            break



if __name__ == '__main__':
    main()
