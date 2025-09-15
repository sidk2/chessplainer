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

![Example](/images/example.png)


---

## Requirements

- Python 3.13+
- [Stockfish](https://stockfishchess.org/download/) installed locally  

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
4. Update `main.py` with the path to Stockfish
5. Run `streamlit run main.py`, and ask away!