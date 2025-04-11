import streamlit as st
from utils import TicTacToe
from agents import get_tic_tac_toe_players

def initialize_game():
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        st.session_state.game_paused = False
        st.session_state.move_history = []
        st.session_state.game_board = None
        st.session_state.player_x = None
        st.session_state.player_o = None

def start_new_game(model_x, model_o):
    st.session_state.player_x, st.session_state.player_o = get_tic_tac_toe_players(
        model_x=model_x, model_o=model_o, debug_mode=True
    )
    st.session_state.game_board = TicTacToe()
    st.session_state.game_started = True
    st.session_state.game_paused = False
    st.session_state.move_history = []
    st.rerun()