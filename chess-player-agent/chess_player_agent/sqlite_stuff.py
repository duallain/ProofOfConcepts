import sqlite3

def setup_sqlite():
    con = sqlite3.connect("chess_results.sql")
    cur = con.cursor()
    cur.execute("CREATE TABLE chess_games(id integer primary key, player1, player2, outcome integer, moves)")
    cur.close()
    