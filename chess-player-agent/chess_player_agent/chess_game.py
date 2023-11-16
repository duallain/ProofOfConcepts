import chess
import sqlite3


class ChessGame:
    def __init__(self, player1, player2, sqlite_db="chess_results.sqlite") -> None:
        self.board = chess.Board()
        self.moves = []
        self.player1 = player1
        self.player2 = player2

        self.result_states = {
            0: "in progress",
            1: "checkmate white",
            2: "checkmate black",
            3: "draw, stalemate",
            4: "draw, fivefold repetition",
            5: "draw, insufficient material",
            6: "draw, claim a draw",
        }

        self.sqlite_db = sqlite_db

    def _current_player(self) -> str:
        return "White" if self.board.turn == chess.WHITE else "Black"

    def display_board(self):
        return self.board._repr_svg_()

    def execute_game(self):
        while not self.board.is_game_over(claim_draw=True):
            if self.board.turn == chess.WHITE:
                uci = self.player1(self.board)
            else:
                uci = self.player2(self.board)

            self.board.push_uci(uci)

    def get_current_state(self):
        result_state = 0

        if self.board.is_checkmate():
            if not self.board.turn:
                result_state = 1
            else:
                result_state = 2
        if self.board.is_stalemate():
            result_state = 3
        if self.board.is_fivefold_repetition():
            result_state = 4
        if self.board.is_insufficient_material():
            result_state = 5
        if self.board.can_claim_draw():
            result_state = 6

        return result_state

    def get_human_state(self):
        return self.result_states[self.get_current_state()]

    def standard_notation(self):
        return [
            f"{move_index+1}. {move}"
            for move_index, move in enumerate(self.board.move_stack)
        ]

    def display_summarized_game(self):
        # this should work for games in progress
        # and games that have ended
        print(f"{self.get_human_state()}: {len(self.board.move_stack)}")
        print(" ".join(self.standard_notation()))
        return self.board._repr_svg_()

    def store_game_result(self):
        player1_name = self.player1.__name__
        player2_name = self.player2.__name__
        outcome = self.get_current_state()
        moves = " ".join([move.uci() for move in self.board.move_stack])
        move_count = len(self.board.move_stack)

        con = sqlite3.connect(self.sqlite_db)
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
