import nest_asyncio
import streamlit as st
from agents import get_tic_tac_toe_players
from agno.utils.log import logger
from utils import (
    CUSTOM_CSS,
    TicTacToeBoard,
    display_board,
    display_move_history,
    show_agent_status,
)

# Apply asyncio patch
nest_asyncio.apply()

# Streamlit page configuration
st.set_page_config(
    page_title="Agent Tic Tac Toe",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS for styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def initialize_game():
    """Initialize session state variables."""
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        st.session_state.game_paused = False
        st.session_state.move_history = []
        st.session_state.game_board = None
        st.session_state.player_x = None
        st.session_state.player_o = None

def start_new_game(model_x, model_o):
    """Start a new game with selected models."""
    st.session_state.player_x, st.session_state.player_o = get_tic_tac_toe_players(
        model_x=model_x, model_o=model_o, debug_mode=True
    )
    st.session_state.game_board = TicTacToeBoard()
    st.session_state.game_started = True
    st.session_state.game_paused = False
    st.session_state.move_history = []
    st.rerun()

def main():
    initialize_game()
    
    # App header
    st.markdown("<h1 class='main-title'>Watch Agents Play Tic Tac Toe</h1>", unsafe_allow_html=True)

    # Sidebar - Game Controls
    with st.sidebar:
        st.markdown("### Game Controls")
        model_options = {
            "GPT-4": "openai:gpt-4",
            "O3-Mini": "openai:o3-mini",
            "Gemini Flash": "google:gemini-2.0-flash",
            "Gemini Pro": "google:gemini-2.0-pro-exp-02-05",
            "Llama 3.3": "groq:llama-3.3-70b-versatile",
            "DeepSeek": "deepseek"
        }
        
        selected_p_x = st.selectbox("Select Player X", list(model_options.keys()), index=3, key="model_p1")
        selected_p_o = st.selectbox("Select Player O", list(model_options.keys()), index=1, key="model_p2")
        
        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.game_started:
                if st.button("▶️ Start Game"):
                    start_new_game(model_options[selected_p_x], model_options[selected_p_o])
            else:
                if st.button("⏸️ Pause" if not st.session_state.game_paused else "▶️ Resume"):
                    st.session_state.game_paused = not st.session_state.game_paused
                    st.rerun()
        with col2:
            if st.session_state.game_started:
                if st.button("🔄 New Game"):
                    start_new_game(model_options[selected_p_x], model_options[selected_p_o])
    
    # Game header with selected models
    if st.session_state.game_started:
        st.markdown(f"<h3 style='color:#87CEEB; text-align:center;'>{selected_p_x} vs {selected_p_o}</h3>", unsafe_allow_html=True)
    
    # Display game board
    if st.session_state.game_started:
        game_over, status = st.session_state.game_board.get_game_state()
        display_board(st.session_state.game_board)

        if game_over:
            winner_player = "X" if "X wins" in status else "O" if "O wins" in status else None
            if winner_player:
                winner_model = selected_p_x if winner_player == "X" else selected_p_o
                st.success(f"🏆 Game Over! {winner_model} wins!")
            else:
                st.info("🤝 Game Over! It's a draw!")

            # Added Replay Options in the Sidebar after game over
            with st.sidebar:
                st.markdown("### Replay Options")
                if st.button("🎮 Replay with New Agents"):
                    # Reset game and pick new agents for a fresh start
                    start_new_game(model_options[selected_p_x], model_options[selected_p_o])

        else:
            current_player = st.session_state.game_board.current_player
            current_model_name = selected_p_x if current_player == "X" else selected_p_o
            show_agent_status(f"Player ({current_model_name})", "It's your turn")
    
            display_move_history()

            if not st.session_state.game_paused and not game_over:
                valid_moves = st.session_state.game_board.get_valid_moves()
                current_agent = st.session_state.player_x if current_player == "X" else st.session_state.player_o
                
                response = current_agent.run(
                    f"""
                    Current board state:\n{st.session_state.game_board.get_board_state()}\n
                    Available valid moves (row, col): {valid_moves}\n
                    Choose your next move from the valid moves above.
                    Respond with ONLY two numbers for row and column, e.g. "1 2".
                    """,
                    stream=False,
                )
                
                try:
                    import re
                    numbers = re.findall(r"\d+", response.content if response else "")
                    row, col = map(int, numbers[:2])
                    success, message = st.session_state.game_board.make_move(row, col)
                    
                    if success:
                        st.session_state.move_history.append({
                            "player": f"Player ({current_model_name})",
                            "move": f"{row},{col}",
                        })
                        st.rerun()
                    else:
                        logger.error(f"Invalid move attempt: {message}")
                        st.rerun()
                except Exception as e:
                    logger.error(f"Error processing move: {str(e)}")
                    st.error(f"Error processing move: {str(e)}")
                    st.rerun()
            else:
                st.info("👈 Press 'Start Game' to begin!")
    
    # About section
    st.sidebar.markdown(f"""
    ### 🎮 Agent Tic Tac Toe Battle
    Watch two AI agents compete in real-time!
    
    **Current Players:**
    * 🔵 Player X: `{selected_p_x}`
    * 🔴 Player O: `{selected_p_o}`
    
    **How it Works:**
    * 🏆 Finds winning moves
    * 🛡️ Blocks opponent strategies
    * ⭐ Controls strategic positions
    * 🤔 Plans multiple moves ahead
    
    Built with Streamlit and Agno
    """)

if __name__ == "__main__":
    main()
