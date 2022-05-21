# --- Piece-Square Tables --- used to give pieces a bonus for moving in a certain way and penalties for moving in
# other ways (for evaluation method) tables are taken from Tomasz Michniewski's article "Simplified Evaluation
# Function" (the tables are not mirrored for black)

pawn = (70, 70, 70, 70, 70, 70, 70, 70,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0)
knight = (-50, -40, -30, -30, -30, -30, -40, -50,
          -40, -20, 0, 0, 0, 0, -20, -40,
          -30, 0, 10, 15, 15, 10, 0, -30,
          -30, 5, 15, 20, 20, 15, 5, -30,
          -30, 0, 15, 20, 20, 15, 0, -30,
          -30, 5, 10, 15, 15, 10, 5, -30,
          -40, -20, 0, 5, 5, 0, -20, -40,
          -50, -40, -30, -30, -30, -30, -40, -50)
bishop = (-20, -10, -10, -10, -10, -10, -10, -20,
          -10, 0, 0, 0, 0, 0, 0, -10,
          -10, 0, 5, 10, 10, 5, 0, -10,
          -10, 5, 5, 10, 10, 5, 5, -10,
          -10, 0, 10, 10, 10, 10, 0, -10,
          -10, 10, 10, 10, 10, 10, 10, -10,
          -10, 5, 0, 0, 0, 0, 5, -10,
          -20, -10, -10, -10, -10, -10, -10, -20)
rook = (0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0)
queen = (-20, -10, -10, -5, -5, -10, -10, -20,
         -10, 0, 0, 0, 0, 0, 0, -10,
         -10, 0, 5, 5, 5, 5, 0, -10,
         -5, 0, 5, 5, 5, 5, 0, -5,
         0, 0, 5, 5, 5, 5, 0, -5,
         -10, 5, 5, 5, 5, 5, 0, -10,
         -10, 0, 5, 0, 0, 0, 0, -10,
         -20, -10, -10, -5, -5, -10, -10, -20)
king_midgame = (-30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20)
king_endgame = (-50, -40, -30, -20, -20, -30, -40, -50,
                -30, -20, -10, 0, 0, -10, -20, -30,
                -30, -10, 20, 30, 30, 20, -10, -30,
                -30, -10, 30, 40, 40, 30, -10, -30,
                -30, -10, 30, 40, 40, 30, -10, -30,
                -30, -10, 20, 30, 30, 20, -10, -30,
                -30, -30, 0, 0, 0, 0, -30, -30,
                -50, -30, -30, -30, -30, -30, -30, -50)


# simple utility functions (shortens the code)
def get_type(val):
    # method returns the type of received value
    if val != 0:
        return int(divmod(abs(val), 10)[0] * (val / abs(val)))
    return 0


def is_same_color(val1, val2):
    # method checks if 2 values are of same color
    if (val1 > 0 and val2 > 0) or (val1 < 0 and val2 < 0):
        return True
    return False


def name_to_val(str):
    # method returns an integer value of a piece by name
    if str == "p":
        return 1
    elif str == "n":
        return 2
    elif str == "b":
        return 3
    elif str == "r":
        return 4
    elif str == "q":
        return 5
    elif str == "k":
        return 6
    return 0


def is_valid(i, j):
    # method returns True if the pos is in the board and False otherwise
    return 0 <= i < 8 and 0 <= j < 8


def get_new_val(val):
    # method adds to the move count of a piece
    if divmod(abs(val), 10)[1] != 2:
        if val > 0:
            return val + 1
        return val - 1
    return val



def get_score_value(val):
    # method returns score value for each peace type
    score_values = (100, 320, 330, 500, 900, 20000)
    return score_values[abs(get_type(val)) - 1]


def is_castle_move(fj, tj):
    # method determines if a move is a castling move
    return fj == 4 and (tj == 6 or tj == 2)


def get_go_message(event, player):
    # method returns a game over message
    message_str = ""
    if event == 1:
        return "Draw"
    elif event == 2:
        message_str = "Mate for "
    elif event == 3:
        message_str = "Stalemate for "
    if player == 1:
        return message_str + "black"
    return message_str + "white"


# --- board comparison / evaluation ---
def translate_fen(fen):
    # method receives a fen string and translates it into an actual board setting
    b = [[], [], [], [], [], [], [], []]
    row = 0
    i = 0
    while fen[i] != " ":  # translating the overall board
        if row == 8:
            break
        if fen[i].isdigit():
            for add_empty in range(int(fen[i])):
                b[row].append(0)
        elif fen[i] == "/" or fen[i] == " ":
            row += 1
        else:
            if fen[i].islower():
                b[row].append(name_to_val(fen[i]) * 10)
            else:
                b[row].append(name_to_val(fen[i].lower()) * (-10))
        i += 1
    i += 1
    i += 2
    # making all castling impossible unless said so in FEN
    if b[0][0] == 40:  # br0
        b[0][0] = 41
    if b[0][7] == 40:  # br0
        b[0][7] = 41
    if b[7][0] == -40:  # wr0
        b[7][0] = -41
    if b[7][7] == -40:  # wr0
        b[7][7] = -41
    while fen[i] != " ":  # correcting board for castling
        if fen[i] == "K" and b[7][7] == -41:
            b[7][7] = -40
        elif fen[i] == "Q" and b[7][0] == -41:
            b[7][0] = -40
        elif fen[i] == "k" and b[0][7] == 41:
            b[0][7] = 40
        elif fen[i] == "q" and b[0][0] == 41:
            b[0][0] = 40
        i += 1
    return b


def get_pst_val(val, i, j, endgame):
    # method receives type of piece and game phase (if endgame) returns correct piece-value table
    if val < 0:
        idx = i * 8 + j
    else:
        idx = 63 - (i * 8 + j)  # count from end (reverses the pst for black)
    val = abs(val)
    if val == 1:
        return pawn[idx]
    elif val == 2:
        return knight[idx]
    elif val == 3:
        return bishop[idx]
    elif val == 4:
        return rook[idx]
    elif val == 5:
        return queen[idx]
    elif val == 6:
        if endgame:
            return king_endgame[idx]
        return king_midgame[idx]


def is_endgame(b):
    # if 3 or less pieces remain (except pawns and kings) return true
    w_counter = 0
    b_counter = 0
    for i in range(8):
        for j in range(8):
            val = abs(get_type(b[i][j]))
            if val != 1 and val != 6:
                if b[i][j] < 0:
                    w_counter += 1
                else:
                    b_counter += 1
    return w_counter <= 3 or b_counter <= 3


# --- getting moves ---
def get_moves(b, i, j):
    # get moves for all pieces apart from pawns and the kings
    moves = []
    val = divmod(abs(b[i][j]), 10)[0]
    if val == 1:
        moves = get_pawn_moves(b, i, j)
    elif val == 2:
        moves = get_knight_moves(i, j)
    elif val == 3:
        moves = get_bishop_moves(b, i, j)
    elif val == 4:
        moves = get_rook_moves(b, i, j)
    elif val == 5:
        moves = get_queen_moves(b, i, j)
    elif val == 6:
        moves = get_king_moves(b, i, j)
    new_moves = []

    for move in moves:
        if is_valid(move[2], move[3]):
            if not is_same_color(b[move[2]][move[3]], b[i][j]):
                new_moves.append(move)
    return new_moves


def get_all_moves(b, color):
    # method returns all of the moves of the pieces in received board of received color
    moves = []
    for i in range(8):
        for j in range(8):
            if is_same_color(b[i][j], color):  # if piece is of received color
                moves.extend(get_moves(b, i, j))  # add to array of all moves
    return moves


def get_pawn_moves(b, i, j):
    # method receives board and the pos of a pawn and returns all it's possible moves
    moves = []
    diff = 1
    opponent = -1
    val = b[i][j]
    if val < 0:
        diff = -1
        opponent = 1

    # move 1, 2 forward
    if is_valid(i + diff, j) and b[i + diff][j] == 0:
        moves.append((i, j, i + diff, j))  # move 1 forward
    if ((i == 6 and val < 0) or (i == 1 and val > 0)) and b[i + diff][j] == 0 and b[i + (diff * 2)][j] == 0:
        moves.append((i, j, i + (diff * 2), j))  # move 2 forward
    # diagonal capture
    for col in range(j - 1, j + 2, 2):
        if is_valid(i + diff, col) and is_same_color(b[i + diff][col], opponent):
            moves.append((i, j, i + diff, col))

    # en passant
    if (val < 0 and i == 3) or (val > 0 and i == 4):  # if white on row 3 or black on row 4
        for col in range(j - 1, j + 2, 2):
            if is_valid(i, col) and b[i][col] == 11 * opponent and (
                    (is_valid(i + diff, col) and b[i + diff][col] == 0) or not is_valid(i + diff, col)):
                moves.append((i, j, i + diff, col))  # left en passant
    return moves


def get_knight_moves(i, j):
    # method returns all possible moves for a knight at received position
    # validity is checked in general "get_moves" method
    moves = [(i, j, i + 2, j + 1), (i, j, i + 2, j - 1), (i, j, i - 2, j + 1), (i, j, i - 2, j - 1),
             (i, j, i + 1, j + 2), (i, j, i - 1, j + 2), (i, j, i + 1, j - 2), (i, j, i - 1, j - 2)]
    return moves


def get_bishop_moves(b, i, j):
    # method returns all possible moves of bishop in received board at received position
    moves = []
    row = i
    col = j
    instructions = ((1, 1), (-1, -1), (1, -1), (-1, 1))
    # going in all 4 directions until end of board or piece is reached
    for direction in range(4):
        while is_valid(row, col) and (b[row][col] == 0 or (row == i and col == j)):
            row += instructions[direction][0]
            col += instructions[direction][1]
            moves.append((i, j, row, col))
        row = i
        col = j
    return moves


def get_rook_moves(b, i, j):
    # method gets all possible moves of rook in received board at received position
    moves = []
    row = i
    col = j
    instructions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    # going in all 4 directions until end of board or piece is reached
    for direction in range(4):
        while is_valid(row, col) and (b[row][col] == 0 or (row == i and col == j)):
            row += instructions[direction][0]
            col += instructions[direction][1]
            moves.append((i, j, row, col))
        row = i
        col = j
    return moves


def get_queen_moves(b, i, j):
    # method returns all possible moves of a queen in received board at received position
    moves = get_rook_moves(b, i, j)
    bishop_moves = get_bishop_moves(b, i, j)
    moves.extend(bishop_moves)
    return moves


def get_king_moves(b, i, j):
    # method returns all possible moves of king in received board at received pos
    moves = []
    val = b[i][j]
    # adding moves in all 4 directions
    for row in range(i - 1, i + 2):
        for col in range(j - 1, j + 2):
            if is_valid(row, col) and not is_same_color(b[row][col], val) and not (row == i and col == j):
                moves.append((i, j, row, col))
    if divmod(val, 10)[1] == 0 and b[i][0] == (val / abs(val)) * 40 and b[i][1] == 0 and b[i][2] == 0 and b[i][3] == 0:
        moves.append((i, j, i, 2))  # long castle
    if divmod(val, 10)[1] == 0 and b[i][7] == (val / abs(val)) * 40 and b[i][5] == 0 and b[i][6] == 0:
        moves.append((i, j, i, 6))  # short castle
    return moves
