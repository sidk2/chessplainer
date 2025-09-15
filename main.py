import streamlit as st
import chess
import chess.svg

from chessplainer.agent import Chessplainer
from chessplainer.tools import ChessBoard

# Use st.cache_resource to ensure the board instance is created only once
@st.cache_resource
def get_chess_board():
    return ChessBoard()

@st.cache_resource
def get_agent():
    board_instance = get_chess_board()
    return Chessplainer(board=board_instance)

agent = get_agent()
board = agent.board

st.set_page_config(layout="wide")

# Create two columns with a 1:2 ratio for the board and chat
col1, col2 = st.columns([1, 1])

# Left Column: Display the chess board
with col1:
    # Always render the interactive board.
    # Initialize the board with the starting position if it's the first run.
    if "interactive_boards" not in st.session_state:
        st.session_state.interactive_boards = [board._board.copy()]
        st.session_state.current_move_index = 0

    # Get the board corresponding to the current index
    current_interactive_board = st.session_state.interactive_boards[st.session_state.current_move_index]

    # Update the agent's internal board to match the interactive view
    board._board.set_fen(current_interactive_board.fen())

    # Render the interactive board
    svg = chess.svg.board(board=current_interactive_board, size=400)
    st.image(svg, caption=f"Move {st.session_state.current_move_index}")

    # --- New button-based navigation section ---

    # Create a sub-column layout for the buttons and move counter
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

    with nav_col1:
        if st.button("⟵"):
            if st.session_state.current_move_index > 0:
                st.session_state.current_move_index -= 1
                st.rerun()

    with nav_col2:
        st.markdown(f"<h3 style='text-align: left;'>Move {st.session_state.current_move_index} of {len(st.session_state.interactive_boards) - 1}</h3>", unsafe_allow_html=True)

    with nav_col3:
        if st.button("⟶"):
            if st.session_state.current_move_index < len(st.session_state.interactive_boards) - 1:
                st.session_state.current_move_index += 1
                st.rerun()

# Right Column: Display the chat interface
with col2:
    st.title("Chessplainer Chat")

    with st.container(height=500, border=True):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about the current position..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        st.rerun()

        # Query agent
        response = agent.query(prompt)
        response_text = response.message['content'][0]['text']

        # Add response to history
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        # Check if the agent's action resulted in a new sequence to render
        if board.move_sequence_to_render:
            # Update the interactive board and reset the slider
            st.session_state.interactive_boards = board.move_sequence_to_render
            st.session_state.current_move_index = 0
            # Clear the agent's sequence
            board.move_sequence_to_render = []
        
        # Force a rerun to render the new messages and board state
        st.rerun()