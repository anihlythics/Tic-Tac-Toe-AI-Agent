import pytest
from utils import TicTacToe

def test_valid_move():
    game = TicTacToe()
    success, message = game.make_move(0, 0)
    assert success
    assert "successful" in message

def test_invalid_move_same_spot():
    game = TicTacToe()
    game.make_move(0, 0)
    success, message = game.make_move(0, 0)
    assert not success
    assert "already occupied" in message

def test_winner_detection():
    game = TicTacToe()
    game.board = [["X", "X", "X"], [" ", "O", "O"], [" ", " ", " "]]
    assert game.check_winner() == "X"