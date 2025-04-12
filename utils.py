from typing import List, Optional, Tuple
import streamlit as st

# Constants for players and empty cells
X_PLAYER = "X"
O_PLAYER = "O"
EMPTY = " "

class TicTacToe:
    def __init__(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = X_PLAYER

    def make_move(self, row: int, col: int) -> Tuple[bool, str]:
        if not (0 <= row < 3 and 0 <= col < 3):
            return False, "Invalid move: Position out of bounds."
        if self.board[row][col] != EMPTY:
            return False, "Invalid move: Position already occupied."
        
        self.board[row][col] = self.current_player
        self.current_player = O_PLAYER if self.current_player == X_PLAYER else X_PLAYER
        return True, "Move successful!"

    def get_board_state(self) -> str:
        return "\n".join([" | ".join(row) for row in self.board])
    
    def check_winner(self) -> Optional[str]:
        for row in self.board:
            if row[0] != EMPTY and row.count(row[0]) == 3:
                return row[0]
        
        for col in range(3):
            if self.board[0][col] != EMPTY and all(self.board[row][col] == self.board[0][col] for row in range(3)):
                return self.board[0][col]
        
        if self.board[0][0] != EMPTY and all(self.board[i][i] == self.board[0][0] for i in range(3)):
            return self.board[0][0]
        if self.board[0][2] != EMPTY and all(self.board[i][2 - i] == self.board[0][2] for i in range(3)):
            return self.board[0][2]
        
        return None
    
    def is_board_full(self) -> bool:
        return all(cell != EMPTY for row in self.board for cell in row)
    
    def get_game_status(self) -> str:
        winner = self.check_winner()
        if winner:
            return f"Player {winner} wins!"
        if self.is_board_full():
            return "It's a draw!"
        return "Game in progress"