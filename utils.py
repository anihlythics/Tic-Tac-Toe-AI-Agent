from typing import List, Optional, Tuple
import streamlit as st
import base64
import re

# --- Constants ---
X_PLAYER = "X"
O_PLAYER = "O"
EMPTY = " "

# --- Weapon-style Emoji Avatars for Agents ---
AGENT_AVATARS = {
    "GPT-4": "🗡️",        # Dagger
    "O3-Mini": "🏹",       # Bow & Arrow
    "Gemini Flash": "🔫",  # Gun
    "Gemini Pro": "🪓",     # Axe
    "Llama 3.3": "⚔️",      # Sword
    "Mistral (OpenRouter)": "🔨"  # Hammer
}

# --- Game Logic ---
class TicTacToe:
    def __init__(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = X_PLAYER
        self.last_move = None

    def make_move(self, row: int, col: int) -> Tuple[bool, str]:
        if not (0 <= row < 3 and 0 <= col < 3):
            return False, "Invalid move: Position out of bounds."
        if self.board[row][col] != EMPTY:
            return False, "Invalid move: Position already occupied."
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        self.current_player = O_PLAYER if self.current_player == X_PLAYER else X_PLAYER
        return True, "Move successful!"

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == EMPTY]

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

# --- Display the Tic-Tac-Toe Board ---
def display_board(game: TicTacToe):
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            cell = game.board[i][j]
            highlight = game.last_move == (i, j)

            symbol = "❌" if cell == "X" else "⭕" if cell == "O" else " "
            glow_color = "#00ffff" if cell == "O" else "#ff004f" if cell == "X" else "#333"
            text_glow = f"text-shadow: 0 0 8px {glow_color}, 0 0 16px {glow_color};"

            style = f"""
                background-color: #111827;
                color: {glow_color};
                font-size: 42px;
                font-weight: bold;
                height: 100px;
                width: 100%;
                border: 3px solid {glow_color};
                border-radius: 20px;
                box-shadow: 0 0 12px {glow_color};
                {text_glow}
            """

            if highlight:
                style += f" background-color: {glow_color}; color: #111827; animation: flash 0.4s ease-in-out;"

            cols[j].markdown(
                f"<button style='{style}' disabled>{symbol}</button>",
                unsafe_allow_html=True
            )

# --- Move History Display ---
def display_move_history():
    st.markdown("### 📝 Move History (Chat Style)")
    for move in st.session_state.move_history:
        st.markdown(f"🧠 **{move['player']}** moved to **{move['move']}**")
        if "explanation" in move:
            st.markdown(f"<div style='margin-left:20px; color:#ccc;'>{move['explanation']}</div>", unsafe_allow_html=True)

# --- Sound FX for Move ---
def play_sound_on_move():
    st.markdown("""
    <audio autoplay>
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-arcade-game-jump-coin-216.wav" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

# --- Convert video to Base64 for Streamlit embed ---
def get_video_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Show agent move status with emoji ---
def show_agent_status(name: str, message: str):
    match = re.search(r"\((.*?)\)", name)
    model_name = match.group(1) if match else name
    avatar = AGENT_AVATARS.get(model_name, "🤖")
    st.info(f"**{avatar} {name}**: {message}")

# --- CSS THEMES ---

GLOW_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

body {
    background: radial-gradient(ellipse at center, #0a0f1d 0%, #000000 100%);
    color: #00f0ff;
    font-family: 'Orbitron', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 48px;
    color: #00ffff;
    text-shadow: 0 0 15px #00ffff, 0 0 30px #00ffff;
}

div.stButton > button {
    background-color: #111827;
    border: 2px solid #00ffff;
    border-radius: 16px;
    color: #00ffff;
    font-size: 36px;
    font-weight: bold;
    height: 100px;
    width: 100%;
    margin: 5px;
    box-shadow: 0 0 20px #00ffff;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #00ffff;
    color: #111827;
    box-shadow: 0 0 40px #00ffff;
}

h3, h1, h2 {
    color: #00ffff;
    text-align: center;
}

body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    z-index: -2;
    background-image: repeating-linear-gradient(
        0deg,
        rgba(0, 255, 255, 0.05),
        rgba(0, 255, 255, 0.05) 1px,
        transparent 1px,
        transparent 20px
    ), repeating-linear-gradient(
        90deg,
        rgba(0, 255, 255, 0.05),
        rgba(0, 255, 255, 0.05) 1px,
        transparent 1px,
        transparent 20px
    );
    animation: flickerGrid 3s linear infinite;
    opacity: 0.15;
}

@keyframes flickerGrid {
    0% {opacity: 0.15;}
    50% {opacity: 0.2;}
    100% {opacity: 0.15;}
}

@keyframes flash {
    0% { box-shadow: 0 0 5px #fff; }
    50% { box-shadow: 0 0 30px #fff; }
    100% { box-shadow: 0 0 5px #fff; }
}
</style>
"""

DARK_CSS = """
<style>
body {
    background-color: #1e1e1e;
    color: #f5f5f5;
    font-family: sans-serif;
}
</style>
"""

LIGHT_CSS = """
<style>
body {
    background-color: #ffffff;
    color: #000000;
    font-family: sans-serif;
}
</style>
"""
