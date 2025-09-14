import chess
import stockfish
from strands import tool

from typing import List

STOCKFISH_PATH = "/PATH/TO/STOCKFISH"  # Update this path to your Stockfish binary location
board = chess.Board()

@tool
def evaluate_position(fen: str) -> int:
    """
    Evaluates a chess position given in FEN notation using Stockfish.

    Args:
        fen (str): The FEN string representing the chess position.

    Returns:
        int: The evaluation score from Stockfish. Positive values favor White, negative values favor Black.
    """
    # Initialize the Stockfish engine
    engine = stockfish.Stockfish(path=STOCKFISH_PATH)

    # Set the position using the provided FEN string
    engine.set_fen_position(fen)

    # Get the evaluation score
    evaluation = engine.get_evaluation()

    # Return the score; if it's a mate score, convert it to a large number
    if evaluation['type'] == 'mate':
        return 10000 if evaluation['value'] > 0 else -10000
    else:
        return evaluation['value']
    
@tool
def suggest_moves(fen: str, n: int) -> List[str] | None:
    """
    Suggests the best move for a given chess position in FEN notation using Stockfish.

    Args:
        fen (str): The FEN string representing the chess position.

    Returns:
        str: The best move suggested by Stockfish in UCI format.
    """
    # Initialize the Stockfish engine
    engine = stockfish.Stockfish(path=STOCKFISH_PATH)

    # Set the position using the provided FEN string
    engine.set_fen_position(fen)

    # Get the best move
    best_moves = engine.get_top_moves(n)

    return best_moves

@tool
def is_checkmate(fen: str) -> bool:
    """
    Determines if the given chess position in FEN notation is a checkmate.

    Args:
        fen (str): The FEN string representing the chess position.

    Returns:
        bool: True if the position is a checkmate, False otherwise.
    """
    return board.is_checkmate()

@tool
def get_continuation(fen: str, move: str) -> str:
    """
    Returns the FEN string after making the specified move on the given position.

    Args:
        fen (str): The FEN string representing the current chess position.
        move (str): The move to be made in UCI format (e.g., 'e2e4').

    Returns:
        str: The FEN string of the new position after the move.
    """
    chess_move = chess.Move.from_uci(move)
    if chess_move in board.legal_moves:
        board.push(chess_move)
        return board.fen()
    else:
        raise ValueError("The provided move is not legal in the given position.")
    
@tool
def get_legal_moves(fen: str) -> list[str]:
    """
    Returns a list of all legal moves for the given chess position in FEN notation.

    Args:
        fen (str): The FEN string representing the chess position.

    Returns:
        list[str]: A list of legal moves in UCI format.
    """
    
    return [move.uci() for move in board.legal_moves]

@tool
def make_move(fen: str, move: str) -> str:
    """
    Makes the specified move on the given chess position in FEN notation and returns the new FEN.

    Args:
        fen (str): The FEN string representing the current chess position.
        move (str): The move to be made in UCI format (e.g., 'e2e4').

    Returns:
        str: The FEN string of the new position after the move.
    """
    
    chess_move = chess.Move.from_uci(move)
    if chess_move in board.legal_moves:
        board.push(chess_move)
        return board.fen()
    else:
        raise ValueError("The provided move is not legal in the given position.")
    
@tool
def make_sequence_of_moves(fen: str, moves: list[str]) -> str:
    """
    Makes a sequence of moves on the given chess position in FEN notation and returns the new FEN.

    Args:
        fen (str): The FEN string representing the current chess position.
        moves (list[str]): A list of moves to be made in UCI format (e.g., ['e2e4', 'e7e5']).

    Returns:
        str: The FEN string of the new position after the moves.
    """
    
    for move in moves:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
        else:
            raise ValueError(f"The move {move} is not legal in the given position.")
    return board.fen()

@tool
def unmake_move() -> str:
    """
    Undoes the last move made on the board and returns the FEN of the resulting position.

    Returns:
        str: The FEN string of the position after undoing the last move.
    """
    if board.move_stack:
        board.pop()
        return board.fen()
    else:
        raise ValueError("No moves to unmake.")
    
@tool
def reset_board() -> str:
    """
    Resets the board to the starting position and returns the FEN of the starting position.

    Returns:
        str: The FEN string of the starting position.
    """
    board.reset()
    return board.fen()

@tool
def unmake_n_moves(n: int) -> str:
    """
    Undoes the last n moves made on the board and returns the FEN of the resulting position.

    Args:
        n (int): The number of moves to unmake.
    Returns:
        str: The FEN string of the position after undoing the last n moves.
    """
    if n > len(board.move_stack):
        raise ValueError("Cannot unmake more moves than have been made.")
    for _ in range(n):
        board.pop()
    return board.fen()

@tool
def play_sequence_and_get_evals(fen: str, moves: list[str]) -> list[int]:
    """
    Plays a sequence of moves on the given chess position in FEN notation and returns the evaluation after each move.

    Args:
        fen (str): The FEN string representing the current chess position.
        moves (list[str]): A list of moves to be made in UCI format (e.g., ['e2e4', 'e7e5']).

    Returns:
        list[int]: A list of evaluation scores after each move.
    """
    evaluations = []
    for move in moves:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
            evaluations.append(evaluate_position(board.fen()))
        else:
            raise ValueError(f"The move {move} is not legal in the given position.")
    return evaluations