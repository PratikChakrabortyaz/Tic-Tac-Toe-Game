import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.user_starts = None
        
        # Add buttons for user to choose starting player
        self.user_starts_button = tk.Button(self.master, text="User Starts", command=self.user_starts_game)
        self.user_starts_button.pack(pady=5)
        self.ai_starts_button = tk.Button(self.master, text="AI Starts", command=self.ai_starts_game)
        self.ai_starts_button.pack(pady=5)

    def user_starts_game(self):
        self.user_starts = True
        self.start_game()

    def ai_starts_game(self):
        self.user_starts = False
        self.start_game()

    def start_game(self):
        self.user_starts_button.pack_forget()
        self.ai_starts_button.pack_forget()

        self.board = [' ' for _ in range(9)]
        self.ai_player = 'O'
        self.human_player = 'X'
        self.current_player = self.human_player if self.user_starts else self.ai_player
        self.buttons = []
        self.game_over = False

        self.create_board()

        if not self.user_starts:
            self.ai_move()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text='', font=('Arial', 30), width=8, height=4,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def make_move(self, row, col):
        if not self.game_over and self.current_player == self.human_player:
            index = row * 3 + col
            if self.board[index] == ' ':
                self.board[index] = self.human_player
                self.buttons[index].config(text=self.human_player)
                if self.check_winner(self.human_player):
                    self.game_over = True
                    messagebox.showinfo("Game Over", "You Win!")
                elif ' ' not in self.board:
                    self.game_over = True
                    messagebox.showinfo("Game Over", "Draw!")
                else:
                    self.current_player = self.ai_player
                    self.ai_move()

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.ai_player
                score = self.minimax(self.board, 0, False, alpha, beta)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        self.board[best_move] = self.ai_player
        self.buttons[best_move].config(text=self.ai_player)
        if self.check_winner(self.ai_player):
            self.game_over = True
            messagebox.showinfo("Game Over", "AI Wins!")
        elif ' ' not in self.board:
            self.game_over = True
            messagebox.showinfo("Game Over", "Draw!")
        else:
            self.current_player = self.human_player

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner(self.ai_player):
            return 10
        elif self.check_winner(self.human_player):
            return -10
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.ai_player
                    score = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.human_player
                    score = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    def check_winner(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if (self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2] == player) or \
               (self.board[i] == self.board[i + 3] == self.board[i + 6] == player):
                return True
        if (self.board[0] == self.board[4] == self.board[8] == player) or \
           (self.board[2] == self.board[4] == self.board[6] == player):
            return True
        return False


def main():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

