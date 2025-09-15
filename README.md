# Chessplainer

This project uses an **LLM agent** to explain chess positions in natural language.  
It integrates with **[Strands](https://strandsagents.com)** for agent orchestration,  
**[python-chess](https://python-chess.readthedocs.io/en/latest/)** for board representation and move handling,  
and **[Stockfish](https://stockfishchess.org/)** as the underlying chess engine.

---

## Features

- Load and analyze any chess position (FEN or PGN).
- Query **Stockfish** for best moves and evaluations.
- Use an **LLM agent** to generate human-readable explanations of the position.
- Renders board visualizations directly in the browser.

---

## Requirements

- Python 3.13+
- [Stockfish](https://stockfishchess.org/download/) installed locally  
  (make sure the `stockfish` binary is available in your system path).

### Python dependencies
- [Strands](https://strandsagents.com)
- [python-chess](https://python-chess.readthedocs.io/en/latest/)
- [stockfish](https://pypi.org/project/stockfish/)
- [streamlit](https://streamlit.io)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/chess-explainer.git
   cd chess-explainer

2. Download the dependencies
   ```pip install .```

3. Install Stockfish from https://stockfishchess.org/download/