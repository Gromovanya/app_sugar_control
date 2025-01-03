import sqlite3
from constants import SUGAR_DB, PATH_DIR_JSON
from os import makedirs


def connect_db() -> sqlite3.Connection:
    makedirs(PATH_DIR_JSON, exist_ok=True)
    return sqlite3.connect(SUGAR_DB)


def create_table(db: sqlite3.Connection):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS indic_sugar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        indicators_sugar DECIMAL(5, 1),
        time_in_day TIME,
        current_day INTEGER,
        current_month INTEGER,
        current_year INTEGER
    )""")

    db.commit()


def insert_db_data(db: sqlite3.Connection, num_sugar: float, current_time: str, current_day: int, current_month: int,
                   current_year: int):
    cur = db.cursor()
    cur.execute("""INSERT INTO indic_sugar
        (indicators_sugar, time_in_day,
        current_day, current_month, current_year)
        VALUES (?, ?, ?, ?, ?)""",
                (num_sugar, current_time, current_day, current_month, current_year))
    db.commit()


def del_table(db: sqlite3.Connection, table: str):
    cur = db.cursor()
    cur.execute(f"DELETE FROM {table};")
    cur.execute("DELETE FROM sqlite_sequence WHERE name=?", (table,))
    db.commit()


def fetch_statistics(db: sqlite3.Connection) -> dict:
    cur = db.cursor()
    stats = {}
    create_table(db)

    cur.execute('SELECT AVG(indicators_sugar) FROM indic_sugar')
    stats['avg'] = cur.fetchone()[0]

    cur.execute('SELECT MAX(indicators_sugar) FROM indic_sugar')
    stats['max'] = cur.fetchone()[0]

    cur.execute('SELECT MIN(indicators_sugar) FROM indic_sugar')
    stats['min'] = cur.fetchone()[0]

    cur.execute('SELECT COUNT(*) FROM indic_sugar')
    stats['count'] = cur.fetchone()[0]

    cur.execute('SELECT * FROM indic_sugar')
    stats['rows'] = cur.fetchall()
    return stats


def verification_table() -> bool:
    db = connect_db()
    stats = fetch_statistics(db)
    db.close()

    return len(stats['rows']) == 0
