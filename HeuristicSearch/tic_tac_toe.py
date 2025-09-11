# tic_tac_toe.py
# Tic-Tac-Toe (3x3) dùng easyAI - chơi tương tác terminal
from easyAI import TwoPlayerGame, AI_Player, Negamax
from easyAI.Player import Human_Player

class TicTacToe(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.current_player = 1
        self.board = [0]*9  # 0 empty, 1 player1 (O), 2 player2 (X)

    def possible_moves(self):
        return [i+1 for i,v in enumerate(self.board) if v==0]

    def make_move(self, move):
        self.board[int(move)-1] = self.current_player

    def unmake_move(self, move):
        self.board[int(move)-1] = 0

    def win_condition(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != 0:
                return True
        return False

    def is_over(self):
        return (self.possible_moves() == []) or self.win_condition()

    def show(self):
        symbols = ['.','O','X']
        for r in range(3):
            print(" ".join(symbols[self.board[3*r + c]] for c in range(3)))
        print()

    def scoring(self):
        # từ góc nhìn của current_player: -100 nếu thua, 0 otherwise
        return -100 if self.win_condition() else 0

if __name__ == "__main__":
    # Negamax depth nhỏ (3-7) đủ cho 3x3; dùng depth=6 cho AI mạnh
    ai_algo = Negamax(6)
    game = TicTacToe([Human_Player(), AI_Player(ai_algo)])
    game.play()
