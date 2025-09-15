import chess
import stockfish
from strands import tool
from typing import List

STOCKFISH_PATH = "PATH/TO/YOUR/STOCKFISH"  # Update this path to your Stockfish binary

class ChessBoard:
    """
    Manages a single chess board instance and provides tools for an agent to interact with it.
    """
    def __init__(self):
        self._board = chess.Board()
        self._engine = stockfish.Stockfish(path=STOCKFISH_PATH)
        # New class variable to store the move sequence for rendering
        self.move_sequence_to_render: List[chess.Board] = []

    @tool
    def get_current_board_fen(self) -> str:
        """
        Returns the FEN string of the current board position to analyze from.

        Returns:
            str: The FEN string of the current board position.
        """
        return self._board.fen()

    @tool
    def evaluate_position(self) -> int:
        """
        Evaluates the current chess position using Stockfish.

        Returns:
            int: The evaluation score from Stockfish. Positive values favor White, negative values favor Black.
        """
        self._engine.set_fen_position(self._board.fen())
        evaluation = self._engine.get_evaluation()
        if evaluation['type'] == 'mate':
            return 10000 if evaluation['value'] > 0 else -10000
        else:
            return evaluation['value']
    
    @tool
    def get_n_best_moves(self, n: int) -> List[dict]:
        """
        Suggests the best n moves for the current chess position using Stockfish.

        Args:
            n (int): The number of moves to suggest.

        Returns:
            List[dict]: A list of dictionaries with move and evaluation details.
        """
        if n <= 0 or n > 3:
            raise ValueError("n must be between 1 and 3.")
        
        self._engine.set_fen_position(self._board.fen())
        return self._engine.get_top_moves(n)

    @tool
    def is_checkmate(self) -> bool:
        """
        Determines if the current chess position is a checkmate.

        Returns:
            bool: True if the position is a checkmate, False otherwise.
        """
        return self._board.is_checkmate()

    @tool
    def get_all_legal_moves(self) -> list[str]:
        """
        Returns a list of all legal moves for the current chess position in UCI format.

        Returns:
            list[str]: A list of legal moves.
        """
        return [move.uci() for move in self._board.legal_moves]

    @tool
    def make_move(self, move: str) -> str:
        """
        Makes the specified move on the current chess board and returns the new FEN.

        Args:
            move (str): The move to be made in UCI format (e.g., 'e2e4').

        Returns:
            str: The FEN string of the new position after the move.
        """
        try:
            self._board.push_uci(move)
            return self._board.fen()
        except ValueError as e:
            raise ValueError(f"The provided move '{move}' is not legal: {e}")
    
    @tool 
    def make_n_moves(self, moves: List[str]) -> str:
        """
        Makes a sequence of moves on the current chess board and returns the new FEN.

        Args:
            moves (List[str]): A list of moves to be made in UCI format (e.g., ['e2e4', 'e7e5']).

        Returns:
            str: The FEN string of the new position after the moves.
        """
        try:
            for move in moves:
                self._board.push_uci(move)
            return self._board.fen()
        except ValueError as e:
            raise ValueError(f"One of the provided moves is not legal: {e}")

    @tool
    def unmake_move(self) -> str:
        """
        Undoes the last move made on the board and returns the FEN of the resulting position.

        Returns:
            str: The FEN string of the position after undoing the last move.
        """
        if self._board.move_stack:
            self._board.pop()
            return self._board.fen()
        else:
            raise ValueError("No moves to unmake.")

    @tool
    def reset_board(self) -> str:
        """
        Resets the board to the starting position and returns the FEN of the starting position.

        Returns:
            str: The FEN string of the starting position.
        """
        self._board.reset()
        return self._board.fen()

    @tool
    def set_move_sequence_for_rendering(self, moves: List[str]) -> str:
        """
        Prepares a sequence of board positions for rendering without modifying the main board state.

        The agent can call this to show a move sequence to the user.
        
        Args:
            moves (List[str]): A list of moves to be demonstrated in UCI format (e.g., ['e2e4', 'e7e5']).

        Returns:
            str: A confirmation message indicating the sequence is ready to be rendered.
        """
        # Start with a copy of the current board state
        temp_board = self._board.copy()
        board_sequence = [temp_board.copy()]
        
        try:
            for move in moves:
                temp_board.push_uci(move)
                board_sequence.append(temp_board.copy())
            
            # Store the generated sequence in the new class variable
            self.move_sequence_to_render = board_sequence
            
            return "Move sequence prepared for rendering. The application can now display it."
        
        except ValueError as e:
            raise ValueError(f"Could not prepare sequence: one of the moves is not legal. Error: {e}")