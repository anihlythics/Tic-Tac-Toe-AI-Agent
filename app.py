import nest_asyncio
import os
import re
import streamlit as st
from dotenv import load_dotenv
from game_state import initialize_game, start_new_game, reset_game
from ui_components import render_game_title
from agents import get_tic_tac_toe_players
from agno.utils.log import logger
from utils import (
    TicTacToe,
    display_board,
    display_move_history,
    show_agent_status,
    get_video_base64,
    play_sound_on_move,
    GLOW_CSS,
    DARK_CSS,
    LIGHT_CSS,
    AGENT_AVATARS,
)

# Load env & apply asyncio patch
load_dotenv()
nest_asyncio.apply()

st.set_page_config(
    page_title="Agent Tic Tac Toe",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎬 Background Video (Optional)
video_path = "Edt/vecteezy_abstract-round-blue-to-purple-sphere-light-bright-glowing_200561751.mp4"
if os.path.exists(video_path):
    video_b64 = get_video_base64(video_path)
    st.markdown(f"""
    <style>
    .stApp {{
      background: transparent;
    }}
    .video-bg {{
      position: fixed;
      right: 0;
      bottom: 0;
      min-width: 100%;
      min-height: 100%;
      z-index: -1;
      object-fit: cover;
      opacity: 0.35;
      filter: blur(2px) brightness(1.2);
    }}
    </style>
    <video autoplay loop muted playsinline class="video-bg">
      <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

# ✅ Initialize session state
initialize_game()
if "score_x" not in st.session_state:
    st.session_state.score_x = 0
if "score_o" not in st.session_state:
    st.session_state.score_o = 0
if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Glow"
if "grid_opacity" not in st.session_state:
    st.session_state.grid_opacity = 0.15
if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = True

# 🌌 Apply dynamic theme CSS
if st.session_state.theme_choice == "Glow":
    st.markdown(GLOW_CSS, unsafe_allow_html=True)
elif st.session_state.theme_choice == "Dark":
    st.markdown(DARK_CSS, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)

st.markdown(f"""
<style>
body::before {{
    opacity: {st.session_state.grid_opacity};
}}
</style>
""", unsafe_allow_html=True)

# 🚀 Welcome screen
if not st.session_state.get("enter_game"):
    st.image("https://i.imgur.com/Fh7XOmF.png", use_container_width=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 class='main-title'>Welcome to AI Battle Arena 🤖🎮</h1>
        <p style="font-size:18px; color:#f0f6fc;">
            Watch top AI agents battle it out in a strategic Tic-Tac-Toe match.<br>
            Select your players, start the game, and enjoy the glowing showdown!
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Enter the Arena"):
        st.session_state.enter_game = True
        st.rerun()
    st.stop()

# 🎮 Game UI
render_game_title()

# 🛠️ Settings Drawer
with st.expander("🛠️ Display & Audio Settings", expanded=False):
    theme_choice = st.radio(
        "🎨 Choose Theme",
        ["Glow", "Dark", "Light"],
        index=["Glow", "Dark", "Light"].index(st.session_state.theme_choice),
        horizontal=True,
    )
    st.session_state.theme_choice = theme_choice

    grid_brightness = st.slider(
        "🔆 Grid Glow Intensity",
        0,
        100,
        int(st.session_state.grid_opacity * 100),
        step=5,
    )
    st.session_state.grid_opacity = grid_brightness / 100
    st.caption(f"Current brightness: {grid_brightness}%")

    sound_toggle = st.checkbox("🔊 Enable Move Sound", value=st.session_state.sound_enabled)
    st.session_state.sound_enabled = sound_toggle

# 🎛️ Game Controls
with st.sidebar:
    st.markdown("### Game Controls")
    model_options = {
        "GPT-4": "openai:gpt-4",
        "O3-Mini": "openai:o3-mini",
        "Gemini Flash": "google:gemini-2.0-flash",
        "Gemini Pro": "google:gemini-2.0-pro-exp-02-05",
        "Llama 3.3": "groq:llama-3.3-70b-versatile",
        "Mistral (OpenRouter)": "openrouter:mistral-7b",
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

    st.markdown("---")
    st.markdown(f"### 🧠 Scoreboard\n- 🔵 Player X: `{st.session_state.score_x}`\n- 🔴 Player O: `{st.session_state.score_o}`")

    if "confirm_reset" not in st.session_state:
        st.session_state.confirm_reset = False

    if st.session_state.confirm_reset:
        st.markdown("⚠️ **Are you sure you want to reset everything?**")
        if st.button("✅ Confirm Reset"):
            reset_game()
        if st.button("❌ Cancel"):
            st.session_state.confirm_reset = False
    else:
        if st.button("🧹 Reset All"):
            st.session_state.confirm_reset = True

# 🧠 Gameplay
if st.session_state.game_started:
    st.markdown(f"<h3 style='color:#87CEEB; text-align:center;'>{selected_p_x} vs {selected_p_o}</h3>", unsafe_allow_html=True)
    status = st.session_state.game_board.get_game_status()
    game_over = "wins" in status.lower() or "draw" in status.lower()

    display_board(st.session_state.game_board)

    if game_over:
        winner_player = "X" if "X wins" in status else "O" if "O wins" in status else None
        if winner_player:
            winner_model = selected_p_x if winner_player == "X" else selected_p_o
            st.session_state.score_x += 1 if winner_player == "X" else 0
            st.session_state.score_o += 1 if winner_player == "O" else 0
            st.success(f"🏆 Game Over! {winner_model} wins!")
        else:
            st.info("🤝 Game Over! It's a draw!")

        st.balloons()
        with st.sidebar:
            st.markdown("### 🔁 Replay Options")
            if st.button("🎮 Replay with New Agents"):
                start_new_game(model_options[selected_p_x], model_options[selected_p_o])

    else:
        current_player = st.session_state.game_board.current_player
        current_model_name = selected_p_x if current_player == "X" else selected_p_o
        avatar = AGENT_AVATARS.get(current_model_name, "🤖")

        show_agent_status(f"Player {current_player} ({current_model_name})", "is thinking...")
        display_move_history()

        if not st.session_state.game_paused:
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
                numbers = re.findall(r"\d+", response.content if response else "")
                row, col = map(int, numbers[:2])
                success, message = st.session_state.game_board.make_move(row, col)

                if success:
                    if st.session_state.sound_enabled:
                        play_sound_on_move()

                    explanation = response.content.strip() if response else "No explanation provided."
                    st.session_state.move_history.append({
                        "player": f"{avatar} Player {current_player} ({current_model_name})",
                        "move": f"{row},{col}",
                        "explanation": explanation
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

if __name__ == "__main__":
    main()