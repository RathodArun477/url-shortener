import sqlite3

DATABASE = "urls.db"
def get_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        original_url TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()

def insert_db(code,original):
    con = get_connection()
    cur = con.cursor()

    try:
        cur.execute("""INSERT INTO urls (code,original_url) VALUES(?,?)""",(code,original))

        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()


def get_original_url(code):
    con = get_connection()
    cur = con.cursor()

    try:
        cur.execute("SELECT original_url FROM urls where code = ?",(code,))
        row = cur.fetchone()
        if row is not None:
            return row["original_url"]
        else:
            return None
    finally:
        con.close()

