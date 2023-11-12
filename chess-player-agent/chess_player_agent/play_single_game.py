from chess_players import stockfish_generator
from chess_game import ChessGame

def run_and_save_chess_game(player1):
    cg = ChessGame(player1, stockfish_generator(0.2))
    cg.execute_game()
    cg.store_game_result()