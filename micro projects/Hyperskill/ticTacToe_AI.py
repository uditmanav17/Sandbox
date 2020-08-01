# https://hyperskill.org/projects/82
import random

# BOARD MAPPING
# 13 23 33
# 12 22 32
# 11 21 31


tup_ind_map = dict(
    zip([(x, y) for y in range(3, 0, -1) for x in range(1, 4)], range(9))
)


def display_field(field: str):
    print("---------")
    print("| {} {} {} |\n| {} {} {} |\n| {} {} {} |".format(*field.replace("_", " ")))
    print("---------")


def row_win(field: str):
    for i in [0, 3, 6]:
        if "XXX" in field[i : i + 3] or "OOO" in field[i : i + 3]:
            return True
    return False


def col_win(field: str):
    for i in range(3):
        if (
            field[i] == field[i + 3] == field[i + 6] == "X"
            or field[i] == field[i + 3] == field[i + 6] == "O"
        ):
            return True
    return False


def diag_win(field: str):
    diagonal_1 = (field[0] == field[4] == field[8]) and field[0] != "_"
    diagonal_2 = (field[2] == field[4] == field[6]) and field[2] != "_"
    if diagonal_1 or diagonal_2:
        return True
    return False


def check_win(field: str):
    conditions = [row_win(field), col_win(field), diag_win(field)]
    # print(conditions)
    if any(conditions):
        return True
    return False


def make_move(field: str, player: str, move_idx: int):
    field = list(field)
    field[move_idx] = player
    return "".join(field)


def user_input(field: str, player: str):
    """takes input from user and validate it """
    while True:
        coords = input("Enter the coordinates: > ")
        try:
            x, y = [int(i) for i in coords.split()]
            if x < 1 or x > 3 or y < 1 or y > 3:
                print("Coordinates should be from 1 to 3!")
            elif field[tup_ind_map[(x, y)]] != "_":
                print("This cell is occupied! Choose another one!")
            else:
                field = make_move(field, player, tup_ind_map[(x, y)])
                break
        except:
            print("You should enter numbers!")
    return field


def get_player(field: str):
    """ based on state of field returns whether to put X or O, assuming X always goes first"""
    if field.count("X") == field.count("O"):
        return "X"
    return "O"


def check_game_state(field: str, player: str):
    if "_" not in field:
        return "Draw"
    elif check_win(field):
        return f"{player} wins"
    else:
        return "Game not finished"


# -----------------------------------------------------  2/5  --------------------------------------------------


def computer_easy(field: str, player: str):
    avail_choices = [ind for ind, val in enumerate(field) if val == "_"]
    selected_choice = random.choice(avail_choices)
    field = list(field)
    field[selected_choice] = player
    field = "".join(field)
    # print_mat(inp)
    return field


def person_or_comp(player_level: str):
    players = {
        "user": user_input,
        "easy": computer_easy,
        "medium": computer_medium,
        "hard": computer_hard,
    }
    return players.get(player_level)


def start_game_bw_players(player1, player2):
    field = "_________"
    p1_tag, p2_tag = player1, player2
    tags2display = ("easy", "medium", "hard")
    player1 = person_or_comp(player1)
    player2 = person_or_comp(player2)
    display_field(field)
    while True:
        player = get_player(field)
        field = player1(field, player)
        # field = computer_easy(field, player)
        if p1_tag in tags2display:
            print(f'Making move level "{p1_tag}"')
        game_state = check_game_state(field, player)
        # print(game_state, field)
        display_field(field)
        game_win_or_draw = ("wins" in game_state) or ("Draw" in game_state)
        if game_win_or_draw:
            break

        player = get_player(field)
        field = player2(field, player)
        if p2_tag in tags2display:
            print(f'Making move level "{p2_tag}"')
        game_state = check_game_state(field, player)
        display_field(field)
        game_win_or_draw = ("wins" in game_state) or ("Draw" in game_state)
        if game_win_or_draw:
            break

    print(game_state)


def check_row_win(inp: str, player: str):
    winning_row = ""
    rows = [inp[i : i + 3] for i in [0, 3, 6]]
    for row in rows:
        player_counts = row.count(player)
        empty_space = row.count("_")
        if player_counts == 2 and empty_space == 1:
            winning_row = row
            break
    return winning_row


def computer_medium(inp: str, player: str):
    players = ("X", "O")
    opponent = players[int(not players.index(player))]

    winning_row = check_row_win(inp, player)
    if winning_row:
        win_row_index = inp.index(winning_row)
        inp = inp.replace(inp[win_row_index : win_row_index + 3], player * 3)
        return inp

    losing_row = check_row_win(inp, opponent)
    if losing_row:
        lose_row_index = inp.index(losing_row)
        move = inp[lose_row_index : lose_row_index + 3].replace("_", player)
        inp = inp.replace(inp[lose_row_index : lose_row_index + 3], move)
        return inp
    inp = computer_easy(inp, player)
    return inp


################### comp hard ###################
def evaluate_field(field: str, player: str):
    # check row win
    for row_ind in [0, 3, 6]:
        row = field[row_ind : row_ind + 3]
        if row[0] == row[1] == row[2]:
            if row[0] == player:
                return 10
            if row[0] == "_":
                pass
            else:
                return -10

    # check column win
    for col_ind in [0, 1, 2]:
        col = field[col_ind : col_ind + 7 : 3]
        if col[0] == col[1] == col[2]:
            if col[0] == player:
                return 10
            if col[0] == "_":
                pass
            else:
                return -10

    # check diagonal win
    if field[0] == field[4] == field[8] or field[2] == field[4] == field[6]:
        if field[4] == player:
            return 10
        if field[4] == "_":
            pass
        else:
            return -10

    # if no one wins
    return 0


# print(evaluate_field("__XXXXO_O", "O"))
# print(evaluate_field("__XXXXO_O", "X"))
# print(evaluate_field("X_O_XO__X", "X"))
# print(evaluate_field("X_O_OO__X", "X"))


def minimax(field: str, depth: int, isMax: bool, player: str):
    players = ("X", "O")
    opponent = players[int(not players.index(player))]

    score = evaluate_field(field, player)
    # maximizer/minimizer won
    if score in (10, -10):
        return score
    # no moves left
    if "_" not in field:
        return 0

    # if maximizer's turn
    if isMax:
        best = float("-inf")
        for indx, pos in enumerate(field):
            if pos == "_":
                field = make_move(field, player, indx)
                best = max(best, minimax(field, depth + 1, not isMax, player))
                # undo move
                field = make_move(field, "_", indx)
        return best
    else:
        best = float("inf")
        for indx, pos in enumerate(field):
            if pos == "_":
                field = make_move(field, opponent, indx)
                best = min(best, minimax(field, depth + 1, not isMax, player))
                # undo move
                field = make_move(field, "_", indx)
        return best


# print(minimax(field:str, depth:int, isMax:bool, player:str))
# print(minimax("XOXXOO___", 2, True, "X"))
# print(minimax("XOXXOO___", 2, False, "X"))


def make_best_move(field: str, player: str):
    best_val = float("-inf")
    best_move = -1
    for indx, pos in enumerate(field):
        if pos == "_":
            field = make_move(field, player, indx)
            move_val = minimax(field, 0, False, player)
            field = make_move(field, "_", indx)

            if move_val > best_val:
                best_val = move_val
                best_move = indx
    return best_move


def computer_hard(field: str, player: str):
    best_move_loc = make_best_move(field, player)
    field = make_move(field, player, best_move_loc)
    return field


valid_players = ("user", "easy", "medium", "hard")
while True:
    commands = input("Input command: > ").strip().split()
    # print(commands)
    if commands[0] == "exit":
        break
    elif len(commands) != 3:
        print("Bad parameters!")
    elif commands[0] == "start":
        if commands[1] in valid_players and commands[2] in valid_players:
            start_game_bw_players(commands[1], commands[2])
        else:
            print("Bad parameters!")

