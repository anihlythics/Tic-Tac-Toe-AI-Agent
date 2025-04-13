"""
Tic Tac Toe Battle
---------------------------------
This example builds a Tic Tac Toe game where two AI agents compete against each other.
A referee agent coordinates between two player agents using different AI models.

Usage Examples:
---------------
1. Quick game with default settings:
   referee_agent = get_tic_tac_toe_referee()
   play_tic_tac_toe()

2. Game with debug mode off:
   referee_agent = get_tic_tac_toe_referee(debug_mode=False)
   play_tic_tac_toe(debug_mode=False)

The game integrates:
  - Multiple AI models (Claude, GPT-4, etc.)
  - Turn-based gameplay coordination
  - Move validation and game state management
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import os
from textwrap import dedent
from typing import Tuple
import openai  # OpenAI integration
import google.generativeai as genai  # Google Gemini integration

# Set API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
genai_api_key = os.getenv("GENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from openrouter_wrapper import OpenRouterChat

# Ensure project root is in the system path
project_root = Path(__file__).resolve().parents
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def get_model_for_provider(provider: str, model_name: str):
    if provider == "openai":
        return OpenAIChat(id=model_name)
    elif provider == "google":
        return Gemini(id=model_name)
    elif provider == "groq":
        return Groq(id=model_name)
    elif provider == "openrouter":
        return OpenRouterChat(id=model_name)
    else:
        raise ValueError(
            f"Unsupported model provider: {provider}. Available providers: openai, google, openrouter, groq."
        )

def get_move_from_openai(board_state: str, valid_moves: list):
    prompt = f"Current board:\n{board_state}\nValid moves: {valid_moves}\nWhat's the best move?"
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=10,
        temperature=0.5
    )
    return response.choices[0].text.strip()

def get_move_from_gemini(board_state: str, valid_moves: list):
    client = genai.TextGenerationClient()
    prompt = f"Current board state:\n{board_state}\nValid moves: {valid_moves}\nWhat's the best move?"
    response = client.generate_text(prompt)
    return response.result

def get_move_from_groq(board_state: str, valid_moves: list):
    client = Groq(api_key=groq_api_key)
    prompt = f"Current board:\n{board_state}\nValid moves: {valid_moves}\nWhat's the best move?"
    response = client.generate_text(prompt)
    return response.result

def get_tic_tac_toe_players(
    model_x: str = "openai:gpt-4",
    model_o: str = "openai:o3-mini",
    debug_mode: bool = True,
) -> Tuple[Agent, Agent]:
    provider_x, model_name_x = model_x.split(":", 1)
    provider_o, model_name_o = model_o.split(":", 1)

    model_x = get_model_for_provider(provider_x, model_name_x)
    model_o = get_model_for_provider(provider_o, model_name_o)

    player_x = Agent(
        name="Player X",
        description=dedent("""
        You are Player X in a Tic Tac Toe game. Your goal is to win by placing three X's in a row.

        BOARD LAYOUT:
        - The board is a 3x3 grid with coordinates from (0,0) to (2,2)
        - Top-left is (0,0), bottom-right is (2,2)

        RULES:
        - You can only place X in empty spaces (shown as " " on the board)
        - Players take turns placing their marks
        - First to get 3 marks in a row (horizontal, vertical, or diagonal) wins
        - If all spaces are filled with no winner, the game is a draw

        YOUR RESPONSE:
        - Provide ONLY two numbers separated by a space (row column)
        - Example: "1 2" places your X in row 1, column 2
        - Choose only from the valid moves list provided to you

        STRATEGY TIPS:
        - Study the board carefully and make strategic moves
        - Block your opponent's potential winning moves
        - Create opportunities for multiple winning paths
        - Pay attention to the valid moves and avoid illegal moves
        """),
        model=model_x,
        debug_mode=debug_mode,
    )

    player_o = Agent(
        name="Player O",
        description=dedent("""
        You are Player O in a Tic Tac Toe game. Your goal is to win by placing three O's in a row.

        BOARD LAYOUT:
        - The board is a 3x3 grid with coordinates from (0,0) to (2,2)
        - Top-left is (0,0), bottom-right is (2,2)

        RULES:
        - You can only place O in empty spaces (shown as " " on the board)
        - Players take turns placing their marks
        - First to get 3 marks in a row (horizontal, vertical, or diagonal) wins
        - If all spaces are filled with no winner, the game is a draw

        YOUR RESPONSE:
        - Provide ONLY two numbers separated by a space (row column)
        - Example: "1 2" places your O in row 1, column 2
        - Choose only from the valid moves list provided to you

        STRATEGY TIPS:
        - Study the board carefully and make strategic moves
        - Block your opponent's potential winning moves
        - Create opportunities for multiple winning paths
        - Pay attention to the valid moves and avoid illegal moves
        """),
        model=model_o,
        debug_mode=debug_mode,
    )

    return player_x, player_o