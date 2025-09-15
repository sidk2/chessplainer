import streamlit as st
import chess
import chess.svg

from chessplainer.agent import Chessplainer
from chessplainer.tools import ChessBoard

STOCKFISH_PATH = "/Users/sidkannan/Code/chessplainer/stockfish-macos-m1-apple-silicon"  # Update this path to your Stockfish binary location

# Use st.cache_resource to ensure the board instance is created only once

@st.cache_resource
def get_agent():
    return Chessplainer(STOCKFISH_PATH)

agent = get_agent()
board = agent.board

st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 1])

# Left Column: Displays the chess board
with col1:
    if "interactive_boards" not in st.session_state:
        st.session_state.interactive_boards = [board._board.copy()]
        st.session_state.current_move_index = 0

    current_interactive_board = st.session_state.interactive_boards[st.session_state.current_move_index]

    svg = chess.svg.board(board=current_interactive_board, size=400)
    st.image(svg, caption=f"Move {st.session_state.current_move_index}")

    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])

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
# Right Column: Display the chat interface
with col2:
    st.title("Chessplainer Chat")

    # The container for displaying chat history remains the same
    with st.container(height=500, border=True):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about the current position..."):
        # Add user message to history and display it instantly
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent's response
        with st.spinner("Thinking..."):
            response = agent.query(prompt)
            response_text = response.message['content'][0]['text']

        # Add assistant response to history and display it instantly
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)

        # Check if the agent's action resulted in a new sequence to render
        # This part of your logic was already correct
        if board.move_sequence_to_render:
            st.session_state.interactive_boards = board.move_sequence_to_render
            st.session_state.current_move_index = 0
            board.move_sequence_to_render = []
            
            # We need to rerun to update the board in the left column
            st.rerun()