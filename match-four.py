# WARNING: the terminal cleaning is only implemented for the macos terminal. Needs check on windows.
import os # to clean the terminal screen

GREEN = '\033[92m' # for x
RED = '\033[91m' # for o
ORANGE = '\033[38;5;215m' # for [!]
RESET = '\033[0m'

# game board arr: [[], [], [], ...] -> each [] being a row
# we only want to set it up once in main(). If set up more, it would override vals to []
board_setup = False 
def setup_board(row_num, col_num):
    global board
    board = [[] for i in range(row_num)]
    for i in board: # i is the row array, inside the 2d board array
        for j in range(col_num):
            i.append(' ')

def print_board(board_array):
    os.system("clear")
    # row numbers header
    for i in range (len(board[0])): # num of elems in the columns
        print(f"| [{i+1}] ", end="")
    print("|")

    print("|-----------------------------------------|")
    for i in board: # each row
        for j in i: # each column of each row
            if j == 'x':
                print(f"| [{GREEN}{j}{RESET}] ", end="")
            else:
                print(f"| [{RED}{j}{RESET}] ", end="")
        print(f"|") # for the closing of each row
    print("|-----------------------------------------|")
    print()

def show_win(player_turn):
    if player_turn == 0:
        print(f"{GREEN}{player[player_turn]}{RESET} Won!")
    else:
        print(f"{RED}{player[player_turn]}{RESET} Won!")

def update_board(col, turn):
    global board, game_in_progress, player, player_turn, free_row
    col -= 1 # converting user's 1-indexed number to 0-indexed

    if board[0][col] == ' ':
        for i in range(len(board) - 1, -1, -1):
            if board[i][col] == ' ':
                if turn == 0:
                    free_row = i
                    board[free_row][col] = 'x'
                    break
                else:
                    free_row = i
                    board[free_row][col] = 'o'
                    break
    else:
        print(f"{ORANGE}[!]{RESET} Column already full. Cannot insert.")
        # since main() is gonna flip the player turn, we do it once prior so that it undos it.
        # because if player 1 makes a mistake, we still want them to play their round.
        player_turn = not player_turn
        main()

    #### START - WIN CHECK SECTION ####
    # vertical - if 4 are on top of each other
    cont = 0 # continuous match counter of the signs (x/o)
    # make sure 3 rows below is not out of bound
    if free_row + 3 <= len(board) - 1:
        for i in range(free_row, free_row + 4): # check until 3 rows below where we just inserted  
            if board[i][col] == board[free_row][col]:
                cont += 1
                if cont == 4:
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # horizontal win (if you place x on the left of 3 other elements e.g: X,x,x,x (X just placed))
    # we did col -= 1, hence board[0] - 1 to convert both to 0-indexed
    cont = 0
    if col + 3 <= (len(board[0]) - 1):
        for i in range(col, col + 4):
            if board[free_row][i] == board[free_row][col]:
                cont += 1
                if cont == 4:
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # horizontal win (if you place the winning x on the right of 3 existing ones: x,x,x,X)
    cont = 0
    if col - 3 >= 0:
        for i in range (col, col - 4, -1):
            if board[free_row][i] == board[free_row][col]:
                cont += 1
                if cont == 4:
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # diagonal - check bottom left of what was just placed
    cont = 0
    if col - 3 >= 0 and free_row + 3 <= len(board) - 1:
        for i in range(free_row, free_row + 4):
            # (i - free_row) is the iteration number so that col could be calculated
            if board[i][col - (i - free_row)] == board[free_row][col]:
                cont += 1
                if cont == 4:
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # diagonal - top right of what was just placed
    cont = 0
    if col + 3 <= len(board[0]) - 1 and free_row - 3 >= 0:
        for i in range(free_row, free_row - 4, -1):
            # (i - free_row) is the iteration number so that col could be calculated
            # in this case col + ... so that we go forward in the column (from left->right)
            if board[i][col + (free_row - i)] == board[free_row][col]:
                cont += 1
                if cont == 4:
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # diagonal - check bottom right of what we just placed
    cont = 0
    if col + 3 <= len(board[0]) - 1 and free_row + 3 <= len(board) - 1:
        for i in range(free_row, free_row + 4):
            # (i - free_row) is the iteration number so that col could be calculated
            # in this case col + ... so that we go forward in the column (from left->right)
            if board[i][col + (i - free_row)] == board[free_row][col]:
                cont += 1
                if cont == 4:
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # diagonal - top left of where we just placed
    cont = 0
    if col - 3 >= 0 and free_row - 3 >= 0:
        for i in range(free_row, free_row - 4, -1):
            # (i - free_row) is the iteration number so that col could be calculated
            # in this case col + ... so that we go forward in the column (from left->right)
            if board[i][col - (free_row - i)] == board[free_row][col]:
                cont += 1
                if cont == 4:
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break
    #### END - WIN CHECK SECTION

player_turn = 1
def main():
    global player_turn, player
    player = ["X", "O"]
    player_turn = not player_turn
    if player_turn == 0:
        print(f"{GREEN}{player[player_turn]}{RESET}'s turn.")
    else:
        print(f"{RED}{player[player_turn]}{RESET}'s turn.")

    while True:
        selected_col = input("Enter the slot's column number: ") # [!] 1-indexed
        try:
            selected_col = int(selected_col)
            while selected_col not in range(1, len(board[0]) + 1):
                selected_col = int(input("Invalid entry. Enter the slot's column number: "))
            break
        except ValueError:
            print("Only enter a number.")

    update_board(selected_col, player_turn)


game_in_progress = True
while(game_in_progress):

    if not board_setup:
        setup_board(6, 7)
        board_setup = True
    print_board(board)
    main()
    # game_in_progress = False
