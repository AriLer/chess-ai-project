import numpy as np
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from utils import *


class Tile(Button):
    def __init__(self, i, j, val, **kwargs):
        # method initializes a tile object
        Button.__init__(self, **kwargs)
        self.i = i  # row / y coordinate
        self.j = j  # col / x coordinate
        self.value = val
        self.keep_ratio = True  # kivy visual property
        self.allow_stretch = False  # kivy visual property
        self.background_normal = "pieces/" + str(get_type(val)) + ".png"

    def set_value(self, new_val):
        # method sets new value to a tile
        self.value = new_val
        self.background_normal = "pieces/" + str(get_type(self.value)) + ".png"


class Board(GridLayout, Screen):
    def __init__(self, **kwargs):
        # method initializes the board object
        GridLayout.__init__(self)
        self.cols = 8  # for building kivy grid
        self.curr_b = None  # pressed piece button
        self.curr_p = None  # pressed piece object
        self.move_to = []  # list of options to move selected piece
        self.first_click = True  # True - selecting piece, False - moving selected piece
        self.human = -1  # human player
        self.comp = 1  # computer player
        start_b = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
        self.board = np.array(translate_fen(start_b))  # the logical side of the board (2d array of strings)
        self.depth = 3  # depth to which computer goes each move
        self.turn = 1  # who's turn it is
        if start_b[start_b.index(" ") + 1] == "w":
            self.turn = -1
        self.neutral_moves = 0  # for 50 moves rule
        self.showing_modal = False  # if a modal opens changes to true
        vis_b_temp = []  # 2d array of buttons (later made into numpy array)
        for i in range(self.cols):
            line_list = []
            for j in range(self.cols):
                cell = Tile(i, j, self.board[i][j])
                cell.bind(on_press=self.click)
                self.add_widget(cell)
                line_list.append(cell)
            vis_b_temp.append(line_list)
        self.vis_b = np.array(vis_b_temp)  # visual representation of the chess board
        if self.turn == self.comp:
            self.comp_move()

    #  immediate move methods
    def click(self, btn):
        # method reacts to clicking on a cell
        if self.turn == self.human:
            over = self.over_state(self.board, self.turn)  # checking if game is over
            if self.first_click and btn.value != 0 and (btn.value / abs(btn.value)) == self.turn:  # if selecting click
                if over == 0:  # if not over
                    self.curr_b = btn  # remembering which button was pressed
                    self.curr_p = (btn.i, btn.j)  # remembering which piece is moving
                    self.move_list = get_moves(self.board, btn.i, btn.j)  # array of piece's possible moves
                    self.highlight_cells(True)  # highlighting cells that player can move to
                    self.first_click = False

            elif not self.first_click and (self.curr_b.value / abs(self.curr_b.value)) == self.turn:
                self.highlight_cells(False)  # deselecting cells
                move = (self.curr_p[0], self.curr_p[1], btn.i, btn.j)
                if self.move_list.count(move) != 0 and self.is_legal(self.board, move):
                    self.make_move(self.board, move, True)  # if move is legal, do it
                    if not self.showing_modal:  # if not promoting
                        self.turn = self.comp
                        self.comp_move()
                if not self.showing_modal:
                    self.first_click = True
            if over != 0:  # if game is over
                self.playing = False
                self.show_go(over)

    def comp_move(self):
        # method preforms the computer's move
        over = self.over_state(self.board, self.turn)  # checking over state
        if over == 0:
            saved_board = self.board.copy()  # copying the board so it won't change
            move = self.minimax(saved_board, self.depth)  # generate smart move
            self.board = saved_board.copy()  # updating the board
            if self.is_legal(self.board, move):  # if move is legal, do it
                self.curr_b = self.vis_b[move[0]][move[1]]
                self.make_move(self.board, move, True)
            self.turn = self.human
            over = self.over_state(self.board, self.turn)
        if over != 0:  # if game is over
            self.playing = False
            self.show_go(over)

    def make_move(self, b, mv, f_mv=False):
        # method preforms a move on the logical side of a board
        val_to = b[mv[2]][mv[3]]  # value of cell that piece is moving to
        val = b[mv[0]][mv[1]]  # moving piece's value

        # 50 moves rule
        if f_mv:  # if final move (not directly from inside the minimax algorithm)
            if 10 <= val < 20 or val_to != 0:
                self.neutral_moves = 0  # if pawn-move or piece captured, counter is reset

        # en passant - if moving piece is a pawn and mt square is free and a first move pawn is standing to the side
        if get_type(val) == 1 and val_to == 0 and mv[3] != mv[1] and abs(b[mv[0]][mv[3]]) == 11:
            i = mv[2] - 1
            if self.turn == -1:
                i = mv[2] + 1
            b[i][mv[3]] = 0
            if f_mv:
                self.vis_b[i][mv[3]].set_value(0)

        # castle
        if abs(val) == 60 and (mv[3] == 6 or mv[3] == 2) and mv[1] == 4:
            cords = (0, 3)  # long castle coordinate
            if mv[3] == 6:
                cords = (7, 5)  # short castle coordinates
            b[mv[0]][cords[1]] = 41 * self.turn  # moving castling rook
            b[mv[0]][cords[0]] = 0  # emptying rook's past cell
            self.apply_move([mv[2], cords[0], mv[2], cords[1]], f_mv)  # graphical application of move

        b[mv[2]][mv[3]] = get_new_val(val)  # moving the piece
        b[mv[0]][mv[1]] = 0  # emptying piece's past cell
        self.apply_move(mv, f_mv)  # moving piece to a new location, leaving empty space

        # promotion
        if abs(get_type(val) == 1) and (mv[2] == 0 or mv[2] == 7):
            if self.turn == self.human and f_mv:
                self.show_promote()  # only human player needs to see promotion popup
            else:
                b[mv[2]][mv[3]] = 52 * self.turn  # automatically setting the piece to a black queen
                if f_mv:  # if needs to move visuals
                    self.vis_b[mv[2]][mv[3]].set_value(52)

    def promote(self, btn):
        # method promotes received piece
        new_val = (int(btn.background_normal[8]) * 10 + 2) * self.turn  # extracting value from image's file name
        self.vis_b[self.curr_b.i][self.curr_b.j].set_value(new_val)  # applying change to visual board
        self.board[self.curr_b.i][self.curr_b.j] = new_val  # applying change to logical board
        self.popup.dismiss()  # closing popup
        self.first_click = True
        self.showing_modal = False
        self.turn = self.comp
        self.comp_move()

    #  ai methods
    def minimax(self, b, depth):
        # method receives a description of the current state of the board and a depth to go to
        alpha = float('-inf')
        beta = float('inf')
        moves = get_all_moves(b, self.comp)  # getting all possible moves in situation
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:  # go over all possible moves
            if self.is_legal(b, move):
                curr_b = b.copy()  # copying the board to make changes to it
                self.make_move(curr_b, move)
                score = self.min_play(curr_b, depth - 1, alpha, beta)  # maybe add "human" parameter
                if score > best_score:
                    best_move = move  # remembering best move
                    best_score = score  # remembering best score
                if alpha < best_score:
                    alpha = best_score
                if beta <= alpha:
                    break
        return best_move

    def min_play(self, b, depth, alpha, beta):
        # method plays out the best move for human
        if depth == 0 or self.over_state(b, self.human) != 0:  # if game is over or depth 0 is reached
            return self.evaluate(b) * (depth + 1)
        moves = get_all_moves(b, self.human)
        best_score = float('inf')
        for move in moves:  # go over all moves
            if self.is_legal(b, move):
                curr_b = b.copy()  # copy board
                self.make_move(curr_b, move)  # applying logical move
                score = self.max_play(curr_b, depth - 1, alpha, beta)
                if score < best_score:
                    best_move = move  # remembering best move
                    best_score = score  # remembering best score
                if beta > best_score:
                    beta = best_score
                if beta <= alpha:
                    break
        return best_score

    def max_play(self, b, depth, alpha, beta):
        # method plays out best move for computer
        if depth == 0 or self.over_state(b, self.comp) != 0:  # if game is over or depth 0 is reached
            return self.evaluate(b) * (depth + 1)
        moves = get_all_moves(b, self.comp)
        best_score = float('-inf')
        for move in moves:  # go over all moves
            if self.is_legal(b, move):
                curr_b = b.copy()  # copy board
                self.make_move(curr_b, move)  # apply logical move
                score = self.min_play(curr_b, depth - 1, alpha, beta)
                if score > best_score:
                    best_move = move  # remembering best move
                    best_score = score  # remembering best score
                if alpha < best_score:
                    alpha = best_score
                if beta <= alpha:
                    break
        return best_score

    def evaluate(self, b):
        # method evaluates the board and returns an integer score
        score = 0
        for i in range(8):
            for j in range(8):
                val = b[i][j]
                if val != 0:
                    is_end = False
                    if get_type(val) == 6:  # check if it's endgame only if king is related
                        is_end = is_endgame(b)
                    pst_score = get_pst_val(get_type(val), i, j, is_end) * 2  # gets piece's pst value
                    piece_score = get_score_value(val) + pst_score  # get piece's type value
                    if is_end:
                        human_over_Stat = self.over_state(b, self.human)
                        if human_over_Stat == 2:  # promote mate
                            score += 5000
                        elif human_over_Stat == 3:  # avoid stalemate
                            score -= 2000
                    if val < 0:
                        score -= piece_score
                    else:
                        score += piece_score
        return score

    #  end related checking
    def is_legal(self, b, move):
        # method checks legality of move
        bool = False
        val = b[move[0]][move[1]]  # moving piece
        val_to = b[move[2]][move[3]]  # cell to move to
        color = val / abs(val)  # 1 if black, -1 if white
        if abs(val) == 60 and self.is_check(b, color) and is_castle_move(move[1], move[3]):
            return False  # castle move when under a check threat is illegal
        b[move[2]][move[3]] = val
        b[move[0]][move[1]] = 0
        if not self.is_check(b, color):  # move is legal if it doesn't lead directly to a mate
            bool = True
        b[move[0]][move[1]] = val
        b[move[2]][move[3]] = val_to
        return bool

    def is_check(self, b, color):
        # method receives board and player and checks if opponent is threatening check
        all_moves = get_all_moves(b, color * -1)  # opponent's all possible moves
        for move in all_moves:
            if 60 <= abs(b[move[2]][move[3]]) < 70:  # if any piece can capture the king
                return True
        return False

    def over_state(self, b, color):
        # method returns if received player has lost or not (or stale mate)
        # 0 = not over, 1 = draw, 2 = mate, 3 = stalemate
        if self.neutral_moves == 20:  # 50 moves rule (reduced to 20)
            return 1
        all_moves = get_all_moves(b, color)
        if len(all_moves) != 0:
            for move in all_moves:
                if move and self.is_legal(b, move):
                    return 0  # if possible move found
            if self.is_check(b, color):  # if no moves and under check
                return 2
        return 3  # no moves and not under check

    #  visual
    def show_go(self, event):
        # method opens a game over popup
        message = get_go_message(event, self.turn)
        self.showing_modal = True
        main_container = BoxLayout(orientation='vertical', size=(self.width, self.height))  # general box
        go_label = Label(text=message, font_size=30, font_name='Arial', color=(.83, .83, .83, 1))  # game over message
        main_container.add_widget(go_label)
        btn_container = BoxLayout(orientation='horizontal', size_hint_y=.5, spacing=10)  # box containing the buttons
        restart_btn = Button(text='Restart', color=(.83, .83, .83, 1))  # restart button
        restart_btn.bind(on_press=self.restart)

        quit_btn = Button(text='Quit', color=(.83, .83, .83, 1))  # quit button
        quit_btn.bind(on_press=self.quit)
        btn_container.add_widget(restart_btn)
        btn_container.add_widget(quit_btn)
        main_container.add_widget(btn_container)

        self.popup = Popup(title="Game over", title_font="Arial", size_hint=(.3, .3), auto_dismiss=False,
                           separator_color=(.46, .59, .33, 1), background_color=(.19, .18, .17, .7),
                           content=main_container)
        self.popup.open()

    def show_promote(self):
        # method opens promotion popup (queen/ bishop / rook / knight)
        self.showing_modal = True
        box = BoxLayout(orientation="horizontal")
        queen_btn = Button(background_normal="pieces/-5.png")  # promote to queen button
        queen_btn.bind(on_press=self.promote)
        bishop_btn = Button(background_normal="pieces/-3.png")  # promote to queen button
        bishop_btn.bind(on_press=self.promote)
        rook_btn = Button(background_normal="pieces/-4.png")  # promote to rook button
        rook_btn.bind(on_press=self.promote)
        knight_btn = Button(background_normal="pieces/-2.png")  # promote to rook button
        knight_btn.bind(on_press=self.promote)
        box.add_widget(queen_btn)
        box.add_widget(bishop_btn)
        box.add_widget(rook_btn)
        box.add_widget(knight_btn)
        self.popup = Popup(title="Promote", content=box, size_hint=(.5, .25), separator_color=(.46, .59, .33, 1),
                           background_color=(.19, .18, .17, .8), auto_dismiss=False)
        self.popup.open()

    def highlight_cells(self, on):
        # method highlighting cells that a piece can move to
        for idx in range(len(self.move_list)):
            if self.is_legal(self.board, self.move_list[idx]):
                i = self.move_list[idx][2]
                j = self.move_list[idx][3]
                if on:  # if method called to highlight cells
                    self.curr_b.background_color = (.8, .2, .2, 1)
                    if self.board[i][j] == 0:
                        self.vis_b[i][j].background_normal = "grey_circle.png"
                    else:
                        self.vis_b[i][j].background_color = (.38, .38, .25, .5)
                else:  # if method called to de-highlight cells
                    self.curr_b.background_color = [1, 1, 1, 1]
                    if self.board[i][j] == 0:
                        self.vis_b[i][j].background_normal = 'pieces/0.png'
                    else:
                        self.vis_b[i][j].background_color = [1, 1, 1, 1]

    def apply_move(self, mv, f_mv=False):
        # method applies visual changes of a move to the board
        if f_mv:  # if needs to move visuals
            self.vis_b[mv[2]][mv[3]].set_value(self.vis_b[mv[0]][mv[1]].value)
            self.vis_b[mv[0]][mv[1]].set_value(0)
            self.curr_b = self.vis_b[mv[2]][mv[3]]

    # essentials
    def restart(self, btn):
        # method restarts the game and send user to start screen
        Chess.get_running_app().stop()
        Chess().run()

    def quit(self, btn):
        # method quits the game
        Chess.get_running_app().stop()


class StartWindow(Screen):
    pass


class RulesWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('chess.kv')


class Chess(App):
    def build(self):
        Window.clearcolor = (.19, .18, .17, 1)
        Window.size = (700, 625)
        self.title = 'Chess'


Chess().run()
