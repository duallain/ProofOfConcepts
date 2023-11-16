import chess.engine
from functools import partial
import random


def random_player(board):
    move = random.choice(list(board.legal_moves))
    return move.uci()

    self.__name__ = 'random_player'
    


def stockfish_generator(time=0.1):
    # return a function that already has a time set
    # name should reflect the time
    
    def stockfish(board, time):  
        engine = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/16/bin/stockfish")
        move = engine.play(board, chess.engine.Limit(time=time)).move
        return move.uci()

    stockfish_partial = partial(stockfish, time=time)
    stockfish_partial.__name__ = f"stockfish_{time}"
    return stockfish_partial
