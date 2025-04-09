CUSTOM_CSS = """
<style>
.main-title {
    color: #2E86C1;
    text-align: center;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 20px;
}
</style>
"""

def render_game_title():
    import streamlit as st
    st.markdown("<h1 class='main-title'>Watch Agents Play Tic Tac Toe</h1>", unsafe_allow_html=True)
