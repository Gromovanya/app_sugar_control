import sqlite3
from constants import SUGAR_DB

def connect_db():
    return sqlite3.connect(SUGAR_DB)


def create_table(db):
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


def insert_db_data(db, num_sugar, current_time, current_day, current_month, current_year):
    cur = db.cursor()
    cur.execute(f"""INSERT INTO indic_sugar
        (indicators_sugar, time_in_day,
        current_day, current_month, current_year)
        VALUES (?, ?, ?, ?, ?)""",
                (num_sugar, current_time, current_day, current_month, current_year))
    db.commit()
    
def del_table(db, table):
    cur = db.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table}")

def fetch_statistics(db):
    cur = db.cursor()
    stats = {}

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

def verification_table(table_name):
    db = connect_db()
    cur = db.cursor()
    
    cur.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
        """, (table_name, ))
    res = cur.fetchone()
    db.close()
    
    return res is None
