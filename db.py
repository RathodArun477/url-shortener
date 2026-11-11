import sqlite3
import os
from pathlib import Path

DATABASE = Path(os.environ.get("DATABASE_PATH", "urls.db"))
DATABASE.parent.mkdir(parents=True, exist_ok=True)
def get_connection():
    con = sqlite3.connect(str(DATABASE))
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
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        clicks INTEGER DEFAULT 0
        )
    """)
    # Ensure clicks column exists if database was created with an older schema
    cur.execute("PRAGMA table_info(urls)")
    columns = [row[1] for row in cur.fetchall()]
    if "clicks" not in columns:
        cur.execute("ALTER TABLE urls ADD COLUMN clicks INTEGER DEFAULT 0")

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
            cur.execute("UPDATE urls SET clicks = clicks + 1 WHERE code = ?", (code,))
            con.commit()
            return row["original_url"]
        else:
            return None
    finally:
        con.close()

def get_url_stats(code):
    con = get_connection()
    cur = con.cursor()

    try:
        cur.execute("SELECT code, original_url, created_at, clicks FROM urls WHERE code = ?", (code,))
        row = cur.fetchone()
        if row is not None:
            return {
                "code": row["code"],
                "original_url": row["original_url"],
                "created_at": row["created_at"],
                "clicks": row["clicks"]
            }
        return None
    finally:
        con.close()

