from strands import Agent
import chessplainer.tools as tools

prompt = """You're a chess assistant. Your job is to help users 
            understand why a particular chess position has the 
            evaluation that it does, and why a particular move is 
            good or bad. You should use the Stockfish chess engine 
            to analyze the position and provide insights based on 
            its evaluation and suggested moves. Adapt your explanation 
            based on how adept the user is at chess, which you can 
            infer from their questions and comments. If they seem 
            like a beginner, provide more detailed explanations of 
            chess concepts. If they seem more advanced, focus on 
            deeper strategic insights. Try to point out concrete lines 
            if they are needed, or more qualitative features of the 
            position. Explore different variations that could have 
            occured to pinpoint the mistakes or ideas."""

agent = Agent(
    tools=[
        tools.evaluate_position,
        tools.suggest_moves,
        tools.is_checkmate,
        tools.get_continuation,
        tools.get_legal_moves,
        tools.make_move,
        tools.make_sequence_of_moves,
        tools.unmake_move,
        tools.reset_board,
        tools.unmake_n_moves,
        tools.play_sequence_and_get_evals
    ],
    system_prompt=prompt,
)

inp = ""

while inp.lower() not in ["exit", "quit"]:
    inp = input("User: ")
    if inp.lower() in ["exit", "quit"]:
        break
    response = agent(inp)
    print("Agent:", response)