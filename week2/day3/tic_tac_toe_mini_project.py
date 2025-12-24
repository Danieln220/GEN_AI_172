
def my_board():
    return [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]



def display_board(board):
    
    for row in board:
        print(" | ".join(row))
        print("---------")
    



def player_input(board, player):
    while True:
        
            row = int(input(f"Player {player} enter row (1-3): ")) - 1
            col = int(input(f"Player {player} enter column (1-3): ")) - 1

            if row in range(3) and col in range(3):
                if board[row][col] == " ":
                    return row, col
                else:
                    print("That spot is already taken. Try again.")
            else:
                print("Row and column must be between 1 and 3.")
        
            



def check_win(board, player):
    
    for row in board:
        if row[0] == row[1] == row[2] == player:
            return True

    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False



def check_tie(board):
    for row in board:
        if " " in row:
            return False
    return True



def play():
    board = my_board()
    player = "X"

    while True:
        display_board(board)

        row, col = player_input(board, player)
        board[row][col] = player

        if check_win(board, player):
            display_board(board)
            print(f"Player {player} wins!")
            break

        if check_tie(board):
            display_board(board)
            print("Its a tie!")
            break

        
        if player == "X":
            player = "O"
        else:
            player = "X"



play()