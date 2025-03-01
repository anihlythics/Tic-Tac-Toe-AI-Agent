# Tic Tac Toe AI Agent 🎮
 A dynamic Tic-Tac-Toe game where two AI agents, each powered by a different language model, compete against each other. 
 Built using the Agno Agent Framework for AI interactions and Streamlit for an intuitive user interface.

- Coordinate multiple AI agents in a turn-based game
- Use different language models for different players
- Create an interactive web interface with Streamlit
- Handle game state and move validation
- Display real-time game progress and move history

## Features

- **Multiple AI Models Support:** GPT-4, Claude, Gemini, and more.
- **Real-time Game Visualization:** See the game updates live.
- **Move History Tracking:** Keep track of moves with board states.
- **Interactive Player Selection:** Choose your AI model for each player.
- **Game State Management:** Handles all aspects of the game state, including moves and turns.
- **Move Validation and Coordination:** Ensures that each move is valid and follows game rules.

## How to Run?

### 1. Setup Environment

Clone the repository:

git clone https://github.com/anihlythics/Tic-Tac-Toe-AI-Agent.git
cd ai_agent_tutorials/ai_tic_tac_toe_agent

### 2. Install Dependencies

Install the required dependencies:

pip install -r requirements.txt

### 3. Export API Keys

The game supports multiple AI models. Export the API keys for the models you want to use:

Required for OpenAI models:
bash
export OPENAI_API_KEY=***

Optional for additional models:

export ANTHROPIC_API_KEY=*** # For Claude models
export GOOGLE_API_KEY=***     # For Gemini models
export GROQ_API_KEY=***       # For Groq models

### 4. Run the Game
streamlit run app.py
Open localhost:8501 to view the game interface

## How It Works

The game consists of three agents:

### Master Agent (Referee)

- Coordinates the game
- Validates moves
- Maintains the game state
- Determines the game outcome

### Two Player Agents

- Make strategic moves
- Analyze board state
- Follow game rules
- Respond to opponent moves

## Available Models

The game supports various AI models, including:

- **GPT-4o** (OpenAI)
- **GPT-o3-mini** (OpenAI)
- **Gemini** (Google)
- **Llama 3** (Groq)
- **Claude** (Anthropic)

## Game Features

### Interactive Board
- Real-time updates
- Visual move tracking
- Clear game status display

### Move History
- Detailed move tracking
- Board state visualization
- Player action timeline

### Game Controls
- Start/Pause game
- Reset board
- Select AI models
- View game history

### Performance Analysis
- Move timing
- Strategy tracking
- Game statistics

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
