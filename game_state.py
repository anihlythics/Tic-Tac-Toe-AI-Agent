import streamlit as st
from utils import TicTacToe
from agents import get_tic_tac_toe_players


def initialize_game():
    # --- Gameplay session state ---
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "game_paused" not in st.session_state:
        st.session_state.game_paused = False
    if "move_history" not in st.session_state:
        st.session_state.move_history = []
    if "game_board" not in st.session_state:
        st.session_state.game_board = None
    if "player_x" not in st.session_state:
        st.session_state.player_x = None
    if "player_o" not in st.session_state:
        st.session_state.player_o = None
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "enter_game" not in st.session_state:
        st.session_state.enter_game = False
    if "confirm_reset" not in st.session_state:
        st.session_state.confirm_reset = False

    # --- Persistent display preferences ---
    if "theme_choice" not in st.session_state:
        st.session_state.theme_choice = "Glow"
    if "grid_opacity" not in st.session_state:
        st.session_state.grid_opacity = 0.15  # default 15%
    if "sound_enabled" not in st.session_state:
        st.session_state.sound_enabled = True

    # --- Score tracking ---
    if "score_x" not in st.session_state:
        st.session_state.score_x = 0
    if "score_o" not in st.session_state:
        st.session_state.score_o = 0


def start_new_game(model_x, model_o):
    st.session_state.player_x, st.session_state.player_o = get_tic_tac_toe_players(
        model_x=model_x, model_o=model_o, debug_mode=True
    )
    st.session_state.game_board = TicTacToe()
    st.session_state.game_paused = False
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.move_history = []
    st.rerun()


def reset_game():
    keys_to_clear = [
        "game_started", "game_paused", "move_history",
        "game_board", "player_x", "player_o", "game_over",
        "enter_game", "confirm_reset",
        "theme_choice", "grid_opacity", "sound_enabled",
        "score_x", "score_o"
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
    st.rerun()
