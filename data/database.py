import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('game_scores.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT,
                score INTEGER
            )
        ''')

    def save_score(self, nickname, score):
        self.cursor.execute("INSERT INTO scores (nickname, score) VALUES (?, ?)", (nickname, score))
        self.conn.commit()

    def get_top_scores(self, limit=5):
        self.cursor.execute("SELECT nickname, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def clear_all_scores(self):
        self.cursor.execute("DELETE FROM scores")
        self.conn.commit()

    def __del__(self):
        self.conn.close()


db = Database()


def save_score(nickname, score):
    db.save_score(nickname, score)


def delete_scores():
    db.clear_all_scores()


def show_top_players():
    top_scores = db.get_top_scores()
    print("Топ 5 игроков:")
    for i, (nickname, score) in enumerate(top_scores, 1):
        print(f"{i}. {nickname} - {score}")


def get_top_players():
    return db.get_top_scores()
