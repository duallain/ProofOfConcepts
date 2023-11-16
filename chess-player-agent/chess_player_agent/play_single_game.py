from chess_players import stockfish_generator, random_player

from prefect import flow, task


import chess
import sqlite3



@task
def play_game(player1, player2):
    board = chess.Board()
    while not board.is_game_over(claim_draw=True):
        if board.turn == chess.WHITE:
            uci = player1(board)
        else:
            uci = player2(board)

        board.push_uci(uci)

    return board

def get_current_state(board):
    result_state = 0

    if board.is_checkmate():
        if not board.turn:
            result_state = 1
        else:
            result_state = 2
    if board.is_stalemate():
        result_state = 3
    if board.is_fivefold_repetition():
        result_state = 4
    if board.is_insufficient_material():
        result_state = 5
    if board.can_claim_draw():
        result_state = 6

    return result_state

@task
def store_game_result(player1, player2, board, sqlite_db="/Users/alan/sandbox/ProofOfConcepts/chess-player-agent/chess_player_agent/chess_results.sqlite"):
    player1_name = player1.__name__
    player2_name = player2.__name__
    outcome = get_current_state(board)
    moves = " ".join([move.uci() for move in board.move_stack])

    con = sqlite3.connect(sqlite_db)
    cur = con.cursor()

    query = f"""
        INSERT INTO chess_games
        (id, player1, player2, outcome, moves)
        VALUES
        (NULL, '{player1_name}', '{player2_name}', {outcome}, '{moves}')
            
    """

    cur.execute(query)
    con.commit()
    cur.close()
    
    return(player1_name, player2_name, outcome)

@flow
def run_and_save_chess_game(player1, player2):
   board = play_game(player1, player2)
   store_game_result(player1, player2, board)
    
if __name__ == '__main__':
    run_and_save_chess_game(random_player, stockfish_generator())
    