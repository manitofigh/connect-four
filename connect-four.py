import os # to clean the terminal screen
from time import sleep

GRN = '\033[92m' # for x
RED = '\033[91m' # for o
ORNG = '\033[38;5;215m' # for [!]
RST = '\033[0m'

# game board arr: [[], [], [], ...] -> each [] being a row
# we only want to set it up once in main(). If set up more, it would override vals to []
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

    separator = "|" + "-" * (6*n_cols - 1) + "|"
    print(separator)
    for i in board: # each row
        for j in i: # each column of each row
            if j == 'x':
                print(f"| [{GRN}{j}{RST}] ", end="")
            # The X-es that connect four are detected in caps
            elif j == 'X':
                j = 'x'
                print(f"| {ORNG}[{RST}{GRN}{j}{RST}{ORNG}]{RST} ", end="")
            elif j == 'o':
                print(f"| [{RED}{j}{RST}] ", end="")
            # The O-es that connect four are detected in caps
            elif j == 'O':
                j = 'o'
                print(f"| {ORNG}[{RST}{RED}{j}{RST}{ORNG}]{RST} ", end="")
            else:
                print(f"| [{j}] ", end="")
        print("|") # for the closing of each row
    print(separator)
    print()

def show_win(player_turn):
    if player_turn == 0:
        print(f"{GRN}{player[player_turn]}{RST} Won!")
    else:
        print(f"{RED}{player[player_turn]}{RST} Won!")

def update_board(col, turn):
    global board, game_in_progress, player, player_turn, cur_chosen_row
    col -= 1 # converting user's 1-indexed number to 0-indexed

    if board[0][col] == ' ':
        for i in range(len(board) - 1, -1, -1):
            if board[i][col] == ' ':
                cur_chosen_row = i
                break

        # start - falling animation
        for j in range(0, cur_chosen_row):
            if turn == 0:
                board[j][col] = 'x'
                print_board(board)
                sleep(0.05)
                board[j][col] = ' '
            else:
                board[j][col] = 'o'
                print_board(board)
                sleep(0.05)
                board[j][col] = ' '
        # end - falling animation

        if turn == 0:
            board[cur_chosen_row][col] = 'x'
        else:
            board[cur_chosen_row][col] = 'o'

    else:
        print(f"{ORNG}[!]{RST} Column already full. Cannot insert.")
        # since main() is gonna flip the player turn, we do it once prior so that it undos it.
        # because if player 1 makes a mistake, we still want them to play their round.
        player_turn = not player_turn
        main()

    #### START - WIN CHECK SECTION ####
    # vertical - if 4 are on top of each other (the only case for vertical is to place last one on top)
    cont = 0 # continuous match counter of the signs (x/o)
    # make sure 3 rows below is not out of bound
    if cur_chosen_row + 3 <= len(board) - 1:
        for i in range(cur_chosen_row, cur_chosen_row + 4): # check until 3 rows below where we just inserted  
            if board[i][col] == board[cur_chosen_row][col]:
                cont += 1
                if cont == 4:
                    # capital x/o would are the winning pieces
                    # when printing the board, they'd be printed with
                    # golden brackets to show the winning path
                    for i in range(cur_chosen_row, cur_chosen_row + 4):
                        if turn == 0:
                            board[i][col] = "X"
                        else:
                            board[i][col]= "O"
                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # START - horizontal win check
    # There is always the chance for a placement to be a horizontal win, so no `if` checks
    # check both ways from where dropped until the opposite sign found, and count continuity
    # right side cap, either the edge (last col#) or 3 to the right
    r_cap = n_cols if col + 3 >= n_cols else col + 4 # !careful: r_cap is 1-indexed
    l_cap = -1 if col - 3 <= 0 else col - 4 # !careful: l_cap is 1-indexed
    cont = 0
    for i in range(col + 1, r_cap): # r_cap already 1-indexed so already takes into account `range`'s exclusiveness
        if board[cur_chosen_row][i] == board[cur_chosen_row][col]:
            cont += 1
            if cont == 3:
                print_board(board)
                show_win(player_turn)
                game_in_progress = False
        else:
            break

    for i in range(col - 1, l_cap, -1):
        if board[cur_chosen_row][i] == board[cur_chosen_row][col]:
            cont += 1
            if cont == 3:
                print_board(board)
                show_win(player_turn)
                game_in_progress = False
        else:
            break
    # END - horizontal win check

    # START - diagonal: bottom left to top right win check
    t_cap = -1 if cur_chosen_row - 3 <= 0 else cur_chosen_row - 3 # top cap
    b_cap = n_rows if cur_chosen_row + 3 >= n_rows else n_rows + 3 # bottom cap
    tr_cap = 
    print(f"top right cap: {tr_cap}")
    sleep(5)
    bl_cap = min(b_cap, l_cap) # bottom left cap
    print(f"bottom left cap: {bl_cap}")
    sleep(5)
    cont = 0
    if tr_cap + bl_cap >= 3:
        # checking bottom left
        for i in range(cur_chosen_row, cur_chosen_row + bl_cap):
            n_iter = i - cur_chosen_row
            if board[i][col - iter] == board[i][col]:
                cont += 1
                if cont == 3:
                    print_board(board)
                    show_win(player_turn)
                    game_in_progress = False
                else:
                    break

        # checking top right
        for i in range(cur_chosen_row, cur_chosen_row - tr_cap, -1):
            n_iter = cur_chosen_row - i
            if board[i][col + n_iter] == board[i][cur_chosen_row]:
                cont += 1
                if cont == 3:
                    print_board(board)
                    show_win(player_turn)
                    game_in_progress = False
            else:
                break



    # START - diagonal: top left to bottom right win check
    cont = 0
    if col + 3 <= len(board[0]) - 1 and cur_chosen_row - 3 >= 0:
        for i in range(cur_chosen_row, cur_chosen_row - 4, -1):
            # (i - cur_chosen_row) is the iteration number so that col could be calculated
            # in this case col + ... so that we go forward in the column (from left->right)
            if board[i][col + (cur_chosen_row - i)] == board[cur_chosen_row][col]:
                cont += 1
                if cont == 4:
                    for i in range(cur_chosen_row, cur_chosen_row - 4, -1):
                        if turn == 0:
                            board[i][col + (cur_chosen_row - i)] = 'X'
                        else:
                            board[i][col + (cur_chosen_row - i)] = 'O'

                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # diagonal - check bottom right of what we just placed
    cont = 0
    if col + 3 <= len(board[0]) - 1 and cur_chosen_row + 3 <= len(board) - 1:
        for i in range(cur_chosen_row, cur_chosen_row + 4):
            # (i - cur_chosen_row) is the iteration number so that col could be calculated
            # in this case col + ... so that we go forward in the column (from left->right)
            if board[i][col + (i - cur_chosen_row)] == board[cur_chosen_row][col]:
                cont += 1
                if cont == 4:
                    for i in range(cur_chosen_row, cur_chosen_row + 4):
                        if turn == 0:
                            board[i][col + (i - cur_chosen_row)] = 'X'
                        else:
                            board[i][col + (i - cur_chosen_row)] = 'O'

                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # diagonal - top left of where we just placed
    cont = 0
    if col - 3 >= 0 and cur_chosen_row - 3 >= 0:
        for i in range(cur_chosen_row, cur_chosen_row - 4, -1):
            # (i - cur_chosen_row) is the iteration number so that col could be calculated
            # in this case col + ... so that we go forward in the column (from left->right)
            if board[i][col - (cur_chosen_row - i)] == board[cur_chosen_row][col]:
                cont += 1
                if cont == 4:
                    for i in range(cur_chosen_row, cur_chosen_row - 4, -1):
                        if turn == 0:
                            board[i][col - (cur_chosen_row - i)] = 'X'
                        else:
                            board[i][col - (cur_chosen_row - i)] = 'O'

                    print_board(board)
                    game_in_progress = False
                    show_win(player_turn)
            else:
                break

    # Draw
    filled_col = 0
    for i in range(0, n_cols):
        if board[0][i] != ' ':
            filled_col += 1
        if filled_col == n_cols:
            print_board(board)
            print("Draw!")
            game_in_progress = False

    #### END - WIN CHECK SECTION ####



player_turn = 1


def main():
    global player_turn, player
    player = ["X", "O"]
    player_turn = not player_turn
    if player_turn == 0:
        print(f"{GRN}{player[player_turn]}{RST}'s turn.")
    else:
        print(f"{RED}{player[player_turn]}{RST}'s turn.")
    print(f"Press {RED}q{RST} to quit.")

    while True:
        selected_col = input("Choose a column number: ")  # [!] 1-indexed
        try:
            if selected_col == 'q':
                exit()
            selected_col = int(selected_col)
            while selected_col not in range(1, len(board[0]) + 1):
                selected_col = int(input("Invalid range. Choose a column number: "))
            break
        except ValueError:
            print("Only enter a number.")

    update_board(selected_col, player_turn)

board_setup = False 
game_in_progress = True
global n_cols
while (game_in_progress):
    if not board_setup:
        os.system("clear")
        while True:
            try:
                n_rows = int(input("How many rows for the board (min 4, max 18)? "))
                while n_rows < 4 or n_rows > 18:
                    n_rows = int(input("Invalid range. How many rows for the board (min 4, max 18)? "))

                n_cols = int(input("How many columns for the board (min 4, max 9)? "))
                while n_cols < 4 or n_cols > 9:
                    n_cols = int(input("Invalid range. How many columns for the board (min 4, max 9)? "))

                break
            except ValueError:
                print("Only enter numbers.")
        setup_board(n_rows, n_cols)
        board_setup = True
    print_board(board)
    main()
