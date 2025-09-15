
from strands import Agent
import chessplainer.tools as tools

class Chessplainer():
    def __init__(self, stockfish_path: str):
        self.sys_prompt = """You're a chess assistant. Your job is to help users 
            understand why a particular chess position has the 
            evaluation that it does. Keep your answers very short.
            You should use the Stockfish chess engine 
            to analyze the position and provide insights based on 
            its evaluation and suggested moves. You should render sample variations when useful.
            Do not go too deep into variations - the user can query further if needed."""
            
        self.board = tools.ChessBoard(stockfish_path=stockfish_path)

        self.agent = Agent(
            tools=[
                self.board.get_current_board_fen,
                self.board.get_all_legal_moves,
                self.board.make_move,
                self.board.unmake_move,
                self.board.reset_board,
                self.board.is_checkmate,
                self.board.evaluate_position,
                # self.board.get_top_n_moves,
                self.board.make_n_moves,
                self.board.set_move_sequence_for_rendering,
                self.board.set_board_fen,
                self.board.get_best_sequence_of_moves,
            ],
            system_prompt=self.sys_prompt,
        )
        

        
    def query(self, input: str) -> str:
        return self.agent(input)