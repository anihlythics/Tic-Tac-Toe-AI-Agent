import os
from agents import get_tic_tac_toe_players

def test_get_tic_tac_toe_players():
    player_x, player_o = get_tic_tac_toe_players("openai:gpt-4", "openai:o3-mini")
    assert player_x.name == "Player X"
    assert player_o.name == "Player O"
    assert callable(player_x.run)
    assert callable(player_o.run)